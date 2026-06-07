from collections import defaultdict
from statistics import mean, pstdev

import numpy as np


DIRECT_TEXT_ALIASES = {
    "canadaPencil": ("canada pencil", "canadian pencil", "maple leaf pencil", "souvenir from canada"),
    "rainbowPens": ("rainbow pen", "rainbow pens", "color pens", "coloured pens"),
    "rubiksCube": ("rubik", "rubiks cube", "rubik's cube"),
    "noisemaker": ("noisemaker", "noise maker", "cheering sticks"),
    "blueSunglasses": ("blue sunglasses",),
    "pinkEraser": ("pink eraser",),
    "lavenderDie": ("lavender die", "purple die", "purple dice"),
    "metalKey": ("metal key",),
    "miniCards": ("mini cards", "tiny cards"),
}


class ForensicAnalysisEngine:
    def __init__(self, master_data, corrections, training_labels=None):
        self.master_data = master_data
        self.corrections = corrections
        self.training_labels = sorted(training_labels or [])
        self.target_size = int(corrections.get("target_group_size", 8))
        self.corrected_labels = corrections.get("corrected_labels", {})
        scoring = corrections.get("candidate_scoring", {})
        self.scoring_weights = {
            "specificity": float(scoring.get("specificity_weight", 0.40)),
            "stability": float(scoring.get("stability_weight", 0.35)),
            "visual": float(scoring.get("visual_weight", 0.15)),
            "text": float(scoring.get("text_weight", 0.10)),
        }
        self.non_target_penalty = float(scoring.get("non_target_penalty", 0.72))
        self.visual_images_per_owner = max(
            1,
            int(scoring.get("visual_images_per_owner", 2)),
        )
        self.rejected = {
            (item["person_id"], item["image_id"], int(item["box_id"]))
            for item in corrections.get("rejected_predictions", [])
        }

    @staticmethod
    def _person_number(person_id):
        try:
            return int(person_id.replace("Person", ""))
        except ValueError:
            return 999

    def _raw_boxes(self):
        for person_id, person in self.master_data.items():
            for image_id, image in person.get("images", {}).items():
                for box in image.get("yolo_boxes", []):
                    if box.get("label") == "unknown" or box.get("score", 0) <= 0:
                        continue
                    yield person_id, image_id, image, box

    def confidence_statistics(self):
        scores = defaultdict(list)
        for _, _, _, box in self._raw_boxes():
            scores[box["label"]].append(float(box["score"]))

        result = {}
        for label, values in scores.items():
            arr = np.asarray(values, dtype=float)
            result[label] = {
                "min": float(np.min(arr)),
                "q1": float(np.percentile(arr, 25)),
                "median": float(np.percentile(arr, 50)),
                "q3": float(np.percentile(arr, 75)),
                "max": float(np.max(arr)),
                "count": len(values),
            }
        return result

    def detection_density(self, limit=600):
        points = []
        for person_id, image_id, _, box in self._raw_boxes():
            width = float(box.get("width", 0))
            height = float(box.get("height", 0))
            x = float(box.get("x", 0)) + width / 2
            y = float(box.get("y", 0)) + height / 2
            if x < 0 or y < 0:
                continue
            points.append({
                "x": x,
                "y": y,
                "score": float(box["score"]),
                "label": box["label"],
                "person_id": person_id,
                "image_id": image_id,
            })
        if len(points) <= limit:
            return points
        step = len(points) / limit
        return [points[int(index * step)] for index in range(limit)]

    def raw_matrix(self, threshold=0.45, excluded_items=None):
        excluded_items = set(excluded_items or [])
        counts = defaultdict(int)
        items = set()
        for person_id, image_id, _, box in self._raw_boxes():
            key = (person_id, image_id, int(box.get("box_id", -1)))
            label = box["label"]
            if (
                float(box["score"]) >= threshold
                and label not in excluded_items
                and key not in self.rejected
            ):
                counts[(person_id, label)] += 1
                items.add(label)
        return self._matrix_payload(counts, items)

    def corrected_matrix(self, excluded_items=None):
        excluded_items = set(excluded_items or [])
        counts = defaultdict(int)
        items = set()
        for label, label_node in self.corrected_labels.items():
            if label in excluded_items:
                continue
            items.add(label)
            for person_id, person_node in label_node.get("persons", {}).items():
                counts[(person_id, label)] = int(person_node.get("occurrence_count", 0))
        return self._matrix_payload(counts, items)

    def _matrix_payload(self, counts, items):
        suspects = sorted(self.master_data, key=self._person_number)
        items = sorted(items)
        matrix = np.zeros((len(suspects), len(items)), dtype=float)
        row_index = {value: index for index, value in enumerate(suspects)}
        col_index = {value: index for index, value in enumerate(items)}
        for (person_id, label), count in counts.items():
            if person_id in row_index and label in col_index:
                matrix[row_index[person_id], col_index[label]] = count

        ordered_suspects = suspects
        ordered_items = items
        if matrix.shape[0] > 1 and matrix.shape[1] > 1 and matrix.sum() > 0:
            try:
                from scipy.cluster.hierarchy import leaves_list, linkage
                from scipy.spatial.distance import pdist

                row_distance = pdist(matrix, metric="euclidean")
                col_distance = pdist(matrix.T, metric="euclidean")
                if np.any(row_distance):
                    ordered_suspects = [suspects[i] for i in leaves_list(linkage(row_distance, method="ward"))]
                if np.any(col_distance):
                    ordered_items = [items[i] for i in leaves_list(linkage(col_distance, method="ward"))]
            except (ValueError, FloatingPointError):
                pass

        cells = [
            {"suspect": person_id, "item": label, "count": int(count)}
            for (person_id, label), count in counts.items()
            if count > 0
        ]
        return ordered_suspects, ordered_items, cells

    def _text_snippets(self, person_id, label):
        person = self.master_data[person_id]
        aliases = DIRECT_TEXT_ALIASES.get(label, (label,))
        snippets = []
        for image in person.get("images", {}).values():
            caption = image.get("caption", "").strip()
            if caption and any(alias.lower() in caption.lower() for alias in aliases):
                snippets.append(caption)
        for text in person.get("independent_texts", []):
            if any(alias.lower() in text.lower() for alias in aliases):
                snippets.append(text)
        return list(dict.fromkeys(snippets))

    def _raw_label_scores(self, person_id, label):
        rows = []
        person = self.master_data[person_id]
        for image_id, image in person.get("images", {}).items():
            for box in image.get("yolo_boxes", []):
                if box.get("label") == label and box.get("score", 0) > 0:
                    rows.append((image_id, float(box["score"]), int(box.get("box_id", -1))))
        return sorted(rows, key=lambda row: row[1], reverse=True)

    def _candidate_raw_detection_images(self, person_id, label, threshold):
        image_ids = set()
        for image_id, score, box_id in self._raw_label_scores(person_id, label):
            if (
                score >= threshold
                and (person_id, image_id, box_id) not in self.rejected
            ):
                image_ids.add(image_id)
        return sorted(image_ids)

    def candidate_rankings(self, threshold=0.45):
        rankings = []
        evaluated_image_count = sum(
            len(person.get("images", {}))
            for person in self.master_data.values()
        )
        for label, label_node in self.corrected_labels.items():
            people = label_node.get("persons", {})
            if not people:
                continue
            counts = [int(node.get("occurrence_count", 0)) for node in people.values()]
            owner_count = len(people)
            exact_group = owner_count == self.target_size
            stable_ratio = sum(value >= 2 for value in counts) / owner_count
            verified_images = sum(
                len(set(person_node.get("image_ids", [])))
                for person_node in people.values()
            )
            verified_image_keys = {
                (person_id, image_id)
                for person_id, person_node in people.items()
                for image_id in person_node.get("image_ids", [])
            }
            raw_image_keys = {
                (person_id, image_id)
                for person_id in self.master_data
                for image_id in self._candidate_raw_detection_images(
                    person_id,
                    label,
                    threshold,
                )
            }
            owner_raw_image_keys = {
                key for key in raw_image_keys
                if key[0] in people
            }
            non_owner_raw_image_keys = raw_image_keys - owner_raw_image_keys
            supporting_image_keys = verified_image_keys | owner_raw_image_keys
            visual_coverage = min(
                1.0,
                len(supporting_image_keys)
                / max(owner_count * self.visual_images_per_owner, 1),
            )
            visual_precision = (
                len(supporting_image_keys)
                / (len(supporting_image_keys) + len(non_owner_raw_image_keys))
                if supporting_image_keys or non_owner_raw_image_keys
                else 0
            )
            visual_ratio = visual_coverage * visual_precision
            text_snippets = {
                person_id: self._text_snippets(person_id, label)
                for person_id in people
            }
            text_support = sum(bool(snippets) for snippets in text_snippets.values())
            text_evidence_count = sum(len(snippets) for snippets in text_snippets.values())
            text_ratio = text_support / owner_count
            specificity = max(0.0, 1 - abs(owner_count - self.target_size) / self.target_size)
            score = sum((
                self.scoring_weights["specificity"] * specificity,
                self.scoring_weights["stability"] * stable_ratio,
                self.scoring_weights["visual"] * visual_ratio,
                self.scoring_weights["text"] * text_ratio,
            ))
            penalty = 1.0
            if not exact_group:
                penalty = self.non_target_penalty
                score *= penalty

            rankings.append({
                "label": label,
                "owner_count": owner_count,
                "coverage": round(owner_count / len(self.master_data), 4),
                "owners": sorted(people, key=self._person_number),
                "min_occurrence": min(counts),
                "mean_occurrence": round(mean(counts), 3),
                "occurrence_std": round(pstdev(counts), 3) if len(counts) > 1 else 0,
                "stable_owner_ratio": round(stable_ratio, 4),
                "text_support_count": text_support,
                "text_evidence_count": text_evidence_count,
                "evidence_image_count": len(supporting_image_keys),
                "verified_image_count": verified_images,
                "raw_detection_image_count": len(raw_image_keys),
                "owner_raw_detection_image_count": len(owner_raw_image_keys),
                "non_owner_raw_detection_image_count": len(non_owner_raw_image_keys),
                "evaluated_image_count": evaluated_image_count,
                "exact_target_size": exact_group,
                "score": round(score, 4),
                "score_components": {
                    "specificity": round(
                        self.scoring_weights["specificity"] * specificity * penalty,
                        4,
                    ),
                    "stability": round(
                        self.scoring_weights["stability"] * stable_ratio * penalty,
                        4,
                    ),
                    "visual": round(
                        self.scoring_weights["visual"] * visual_ratio * penalty,
                        4,
                    ),
                    "text": round(
                        self.scoring_weights["text"] * text_ratio * penalty,
                        4,
                    ),
                    "penalty": penalty,
                },
                "score_factors": {
                    "specificity": round(specificity, 4),
                    "stability": round(stable_ratio, 4),
                    "visual": round(visual_ratio, 4),
                    "visual_coverage": round(visual_coverage, 4),
                    "visual_precision": round(visual_precision, 4),
                    "text": round(text_ratio, 4),
                },
                "source": label_node.get("source", "人工纠正"),
            })
        return sorted(rankings, key=lambda item: (-item["score"], item["label"]))

    def raw_hypothesis(self, label=None, threshold=0.55):
        if label is None:
            candidates = defaultdict(lambda: {"owners": set(), "scores": []})
            for person_id, _, _, box in self._raw_boxes():
                if float(box["score"]) < threshold:
                    continue
                candidate = candidates[box["label"]]
                candidate["owners"].add(person_id)
                candidate["scores"].append(float(box["score"]))
            if candidates:
                label = min(
                    candidates,
                    key=lambda candidate_label: (
                        abs(len(candidates[candidate_label]["owners"]) - self.target_size),
                        -mean(candidates[candidate_label]["scores"]),
                        -len(candidates[candidate_label]["scores"]),
                        candidate_label,
                    ),
                )
            else:
                label = ""

        owners = defaultdict(int)
        detections = []
        for person_id, image_id, _, box in self._raw_boxes():
            if box["label"] == label and float(box["score"]) >= threshold:
                owners[person_id] += 1
                detections.append({
                    "person_id": person_id,
                    "image_id": image_id,
                    "box_id": int(box.get("box_id", -1)),
                    "score": round(float(box["score"]), 4),
                    "rejected": (
                        person_id,
                        image_id,
                        int(box.get("box_id", -1))
                    ) in self.rejected,
                })
        return {
            "label": label,
            "threshold": threshold,
            "owner_count": len(owners),
            "owners": sorted(owners, key=self._person_number),
            "detections": sorted(detections, key=lambda item: -item["score"]),
            "status": "invalidated" if detections and all(item["rejected"] for item in detections) else "unreviewed",
        }

    def threshold_curves(self):
        raw_boxes = list(self._raw_boxes())
        all_labels = {box["label"] for _, _, _, box in raw_boxes}
        all_people = {person_id for person_id, _, _, _ in raw_boxes}
        total_predictions = len(raw_boxes)
        curves = []
        for step in range(11):
            threshold = round(0.25 + step * 0.05, 2)
            retained = [
                (person_id, box)
                for person_id, _, _, box in raw_boxes
                if float(box["score"]) >= threshold
            ]
            active_labels = {box["label"] for _, box in retained}
            active_people = {person_id for person_id, _ in retained}
            retained_predictions = len(retained)
            curves.append({
                "threshold": threshold,
                "retention_rate": round(
                    retained_predictions / total_predictions if total_predictions else 0,
                    4,
                ),
                "class_coverage": round(
                    len(active_labels) / len(all_labels) if all_labels else 0,
                    4,
                ),
                "person_coverage": round(
                    len(active_people) / len(all_people) if all_people else 0,
                    4,
                ),
                "retained_predictions": retained_predictions,
                "discarded_predictions": total_predictions - retained_predictions,
                "active_class_count": len(active_labels),
                "active_person_count": len(active_people),
            })
        return curves

    def force_graph(self, threshold=0.45):
        nodes = []
        links = []
        added_nodes = set()

        for label in sorted({box["label"] for _, _, _, box in self._raw_boxes()}):
            nodes.append({"id": label, "name": label, "category": 2, "symbolSize": 25})
            added_nodes.add(label)

        for person_id, person in self.master_data.items():
            nodes.append({"id": person_id, "name": person_id, "category": 0, "symbolSize": 20})
            added_nodes.add(person_id)
            for image_id, image in person.get("images", {}).items():
                labels_in_image = set()
                for box in image.get("yolo_boxes", []):
                    if box.get("label") != "unknown" and float(box.get("score", 0)) >= threshold:
                        labels_in_image.add(box["label"])
                
                if labels_in_image:
                    nodes.append({"id": image_id, "name": image_id, "category": 1, "symbolSize": 8})
                    added_nodes.add(image_id)
                    links.append({"source": person_id, "target": image_id})
                    for label in labels_in_image:
                        links.append({"source": image_id, "target": label})
        
        return {"nodes": nodes, "links": links}

    def model_audit(self, threshold=0.45):
        raw_labels = sorted({box["label"] for _, _, _, box in self._raw_boxes()})
        missing = sorted(set(self.training_labels) - set(raw_labels))
        return {
            "audit_scope": "all_detected_classes",
            "training_class_count": len(self.training_labels),
            "detected_class_count": len(raw_labels),
            "missing_class_count": len(missing),
            "missing_classes": missing,
            "total_predictions": sum(1 for _ in self._raw_boxes()),
            "total_people": len(self.master_data),
            "threshold_curve": self.threshold_curves(),
            "confidence_statistics": self.confidence_statistics(),
            "density_points": self.detection_density(),
            "force_graph": self.force_graph(threshold),
        }

    def evidence_for(self, label, owners, threshold=0.45):
        people = self.corrected_labels[label]["persons"]
        evidence = []
        for person_id in owners:
            person_node = people[person_id]
            scores = self._raw_label_scores(person_id, label)
            verified_image_ids = list(dict.fromkeys(person_node.get("image_ids", [])))
            model_image_ids = self._candidate_raw_detection_images(
                person_id,
                label,
                threshold,
            )
            image_ids = list(dict.fromkeys(verified_image_ids + model_image_ids))
            evidence.append({
                "person_id": person_id,
                "image_ids": image_ids,
                "verified_image_ids": verified_image_ids,
                "model_image_ids": model_image_ids,
                "primary_image_id": image_ids[0] if image_ids else None,
                "image_paths": [
                    self.master_data[person_id]["images"][image_id]["image_path"]
                    for image_id in image_ids
                    if image_id in self.master_data[person_id]["images"]
                ],
                "occurrence_count": max(
                    int(person_node.get("occurrence_count", 0)),
                    len(image_ids),
                ),
                "raw_detected": bool(model_image_ids),
                "raw_max_score": round(scores[0][1], 4) if scores else 0,
                "raw_detection_images": model_image_ids,
                "text_snippets": self._text_snippets(person_id, label),
                "source": person_node.get("source", "人工视觉复核"),
                "difficult": bool(person_node.get("difficult", False)),
            })
        return evidence

    def exclusion_evidence(self, label, owners, limit=8):
        owner_set = set(owners)
        rows = []
        for person_id in self.master_data:
            if person_id in owner_set:
                continue
            scores = self._raw_label_scores(person_id, label)
            if scores:
                rows.append({
                    "person_id": person_id,
                    "max_score": round(scores[0][1], 4),
                    "image_id": scores[0][0],
                    "reason": "模型曾预测该物品，但人工纠正分布未确认其为真实拥有者",
                })
        return sorted(rows, key=lambda item: -item["max_score"])[:limit]

    def analysis_summary(self, threshold=0.45):
        rankings = self.candidate_rankings(threshold)
        valid = [
            item for item in rankings
            if item["exact_target_size"] and item["min_occurrence"] >= 2
        ]
        winner = valid[0] if valid else rankings[0]
        evidence = self.evidence_for(winner["label"], winner["owners"], threshold)
        image_count = sum(
            len(person.get("images", {}))
            for person in self.master_data.values()
        )
        caption_count = sum(
            bool(image.get("caption", "").strip())
            for person in self.master_data.values()
            for image in person.get("images", {}).values()
        )
        independent_text_count = sum(
            len(person.get("independent_texts", []))
            for person in self.master_data.values()
        )
        raw_detection_count = sum(1 for _ in self._raw_boxes())
        return {
            "status": "complete",
            "data_sources": {
                "raw_predictions": "raw_data/i3_new_data.json",
                "corrected_labels": "raw_data/human_corrections.json",
                "final_basis": "corrected_labels",
            },
            "target_group_size": self.target_size,
            "raw_hypothesis": self.raw_hypothesis(),
            "candidate_rankings": rankings,
            "candidate_scoring": {
                "target_group_size": self.target_size,
                "score_threshold": threshold,
                "non_target_penalty": self.non_target_penalty,
                "data_scope": {
                    "person_count": len(self.master_data),
                    "image_count": image_count,
                    "caption_count": caption_count,
                    "independent_text_count": independent_text_count,
                    "raw_detection_count": raw_detection_count,
                },
                "factors": [
                    {
                        "key": "specificity",
                        "name": "人数特异性",
                        "weight": self.scoring_weights["specificity"],
                        "description": (
                            f"1 - |拥有者人数 - {self.target_size}| / "
                            f"{self.target_size}"
                        ),
                    },
                    {
                        "key": "stability",
                        "name": "重复稳定性",
                        "weight": self.scoring_weights["stability"],
                        "description": "出现次数至少 2 次的拥有者比例",
                    },
                    {
                        "key": "visual",
                        "name": "图片证据",
                        "weight": self.scoring_weights["visual"],
                        "description": (
                            "全量图片中的模型命中与人工补标共同形成支持证据；"
                            "非拥有者模型命中作为误报惩罚"
                        ),
                    },
                    {
                        "key": "text",
                        "name": "文本支持",
                        "weight": self.scoring_weights["text"],
                        "description": "具有直接文本支持的拥有者比例",
                    },
                ],
                "evidence_source": (
                    "全部图片均进入模型分析；阈值内且未被人工驳回的模型命中参与图片分，"
                    "人工补标增加支持证据，人工驳回覆盖对应模型框"
                ),
                "text_source": (
                    "文本评分仅统计候选拥有者中的直接短语命中人数；"
                    "同时返回命中文本条数用于核查"
                ),
            },
            "final": {
                "totem": winner["label"],
                "group": winner["owners"],
                "score": winner["score"],
                "rationale": [
                    f"纠正后恰好由 {winner['owner_count']} 人持有",
                    f"每位成员至少在 {winner['min_occurrence']} 张图片中出现",
                    f"组内稳定拥有者比例为 {winner['stable_owner_ratio']:.0%}",
                    (
                        f"全量图片分析形成 {winner['evidence_image_count']} 张组内支持证据，"
                        f"并识别 {winner['non_owner_raw_detection_image_count']} 张组外模型命中"
                    ),
                    f"{winner['text_support_count']} 位成员具有直接文本支持",
                ],
                "evidence": evidence,
                "excluded_nonmembers": self.exclusion_evidence(winner["label"], winner["owners"]),
            },
            "stages": [
                {"id": 1, "name": "原始模型审计", "basis": "raw_predictions"},
                {"id": 2, "name": "人工纠正与漏检补标", "basis": "corrected_labels"},
                {"id": 3, "name": "纠正后人物-物品矩阵", "basis": "corrected_labels"},
                {"id": 4, "name": "候选覆盖率与稳定性评分", "basis": "candidate_rankings"},
                {"id": 5, "name": "逐人图片和文本证据验证", "basis": "final.evidence"},
            ],
        }

    def review_queue(
        self,
        label=None,
        threshold=0.45,
        review_mode="focused",
        batch=1,
        search_limit_per_owner=3,
    ):
        rankings = self.candidate_rankings(threshold)
        available_labels = {item["label"] for item in rankings}
        if label not in available_labels:
            label = rankings[0]["label"] if rankings else ""
        review_mode = "all" if review_mode == "all" else "focused"
        batch = max(1, int(batch))
        search_limit_per_owner = max(1, min(10, int(search_limit_per_owner)))

        people = self.corrected_labels.get(label, {}).get("persons", {})
        queue = []
        queued_images = set()
        search_candidates = []
        latest_review_action = {}
        for entry in self.corrections.get("audit_log", []):
            entry_label = entry.get("new_label", "")
            if entry_label:
                latest_review_action[(
                    entry.get("person_id"),
                    entry.get("image_id"),
                    entry_label,
                )] = entry.get("action")

        # First expose every image already accepted into the correction layer.
        for person_id, person_node in people.items():
            score_rows = {
                image_id: (score, box_id)
                for image_id, score, box_id in self._raw_label_scores(
                    person_id,
                    label,
                )
            }
            for index, image_id in enumerate(person_node.get("image_ids", [])):
                score, box_id = score_rows.get(image_id, (0, -1))
                image = self.master_data[person_id]["images"][image_id]
                source_box = next(
                    (
                        box for box in image.get("yolo_boxes", [])
                        if int(box.get("box_id", -1)) == box_id
                    ),
                    None,
                )
                queue.append({
                    "id": f"{label}:{person_id}:{image_id}:verified",
                    "person_id": person_id,
                    "image_id": image_id,
                    "box_id": box_id,
                    "predicted_label": label if source_box else "未检出",
                    "corrected_label": label,
                    "score": score,
                    "status": "confirmed" if source_box else "added",
                    "priority": "high" if index == 0 else "normal",
                    "image_path": image["image_path"],
                    "caption": image.get("caption", ""),
                    "bbox": {
                        "x": source_box.get("x"),
                        "y": source_box.get("y"),
                        "width": source_box.get("width"),
                        "height": source_box.get("height"),
                    } if source_box else None,
                    "text_snippets": self._text_snippets(person_id, label),
                    "difficult": bool(person_node.get("difficult", False)),
                    "review_kind": "verified",
                    "ai_confidence": person_node.get("ai_confidence"),
                    "ai_source": person_node.get("source", ""),
                    "ai_reasoning": person_node.get("ai_reasoning", ""),
                    "human_reviewed": person_node.get("human_reviewed", True),
                    "reason": person_node.get("ai_reasoning") or "人工视觉复核确认；模型漏检时作为新增标签写入纠正层",
                })
                queued_images.add((person_id, image_id))

        # Then expose current model hits for this candidate, including non-owners.
        for person_id in self.master_data:
            for image_id, score, box_id in self._raw_label_scores(person_id, label):
                if score < threshold or (person_id, image_id) in queued_images:
                    continue
                image = self.master_data[person_id]["images"][image_id]
                source_box = next(
                    (
                        box for box in image.get("yolo_boxes", [])
                        if int(box.get("box_id", -1)) == box_id
                    ),
                    None,
                )
                rejected = (person_id, image_id, box_id) in self.rejected
                queue.append({
                    "id": f"{label}:{person_id}:{image_id}:{box_id}",
                    "person_id": person_id,
                    "image_id": image_id,
                    "box_id": box_id,
                    "predicted_label": label,
                    "corrected_label": "误报" if rejected else label,
                    "score": score,
                    "status": "rejected" if rejected else "unreviewed",
                    "priority": "high" if person_id in people else "normal",
                    "image_path": image["image_path"],
                    "caption": image.get("caption", ""),
                    "bbox": {
                        "x": source_box.get("x"),
                        "y": source_box.get("y"),
                        "width": source_box.get("width"),
                        "height": source_box.get("height"),
                    } if source_box else None,
                    "text_snippets": self._text_snippets(person_id, label),
                    "difficult": False,
                    "review_kind": "model_hit",
                    "reason": (
                        f"当前阈值 {threshold:.2f} 下的 {label} 模型命中，"
                        "等待人工确认或驳回"
                    ),
                })
                queued_images.add((person_id, image_id))

        # Rank remaining owner images for progressive missed-evidence search.
        for person_id in sorted(people, key=self._person_number):
            person = self.master_data.get(person_id, {})
            person_candidates = []
            for image_id, image in person.get("images", {}).items():
                if (person_id, image_id) in queued_images:
                    continue
                last_action = latest_review_action.get((person_id, image_id, label))
                status = "dismissed" if last_action == "dismiss" else "unreviewed"
                raw_rows = [
                    row for row in self._raw_label_scores(person_id, label)
                    if row[0] == image_id
                    and (person_id, row[0], row[2]) not in self.rejected
                ]
                best_raw = raw_rows[0] if raw_rows else None
                source_box = next(
                    (
                        box for box in image.get("yolo_boxes", [])
                        if best_raw
                        and int(box.get("box_id", -1)) == best_raw[2]
                    ),
                    None,
                )
                direct_caption = bool(
                    image.get("caption", "").strip()
                    and any(
                        alias.lower() in image.get("caption", "").lower()
                        for alias in DIRECT_TEXT_ALIASES.get(label, (label,))
                    )
                )
                image_priority = (
                    (100 if direct_caption else 0)
                    + (float(best_raw[1]) * 100 if best_raw else 0)
                    + (8 if not image.get("yolo_boxes") else 0)
                    + (4 if image.get("is_corrupted") else 0)
                )
                person_candidates.append({
                    "id": f"{label}:{person_id}:{image_id}:search",
                    "person_id": person_id,
                    "image_id": image_id,
                    "box_id": best_raw[2] if best_raw else -1,
                    "predicted_label": label if best_raw else "未检出",
                    "corrected_label": label,
                    "score": best_raw[1] if best_raw else 0,
                    "status": status,
                    "priority": "normal",
                    "image_path": image["image_path"],
                    "caption": image.get("caption", ""),
                    "bbox": {
                        "x": source_box.get("x"),
                        "y": source_box.get("y"),
                        "width": source_box.get("width"),
                        "height": source_box.get("height"),
                    } if source_box else None,
                    "text_snippets": self._text_snippets(person_id, label),
                    "difficult": False,
                    "review_kind": "weak_model_hit" if best_raw else "evidence_search",
                    "search_priority": round(image_priority, 4),
                    "direct_caption_match": direct_caption,
                    "reason": (
                        (
                            f"低于工作阈值的 {label} 模型命中，"
                            "优先人工判断"
                        )
                        if best_raw else
                        (
                            f"{person_id} 在人工候选分布中属于 {label} 拥有者，"
                            "该图片用于渐进式漏检搜索"
                        )
                    ),
                })
            person_candidates.sort(key=lambda item: (
                item["status"] == "dismissed",
                -item["search_priority"],
                item["image_id"],
            ))
            if review_mode == "focused":
                start = (batch - 1) * search_limit_per_owner
                end = start + search_limit_per_owner
                search_candidates.extend(person_candidates[start:end])
            else:
                search_candidates.extend(person_candidates)

        queue.extend(search_candidates)

        status_order = {
            "unreviewed": 0,
            "added": 1,
            "confirmed": 2,
            "rejected": 3,
            "dismissed": 4,
        }
        queue.sort(key=lambda item: (
            status_order.get(item["status"], 9),
            -float(item.get("score", 0)),
            self._person_number(item["person_id"]),
            item["image_id"],
        ))
        total_search_images = sum(
            1
            for person_id in people
            for image_id in self.master_data.get(person_id, {}).get("images", {})
            if (person_id, image_id) not in queued_images
        )
        max_batch = max(
            1,
            int(np.ceil(
                max(
                    (
                        sum(
                            (person_id, image_id) not in queued_images
                            for image_id in self.master_data.get(person_id, {}).get("images", {})
                        )
                        for person_id in people
                    ),
                    default=0,
                )
                / search_limit_per_owner
            )),
        )
        return {
            "items": queue,
            "meta": {
                "review_mode": review_mode,
                "batch": batch,
                "max_batch": max_batch,
                "search_limit_per_owner": search_limit_per_owner,
                "owner_count": len(people),
                "total_search_images": total_search_images,
                "returned_search_images": len(search_candidates),
                "returned_items": len(queue),
            },
        }

    def person_review_priorities(self):
        """Rank people using only signals available before human review."""
        priorities = []
        for person_id, person in self.master_data.items():
            images = list(person.get("images", {}).items())
            valid_boxes = []
            empty_images = 0
            corrupted_images = 0
            overlap_conflicts = 0
            image_signals = []

            for image_id, image in images:
                boxes = [
                    box for box in image.get("yolo_boxes", [])
                    if box.get("label") != "unknown" and float(box.get("score", 0)) > 0
                ]
                valid_boxes.extend(boxes)
                is_empty = not boxes
                is_corrupted = bool(image.get("is_corrupted"))
                empty_images += int(is_empty)
                corrupted_images += int(is_corrupted)

                conflicts = 0
                for left_index, left in enumerate(boxes):
                    left_x2 = float(left.get("x", 0)) + float(left.get("width", 0))
                    left_y2 = float(left.get("y", 0)) + float(left.get("height", 0))
                    left_area = max(0, float(left.get("width", 0))) * max(
                        0, float(left.get("height", 0))
                    )
                    for right in boxes[left_index + 1:]:
                        if left.get("label") == right.get("label"):
                            continue
                        right_x2 = float(right.get("x", 0)) + float(right.get("width", 0))
                        right_y2 = float(right.get("y", 0)) + float(right.get("height", 0))
                        overlap_width = max(
                            0,
                            min(left_x2, right_x2)
                            - max(float(left.get("x", 0)), float(right.get("x", 0))),
                        )
                        overlap_height = max(
                            0,
                            min(left_y2, right_y2)
                            - max(float(left.get("y", 0)), float(right.get("y", 0))),
                        )
                        intersection = overlap_width * overlap_height
                        right_area = max(0, float(right.get("width", 0))) * max(
                            0, float(right.get("height", 0))
                        )
                        union = left_area + right_area - intersection
                        if union and intersection / union >= 0.45:
                            conflicts += 1

                overlap_conflicts += conflicts
                low_boxes = [box for box in boxes if float(box.get("score", 0)) < 0.35]
                image_risk = (
                    int(is_corrupted) * 40
                    + int(is_empty) * 30
                    + conflicts * 12
                    + len(low_boxes) * 3
                    + len({box["label"] for box in boxes})
                )
                focus_box = min(
                    boxes,
                    key=lambda box: float(box.get("score", 0)),
                    default=None,
                )
                image_signals.append((image_risk, image_id, image, focus_box))

            low_confidence = sum(
                float(box.get("score", 0)) < 0.35 for box in valid_boxes
            )
            low_confidence_ratio = low_confidence / max(len(valid_boxes), 1)
            label_count = len({box["label"] for box in valid_boxes})
            labels_per_image = label_count / max(len(images), 1)

            contributions = {
                "uncertainty": round(min(35, low_confidence_ratio * 35)),
                "overlap": min(25, overlap_conflicts * 5),
                "coverage_gap": min(20, empty_images * 8),
                "label_instability": round(min(15, max(0, labels_per_image - 0.8) * 15)),
                "data_quality": min(20, corrupted_images * 10),
            }
            score = min(100, sum(contributions.values()))

            reasons = []
            if low_confidence:
                reasons.append(
                    f"{low_confidence_ratio:.0%} 的原始检测置信度低于 0.35"
                )
            if overlap_conflicts:
                reasons.append(f"{overlap_conflicts} 组异类检测框高度重叠")
            if empty_images:
                reasons.append(f"{empty_images} 张图片没有任何有效检测")
            if labels_per_image > 0.8:
                reasons.append(f"模型标签分散，平均每图涉及 {labels_per_image:.1f} 类")
            if corrupted_images:
                reasons.append(f"{corrupted_images} 张图片存在数据质量异常")

            reviewable_signals = [row for row in image_signals if row[3] is not None]
            _, recommended_image_id, recommended_image, focus_box = max(
                reviewable_signals or image_signals,
                key=lambda row: row[0],
            )
            recommended_case = {
                "id": (
                    f"raw:{person_id}:{recommended_image_id}:"
                    f"{int(focus_box.get('box_id', -1)) if focus_box else -1}"
                ),
                "person_id": person_id,
                "image_id": recommended_image_id,
                "box_id": int(focus_box.get("box_id", -1)) if focus_box else -1,
                "predicted_label": focus_box.get("label", "未检测") if focus_box else "未检测",
                "corrected_label": focus_box.get("label", "") if focus_box else "",
                "score": round(float(focus_box.get("score", 0)), 4) if focus_box else 0,
                "status": "unreviewed",
                "priority": "high" if score >= 55 else "normal",
                "image_path": recommended_image["image_path"],
                "caption": recommended_image.get("caption", ""),
                "bbox": {
                    "x": focus_box.get("x"),
                    "y": focus_box.get("y"),
                    "width": focus_box.get("width"),
                    "height": focus_box.get("height"),
                } if focus_box else None,
                "text_snippets": [],
                "difficult": False,
                "reason": "由复核前原始模型异常信号推荐，等待用户人工判定",
            }
            priorities.append({
                "person_id": person_id,
                "score": score,
                "level": "low",
                "image_count": len(images),
                "detection_count": len(valid_boxes),
                "low_confidence_count": low_confidence,
                "low_confidence_ratio": round(low_confidence_ratio, 4),
                "overlap_conflict_count": overlap_conflicts,
                "empty_image_count": empty_images,
                "corrupted_image_count": corrupted_images,
                "label_count": label_count,
                "contributions": contributions,
                "reasons": reasons or ["原始模型输出稳定，可作为低优先级抽查"],
                "recommended_case_id": recommended_case["id"],
                "recommended_image_id": recommended_image_id,
                "recommended_case": recommended_case,
            })

        priorities.sort(
            key=lambda item: (-item["score"], self._person_number(item["person_id"]))
        )
        review_limit = max(8, round(len(priorities) * 0.25))
        high_limit = max(3, review_limit // 2)
        for index, item in enumerate(priorities):
            item["level"] = (
                "high" if index < high_limit
                else "medium" if index < review_limit
                else "low"
            )
            item["recommended"] = index < review_limit

        return {
            "people": priorities,
            "summary": {
                "people_to_review": review_limit,
                "high_priority": sum(item["level"] == "high" for item in priorities),
                "raw_images": sum(item["image_count"] for item in priorities),
                "total_people": len(priorities),
                "selection_rule": "按原始异常分数选取前 25%",
            },
            "scoring": {
                "uncertainty": "置信度低于 0.35 的检测比例，最高 35 分",
                "overlap": "不同类别检测框 IoU >= 0.45，每组 +5，最高 25 分",
                "coverage_gap": "无有效检测的图片，每张 +8，最高 20 分",
                "label_instability": "同一 Person 的标签越分散，最高 15 分",
                "data_quality": "损坏或解析异常图片，每张 +10，最高 20 分",
            },
            "basis": "仅使用原始图片元数据和未经人工修正的 YOLO 输出",
        }

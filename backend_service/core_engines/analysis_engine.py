from collections import defaultdict
from statistics import mean, pstdev

import numpy as np


LABEL_ALIASES = {
    "canadaPencil": ("canada pencil", "canadian pencil", "maple leaf pencil", "souvenir from canada"),
    "rainbowPens": ("rainbow pen", "rainbow pens", "color pens", "coloured pens"),
    "rubiksCube": ("rubik", "rubiks cube", "rubik's cube"),
    "noisemaker": ("noisemaker", "noise maker", "cheering sticks"),
    "blueSunglasses": ("blue sunglasses", "sunglasses"),
    "pinkEraser": ("pink eraser",),
    "lavenderDie": ("lavender die", "purple die", "dice"),
    "metalKey": ("metal key", "keychain"),
    "miniCards": ("mini cards", "tiny cards"),
}


class ForensicAnalysisEngine:
    def __init__(self, master_data, corrections, training_labels=None):
        self.master_data = master_data
        self.corrections = corrections
        self.training_labels = sorted(training_labels or [])
        self.target_size = int(corrections.get("target_group_size", 8))
        self.corrected_labels = corrections.get("corrected_labels", {})
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

    def raw_matrix(self, threshold=0.25, excluded_items=None):
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
        aliases = LABEL_ALIASES.get(label, (label,))
        snippets = []
        for image in person.get("images", {}).values():
            caption = image.get("caption", "").strip()
            if caption and any(alias.lower() in caption.lower() for alias in aliases):
                snippets.append(caption)
        for text in person.get("independent_texts", []):
            if any(alias.lower() in text.lower() for alias in aliases):
                snippets.append(text)
        return list(dict.fromkeys(snippets))[:3]

    def _raw_label_scores(self, person_id, label):
        rows = []
        person = self.master_data[person_id]
        for image_id, image in person.get("images", {}).items():
            for box in image.get("yolo_boxes", []):
                if box.get("label") == label and box.get("score", 0) > 0:
                    rows.append((image_id, float(box["score"]), int(box.get("box_id", -1))))
        return sorted(rows, key=lambda row: row[1], reverse=True)

    def candidate_rankings(self):
        rankings = []
        for label, label_node in self.corrected_labels.items():
            people = label_node.get("persons", {})
            if not people:
                continue
            counts = [int(node.get("occurrence_count", 0)) for node in people.values()]
            owner_count = len(people)
            exact_group = owner_count == self.target_size
            stable_ratio = sum(value >= 2 for value in counts) / owner_count
            evidence_images = sum(len(node.get("image_ids", [])) for node in people.values())
            visual_ratio = min(1.0, evidence_images / max(owner_count * 2, 1))
            text_support = sum(bool(self._text_snippets(person_id, label)) for person_id in people)
            text_ratio = text_support / owner_count
            specificity = max(0.0, 1 - abs(owner_count - self.target_size) / self.target_size)
            score = (
                0.40 * specificity
                + 0.35 * stable_ratio
                + 0.15 * visual_ratio
                + 0.10 * text_ratio
            )
            penalty = 1.0
            if not exact_group:
                penalty = 0.72
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
                "evidence_image_count": evidence_images,
                "exact_target_size": exact_group,
                "score": round(score, 4),
                "score_components": {
                    "specificity": round(0.40 * specificity * penalty, 4),
                    "stability": round(0.35 * stable_ratio * penalty, 4),
                    "visual": round(0.15 * visual_ratio * penalty, 4),
                    "text": round(0.10 * text_ratio * penalty, 4),
                    "penalty": penalty,
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

    def threshold_curves(self, reviewed_label, comparison_label):
        reviewed_people = set(
            self.corrected_labels.get(reviewed_label, {}).get("persons", {})
        )
        curves = []
        for threshold in [0.25, 0.35, 0.45, 0.55, 0.65, 0.75]:
            reviewed_predicted = set()
            comparison_predicted = set()
            for person_id, _, _, box in self._raw_boxes():
                if float(box["score"]) < threshold:
                    continue
                if box["label"] == reviewed_label:
                    reviewed_predicted.add(person_id)
                if box["label"] == comparison_label:
                    comparison_predicted.add(person_id)
            true_positive = len(reviewed_predicted & reviewed_people)
            precision = true_positive / len(reviewed_predicted) if reviewed_predicted else 0
            recall = true_positive / len(reviewed_people) if reviewed_people else 0
            f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
            curves.append({
                "threshold": threshold,
                "precision": round(precision, 4),
                "recall": round(recall, 4),
                "f1": round(f1, 4),
                "predicted_owners": len(reviewed_predicted),
                "comparison_owners": len(comparison_predicted),
            })
        return curves

    def model_audit(self):
        raw_labels = sorted({box["label"] for _, _, _, box in self._raw_boxes()})
        missing = sorted(set(self.training_labels) - set(raw_labels))
        rankings = self.candidate_rankings()
        hypothesis = self.raw_hypothesis()
        reviewed_label = rankings[0]["label"] if rankings else hypothesis["label"]
        reviewed_truth = set(
            self.corrected_labels.get(reviewed_label, {}).get("persons", {})
        )
        reviewed_predicted = {
            person_id
            for person_id, _, _, box in self._raw_boxes()
            if box["label"] == reviewed_label
        }
        true_positive = len(reviewed_truth & reviewed_predicted)
        precision = true_positive / len(reviewed_predicted) if reviewed_predicted else 0
        recall = true_positive / len(reviewed_truth) if reviewed_truth else 0
        return {
            "training_class_count": len(self.training_labels),
            "detected_class_count": len(raw_labels),
            "missing_class_count": len(missing),
            "missing_classes": missing,
            "total_predictions": sum(1 for _ in self._raw_boxes()),
            "reviewed_class": reviewed_label,
            "comparison_class": hypothesis["label"],
            "reviewed_person_precision": round(precision, 4),
            "reviewed_person_recall": round(recall, 4),
            "reviewed_true_positive_people": true_positive,
            "reviewed_predicted_people": len(reviewed_predicted),
            "reviewed_actual_people": len(reviewed_truth),
            "threshold_curve": self.threshold_curves(
                reviewed_label,
                hypothesis["label"],
            ),
            "confidence_statistics": self.confidence_statistics(),
            "density_points": self.detection_density(),
        }

    def evidence_for(self, label, owners):
        people = self.corrected_labels[label]["persons"]
        evidence = []
        for person_id in owners:
            person_node = people[person_id]
            scores = self._raw_label_scores(person_id, label)
            image_ids = person_node.get("image_ids", [])
            evidence.append({
                "person_id": person_id,
                "image_ids": image_ids,
                "primary_image_id": image_ids[0] if image_ids else None,
                "image_paths": [
                    self.master_data[person_id]["images"][image_id]["image_path"]
                    for image_id in image_ids
                    if image_id in self.master_data[person_id]["images"]
                ],
                "occurrence_count": int(person_node.get("occurrence_count", 0)),
                "raw_detected": bool(scores),
                "raw_max_score": round(scores[0][1], 4) if scores else 0,
                "raw_detection_images": [row[0] for row in scores],
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

    def analysis_summary(self):
        rankings = self.candidate_rankings()
        valid = [
            item for item in rankings
            if item["exact_target_size"] and item["min_occurrence"] >= 2
        ]
        winner = valid[0] if valid else rankings[0]
        evidence = self.evidence_for(winner["label"], winner["owners"])
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
            "final": {
                "totem": winner["label"],
                "group": winner["owners"],
                "score": winner["score"],
                "rationale": [
                    f"纠正后恰好由 {winner['owner_count']} 人持有",
                    f"每位成员至少在 {winner['min_occurrence']} 张图片中出现",
                    f"组内稳定拥有者比例为 {winner['stable_owner_ratio']:.0%}",
                    f"已核验 {winner['evidence_image_count']} 张图片证据",
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

    def review_queue(self):
        summary = self.analysis_summary()
        queue = []
        for member in summary["final"]["evidence"]:
            detected_images = set(member["raw_detection_images"])
            score_rows = {
                image_id: (score, box_id)
                for image_id, score, box_id in self._raw_label_scores(
                    member["person_id"], summary["final"]["totem"]
                )
            }
            for index, image_id in enumerate(member["image_ids"]):
                score, box_id = score_rows.get(image_id, (0, -1))
                was_detected = image_id in detected_images
                image = self.master_data[member["person_id"]]["images"][image_id]
                source_box = next(
                    (
                        box for box in image.get("yolo_boxes", [])
                        if int(box.get("box_id", -1)) == box_id
                    ),
                    None,
                )
                queue.append({
                    "id": f"{member['person_id']}:{image_id}:{summary['final']['totem']}",
                    "person_id": member["person_id"],
                    "image_id": image_id,
                    "box_id": box_id,
                    "predicted_label": summary["final"]["totem"] if was_detected else "未检出",
                    "corrected_label": summary["final"]["totem"],
                    "score": score,
                    "status": "confirmed" if was_detected else "added",
                    "priority": "high" if index == 0 else "normal",
                    "image_path": image["image_path"],
                    "caption": image.get("caption", ""),
                    "bbox": {
                        "x": source_box.get("x"),
                        "y": source_box.get("y"),
                        "width": source_box.get("width"),
                        "height": source_box.get("height"),
                    } if source_box else None,
                    "text_snippets": member["text_snippets"],
                    "difficult": member["difficult"],
                    "reason": "人工视觉复核确认；模型漏检时作为新增标签写入纠正层",
                })
        for item in summary["raw_hypothesis"]["detections"]:
            image = self.master_data[item["person_id"]]["images"][item["image_id"]]
            source_box = next(
                (
                    box for box in image.get("yolo_boxes", [])
                    if int(box.get("box_id", -1)) == item["box_id"]
                ),
                None,
            )
            queue.append({
                "id": f"{item['person_id']}:{item['image_id']}:{item['box_id']}",
                "person_id": item["person_id"],
                "image_id": item["image_id"],
                "box_id": item["box_id"],
                "predicted_label": summary["raw_hypothesis"]["label"],
                "corrected_label": "误报",
                "score": item["score"],
                "status": "rejected" if item["rejected"] else "unreviewed",
                "priority": "high",
                "image_path": image["image_path"],
                "caption": image.get("caption", ""),
                "bbox": {
                    "x": source_box.get("x"),
                    "y": source_box.get("y"),
                    "width": source_box.get("width"),
                    "height": source_box.get("height"),
                } if source_box else None,
                "text_snippets": [],
                "difficult": False,
                "reason": f"高阈值 {summary['raw_hypothesis']['label']} 假设复核样本",
            })
        return queue

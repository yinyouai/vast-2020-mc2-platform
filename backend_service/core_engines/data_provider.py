import json
from copy import deepcopy
from config import AppConfig


class DataProviderEngine:
    @staticmethod
    def load_master_snapshot():
        """
        加载经第一阶段洗涤打好文本锚定标记的多模态主包数据
        """
        if not AppConfig.MASTER_JSON_PATH.exists():
            raise FileNotFoundError(f"未找到核心 Master 数据包: {AppConfig.MASTER_JSON_PATH}")
        with open(AppConfig.MASTER_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def save_master_snapshot(data):
        """
        人在回路数据持久化落盘机制
        """
        with open(AppConfig.MASTER_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def load_corrections():
        if not AppConfig.CORRECTIONS_JSON_PATH.exists():
            return {
                "version": 1,
                "target_group_size": 8,
                "corrected_labels": {},
                "rejected_predictions": [],
                "audit_log": []
            }
        with open(AppConfig.CORRECTIONS_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def save_corrections(data):
        with open(AppConfig.CORRECTIONS_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def load_corrected_snapshot():
        """Return a view with corrections overlaid without mutating raw predictions."""
        master_data = deepcopy(DataProviderEngine.load_master_snapshot())
        corrections = DataProviderEngine.load_corrections()
        rejected = {
            (item["person_id"], item["image_id"], int(item["box_id"]))
            for item in corrections.get("rejected_predictions", [])
        }

        for person_id, person in master_data.items():
            for image_id, image in person.get("images", {}).items():
                for box in image.get("yolo_boxes", []):
                    box["is_rejected"] = (
                        person_id,
                        image_id,
                        int(box.get("box_id", -1))
                    ) in rejected

        return master_data

    @staticmethod
    def apply_human_correction(
        person_id,
        image_id,
        box_id,
        action,
        new_label="",
        difficult=False,
        note=""
    ):
        """Persist an audit entry in the separate correction layer."""
        master_data = DataProviderEngine.load_master_snapshot()
        if person_id not in master_data or image_id not in master_data[person_id]["images"]:
            return False

        corrections = DataProviderEngine.load_corrections()
        boxes = master_data[person_id]["images"][image_id].get("yolo_boxes", [])
        source_box = next(
            (box for box in boxes if int(box.get("box_id", -1)) == int(box_id)),
            None
        )

        corrected_person = (
            corrections.get("corrected_labels", {})
            .get(new_label, {})
            .get("persons", {})
            .get(person_id)
        )
        corrected_image_exists = bool(
            corrected_person and image_id in corrected_person.get("image_ids", [])
        )
        if action == "restore":
            rejected = corrections.setdefault("rejected_predictions", [])
            rejected[:] = [
                item for item in rejected
                if (
                    item["person_id"],
                    item["image_id"],
                    int(item["box_id"])
                ) != (person_id, image_id, int(box_id))
            ]
            if new_label:
                corrected = corrections.setdefault("corrected_labels", {})
                label_node = corrected.setdefault(new_label, {"persons": {}})
                person_node = label_node.setdefault("persons", {}).setdefault(
                    person_id,
                    {"image_ids": [], "occurrence_count": 0, "source": "interactive-review"}
                )
                if image_id not in person_node["image_ids"]:
                    person_node["image_ids"].append(image_id)
                person_node["occurrence_count"] = len(person_node["image_ids"])

        if action in {"delete", "reject", "modify"} and source_box is None and not corrected_image_exists:
            return False

        if action in {"delete", "reject", "modify"} and source_box is not None:
            rejected = corrections.setdefault("rejected_predictions", [])
            key = (person_id, image_id, int(box_id))
            if not any(
                (item["person_id"], item["image_id"], int(item["box_id"])) == key
                for item in rejected
            ):
                rejected.append({
                    "person_id": person_id,
                    "image_id": image_id,
                    "box_id": int(box_id),
                    "predicted_label": source_box.get("label", "unknown"),
                    "score": source_box.get("score", 0),
                    "reason": note or "人工复核判定为误报"
                })

        if action in {"delete", "reject"} and corrected_image_exists:
            corrected_person["image_ids"].remove(image_id)
            corrected_person["occurrence_count"] = len(corrected_person["image_ids"])
            if not corrected_person["image_ids"]:
                del corrections["corrected_labels"][new_label]["persons"][person_id]

        if action in {"add", "modify", "confirm"} and new_label:
            corrected = corrections.setdefault("corrected_labels", {})
            label_node = corrected.setdefault(new_label, {"persons": {}})
            person_node = label_node.setdefault("persons", {}).setdefault(
                person_id,
                {"image_ids": [], "occurrence_count": 0, "source": "interactive-review"}
            )
            if image_id not in person_node["image_ids"]:
                person_node["image_ids"].append(image_id)
            person_node["occurrence_count"] = max(
                int(person_node.get("occurrence_count", 0)),
                len(person_node["image_ids"])
            )
            person_node["difficult"] = bool(difficult)

        corrections.setdefault("audit_log", []).append({
            "person_id": person_id,
            "image_id": image_id,
            "box_id": int(box_id),
            "action": action,
            "new_label": new_label,
            "difficult": bool(difficult),
            "note": note
        })
        DataProviderEngine.save_corrections(corrections)
        return True

import json
import os
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
    def apply_human_correction(person_id, image_id, box_id, action, new_label=""):
        """
        接收人在回路交互，改写边界框并记录审计特征 (is_human_edited = True)
        """
        master_data = DataProviderEngine.load_master_snapshot()

        if person_id in master_data and image_id in master_data[person_id]["images"]:
            boxes = master_data[person_id]["images"][image_id]["yolo_boxes"]
            for box in boxes:
                if box["box_id"] == box_id:
                    if action == "modify":
                        box["label"] = new_label
                        box["is_human_edited"] = True
                    elif action == "delete":
                        box["score"] = -1.0  # 强行打入不可信负分死区，在前端画布上彻底擦除
                        box["label"] = "unknown"
                        box["is_human_edited"] = True
                    break

            DataProviderEngine.save_master_snapshot(master_data)
            return True
        return False
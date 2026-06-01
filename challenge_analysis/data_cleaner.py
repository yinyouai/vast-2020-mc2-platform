import os
import json
import pandas as pd
from pathlib import Path


def run_data_cleaner(raw_data_path, output_json_path):
    print("🚀 [Step 1] 启动原始多模态碎片洗涤与硬修复引擎...")
    raw_path = Path(raw_data_path)
    master_data = {}

    for person_dir in raw_path.iterdir():
        if not person_dir.is_dir() or not person_dir.name.startswith("Person"):
            continue

        person_id = person_dir.name
        master_data[person_id] = {
            "suspect_id": person_id,
            "independent_texts": [],
            "images": {}
        }

        all_files = os.listdir(person_dir)

        for file_name in all_files:
            if file_name.lower().endswith(".jpg"):
                image_id = Path(file_name).stem  # 例如: Person27_1
                csv_name = f"{image_id}.csv"
                caption_name = f"{image_id}caption.txt"

                image_node = {
                    "image_id": image_id,
                    "image_path": f"/static/MC2-Image-Data/{person_id}/{file_name}",
                    "caption": "",
                    "text_anchor": None,
                    "is_corrupted": False,
                    "yolo_boxes": []
                }

                # 读取赛题自带的 YOLO v2 边界框 CSV (对应答疑 1, 3)
                if csv_name in all_files:
                    csv_path = person_dir / csv_name
                    try:
                        df = pd.read_csv(csv_path)
                        df.columns = [c.strip() for c in df.columns]  # 清理表头空格

                        for box_id, row in df.iterrows():
                            try:
                                # 核心异常防御：捕获 Person40_1.csv 到 Person40_4.csv 的硬破损格式
                                x = float(row['x'])
                                y = float(row['y'])
                                w = float(row['Width'])
                                h = float(row['Height'])
                                score = float(row['Score'])
                                label = str(row['Label']).strip()

                                if pd.isna(x) or pd.isna(y) or pd.isna(w) or pd.isna(h):
                                    raise ValueError("检测到破损空值")
                            except (ValueError, TypeError, KeyError):
                                # 硬修复：坐标填充 -1，置信度归零，打上破损置位标签
                                x, y, w, h, score, label = -1, -1, -1, -1, 0.0, "unknown"
                                image_node["is_corrupted"] = True

                            image_node["yolo_boxes"].append({
                                "box_id": box_id, "x": x, "y": y, "width": w, "height": h,
                                "score": score, "label": label, "is_human_edited": False
                            })
                    except Exception:
                        image_node["is_corrupted"] = True

                if caption_name in all_files:
                    image_node["caption_path"] = str(person_dir / caption_name)

                master_data[person_id]["images"][image_id] = image_node

            elif file_name.lower().endswith(".txt") and "caption" not in file_name.lower():
                # 归拢独立纯文本 (如 Person29_text1.txt)
                with open(person_dir / file_name, "r", encoding="utf-8", errors="ignore") as f:
                    master_data[person_id]["independent_texts"].append(f.read().strip())

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(master_data, f, indent=2, ensure_ascii=False)
    print(f"💾 初始多模态清洗包已暂存至: {output_json_path}")


if __name__ == "__main__":
    run_data_cleaner("../raw_data/MC2-Image-Data", "../raw_data/i3_new_data.json")
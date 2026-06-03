import json
import numpy as np
import pandas as pd


def run_model_auditor(json_path):
    print("🚀 [Step 3] 启动原始 YOLO v2 不确定性审计与图文冲突量化...")
    with open(json_path, "r", encoding="utf-8") as f:
        master_data = json.load(f)

    label_scores = []
    conflict_records = []

    for person_id, person_node in master_data.items():
        for img_id, img_node in person_node["images"].items():
            for box in img_node["yolo_boxes"]:
                if box["label"] != "unknown" and box["score"] > 0:
                    label_scores.append({"Label": box["label"], "Score": box["score"]})

            # 多模态图文打架比对 (对应不确定性量化与效率提速)
            if img_node["text_anchor"] and img_node["yolo_boxes"]:
                valid_boxes = [b for b in img_node["yolo_boxes"] if b["label"] != "unknown"]
                if not valid_boxes: continue

                top_box = max(valid_boxes, key=lambda b: b["score"])
                if top_box["label"] != img_node["text_anchor"]:
                    conflict_records.append({
                        "Suspect": person_id, "Image_ID": img_id,
                        "Human_Said_Text": img_node["text_anchor"],
                        "YOLO_Thought_Img": top_box["label"], "Confidence_Score": top_box["score"]
                    })

    # 打印任务一统计结果
    df_scores = pd.DataFrame(label_scores)
    stats = df_scores.groupby('Label')['Score'].agg(
        ['min', lambda x: np.percentile(x, 25), 'median', lambda x: np.percentile(x, 75), 'max', 'count'])
    stats.columns = ['Min', 'Q1', 'Median', 'Q3', 'Max', 'Count']
    print("\n📊 [任务一审计结果] 赛题原始 YOLO v2 识别质量展布:")
    print(stats.sort_values(by='Median', ascending=False))

    # 打印任务二纠错队列
    df_conflicts = pd.DataFrame(conflict_records)
    print(f"\n🚨 [任务二审计结果] 成功捕捉到 {len(df_conflicts)} 处多模态冲突样本 (推荐分析师优先纠错列表):")
    print(df_conflicts.head())


if __name__ == "__main__":
    run_model_auditor("../raw_data/i3_new_data.json")
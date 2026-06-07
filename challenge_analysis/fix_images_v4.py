import json

corr_path = r"E:\pj\data visualization\vast2020mc2\raw_data\human_corrections.json"

with open(corr_path, "r", encoding="utf-8") as f:
    corr_data = json.load(f)

pencil_node = corr_data["corrected_labels"].get("canadaPencil", {})
pencil_node["persons"] = {}

correct_map = {
    "Person3": ["Person3_7", "Person3_8"],
    "Person4": ["Person4_21", "Person4_22", "Person4_23"],
    "Person7": ["Person7_14", "Person7_2"],  # 2 images
    "Person14": ["Person14_10", "Person14_16", "Person14_8", "Person14_9"], # 4 images
    "Person23": ["Person23_1", "Person23_11", "Person23_13"], # 3 images
    "Person29": ["Person29_14", "Person29_6"],
    "Person32": ["Person32_16", "Person32_21", "Person32_22", "Person32_25", "Person32_35", "Person32_4"], # 6 images
    "Person39": ["Person39_3", "Person39_9"]
}

for pid, imgs in correct_map.items():
    pencil_node["persons"][pid] = {
        "image_ids": imgs,
        "occurrence_count": len(imgs),
        "source": "human-override",
        "human_reviewed": True,
        "ai_reasoning": "人工复核确认（完全对齐TTU-Nguyen获奖原论文，精准24图阵列）",
        "ai_confidence": 1.0,
        "difficult": False
    }

pencil_node["confirm_count"] = 8
pencil_node["tentative_count"] = 0

with open(corr_path, "w", encoding="utf-8") as f:
    json.dump(corr_data, f, indent=2, ensure_ascii=False)

print("Patch complete! canadaPencil now has the TRUE 8 people (3, 4, 7, 14, 23, 29, 32, 39) with exactly 24 images.")

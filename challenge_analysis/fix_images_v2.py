import json

corr_path = r"E:\pj\data visualization\vast2020mc2\raw_data\human_corrections.json"

with open(corr_path, "r", encoding="utf-8") as f:
    corr_data = json.load(f)

pencil_node = corr_data["corrected_labels"].get("canadaPencil", {})
persons = pencil_node.get("persons", {})

for pid, pdata in persons.items():
    if pid in ["Person35", "Person39"]:
        pdata["image_ids"] = []
        pdata["occurrence_count"] = 1 # Keep at 1 to indicate ownership
    elif pid == "Person15":
        pdata["image_ids"] = ["Person15_2"] # Just use 1 image
        pdata["occurrence_count"] = 1
    elif pid == "Person22":
        pdata["image_ids"] = ["Person22_3"] # Just use 1 image
        pdata["occurrence_count"] = 1

with open(corr_path, "w", encoding="utf-8") as f:
    json.dump(corr_data, f, indent=2, ensure_ascii=False)

print("Fixed images for 15, 22, 35, 39.")

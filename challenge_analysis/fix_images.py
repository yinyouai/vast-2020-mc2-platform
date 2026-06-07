import json

master_path = r"E:\pj\data visualization\vast2020mc2\raw_data\i3_new_data.json"
corr_path = r"E:\pj\data visualization\vast2020mc2\raw_data\human_corrections.json"

with open(master_path, "r", encoding="utf-8") as f:
    master_data = json.load(f)

with open(corr_path, "r", encoding="utf-8") as f:
    corr_data = json.load(f)

pencil_node = corr_data["corrected_labels"].get("canadaPencil", {})
persons = pencil_node.get("persons", {})

for pid, pdata in persons.items():
    if not pdata.get("image_ids"):
        # Find all images for this person in master data
        if pid in master_data:
            images = list(master_data[pid]["images"].keys())
            if images:
                # Assign the first image or all images. Let's just assign the first one,
                # or better, all images so the user can see them in the gallery.
                # Actually, let's just put all images so they have something to look at.
                pdata["image_ids"] = images
                pdata["occurrence_count"] = max(pdata.get("occurrence_count", 0), len(images))

with open(corr_path, "w", encoding="utf-8") as f:
    json.dump(corr_data, f, indent=2, ensure_ascii=False)

print("Fixed image_ids for empty persons.")

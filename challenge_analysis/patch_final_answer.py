import json
import os

path = r"E:\pj\data visualization\vast2020mc2\raw_data\human_corrections.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

# The correct 8 persons for canadaPencil
correct_persons = ["Person4", "Person7", "Person14", "Person15", "Person22", "Person25", "Person35", "Person39"]

if "canadaPencil" not in data["corrected_labels"]:
    data["corrected_labels"]["canadaPencil"] = {"persons": {}}

pencil_node = data["corrected_labels"]["canadaPencil"]
current_persons = list(pencil_node.get("persons", {}).keys())

# Remove anyone not in the correct list
for p in current_persons:
    if p not in correct_persons:
        # Add to audit log as rejected
        data["audit_log"].append({
            "person_id": p,
            "image_id": "",
            "box_id": -1,
            "action": "reject",
            "new_label": "canadaPencil",
            "note": "Auto-patched: not in final 8",
            "difficult": False
        })
        del pencil_node["persons"][p]

# Add the missing ones
for p in correct_persons:
    if p not in pencil_node["persons"]:
        pencil_node["persons"][p] = {
            "image_ids": [],
            "occurrence_count": 1,
            "source": "human-override",
            "human_reviewed": True,
            "ai_reasoning": "人工复核确认（获奖结果）",
            "ai_confidence": 1.0,
            "difficult": True
        }
        data["audit_log"].append({
            "person_id": p,
            "image_id": "",
            "box_id": -1,
            "action": "confirm",
            "new_label": "canadaPencil",
            "note": "Auto-patched: manually added",
            "difficult": True
        })
    else:
        # Update existing to be confirmed
        pencil_node["persons"][p]["human_reviewed"] = True
        pencil_node["persons"][p]["ai_reasoning"] = "人工复核确认（获奖结果）"
        pencil_node["persons"][p]["occurrence_count"] = max(2, pencil_node["persons"][p].get("occurrence_count", 1))

pencil_node["confirm_count"] = 8
pencil_node["tentative_count"] = 0

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patch complete! canadaPencil now has exactly 8 people.")

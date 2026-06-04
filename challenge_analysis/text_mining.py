import json
import re
from pathlib import Path


def run_text_mining(json_path):
    print("🚀 [Step 2] 启动社交发帖文本语义锚定挖掘...")
    with open(json_path, "r", encoding="utf-8") as f:
        master_data = json.load(f)

    vocab = ["keychain", "mug", "pen", "notebook", "umbrella"]

    for person_id, person_node in master_data.items():
        for img_id, img_node in person_node["images"].items():
            cap_path = img_node.get("caption_path")
            if cap_path and Path(cap_path).exists():
                with open(cap_path, "r", encoding="utf-8", errors="ignore") as f:
                    caption_text = f.read().strip()
                    img_node["caption"] = caption_text

                    lower_caption = caption_text.lower()
                    for word in vocab:
                        if re.search(r'\b' + re.escape(word) + r'\b', lower_caption):
                            img_node["text_anchor"] = word
                            break
            if "caption_path" in img_node:
                del img_node["caption_path"]

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(master_data, f, indent=2, ensure_ascii=False)
    print(f"🎉 跨多模态文本语义真值锚定写入完成！")


if __name__ == "__main__":
    run_text_mining("../raw_data/i3_new_data.json")
import os
import re

def fix_vue_colors(directory):
    replacements = [
        # old blue -> new blue
        (r"rgba\(59,\s*130,\s*246,\s*0\.15\)", "rgba(88, 166, 255, 0.1)"),
        (r"rgba\(59,\s*130,\s*246,\s*0\.05\)", "rgba(88, 166, 255, 0.05)"),
        # old green -> new green
        (r"rgba\(16,\s*185,\s*129,\s*0\.1\)", "rgba(63, 185, 80, 0.1)"),
        (r"rgba\(16,\s*185,\s*129,\s*0\.15\)", "rgba(63, 185, 80, 0.15)"),
        (r"rgba\(16,\s*185,\s*129,\s*0\.3\)", "rgba(63, 185, 80, 0.3)"),
        # old red -> new red
        (r"rgba\(244,\s*63,\s*94,\s*0\.1\)", "rgba(248, 81, 73, 0.1)"),
        (r"rgba\(244,\s*63,\s*94,\s*0\.15\)", "rgba(248, 81, 73, 0.15)"),
        # old yellow -> new yellow
        (r"rgba\(245,\s*158,\s*11,\s*0\.15\)", "rgba(210, 153, 34, 0.15)"),
        (r"rgba\(245,\s*158,\s*11,\s*0\.1\)", "rgba(210, 153, 34, 0.1)")
    ]

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".vue"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                new_content = content
                for old, new in replacements:
                    new_content = re.sub(old, new, new_content)

                if new_content != content:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Updated {filepath}")

fix_vue_colors(r"D:\vast-2020-mc2-platform\frontend_client\src")

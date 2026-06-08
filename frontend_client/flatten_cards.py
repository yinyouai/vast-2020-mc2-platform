import os
import re

def flatten_cards(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.vue'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace border: 1px solid var(--border); with border: none; or border: 1px solid rgba(255,255,255,0.05);
                new_content = re.sub(r"border:\s*1px\s+solid\s+var\(--border\);", "border: 1px solid rgba(255, 255, 255, 0.03);", content)
                new_content = re.sub(r"border:\s*1px\s+solid\s+rgba\([^)]+\);", "border: 1px solid rgba(255, 255, 255, 0.03);", new_content)
                new_content = re.sub(r"box-shadow:\s*var\(--shadow[^)]*\);", "box-shadow: none;", new_content)
                
                # Specifically replace component borders that look too card-like
                new_content = re.sub(r"border-radius:\s*[0-9]+px;", "border-radius: 12px;", new_content)
                
                # Some specific card classes to remove borders entirely
                new_content = re.sub(r"\.metric-card\s*\{[^}]*\}", "", new_content)
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Flattened cards in {file}")

flatten_cards(r"D:\vast-2020-mc2-platform\frontend_client\src")

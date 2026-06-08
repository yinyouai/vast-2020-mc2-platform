import os
import re

def fix_task2_colors(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content
    # Common light badge backgrounds
    new_content = re.sub(r"#fff6e5", "rgba(245, 158, 11, 0.15)", new_content, flags=re.IGNORECASE)
    new_content = re.sub(r"#ecf8f3", "rgba(16, 185, 129, 0.15)", new_content, flags=re.IGNORECASE)
    new_content = re.sub(r"#edf5ff", "rgba(59, 130, 246, 0.15)", new_content, flags=re.IGNORECASE)
    new_content = re.sub(r"#e0f2fe", "rgba(6, 182, 212, 0.15)", new_content, flags=re.IGNORECASE)
    new_content = re.sub(r"#0284c7", "var(--cyan)", new_content, flags=re.IGNORECASE)
    
    # Text colors
    new_content = re.sub(r"#d18a22", "var(--warning)", new_content, flags=re.IGNORECASE)
    new_content = re.sub(r"#24956f", "var(--success)", new_content, flags=re.IGNORECASE)
    new_content = re.sub(r"#2f7df6", "var(--accent)", new_content, flags=re.IGNORECASE)
    new_content = re.sub(r"#cf5656", "var(--danger)", new_content, flags=re.IGNORECASE)
    new_content = re.sub(r"#a94141", "var(--danger)", new_content, flags=re.IGNORECASE)
    new_content = re.sub(r"#1d65c1", "var(--accent)", new_content, flags=re.IGNORECASE)
    
    # Box shadows that create "cards"
    new_content = re.sub(r"box-shadow:[^;]+;", "box-shadow: none;", new_content)
    new_content = re.sub(r"border-color:\s*var\(--risk-color\);", "border-color: rgba(255,255,255,0.05);", new_content)
    
    # Any stray whites
    new_content = re.sub(r"#fff\b", "var(--text)", new_content, flags=re.IGNORECASE)
    new_content = re.sub(r"#ffffff\b", "var(--text)", new_content, flags=re.IGNORECASE)
    
    # Remove remaining borders
    new_content = re.sub(r"border:\s*1px\s+solid\s+[^;]+;", "border: none;", new_content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed colors in {filepath}")

directory = r"D:\vast-2020-mc2-platform\frontend_client\src"
for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith('.vue'):
            fix_task2_colors(os.path.join(root, file))

import os
import re

def process_vue_files(directory):
    replacements = [
        # Backgrounds
        (r"background:\s*#fff(?:fff)?;", "background: var(--surface);"),
        (r"background:\s*rgba\(255,\s*255,\s*255,\s*[\d.]+\);", "background: var(--surface-2);"),
        (r"background:\s*#f[a-f0-9]{5};", "background: var(--surface-3);"),
        (r"background:\s*linear-gradient\([^)]+255,255,255[^)]+\);", "background: var(--surface);"),
        
        # Colors
        (r"color:\s*#333;", "color: var(--text);"),
        (r"color:\s*#666;", "color: var(--muted);"),
        (r"color:\s*#999;", "color: var(--subtle);"),
        (r"color:\s*#000;", "color: var(--text);"),
        
        # Box Shadows
        (r"box-shadow:\s*0\s+[^;]+rgba\(0,0,0,0.1\);", "box-shadow: var(--shadow-soft);"),
        (r"border:\s*1px\s+solid\s+#e[a-f0-9]{5};", "border: 1px solid var(--border);"),
    ]
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.vue'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                for old, new in replacements:
                    new_content = re.sub(old, new, new_content, flags=re.IGNORECASE)
                
                # specific patches
                new_content = re.sub(r"background:\s*rgba\(255,255,255,\.82\)", "background: var(--surface-2)", new_content)
                new_content = re.sub(r"background:\s*#f8fbff", "background: var(--surface-3)", new_content)
                new_content = re.sub(r"background:\s*#eef3f8", "background: var(--surface)", new_content)
                new_content = re.sub(r"background:\s*#f1f6ff", "background: var(--surface-glow)", new_content)
                new_content = re.sub(r"background:\s*#effaf5", "background: rgba(16, 185, 129, 0.1)", new_content)
                new_content = re.sub(r"color:\s*#187553", "color: var(--success)", new_content)
                new_content = re.sub(r"border:\s*1px\s+solid\s*#bfe2d4", "border: 1px solid var(--success)", new_content)
                new_content = re.sub(r"background:\s*#f7f9fc", "background: var(--surface)", new_content)
                new_content = re.sub(r"background:\s*#fafcff", "background: var(--surface-2)", new_content)
                new_content = re.sub(r"background:\s*#eef2f6", "background: var(--surface-3)", new_content)
                new_content = re.sub(r"background:\s*#fff4d9", "background: rgba(245, 158, 11, 0.15)", new_content)
                new_content = re.sub(r"color:\s*#8a5a0a", "color: var(--warning)", new_content)
                new_content = re.sub(r"background:\s*#e5ebf1", "background: var(--surface-3)", new_content)
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated {file}")

process_vue_files(r"D:\vast-2020-mc2-platform\frontend_client\src")

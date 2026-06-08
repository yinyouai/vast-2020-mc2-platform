import os
import re

def aggressive_dark_mode(directory):
    replacements = [
        # Whites and Light Grays
        (r"background:\s*#fff(?:fff)?\b", "background: var(--surface)"),
        (r"background-color:\s*#fff(?:fff)?\b", "background-color: var(--surface)"),
        (r"fill:\s*#fff(?:fff)?\b", "fill: var(--surface-2)"),
        (r"stroke:\s*#fff(?:fff)?\b", "stroke: var(--surface-3)"),
        (r"borderColor:\s*['\"]#fff(?:fff)?['\"]", "borderColor: 'var(--border)'"),
        (r"color:\s*#fff(?:fff)?\b", "color: var(--text)"),
        
        # Specific light backgrounds used in the UI
        (r"background:\s*#f9fbfd\b", "background: var(--surface)"),
        (r"background:\s*#edf1f5\b", "background: var(--surface-2)"),
        (r"background:\s*#edf5ff\b", "background: var(--surface-glow)"),
        (r"background:\s*#e7f0ff\b", "background: var(--surface-glow)"),
        (r"background:\s*#f2f7ff\b", "background: var(--surface-glow)"),
        (r"background:\s*#fff9e9\b", "background: rgba(245, 158, 11, 0.1)"),
        (r"background:\s*#eef1f4\b", "background: var(--surface-3)"),
        (r"background:\s*#eef8f5\b", "background: rgba(16, 185, 129, 0.1)"),
        (r"background:\s*#fffdf7\b", "background: var(--surface)"),
        (r"background:\s*#fcecec\b", "background: rgba(244, 63, 94, 0.1)"),
        (r"background:\s*#e9eef4\b", "background: var(--surface-3)"),
        (r"background:\s*#f5f8fc\b", "background: var(--surface)"),
        (r"background:\s*#ecf8f3\b", "background: rgba(16, 185, 129, 0.1)"),
        (r"background:\s*#fff6e5\b", "background: rgba(245, 158, 11, 0.1)"),
        (r"background:\s*#fdf0f0\b", "background: rgba(244, 63, 94, 0.1)"),
        (r"background:\s*#eaf7f1\b", "background: rgba(16, 185, 129, 0.1)"),
        
        (r"background:linear-gradient\(120deg,#fffdf7,#f5f9ff 56%,#eef8f5\)", "background: var(--surface-2)"),
        
        # Text and border colors from old theme
        (r"color:\s*#17324d\b", "color: var(--text)"),
        (r"color:\s*#7890ab\b", "color: var(--subtle)"),
        (r"color:\s*#56708f\b", "color: var(--muted)"),
        (r"fill:\s*#17324d\b", "fill: var(--text)"),
        (r"fill:\s*#7890ab\b", "fill: var(--subtle)"),
        (r"fill:\s*#56708f\b", "fill: var(--muted)"),
        
        (r"border-color:\s*#efc6c6\b", "border-color: rgba(244, 63, 94, 0.3)"),
        (r"border-color:\s*#cbe8dc\b", "border-color: rgba(16, 185, 129, 0.3)"),
        
        # Explicit rgba whites
        (r"rgba\(255,\s*255,\s*255,\s*0?\.[89]\d*\)", "rgba(255, 255, 255, 0.1)"),
        
        # Box shadow removals to flatten cards
        (r"box-shadow:var\(--shadow[^)]*\)", "box-shadow: none"),
        (r"box-shadow:[^;]+;", "box-shadow: none;"),
    ]
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.vue') or file.endswith('.css'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                for old, new in replacements:
                    new_content = re.sub(old, new, new_content, flags=re.IGNORECASE)
                
                # In task 2 components, completely remove borders for list items and grids
                if "ConflictPriorityQueue.vue" in file or "PersonReviewRadar.vue" in file or "CorrectionCanvas.vue" in file or "DataExplorationView.vue" in file:
                    new_content = re.sub(r"border:\s*1px\s+solid\s+[^;]+;", "border: none;", new_content)
                    # Use subtle backgrounds instead of borders
                    new_content = re.sub(r"background:\s*transparent;", "background: var(--surface);", new_content)

                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Deep darkified {file}")

aggressive_dark_mode(r"D:\vast-2020-mc2-platform\frontend_client\src")

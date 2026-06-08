import re

filepath = r"D:\vast-2020-mc2-platform\frontend_client\src\assets\global.css"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    # Remove explicit borders on panels and cards
    (r"border: 1px solid var\(--border\);\n\s*border-radius: var\(--radius\);", 
     "border: 1px solid rgba(255, 255, 255, 0.05);\n  border-radius: var(--radius);\n  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.05), var(--shadow);"),
     
    # Remove border on metric cards specifically if any
    (r"\.metric-card \{[^}]+\}", 
     ".metric-card {\n  background: linear-gradient(180deg, rgba(59, 130, 246, 0.05), transparent);\n  border: 1px solid rgba(255, 255, 255, 0.03);\n  border-radius: var(--radius);\n}"),
     
    # Make the topbar and sidebar completely blend in with glassmorphism
    (r"border-bottom: 1px solid var\(--border\);", "border-bottom: 1px solid rgba(255, 255, 255, 0.05);"),
    (r"border-right: 1px solid rgba\(53, 89, 138, 0.1\);", "border-right: 1px solid rgba(255, 255, 255, 0.05);"),
    
    # Improve nav item background
    (r"background: rgba\(255, 255, 255, 0.72\);", "background: rgba(255, 255, 255, 0.03);"),
    
    # Fix the brand-mark color
    (r"background: rgba\(47, 125, 246, 0.08\);", "background: rgba(59, 130, 246, 0.15);"),
    (r"border: 1px solid rgba\(47, 125, 246, 0.18\);", "border: 1px solid rgba(59, 130, 246, 0.3);"),
    (r"box-shadow: inset 0 1px 0 rgba\(255, 255, 255, 0.95\);", "box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.1);"),
    
    # Nav items active state
    (r"background: linear-gradient\(135deg, var\(--surface-glow\), var\(--surface-3\)\);", 
     "background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(59, 130, 246, 0.05));"),
]

for old, new in replacements:
    content = re.sub(old, new, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("global.css refined for glassmorphism!")

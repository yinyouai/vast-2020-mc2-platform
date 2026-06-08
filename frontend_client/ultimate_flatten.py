import re

def flatten_component(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for old, new in replacements:
        new_content = re.sub(old, new, new_content, flags=re.IGNORECASE)
        
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Flattened {filepath}")

# 1. DataExplorationView.vue
flatten_component(r"D:\vast-2020-mc2-platform\frontend_client\src\views\DataExplorationView.vue", [
    (r'class="review-scope panel"', 'class="review-scope"'),
    (r'class="review-policy panel"', 'class="review-policy"'),
    (r'background:\s*var\(--surface\)', 'background: transparent'),
    (r'background:\s*var\(--surface-3\)', 'background: rgba(255, 255, 255, 0.02)'),
])

# 2. ConflictPriorityQueue.vue
flatten_component(r"D:\vast-2020-mc2-platform\frontend_client\src\components\interaction\ConflictPriorityQueue.vue", [
    (r'background:\s*var\(--surface\)', 'background: transparent'),
    (r'background:\s*var\(--surface-3\)', 'background: transparent'),
    (r'\.review-lane\s*\{[^}]*\}', '.review-lane { min-width:0; padding:0 14px; border: none; }'),
    (r'\.review-card\s*\{[^}]*\}', '.review-card { border-bottom: 1px solid rgba(255, 255, 255, 0.05); padding: 8px 0; transition: 150ms ease; }'),
    (r'\.card-main\s*\{[^}]*\}', '.card-main { display:grid; grid-template-columns:36px minmax(0,1fr) auto; align-items:center; gap:9px; width:100%; min-height:60px; padding:0 9px; color:inherit; text-align:left; background: transparent; border: none; outline: none; cursor: pointer; }'),
])

# 3. PersonReviewRadar.vue
flatten_component(r"D:\vast-2020-mc2-platform\frontend_client\src\components\interaction\PersonReviewRadar.vue", [
    (r'background:\s*var\(--surface\)', 'background: transparent'),
    (r'\.priority-row\s*\{[^}]*\}', '.priority-row { display:grid; grid-template-columns:38px minmax(0,1fr) auto 68px; align-items:center; gap:12px; width:100%; min-height:64px; padding:10px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.05); color:var(--text); text-align:left; background: transparent; cursor:pointer; }'),
    (r'\.radar-summary\s*div\s*\{[^}]*\}', '.radar-summary div { display:flex; align-items:baseline; gap:8px; padding:10px 0; border:none; background: transparent; }'),
    (r'border-left:4px solid var\(--risk-color\);', ''),
])

# 4. CorrectionCanvas.vue
flatten_component(r"D:\vast-2020-mc2-platform\frontend_client\src\components\interaction\CorrectionCanvas.vue", [
    (r'background:\s*var\(--surface\)', 'background: transparent'),
    (r'background:\s*var\(--surface-3\)', 'background: transparent'),
    (r'background:\s*#ebf3ff', 'background: rgba(59, 130, 246, 0.15)'),
    (r'background:\s*rgba\(244,248,255,\.94\)', 'background: rgba(59, 130, 246, 0.15)'),
    (r'\.image-stage\s*\{[^}]*\}', '.image-stage { position:relative; display:grid; place-items:center; overflow:hidden; height:520px; border: none; border-radius: 12px; background: rgba(0, 0, 0, 0.2); }'),
    (r'\.review-layer,\.review-context\s*\{[^}]*\}', '.review-layer, .review-context { padding:13px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.05); }'),
    (r'background:#b94646', 'background: var(--danger)'),
])

# 5. ManualReviewComparison.vue (just in case)
flatten_component(r"D:\vast-2020-mc2-platform\frontend_client\src\components\process\ManualReviewComparison.vue", [
    (r'background:\s*var\(--surface\)', 'background: transparent'),
    (r'background:\s*var\(--surface-3\)', 'background: transparent'),
    (r'\.audit-trace\s*\{[^}]*\}', '.audit-trace { display:grid; grid-template-columns:1fr 40px 1fr 40px 1fr; align-items:center; gap:8px; padding:14px 0; border-top: 1px solid rgba(255, 255, 255, 0.05); background: transparent; }'),
])

print("Flattening pass complete.")

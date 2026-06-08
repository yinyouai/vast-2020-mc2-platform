import re

filepath = r"D:\vast-2020-mc2-platform\frontend_client\src\App.vue"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Use regex to remove the entire case-card block
# The block starts at <div class="case-card"> and ends at the closing </div> right before </aside>
pattern = re.compile(r'\s*<div class="case-card">.*?</aside>', re.DOTALL)
new_content = pattern.sub('\n    </aside>', content)

if new_content != content:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Removed case-card successfully")
else:
    print("case-card not found or regex failed")

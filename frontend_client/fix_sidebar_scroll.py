import re

filepath = r"D:\vast-2020-mc2-platform\frontend_client\src\assets\global.css"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Make sidebar scrollable
old_sidebar = r"\.sidebar \{\n  display: flex;\n  flex-direction: column;\n  gap: 24px;\n  min-width: 0;\n  padding: 28px 22px 24px;"
new_sidebar = """.sidebar {
  display: flex;
  flex-direction: column;
  gap: 24px;
  min-width: 0;
  padding: 28px 22px 24px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.1) transparent;"""

content = re.sub(old_sidebar, new_sidebar, content)

# Also add standard webkit scrollbar for sidebar
scrollbar_css = """
.sidebar::-webkit-scrollbar {
  width: 6px;
}
.sidebar::-webkit-scrollbar-track {
  background: transparent;
}
.sidebar::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
}
.sidebar::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 255, 255, 0.2);
}
"""

if "sidebar::-webkit-scrollbar" not in content:
    content += scrollbar_css

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Sidebar scrolling added")

import os
import re

def replace_in_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements:
        content = content.replace(old, new)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# 1. Update chartTheme.js
chartTheme = r"D:\vast-2020-mc2-platform\frontend_client\src\utils\chartTheme.js"
replace_in_file(chartTheme, [
    (
        "export const chartPalette = {\n  text: '#17324d',\n  muted: '#56708f',\n  subtle: '#7890ab',\n  line: 'rgba(53, 89, 138, 0.1)',\n  lineStrong: 'rgba(53, 89, 138, 0.2)',\n  accent: '#2f7df6',\n  accentSoft: 'rgba(47, 125, 246, 0.14)',\n  cyan: '#35a8c8',\n  gold: '#d99522',\n  red: '#cf5656',\n  green: '#24956f',\n  panel: 'rgba(255, 255, 255, 0.98)',\n  panelEdge: 'rgba(53, 89, 138, 0.14)'\n}",
        "export const chartPalette = {\n  text: '#e0e6ed',\n  muted: '#94a3b8',\n  subtle: '#64748b',\n  line: 'rgba(100, 149, 237, 0.15)',\n  lineStrong: 'rgba(100, 149, 237, 0.3)',\n  accent: '#3b82f6',\n  accentSoft: 'rgba(59, 130, 246, 0.15)',\n  cyan: '#06b6d4',\n  gold: '#f59e0b',\n  red: '#f43f5e',\n  green: '#10b981',\n  panel: 'rgba(13, 22, 43, 0.85)',\n  panelEdge: 'rgba(100, 149, 237, 0.2)'\n}"
    )
])

# 2. Update global.css root variables and body
global_css = r"D:\vast-2020-mc2-platform\frontend_client\src\assets\global.css"
replace_in_file(global_css, [
    (
        """:root {
  color-scheme: light;
  --bg: #f4f7fb;
  --bg-deep: #eaf0f7;
  --bg-soft: #ffffff;
  --surface: rgba(255, 255, 255, 0.92);
  --surface-2: rgba(248, 251, 255, 0.96);
  --surface-3: rgba(240, 246, 255, 0.98);
  --surface-glow: rgba(58, 120, 255, 0.08);
  --border: rgba(53, 89, 138, 0.12);
  --border-strong: rgba(53, 89, 138, 0.24);
  --text: #17324d;
  --muted: #56708f;
  --subtle: #7890ab;
  --accent: #2f7df6;
  --accent-2: #35b5a6;
  --accent-3: #f0b44c;
  --warning: #f0b44c;
  --danger: #df6a6a;
  --success: #39a97d;
  --shadow: 0 20px 48px rgba(48, 78, 114, 0.1);
  --shadow-soft: 0 12px 28px rgba(48, 78, 114, 0.08);
  --shadow-stage: 0 34px 86px rgba(34, 68, 108, 0.15);
  --radius: 8px;
  --radius-sm: 6px;
  --radius-xl: 12px;
  --panel-padding: 22px;
  --content-max: 1480px;
  --stage-gap: clamp(28px, 4.2vw, 58px);
  --ease-out-quint: cubic-bezier(0.22, 1, 0.36, 1);
  --ease-spring: cubic-bezier(0.16, 1, 0.3, 1);
  --motion-fast: 220ms;
  --motion-medium: 420ms;
  --motion-slow: 760ms;
  font-family: "Microsoft YaHei UI", "PingFang SC", "Noto Sans SC", "Segoe UI", sans-serif;
  font-size: 16px;
}""",
        """:root {
  color-scheme: dark;
  --bg: #050b14;
  --bg-deep: #03070d;
  --bg-soft: #0a1121;
  --surface: rgba(13, 22, 43, 0.4);
  --surface-2: rgba(16, 28, 56, 0.5);
  --surface-3: rgba(22, 38, 72, 0.6);
  --surface-glow: rgba(59, 130, 246, 0.15);
  --border: rgba(100, 149, 237, 0.15);
  --border-strong: rgba(100, 149, 237, 0.3);
  --text: #e0e6ed;
  --muted: #94a3b8;
  --subtle: #64748b;
  --accent: #3b82f6;
  --accent-2: #10b981;
  --accent-3: #8b5cf6;
  --warning: #f59e0b;
  --danger: #f43f5e;
  --success: #10b981;
  --shadow: 0 20px 48px rgba(0, 0, 0, 0.5);
  --shadow-soft: 0 12px 28px rgba(0, 0, 0, 0.3);
  --shadow-stage: 0 34px 86px rgba(0, 0, 0, 0.6);
  --radius: 12px;
  --radius-sm: 8px;
  --radius-xl: 16px;
  --panel-padding: 24px;
  --content-max: 1480px;
  --stage-gap: clamp(28px, 4.2vw, 58px);
  --ease-out-quint: cubic-bezier(0.22, 1, 0.36, 1);
  --ease-spring: cubic-bezier(0.16, 1, 0.3, 1);
  --motion-fast: 220ms;
  --motion-medium: 420ms;
  --motion-slow: 760ms;
  font-family: "Inter", "Outfit", "Microsoft YaHei UI", sans-serif;
  font-size: 16px;
}"""
    ),
    (
        "background: linear-gradient(180deg, #f9fbfe 0%, #eef3f9 100%);",
        "background: linear-gradient(180deg, var(--bg-deep) 0%, var(--bg) 100%);"
    ),
    (
        "background-image:\n    linear-gradient(rgba(71, 111, 157, 0.05) 1px, transparent 1px),\n    linear-gradient(90deg, rgba(71, 111, 157, 0.05) 1px, transparent 1px);",
        "background-image:\n    linear-gradient(var(--border) 1px, transparent 1px),\n    linear-gradient(90deg, var(--border) 1px, transparent 1px);"
    ),
    (
        "mask-image: linear-gradient(180deg, rgba(255, 255, 255, 0.8), transparent 86%);",
        "mask-image: linear-gradient(180deg, rgba(0, 0, 0, 0.8), transparent 86%);"
    ),
    (
        "background: rgba(250, 252, 255, 0.84);",
        "background: var(--surface);"
    ),
    (
        "background: rgba(255, 255, 255, 0.72);",
        "background: var(--surface-2);"
    ),
    (
        "background: linear-gradient(135deg, rgba(47, 125, 246, 0.1), rgba(255, 255, 255, 0.85));",
        "background: linear-gradient(135deg, var(--surface-glow), var(--surface-3));"
    ),
    (
        "background: rgba(255, 255, 255, 0.82);",
        "background: var(--surface-2);"
    ),
    (
        "background: linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(248, 251, 255, 0.92)),\n    var(--surface);",
        "background: var(--surface);"
    ),
    (
        "background:\n    radial-gradient(circle at top right, rgba(240, 180, 76, 0.14), transparent 28%),\n    linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(247, 251, 255, 0.94));",
        "background:\n    radial-gradient(circle at top right, rgba(245, 158, 11, 0.1), transparent 28%),\n    var(--surface);"
    ),
    (
        "background:\n    linear-gradient(180deg, rgba(249, 252, 255, 0.9), rgba(249, 252, 255, 0.66)),\n    rgba(249, 252, 255, 0.72);",
        "background: var(--surface); border-bottom: 1px solid var(--border);"
    ),
    (
        "background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(246, 250, 255, 0.98));",
        "background: linear-gradient(135deg, var(--surface-2), var(--surface));"
    ),
    (
        "background: rgba(255, 255, 255, 0.78);",
        "background: var(--surface-3);"
    ),
    (
        "background:\n    linear-gradient(180deg, rgba(47, 125, 246, 0.05), rgba(255, 255, 255, 0.96)),\n    var(--surface);",
        "background: linear-gradient(180deg, var(--surface-glow), var(--surface));"
    ),
    (
        "background:\n    linear-gradient(180deg, rgba(255, 255, 255, 0.94), rgba(247, 251, 255, 0.84)),\n    rgba(255, 255, 255, 0.86);",
        "background: var(--surface);"
    )
])

print("global.css and chartTheme.js updated!")

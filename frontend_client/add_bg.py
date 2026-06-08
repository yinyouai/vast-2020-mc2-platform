import re

filepath = r"D:\vast-2020-mc2-platform\frontend_client\src\assets\global.css"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add dynamic animated background and modern micro-interactions
app_shell_backdrop_old = r"\.app-shell__backdrop \{\n  display: none;\n\}"
app_shell_backdrop_new = """.app-shell__backdrop {
  display: block;
  position: absolute;
  inset: 0;
  overflow: hidden;
  z-index: 0;
  pointer-events: none;
}
.app-shell__backdrop::before, .app-shell__backdrop::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.4;
  animation: float 20s infinite ease-in-out alternate;
}
.app-shell__backdrop::before {
  width: 60vw;
  height: 60vw;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.15), transparent 70%);
  top: -20vw;
  left: -10vw;
}
.app-shell__backdrop::after {
  width: 50vw;
  height: 50vw;
  background: radial-gradient(circle, rgba(16, 185, 129, 0.1), transparent 70%);
  bottom: -10vw;
  right: -10vw;
  animation-delay: -10s;
}
@keyframes float {
  0% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(5%, 5%) scale(1.1); }
  100% { transform: translate(-5%, -5%) scale(0.95); }
}"""

content = re.sub(app_shell_backdrop_old, app_shell_backdrop_new, content)

# Make panels feel more premium with a subtle top highlight
panel_border_old = r"\.panel,[^{]*\n\.apple-glass-card,[^{]*\n\.dashboard-cell-card \{[^{]*\n\s*min-width: 0;\n\}"
panel_border_new = """.panel,
.apple-glass-card,
.dashboard-cell-card {
  min-width: 0;
  background: rgba(13, 22, 43, 0.45);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 24px -4px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
}
.panel:hover {
  background: rgba(16, 28, 56, 0.55);
  border-top: 1px solid rgba(255, 255, 255, 0.15);
}"""
content = re.sub(panel_border_old, panel_border_new, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Added premium glassmorphism background and animations!")

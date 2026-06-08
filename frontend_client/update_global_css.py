css_content = """
:root {
  color-scheme: dark;
  --bg: #0d1117;
  --bg-deep: #010409;
  --bg-soft: #161b22;
  --surface: #161b22;
  --surface-2: #21262d;
  --surface-3: #30363d;
  --surface-glow: rgba(88, 166, 255, 0.1);
  --border: #30363d;
  --border-strong: #8b949e;
  --text: #c9d1d9;
  --muted: #8b949e;
  --subtle: #6e7681;
  --accent: #58a6ff;
  --accent-2: #3fb950;
  --accent-3: #bc8cff;
  --warning: #d29922;
  --danger: #f85149;
  --success: #238636;
  --shadow: 0 8px 24px rgba(1, 4, 9, 1);
  --shadow-soft: 0 4px 12px rgba(1, 4, 9, 0.5);
  --shadow-stage: 0 16px 32px rgba(1, 4, 9, 0.8);
  --radius: 6px;
  --radius-sm: 4px;
  --radius-xl: 12px;
  --panel-padding: 20px;
  --content-max: 1480px;
  --stage-gap: 24px;
  --ease-out-quint: cubic-bezier(0.22, 1, 0.36, 1);
  --ease-spring: cubic-bezier(0.16, 1, 0.3, 1);
  --motion-fast: 150ms;
  --motion-medium: 250ms;
  --motion-slow: 400ms;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
  font-size: 14px;
}

* {
  box-sizing: border-box;
}

html,
body,
#app {
  width: 100%;
  min-width: 0;
  min-height: 100%;
  margin: 0;
}

body {
  background: var(--bg);
  color: var(--text);
  line-height: 1.5;
}

html {
  scroll-behavior: smooth;
}

button,
input {
  font: inherit;
}

button {
  min-height: 32px;
  border: 0;
  cursor: pointer;
}

button:focus-visible,
a:focus-visible,
input:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

a {
  color: inherit;
}

h1,
h2,
h3,
h4,
h5,
p {
  margin-top: 0;
}

.app-shell {
  position: relative;
  display: grid;
  grid-template-columns: 280px minmax(0, 1fr);
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

.app-shell__backdrop {
  display: none; /* Removed AI orbs and grid */
}

.sidebar,
.workspace-shell {
  position: relative;
  z-index: 1;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
  min-width: 0;
  padding: 24px 16px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--border) transparent;
  background: var(--bg-soft);
  border-right: 1px solid var(--border);
}

.sidebar-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.brand-block {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
}

.brand-mark {
  display: grid;
  place-items: center;
  width: 40px;
  height: 40px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface-2);
}

.brand-mark span {
  color: var(--text);
  font-size: 0.9rem;
  font-weight: 600;
}

.brand-copy h1 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.brand-description {
  display: none; /* Too wordy for a clean UI */
}

.eyebrow {
  margin: 0 0 4px;
  color: var(--muted);
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.task-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  border: 1px solid transparent;
  border-radius: var(--radius);
  color: var(--text);
  text-decoration: none;
  background: transparent;
  transition: background var(--motion-fast) ease;
}

.nav-item:hover {
  background: var(--surface-2);
}

.nav-item.router-link-active {
  background: var(--surface-3);
  border-color: var(--border);
}

.nav-index {
  color: var(--muted);
  font-size: 0.8rem;
  font-weight: 500;
  font-variant-numeric: tabular-nums;
}

.nav-item.router-link-active .nav-index {
  color: var(--text);
}

.nav-copy {
  min-width: 0;
  flex: 1;
}

.nav-item strong {
  display: block;
  font-size: 0.9rem;
  font-weight: 500;
}

.nav-item small {
  display: none; /* Keep sidebar clean */
}

.nav-state {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--border);
}

.nav-state.is-active {
  background: var(--accent);
}

.story-card,
.case-card,
.panel,
.apple-glass-card,
.dashboard-cell-card,
.metric-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
}

.story-card,
.case-card,
.metric-card,
.panel {
  padding: var(--panel-padding);
}

.story-card h3 {
  margin: 0 0 8px;
  font-size: 1rem;
  font-weight: 600;
  line-height: 1.4;
}

.story-card p:last-child {
  margin: 0;
  color: var(--muted);
  line-height: 1.5;
  font-size: 0.85rem;
}

.case-card {
  margin-top: auto;
  background: var(--surface);
}

.case-card__header {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.case-card strong {
  display: block;
  font-size: 1.2rem;
  font-weight: 600;
}

.case-card__grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-top: 16px;
}

.case-card__grid span,
.metric-card span {
  display: block;
  color: var(--muted);
  font-size: 0.75rem;
}

.case-card__grid b {
  display: block;
  margin-top: 4px;
  font-size: 0.9rem;
  font-weight: 500;
}

.risk-pill,
.sync-state,
.threshold-chip,
.data-chip {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 24px;
  padding: 0 10px;
  border-radius: 12px;
  border: 1px solid var(--border);
  font-size: 0.75rem;
  font-weight: 500;
  background: var(--surface-2);
}

.risk-high,
.is-busy {
  color: var(--danger);
  border-color: rgba(248, 81, 73, 0.4);
  background: rgba(248, 81, 73, 0.1);
}

.risk-low,
.is-ready {
  color: var(--success);
  border-color: rgba(35, 134, 54, 0.4);
  background: rgba(35, 134, 54, 0.1);
}

.workspace-shell {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  min-width: 0;
  height: 100vh;
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 16px 24px;
  border-bottom: 1px solid var(--border);
  background: var(--bg);
}

.topbar-copy {
  min-width: 0;
}

.topbar h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.topbar-summary {
  display: none;
}

.topbar-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  flex-wrap: wrap;
}

.stage-progress {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 28px;
  padding: 0 10px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
}

.stage-progress__dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--surface-3);
}

.stage-progress__dot.is-past {
  background: var(--accent);
}

.stage-progress__dot.is-current {
  width: 6px;
  background: var(--text);
}

.threshold-chip,
.data-chip {
  color: var(--text);
  background: var(--surface-2);
  border-color: var(--border);
}

.mobile-nav {
  display: none;
  gap: 8px;
  padding: 12px 16px;
  overflow: auto hidden;
  border-bottom: 1px solid var(--border);
  background: var(--bg-soft);
}

.mobile-nav__item {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  text-decoration: none;
  white-space: nowrap;
}

.mobile-nav__item span {
  color: var(--muted);
  font-size: 0.75rem;
}

.mobile-nav__item strong {
  color: var(--text);
  font-size: 0.85rem;
  font-weight: 500;
}

.mobile-nav__item.router-link-active {
  border-color: var(--border-strong);
  background: var(--surface-2);
}

.viewport-container {
  min-width: 0;
  min-height: 0;
  overflow: auto;
  scroll-behavior: smooth;
  scroll-padding: 24px;
}

.page-layer {
  display: block;
  min-height: 100%;
}

.view-grid-layout {
  display: flex;
  flex-direction: column;
  gap: var(--stage-gap);
  min-height: 100%;
  max-width: var(--content-max);
  margin: 0 auto;
  padding: 24px 32px 48px;
}

.page-intro {
  display: none; /* Too much screen space wasted */
}

.intro-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.intro-pills .data-chip {
  color: var(--text);
  background: var(--surface-2);
  border-color: var(--border);
}

.panel,
.apple-glass-card,
.dashboard-cell-card {
  min-width: 0;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
}

.panel:hover {
  border-color: var(--border-strong);
}

.metric-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
}

.panel:hover,
.metric-card:hover {
  border-color: var(--border-strong);
}

.panel-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
}

.panel-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text);
}

.panel-subtitle {
  display: block;
  margin: 4px 0 0;
  color: var(--muted);
  font-size: 0.85rem;
}

.chart-frame {
  width: 100%;
  min-height: 320px;
}

.primary-btn,
.ghost-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-width: auto;
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  font-weight: 500;
  font-size: 0.85rem;
  border: 1px solid transparent;
  transition: background var(--motion-fast) ease, border-color var(--motion-fast) ease;
}

.primary-btn {
  color: #ffffff;
  background: var(--success);
  border-color: rgba(240, 246, 252, 0.1);
}

.primary-btn:hover {
  background: #2ea043;
}

.ghost-btn {
  color: var(--text);
  border-color: var(--border);
  background: var(--surface-2);
}

.ghost-btn:hover {
  background: var(--surface-3);
  border-color: var(--border-strong);
}

.apple-slider,
input[type="range"] {
  width: 100%;
  accent-color: var(--accent);
}

.metric-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.metric-card strong {
  display: block;
  margin-top: 8px;
  font-size: 1.5rem;
  font-weight: 600;
}

.split-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px;
  align-items: stretch;
}

.three-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 24px;
}

.analysis-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.analysis-card {
  position: relative;
  padding: 16px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  transition: border-color var(--motion-fast) ease;
}

.analysis-card:hover {
  border-color: var(--border-strong);
}

.analysis-card span {
  display: block;
  margin-bottom: 8px;
  color: var(--muted);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.analysis-card strong {
  display: block;
  margin-bottom: 6px;
  font-size: 1rem;
  font-weight: 500;
}

.analysis-card p {
  display: block;
  margin: 0;
  color: var(--muted);
  font-size: 0.85rem;
}

.case-card__text p,
.case-log,
.curve-card p,
.compare-note,
.insight-card p,
.verdict-item p,
.verdict-radar-head p,
.evidence-insight-grid p,
.network-detail-card p,
.evidence-block p,
.evidence-block blockquote,
.modal-grid p {
  display: none !important;
}

/* Remove reveal animations */
.reveal,
.sample-dot.reveal {
  opacity: 1 !important;
  filter: none !important;
  transform: none !important;
  transition: none !important;
}

@media (max-width: 1240px) {
  .metric-grid,
  .analysis-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 1040px) {
  .app-shell {
    grid-template-columns: 1fr;
  }

  .sidebar {
    display: none;
  }

  .workspace-shell {
    grid-template-rows: auto auto minmax(0, 1fr);
  }

  .topbar {
    align-items: flex-start;
    flex-direction: column;
    padding: 16px;
  }

  .mobile-nav {
    display: flex;
  }

  .view-grid-layout {
    padding: 16px;
  }

  .split-grid,
  .three-grid,
  .metric-grid,
  .analysis-grid {
    grid-template-columns: 1fr;
  }
}

.sidebar::-webkit-scrollbar {
  width: 6px;
}
.sidebar::-webkit-scrollbar-track {
  background: transparent;
}
.sidebar::-webkit-scrollbar-thumb {
  background-color: var(--border-strong);
  border-radius: 10px;
}
.sidebar::-webkit-scrollbar-thumb:hover {
  background-color: var(--subtle);
}
"""

with open(r"D:\vast-2020-mc2-platform\frontend_client\src\assets\global.css", "w", encoding="utf-8") as f:
    f.write(css_content)

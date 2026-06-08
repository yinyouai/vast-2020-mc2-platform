
export const chartPalette = {
  text: '#111827',
  muted: '#6b7280',
  subtle: '#9ca3af',
  line: '#e5e7eb',
  lineStrong: '#d1d5db',
  accent: '#2563eb',
  accentSoft: 'rgba(37, 99, 235, 0.15)',
  cyan: '#0891b2',
  gold: '#d97706',
  red: '#dc2626',
  green: '#059669',
  panel: '#ffffff',
  panelEdge: '#e5e7eb'
}

export const animationTiming = {
  duration: 800,
  delay: (index = 0) => Math.min(index * 30, 300),
  easing: 'cubicOut'
}

export const buildTooltip = (formatter) => ({
  trigger: 'item',
  backgroundColor: chartPalette.panel,
  borderColor: chartPalette.panelEdge,
  borderWidth: 1,
  padding: 12,
  textStyle: {
    color: chartPalette.text,
    fontSize: 12,
    lineHeight: 18
  },
  extraCssText: 'box-shadow: 0 4px 16px rgba(0,0,0,0.08); border-radius: 8px;',
  formatter
})

export const buildAxis = ({ rotate = 0, formatter, interval = 'auto', fontSize = 11 } = {}) => ({
  axisLabel: {
    color: chartPalette.muted,
    rotate,
    interval,
    fontSize,
    formatter
  },
  axisLine: {
    lineStyle: {
      color: chartPalette.lineStrong
    }
  },
  axisTick: {
    show: false
  }
})

export const splitLine = {
  lineStyle: {
    color: chartPalette.line,
    type: 'dashed'
  }
}

export const legendStyle = {
  textStyle: {
    color: chartPalette.muted
  }
}

export const titleBlock = (title, subtitle) => ({
  text: title,
  subtext: subtitle,
  left: 0,
  top: 0,
  textStyle: {
    color: chartPalette.text,
    fontSize: 14,
    fontWeight: 700
  },
  subtextStyle: {
    color: chartPalette.subtle,
    fontSize: 11,
    lineHeight: 17
  }
})

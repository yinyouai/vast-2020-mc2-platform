export const chartPalette = {
  text: '#e0e6ed',
  muted: '#94a3b8',
  subtle: '#64748b',
  line: 'rgba(100, 149, 237, 0.15)',
  lineStrong: 'rgba(100, 149, 237, 0.3)',
  accent: '#3b82f6',
  accentSoft: 'rgba(59, 130, 246, 0.15)',
  cyan: '#06b6d4',
  gold: '#f59e0b',
  red: '#f43f5e',
  green: '#10b981',
  panel: 'rgba(13, 22, 43, 0.85)',
  panelEdge: 'rgba(100, 149, 237, 0.2)'
}

export const animationTiming = {
  duration: 900,
  delay: (index = 0) => Math.min(index * 40, 320),
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
  extraCssText: 'box-shadow: 0 18px 42px rgba(48,78,114,0.18); border-radius: 8px;',
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

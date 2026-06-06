export const chartPalette = {
  text: '#17324d',
  muted: '#56708f',
  subtle: '#7890ab',
  line: 'rgba(53, 89, 138, 0.1)',
  lineStrong: 'rgba(53, 89, 138, 0.2)',
  accent: '#2f7df6',
  accentSoft: 'rgba(47, 125, 246, 0.14)',
  cyan: '#35a8c8',
  gold: '#d99522',
  red: '#cf5656',
  green: '#24956f',
  panel: 'rgba(255, 255, 255, 0.98)',
  panelEdge: 'rgba(53, 89, 138, 0.14)'
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

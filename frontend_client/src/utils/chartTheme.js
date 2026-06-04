export const chartPalette = {
  text: '#edf4fb',
  muted: '#a2b4c8',
  subtle: '#6f859d',
  line: 'rgba(162, 180, 200, 0.18)',
  lineStrong: 'rgba(162, 180, 200, 0.3)',
  accent: '#74f2ce',
  accentSoft: 'rgba(116, 242, 206, 0.18)',
  cyan: '#7cc8ff',
  gold: '#f7d774',
  red: '#ff7d7d',
  green: '#7af2b2',
  panel: 'rgba(10, 20, 30, 0.78)',
  panelEdge: 'rgba(255, 255, 255, 0.08)'
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
  extraCssText: 'backdrop-filter: blur(12px); box-shadow: 0 18px 42px rgba(0,0,0,0.35); border-radius: 14px;',
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

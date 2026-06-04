/**
 * useMagicColor.js
 * 从人物照片中提取主色调，实现 QQ Music 风格的 "魔法色彩" 动态效果
 * 使用 Canvas API 进行像素采样 + 简易 K-Means 聚类
 */

import { ref } from 'vue'

const colorCache = new Map()

/**
 * 加载图片并提取主色调
 * @param {string} imageUrl - 图片 URL
 * @returns {Promise<{hex: string, rgb: number[], gradient: string}>}
 */
export function useMagicColor() {
  const dominantColor = ref('#31C27C')
  const isLoading = ref(false)

  async function extractDominantColor(imageUrl) {
    if (!imageUrl) return null

    // 缓存命中
    if (colorCache.has(imageUrl)) {
      const cached = colorCache.get(imageUrl)
      dominantColor.value = cached.hex
      return cached
    }

    isLoading.value = true
    try {
      const color = await sampleImageColor(imageUrl)
      if (color) {
        colorCache.set(imageUrl, color)
        dominantColor.value = color.hex
      }
      return color
    } catch (err) {
      console.warn('魔法色彩提取失败:', err)
      return null
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 从颜色生成渐变色样式
   * @param {string} hex - 主色调
   * @returns {{ background: string, border: string, shadow: string }}
   */
  function getGradientFromColor(hex) {
    const rgb = hexToRgb(hex)
    if (!rgb) return {
      background: 'rgba(49, 194, 124, 0.08)',
      border: 'rgba(49, 194, 124, 0.3)',
      shadow: '0 0 12px rgba(49, 194, 124, 0.2)'
    }
    const { r, g, b } = rgb
    return {
      background: `linear-gradient(135deg, rgba(${r},${g},${b},0.12) 0%, rgba(${r},${g},${b},0.04) 100%)`,
      border: `rgba(${r},${g},${b},0.35)`,
      shadow: `0 0 16px rgba(${r},${g},${b},0.2)`
    }
  }

  /**
   * 批量预加载多个图片的主色调
   * @param {string[]} urls
   */
  async function preloadColors(urls) {
    const promises = urls.map(url => extractDominantColor(url).catch(() => null))
    await Promise.allSettled(promises)
  }

  return {
    dominantColor,
    isLoading,
    extractDominantColor,
    getGradientFromColor,
    preloadColors
  }
}

/* ═══ 内部实现 ═══ */

/**
 * Canvas 像素采样提取主色调
 */
async function sampleImageColor(imageUrl) {
  return new Promise((resolve, reject) => {
    const img = new Image()
    img.crossOrigin = 'anonymous'

    img.onload = () => {
      try {
        const canvas = document.createElement('canvas')
        // 缩小到 10x10 以快速采样
        const sampleSize = 10
        canvas.width = sampleSize
        canvas.height = sampleSize
        const ctx = canvas.getContext('2d')
        ctx.drawImage(img, 0, 0, sampleSize, sampleSize)

        const imageData = ctx.getImageData(0, 0, sampleSize, sampleSize)
        const pixels = []
        for (let i = 0; i < imageData.data.length; i += 4) {
          const r = imageData.data[i]
          const g = imageData.data[i + 1]
          const b = imageData.data[i + 2]
          // 跳过太暗或太亮的像素
          const brightness = (r + g + b) / 3
          if (brightness > 25 && brightness < 230) {
            pixels.push([r, g, b])
          }
        }

        if (pixels.length === 0) {
          resolve({ hex: '#31C27C', rgb: [49, 194, 124] })
          return
        }

        // 简易 K-Means (k=3) 找到聚类中心
        const k = Math.min(3, pixels.length)
        const centroids = simpleKMeans(pixels, k, 5)

        // 选择最饱和的颜色作为主色调
        let bestCentroid = centroids[0]
        let bestSaturation = 0
        for (const c of centroids) {
          const saturation = getSaturation(c[0], c[1], c[2])
          if (saturation > bestSaturation) {
            bestSaturation = saturation
            bestCentroid = c
          }
        }

        const hex = rgbToHex(bestCentroid[0], bestCentroid[1], bestCentroid[2])
        resolve({ hex, rgb: bestCentroid })
      } catch (err) {
        reject(err)
      }
    }

    img.onerror = () => reject(new Error('图片加载失败'))
    img.src = imageUrl
  })
}

/**
 * 简易 K-Means 聚类
 */
function simpleKMeans(pixels, k, maxIterations) {
  // 随机初始化质心
  const centroids = []
  const used = new Set()
  while (centroids.length < k) {
    const idx = Math.floor(Math.random() * pixels.length)
    if (!used.has(idx)) {
      used.add(idx)
      centroids.push([...pixels[idx]])
    }
  }

  for (let iter = 0; iter < maxIterations; iter++) {
    // 分配每个像素到最近的质心
    const clusters = Array.from({ length: k }, () => [])
    for (const pixel of pixels) {
      let minDist = Infinity
      let closest = 0
      for (let j = 0; j < k; j++) {
        const dist = colorDistance(pixel, centroids[j])
        if (dist < minDist) {
          minDist = dist
          closest = j
        }
      }
      clusters[closest].push(pixel)
    }

    // 更新质心
    let changed = false
    for (let j = 0; j < k; j++) {
      if (clusters[j].length === 0) continue
      const sum = [0, 0, 0]
      for (const p of clusters[j]) {
        sum[0] += p[0]; sum[1] += p[1]; sum[2] += p[2]
      }
      const newCentroid = [
        Math.round(sum[0] / clusters[j].length),
        Math.round(sum[1] / clusters[j].length),
        Math.round(sum[2] / clusters[j].length)
      ]
      if (colorDistance(newCentroid, centroids[j]) > 1) changed = true
      centroids[j] = newCentroid
    }

    if (!changed) break
  }

  return centroids
}

function colorDistance(a, b) {
  // 加权欧几里得距离 (人眼对绿色更敏感)
  const dr = (a[0] - b[0]) * 1.0
  const dg = (a[1] - b[1]) * 1.4
  const db = (a[2] - b[2]) * 0.8
  return Math.sqrt(dr * dr + dg * dg + db * db)
}

function getSaturation(r, g, b) {
  const max = Math.max(r, g, b)
  const min = Math.min(r, g, b)
  if (max === 0) return 0
  return (max - min) / max
}

function hexToRgb(hex) {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null
}

function rgbToHex(r, g, b) {
  return '#' + [r, g, b].map(x => {
    const hex = Math.max(0, Math.min(255, Math.round(x))).toString(16)
    return hex.length === 1 ? '0' + hex : hex
  }).join('')
}

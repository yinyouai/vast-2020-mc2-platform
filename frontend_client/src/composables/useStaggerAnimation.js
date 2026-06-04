/**
 * useStaggerAnimation.js
 * 列表交错进入动画 — 配合 TransitionGroup 或 IntersectionObserver
 */

import { ref, onMounted, onUnmounted } from 'vue'

/**
 * 支持两种模式:
 * 1. `list` 模式: 返回延迟计算函数，用于 TransitionGroup 的 v-enter
 * 2. `observer` 模式: 使用 IntersectionObserver 在元素进入视口时触发动画
 *
 * @param {{ mode?: 'list'|'observer', baseDelay?: number, threshold?: number }} options
 */
export function useStaggerAnimation(options = {}) {
  const { mode = 'list', baseDelay = 60, threshold = 0.1 } = options
  const isReady = ref(false)

  // 模式 1: 返回动画配置对象
  function getItemStyle(index) {
    return {
      animationDelay: `${index * baseDelay}ms`,
      '--stagger-index': index,
      '--stagger-delay': `${index * baseDelay}ms`
    }
  }

  // 模式 2: IntersectionObserver 驱动
  const observedElements = ref(new Set())
  let observer = null

  function observeElement(el, index) {
    if (!observer) {
      observer = new IntersectionObserver((entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            entry.target.style.setProperty('--stagger-delay', `${index * baseDelay}ms`)
            entry.target.classList.add('card-pop-enter-active')
            entry.target.style.opacity = '1'
            entry.target.style.transform = 'translateY(0)'
            observer.unobserve(entry.target)
            observedElements.value.delete(entry.target)
          }
        }
      }, { threshold })
    }
    observer.observe(el)
    observedElements.value.add(el)
  }

  onMounted(() => {
    isReady.value = true
  })

  onUnmounted(() => {
    if (observer) {
      observer.disconnect()
      observer = null
    }
    observedElements.value.clear()
  })

  return {
    isReady,
    getItemStyle,
    observeElement
  }
}

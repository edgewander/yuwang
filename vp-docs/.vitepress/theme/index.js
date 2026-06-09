import DefaultTheme from 'vitepress/theme'
import './style.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ router }) {
    // Reading progress bar
    if (typeof window !== 'undefined') {
      const bar = document.createElement('div')
      bar.id = 'reading-progress'
      document.body.appendChild(bar)
      window.addEventListener('scroll', () => {
        const scrollTop = window.scrollY
        const docHeight = document.documentElement.scrollHeight - window.innerHeight
        bar.style.width = (docHeight > 0 ? (scrollTop / docHeight) * 100 : 0) + '%'
      })
    }
  },
}

// src/permission.js
import router, { resetRouter } from './router' // 添加 resetRouter 导入
import store from './store'
import { Message } from 'element-ui'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

NProgress.configure({ showSpinner: false })

const whiteList = ['/login']

router.beforeEach(async(to, from, next) => {
  NProgress.start()
  const hasToken = store.getters.token || localStorage.getItem('token')
  if (hasToken) {
    if (to.path === '/login') {
      next({ path: '/' })
      NProgress.done()
    } else {
      try {
        const hasPerms = store.getters.perms && store.getters.perms.length > 0
        if (hasPerms) {
          next()
        } else {
          // 获取用户信息
          const { perms } = await store.dispatch('user/getInfo')
          // 重置路由，避免重复添加
          resetRouter()
          // 根据权限生成可访问的路由
          const accessRoutes = await store.dispatch('permission/generateRoutes', perms)
          // 动态添加路由
          router.addRoutes(accessRoutes)
          // 使用 replace: true 避免导航重复
          next({ ...to, replace: true })
        }
      } catch (error) {
        console.error('路由守卫错误:', error)
        await store.dispatch('user/resetToken')
        Message.error(error || 'Has Error')
        next(`/login?redirect=${to.path}`)
        NProgress.done()
      }
    }
  } else {
    if (whiteList.includes(to.path)) {
      next()
    } else {
      next(`/login?redirect=${to.path}`)
      NProgress.done()
    }
  }
})

router.afterEach(() => {
  NProgress.done()
})

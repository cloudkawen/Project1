// src/permission.js
import router, { resetRouter } from './router'  // 添加 resetRouter 导入
import store from './store'
import { Message } from 'element-ui'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

NProgress.configure({ showSpinner: false })

// 调试：检查router是否正确导入
console.log('router对象:', router)
console.log('router类型:', typeof router)
console.log('router.beforeEach:', router.beforeEach)
console.log('router是VueRouter实例吗?', router instanceof VueRouter)

const whiteList = ['/login', '/404', '/401']  // 添加错误页面到白名单

router.beforeEach(async(to, from, next) => {
  console.log('路由守卫开始执行，目标路由:', to.path)
  NProgress.start()
  
  const hasToken = store.getters.token || localStorage.getItem('token')
  console.log('检查token:', hasToken)
  
  if (hasToken) {
    if (to.path === '/login') {
      console.log('已登录，跳转到首页')
      next({ path: '/' })
      NProgress.done()
    } else {
      try {
        const hasPerms = store.getters.perms && store.getters.perms.length > 0
        console.log('检查权限:', hasPerms)
        
        if (hasPerms) {
          console.log('已有权限，放行')
          next()
        } else {
          console.log('获取用户信息...')
          // 获取用户信息
          const { perms } = await store.dispatch('user/getInfo')
          console.log('用户权限:', perms)
          
          // 重置路由，避免重复添加
          resetRouter()
          
          // 根据权限生成可访问的路由
          const accessRoutes = await store.dispatch('permission/generateRoutes', perms)
          console.log('生成的路由:', accessRoutes)
          
          // 动态添加路由
          router.addRoutes(accessRoutes)
          
          console.log('路由添加完成，重定向到:', to.path)
          // 使用 replace: true 避免导航重复
          next({ ...to, replace: true })
        }
      } catch (error) {
        console.error('路由守卫错误:', error)
        await store.dispatch('user/resetToken')
        Message.error(error?.message || '系统错误')
        next(`/login?redirect=${to.path}`)
        NProgress.done()
      }
    }
  } else {
    console.log('无token，检查白名单')
    if (whiteList.includes(to.path)) {
      console.log('在白名单中，放行')
      next()
    } else {
      console.log('不在白名单，跳转到登录页')
      next(`/login?redirect=${to.path}`)
      NProgress.done()
    }
  }
})

router.afterEach(() => {
  console.log('路由导航完成')
  NProgress.done()
})
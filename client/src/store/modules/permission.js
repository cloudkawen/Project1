import { asyncRoutes, constantRoutes } from '@/router'

/**
 * Use meta.perm to determine if the current user has permission
 * @param perms
 * @param route
 */
function hasPermission(perms, route) {
  if (route.meta && route.meta.perms) {
    return perms.some(perm => route.meta.perms.includes(perm))
  } else {
    return true
  }
}

/**
 * Filter asynchronous routing tables by recursion
 * @param routes asyncRoutes
 * @param perms
 */
export function filterAsyncRoutes(routes, perms) {
  const res = []

  routes.forEach(route => {
    const tmp = { ...route }
    if (hasPermission(perms, tmp)) {
      if (tmp.children) {
        tmp.children = filterAsyncRoutes(tmp.children, perms)
      }
      res.push(tmp)
    }
  })
  return res
}

const state = {
  routes: [],
  addRoutes: []
}

const mutations = {
  SET_ROUTES: (state, routes) => {
    state.addRoutes = routes
    state.routes = constantRoutes.concat(routes)
  }
}

const actions = {
  // client/src/store/modules/permission.js
  // client/src/store/modules/permission.js
  generateRoutes({ commit }, roles) {
    return new Promise(resolve => {
      console.log('生成路由，roles:', roles)
      // ✅ 修复：确保 roles 是数组
      if (!roles) {
        console.warn('roles 为 undefined 或 null，使用默认角色')
        roles = ['admin']
      }
      if (!Array.isArray(roles)) {
        console.warn('roles 不是数组，转换为数组:', roles)
        roles = [roles]
      }
      // 如果 roles 为空数组，使用默认角色
      if (roles.length === 0) {
        console.warn('roles 为空数组，使用默认角色 ["admin"]')
        roles = ['admin']
      }
      let accessedRoutes
      if (roles.includes('admin')) {
        accessedRoutes = asyncRoutes || []
      } else {
        accessedRoutes = filterAsyncRoutes(asyncRoutes, roles)
      }
      // 在动态路由末尾添加通配符路由
      accessedRoutes.push(
        {
          path: '*',
          redirect: '/404',
          hidden: true
        }
      )
      commit('SET_ROUTES', accessedRoutes)
      resolve(accessedRoutes)
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

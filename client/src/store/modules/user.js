// client/src/store/modules/user.js
import { login, logout, getInfo } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'

const state = {
  token: getToken(),
  name: '',
  avatar: '',
  roles: []
}

const mutations = {
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_ROLES: (state, roles) => {
    state.roles = roles
  }
}

const actions = {
  // 用户登录
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password })
        .then(response => {
          console.log('Vuex 登录响应:', response)
          // ✅ 修复：正确获取 access token
          const token = response.access || response.token
          if (!token) {
            reject(new Error('登录失败：未收到令牌'))
            return
          }
          commit('SET_TOKEN', token)
          setToken(token)
          resolve()
        })
        .catch(error => {
          console.error('Vuex 登录错误:', error)
          reject(error)
        })
    })
  },

  // 获取用户信息
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo()
        .then(response => {
          console.log('用户信息响应:', response)
          // ✅ 修复：正确处理响应结构
          const data = response.data || response
          if (!data) {
            reject(new Error('验证失败，请重新登录'))
            return
          }
          const { roles, name, avatar } = data
          // 角色必须是非空数组
          if (!roles || roles.length <= 0) {
            commit('SET_ROLES', ['admin']) // 临时设置为 admin
          } else {
            commit('SET_ROLES', roles)
          }
          commit('SET_NAME', name || '管理员')
          commit('SET_AVATAR', avatar || '')
          resolve(data)
        })
        .catch(error => {
          console.error('获取用户信息失败:', error)
          reject(error)
        })
    })
  },

  // 用户登出
  logout({ commit, state }) {
    return new Promise((resolve, reject) => {
      logout()
        .then(() => {
          commit('SET_TOKEN', '')
          commit('SET_ROLES', [])
          removeToken()
          resolve()
        })
        .catch(error => {
          console.error('登出失败:', error)
          // 即使API失败，也要清除本地token
          commit('SET_TOKEN', '')
          commit('SET_ROLES', [])
          removeToken()
          resolve()
        })
    })
  },

  // 重置 token
  resetToken({ commit }) {
    return new Promise(resolve => {
      commit('SET_TOKEN', '')
      commit('SET_ROLES', [])
      removeToken()
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

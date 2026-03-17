import { login, logout, getInfo } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'
const state = {
  token: getToken(),
  name: '',
  avatar: '',
  roles: [],
  perms: []
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
  },
  SET_PERMS: (state, perms) => {
    state.perms = perms
  }
}
const actions = {
  // 用户登录
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password })
        .then(response => {
          console.log('登录API响应:', response)
          // 尝试多种可能的 token 路径
          const token = (response && response.access) ||
                      (response && response.data && response.data.access) ||
                      (response && response.token) ||
                      (response && response.data && response.data.token)
          if (!token) {
            console.error('Token 获取失败，响应结构:', response)
            reject(new Error('登录失败：未收到令牌'))
            return
          }
          commit('SET_TOKEN', token)
          setToken(token)
          resolve()
        })
        .catch(error => {
          console.error('登录失败:', error)
          reject(error)
        })
    })
  },
  // 获取用户信息
  getInfo({ commit }) {
    return new Promise((resolve, reject) => {
      getInfo().then(response => {
        const data = response.data
        const { roles, name, avatar, perms } = data
        commit('SET_ROLES', roles)
        commit('SET_PERMS', perms || [])
        commit('SET_NAME', name)
        commit('SET_AVATAR', avatar)
        resolve(data)
      }).catch(error => {
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
          commit('SET_PERMS', [])
          removeToken()
          resolve()
        })
        .catch(error => {
          console.error('登出失败:', error)
          // 即使API失败，也要清除本地token
          commit('SET_TOKEN', '')
          commit('SET_ROLES', [])
          commit('SET_PERMS', [])
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
      commit('SET_PERMS', [])
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

import axios from 'axios'
import { Message, MessageBox } from 'element-ui'
import store from '@/store'

// 创建axios实例
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API || '/',
  timeout: 15000
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('响应错误:', error.response || error)
    if (error.response && error.response.status === 401) {
      Message({
        message: '登录已过期，请重新登录',
        type: 'error',
        duration: 3000
      })
      // 清除 token
      localStorage.removeItem('token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('userInfo')
      // 跳转到登录页
      setTimeout(() => {
        window.location.href = '/login'
      }, 1500)
    } else if (error.response) {
      const message = error.response.data.detail ||
                     error.response.data.message ||
                     error.response.data.msg ||
                     '请求失败'
      Message({
        message: message,
        type: 'error',
        duration: 5000
      })
    } else {
      Message({
        message: error.message || '网络错误',
        type: 'error',
        duration: 5000
      })
    }
    return Promise.reject(error)
  }
)

export default service

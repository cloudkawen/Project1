// client/src/api/user.js
import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/api/token/',
    method: 'post',
    data
  }).then(response => {
    console.log('登录API响应:', response)

    // 根据实际返回结构调整
    if (response.access) {
      return response
    } else if (response.data && response.data.access) {
      return response.data
    } else {
      // 如果没有找到 access，返回原始响应
      return response
    }
  })
}

export function logout() {
  return request({
    url: '/api/token/black/',
    method: 'get'
  }).finally(() => {
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('userInfo')
  })
}

export function getInfo() {
  return request({
    url: '/api/system/user/info/',
    method: 'get'
  })
}

// 如果后端接口不存在，使用这个临时版本
export function getInfoMock() {
  return Promise.resolve({
    data: {
      name: '管理员',
      avatar: '',
      roles: ['admin']
    }
  })
}
// ✅ 添加 changePassword 函数
export function changePassword(data) {
  return request({
    url: '/api/user/change-password/', // 修改为正确的后端接口
    method: 'post',
    data
  })
}

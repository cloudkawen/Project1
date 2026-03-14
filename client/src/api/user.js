// src/api/user.js
import request from '@/utils/request'

// 用户认证相关
export function login(data) {
  return request({
    url: '/api/token/',
    method: 'post',
    data
  }).then(response => {
    console.log('登录API响应:', response)
    
    if (response.access) {
      return response
    }
    
    throw new Error('登录失败：未收到令牌')
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

// 用户管理相关
export function getUserList(query) {
  return request({
    url: '/api/system/user/',
    method: 'get',
    params: query
  })
}

export function getUser(id) {
  return request({
    url: `/api/system/user/${id}/`,
    method: 'get'
  })
}

export function createUser(data) {
  return request({
    url: '/api/system/user/',
    method: 'post',
    data
  })
}

export function updateUser(id, data) {
  return request({
    url: `/api/system/user/${id}/`,
    method: 'put',
    data
  })
}

export function deleteUser(id) {
  return request({
    url: `/api/system/user/${id}/`,
    method: 'delete'
  })
}

// 修改密码
export function changePassword(data) {
  return request({
    url: '/api/user/change-password/',
    method: 'post',
    data
  })
}

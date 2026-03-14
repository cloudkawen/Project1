// src/utils/auth.js
export function getToken() {
  return localStorage.getItem('token')
}

export function getRefreshToken() {
  return localStorage.getItem('refresh_token')
}

export function setToken(token) {
  localStorage.setItem('token', token)
}

export function setRefreshToken(token) {
  localStorage.setItem('refresh_token', token)
}

export function removeToken() {
  localStorage.removeItem('token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('userInfo')
}

export function isLoggedIn() {
  return !!getToken()
}

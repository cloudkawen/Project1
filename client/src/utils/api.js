// src/utils/api.js
const API = {
  // 认证相关
  LOGIN: '/token/',
  LOGOUT: '/token/black/',
  USER_INFO: '/system/user/info/',
  CHANGE_PASSWORD: '/api/user/change-password/',
  // 用户管理
  USER_LIST: '/system/user/',
  USER_DETAIL: (id) => '/system/user/${id}/',
  // 物品管理
  ITEMS: '/api/items/',
  ITEM_DETAIL: (id) => '/api/items/${id}/',
  // 分类管理
  CATEGORIES: '/api/categories/',
  CATEGORY_DETAIL: (id) => '/api/categories/${id}/',
  // Dashboard
  DASHBOARD: '/api/dashboard/'
}

export default API

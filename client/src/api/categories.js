import request from '@/utils/request'

// 获取分类列表
export function getCategories(query) {
  return request({
    url: '/api/categories/',
    method: 'get',
    params: query
  })
}

// 获取单个分类
export function getCategory(id) {
  return request({
    url: `/api/categories/${id}/`,
    method: 'get'
  })
}

// 创建分类
export function createCategory(data) {
  return request({
    url: '/api/categories/',
    method: 'post',
    data
  })
}

// 更新分类
export function updateCategory(id, data) {
  return request({
    url: `/api/categories/${id}/`,
    method: 'put',
    data
  })
}

// 部分更新分类
export function patchCategory(id, data) {
  return request({
    url: `/api/categories/${id}/`,
    method: 'patch',
    data
  })
}

// 删除分类
export function deleteCategory(id) {
  return request({
    url: `/api/categories/${id}/`,
    method: 'delete'
  })
}

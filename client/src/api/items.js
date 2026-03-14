import request from '@/utils/request'

// 获取物品列表
export function getItems(query) {
  return request({
    url: '/api/items/',
    method: 'get',
    params: query
  })
}

// 获取单个物品
export function getItem(id) {
  return request({
    url: `/api/items/${id}/`,
    method: 'get'
  })
}

// 创建物品
export function createItem(data) {
  return request({
    url: '/api/items/',
    method: 'post',
    data
  })
}

// 更新物品
export function updateItem(id, data) {
  return request({
    url: `/api/items/${id}/`,
    method: 'put',
    data
  })
}

// 部分更新物品
export function patchItem(id, data) {
  return request({
    url: `/api/items/${id}/`,
    method: 'patch',
    data
  })
}

// 删除物品
export function deleteItem(id) {
  return request({
    url: `/api/items/${id}/`,
    method: 'delete'
  })
}

// 获取物品统计信息
export function getItemsStats() {
  return request({
    url: '/api/items/stats/',
    method: 'get'
  })
}

// 获取物品概览
export function getItemsSummary() {
  return request({
    url: '/api/items/summary/',
    method: 'get'
  })
}

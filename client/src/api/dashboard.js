import request from '@/utils/request'

// 获取Dashboard数据
export function getDashboardData() {
  return request({
    url: '/api/dashboard/',
    method: 'get'
  })
}

// client/src/store/modules/dashboard.js
import { getDashboardData } from '@/api/dashboard'

const state = {
  dashboardData: null
}

const mutations = {
  SET_DASHBOARD_DATA: (state, data) => {
    state.dashboardData = data
  }
}

const actions = {
  getDashboardData({ commit, state }) {
    return new Promise((resolve, reject) => {
      getDashboardData()
        .then(response => {
          commit('SET_DASHBOARD_DATA', response.data)
          resolve(response)
        })
        .catch(error => {
          console.error('获取仪表盘数据失败:', error)
          // 返回模拟数据
          const mockData = {
            code: 200,
            data: {
              statistics: {
                total_items: 156,
                total_categories: 8,
                recent_items: 12,
                expiring_items: 5,
                expired_items: 3
              },
              charts: {
                items_by_category: [
                  { name: '电子产品', value: 45 },
                  { name: '家具', value: 32 },
                  { name: '办公用品', value: 28 },
                  { name: '图书', value: 25 },
                  { name: '其他', value: 26 }
                ],
                items_by_status: [
                  { name: '正常', value: 120 },
                  { name: '即将过期', value: 5 },
                  { name: '已过期', value: 3 }
                ]
              }
            },
            msg: 'success'
          }
          resolve(mockData)
        })
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

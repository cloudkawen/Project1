// client/src/views/dashboard/index.vue
<template>
  <div class="dashboard-container">
    <!-- 页面标题和时间 -->
    <div class="dashboard-header">
      <div>
        <h2>数据总览</h2>
        <p class="subtitle">系统数据统计与分析</p>
      </div>
      <div class="header-actions">
        <el-tag type="info">
          <i class="el-icon-time" /> 最后更新: {{ formatTime(lastUpdated) }}
        </el-tag>
        <el-button
          type="primary"
          icon="el-icon-refresh"
          :loading="refreshing"
          @click="refreshDashboard"
        >
          刷新数据
        </el-button>
      </div>
    </div>

    <!-- 用户信息卡片 -->
    <el-card v-if="userInfo" shadow="never" class="user-info-card">
      <div class="user-info-content">
        <div class="user-avatar">
          <i class="el-icon-user-solid" />
        </div>
        <div class="user-details">
          <h3>{{ userInfo.username || '管理员' }}</h3>
          <p class="user-meta">
            <span>最后登录: {{ formatDateTime(userInfo.last_login) }}</span>
            <span>注册时间: {{ formatDate(userInfo.date_joined) }}</span>
          </p>
        </div>
        <div class="user-stats">
          <el-tag type="success">已登录</el-tag>
        </div>
      </div>
    </el-card>

    <!-- 统计数据卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="12" :sm="6" :md="6" :lg="6" :xl="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: #409EFF;">
              <i class="el-icon-shopping-bag-1" />
            </div>
            <div class="stat-info">
              <h3>{{ statistics.total_items || 0 }}</h3>
              <p>物品总数</p>
              <div v-if="trendData.length > 0" class="stat-trend">
                <span :class="getTrendClass('items')">
                  <i :class="getTrendIcon('items')" />
                  {{ calculateTrend('items') }}%
                </span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="6" :md="6" :lg="6" :xl="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: #67C23A;">
              <i class="el-icon-folder" />
            </div>
            <div class="stat-info">
              <h3>{{ statistics.total_categories || 0 }}</h3>
              <p>分类数量</p>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="6" :md="6" :lg="6" :xl="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: #E6A23C;">
              <i class="el-icon-time" />
            </div>
            <div class="stat-info">
              <h3>{{ statistics.recent_items || 0 }}</h3>
              <p>最近7天新增</p>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="6" :md="6" :lg="6" :xl="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: #F56C6C;">
              <i class="el-icon-warning" />
            </div>
            <div class="stat-info">
              <h3>{{ statistics.expiring_items || 0 }}</h3>
              <p>即将过期</p>
              <small v-if="statistics.expired_items > 0" class="expired-count">
                已过期: {{ statistics.expired_items }}
              </small>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="charts-row">
      <!-- 物品分类统计 -->
      <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
        <el-card shadow="hover" class="chart-card">
          <div slot="header" class="chart-header">
            <span>物品分类统计</span>
            <el-tag v-if="charts.items_by_category.length > 0" type="info" size="small">
              {{ charts.items_by_category.length }} 个分类
            </el-tag>
          </div>
          <div v-if="loading" class="loading-container">
            <i class="el-icon-loading" /> 加载中...
          </div>
          <div v-else-if="charts.items_by_category.length > 0" class="chart-container">
            <div class="chart-list">
              <div v-for="item in charts.items_by_category.slice(0, 5)" :key="item.id" class="category-item">
                <div class="category-info">
                  <span class="category-name">{{ item.name }}</span>
                  <span class="category-count">{{ item.value }} 个</span>
                </div>
                <el-progress
                  :percentage="(item.value / totalItems) * 100"
                  :stroke-width="8"
                  :color="getCategoryColor(item.name)"
                />
              </div>
            </div>
            <div v-if="charts.items_by_category.length > 5" class="more-categories">
              <el-button type="text" @click="showAllCategories = true">
                还有 {{ charts.items_by_category.length - 5 }} 个分类...
              </el-button>
            </div>
          </div>
          <div v-else class="empty-chart">
            <i class="el-icon-data-line" />
            <p>暂无分类数据</p>
            <el-button type="text" @click="$router.push('/categories')">去添加分类</el-button>
          </div>
        </el-card>
      </el-col>

      <!-- 物品状态分布 -->
      <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
        <el-card shadow="hover" class="chart-card">
          <div slot="header" class="chart-header">
            <span>物品状态分布</span>
            <el-tag type="info" size="small">总计 {{ totalItems }} 个</el-tag>
          </div>
          <div v-if="loading" class="loading-container">
            <i class="el-icon-loading" /> 加载中...
          </div>
          <div v-else class="chart-container">
            <div class="status-chart">
              <div v-for="item in charts.items_by_status" :key="item.name" class="status-item">
                <div class="status-header">
                  <div class="status-label">
                    <span class="status-dot" :style="{backgroundColor: item.color}" />
                    <span class="status-name">{{ item.name }}</span>
                  </div>
                  <span class="status-count">{{ item.value }} 个</span>
                </div>
                <el-progress
                  :percentage="(item.value / totalItems) * 100"
                  :stroke-width="12"
                  :color="item.color"
                  :show-text="false"
                />
                <div class="status-percentage">
                  {{ ((item.value / totalItems) * 100).toFixed(1) }}%
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 新增物品趋势（最近30天） -->
      <el-col v-if="trendData.length > 0" :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
        <el-card shadow="hover" class="trend-card">
          <div slot="header">
            <span>新增物品趋势(最近30天)</span>
          </div>
          <div class="trend-chart">
            <div
              v-for="(day, index) in trendData"
              :key="index"
              class="trend-bar"
              :style="{height: Math.max(20, (day.count / maxDailyCount) * 100) + 'px'}"
              :title="`${day.date}: ${day.count}个`"
            >
              <div class="trend-label">{{ day.date }}</div>
              <div v-if="day.count > 0" class="trend-value">{{ day.count }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 底部区域 -->
    <el-row :gutter="20" class="bottom-row">
      <!-- 快速链接 -->
      <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
        <el-card shadow="hover" class="quick-links-card">
          <div slot="header">
            <span>快速操作</span>
          </div>
          <el-row :gutter="20">
            <el-col
              v-for="link in quickLinks"
              :key="link.title"
              :xs="12"
              :sm="12"
              :md="6"
              :lg="6"
              :xl="6"
              class="quick-link-col"
            >
              <div class="quick-link" @click="handleQuickLink(link)">
                <div class="link-icon" :style="{backgroundColor: link.color}">
                  <i :class="link.icon" />
                </div>
                <p class="link-title">{{ link.title }}</p>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>

      <!-- 最近活动 -->
      <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
        <el-card shadow="hover" class="activities-card">
          <div slot="header" class="activities-header">
            <span>最近活动</span>
            <el-button type="text" :loading="refreshing" @click="refreshActivities">
              <i class="el-icon-refresh" />
            </el-button>
          </div>
          <div v-if="recentActivities.length > 0" class="activities-list">
            <div v-for="activity in recentActivities" :key="activity.time" class="activity-item">
              <div class="activity-icon" :style="{backgroundColor: getActivityColor(activity.type)}">
                <i :class="getActivityIcon(activity.type)" />
              </div>
              <div class="activity-content">
                <p class="activity-message">{{ activity.message }}</p>
                <p class="activity-time">{{ formatDateTime(activity.time) }}</p>
              </div>
            </div>
          </div>
          <div v-else class="empty-activities">
            <i class="el-icon-news" />
            <p>暂无最近活动</p>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 全部分类对话框 -->
    <el-dialog
      title="全部分类统计"
      :visible.sync="showAllCategories"
      width="60%"
    >
      <el-table :data="charts.items_by_category" stripe>
        <el-table-column prop="name" label="分类名称" />
        <el-table-column prop="value" label="物品数量" width="120" />
        <el-table-column label="占比" width="200">
          <template slot-scope="scope">
            <el-progress
              :percentage="(scope.row.value / totalItems) * 100"
              :stroke-width="8"
              :color="getCategoryColor(scope.row.name)"
            />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template slot-scope="scope">
            <el-button
              type="text"
              @click="viewCategoryItems(scope.row)"
            >
              查看物品
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script>
import { getDashboardData } from '@/api/dashboard'
import { formatDate, formatDateTime, formatTime } from '@/utils/date'

export default {
  name: 'Dashboard',
  data() {
    return {
      loading: false,
      refreshing: false,
      showAllCategories: false,
      lastUpdated: null,
      statistics: {
        total_items: 0,
        total_categories: 0,
        recent_items: 0,
        expiring_items: 0,
        expired_items: 0
      },
      charts: {
        items_by_category: [],
        items_by_status: [],
        items_by_location: [],
        items_by_month: []
      },
      trendData: [],
      quickLinks: [],
      recentActivities: [],
      userInfo: null
    }
  },
  computed: {
    totalItems() {
      return this.statistics.total_items || 1
    },
    maxDailyCount() {
      if (this.trendData.length === 0) return 1
      return Math.max(...this.trendData.map(d => d.count))
    }
  },
  created() {
    this.fetchDashboardData()
  },
  methods: {
    // 工具函数
    formatDate,
    formatDateTime,
    formatTime,
    // 获取仪表盘数据
    async fetchDashboardData() {
      this.loading = true
      try {
        console.log('📊 获取仪表盘数据...')
        const response = await getDashboardData()
        if (response.code === 200 && response.data) {
          this.setDashboardData(response.data)
          this.lastUpdated = response.timestamp || new Date().toISOString()
          console.log('✅ 仪表盘数据获取成功')
        } else {
          console.error('获取仪表盘数据失败:', response.msg)
          this.$message.error('获取数据失败')
        }
      } catch (error) {
        console.error('获取仪表盘数据异常:', error)
        this.$message.error('获取数据异常')
      } finally {
        this.loading = false
      }
    },
    // 设置仪表盘数据
    setDashboardData(data) {
      this.statistics = data.statistics || this.statistics
      this.charts = data.charts || this.charts
      this.quickLinks = data.quick_links || this.quickLinks
      this.recentActivities = data.recent_activities || this.recentActivities
      this.trendData = data.trend_data || this.trendData
      this.userInfo = data.user_info || this.userInfo
    },
    // 刷新仪表盘
    async refreshDashboard() {
      this.refreshing = true
      try {
        await this.fetchDashboardData()
        this.$message.success('数据已刷新')
      } finally {
        this.refreshing = false
      }
    },
    // 刷新活动
    async refreshActivities() {
      this.refreshing = true
      try {
        // 这里可以调用专门的刷新接口
        setTimeout(() => {
          this.fetchDashboardData()
        }, 500)
      } finally {
        this.refreshing = false
      }
    },
    // 计算趋势
    calculateTrend(type) {
      if (!this.trendData || this.trendData.length < 2) return 0
      const today = this.trendData[this.trendData.length - 1].count
      const yesterday = this.trendData[this.trendData.length - 2].count
      if (yesterday === 0) return 100
      return ((today - yesterday) / yesterday * 100).toFixed(1)
    },
    getTrendClass(type) {
      const trend = this.calculateTrend(type)
      if (trend > 0) return 'trend-up'
      if (trend < 0) return 'trend-down'
      return 'trend-stable'
    },
    getTrendIcon(type) {
      const trend = this.calculateTrend(type)
      if (trend > 0) return 'el-icon-top'
      if (trend < 0) return 'el-icon-bottom'
      return 'el-icon-minus'
    },
    // 获取分类颜色
    getCategoryColor(name) {
      const colors = {
        '电子产品': '#409EFF',
        '家具': '#67C23A',
        '办公用品': '#E6A23C',
        '图书': '#F56C6C',
        '其他': '#909399'
      }
      return colors[name] || this.generateColor(name)
    },
    // 生成颜色
    generateColor(str) {
      let hash = 0
      for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash)
      }
      const color = Math.floor(Math.abs(Math.sin(hash) * 16777215))
      return '#' + color.toString(16).padStart(6, '0').slice(0, 6)
    },
    // 获取活动图标
    getActivityIcon(type) {
      const icons = {
        'item_added': 'el-icon-circle-plus',
        'item_updated': 'el-icon-edit',
        'category_added': 'el-icon-folder-add',
        'item_expired': 'el-icon-warning',
        'default': 'el-icon-info'
      }
      return icons[type] || icons.default
    },
    // 获取活动颜色
    getActivityColor(type) {
      const colors = {
        'item_added': '#67C23A',
        'item_updated': '#409EFF',
        'category_added': '#E6A23C',
        'item_expired': '#F56C6C',
        'default': '#909399'
      }
      return colors[type] || colors.default
    },
    // 处理快速链接
    handleQuickLink(link) {
      if (link.path) {
        this.$router.push(link.path)
      }
    },
    // 查看分类物品
    viewCategoryItems(category) {
      this.$router.push({
        path: '/items',
        query: { category: category.id }
      })
    }
  }
}
</script>

<style scoped>
/* 样式优化，保持原有样式基础，添加新的样式 */

/* 页面标题和操作栏 */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
}

/* 用户信息卡片 */
.user-info-card {
  margin-bottom: 20px;
  border-left: 4px solid #409EFF;
}

.user-info-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: #409EFF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: white;
}

.user-details h3 {
  margin: 0 0 8px 0;
  font-size: 18px;
  color: #303133;
}

.user-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 12px;
  color: #909399;
}

.user-stats {
  margin-left: auto;
}

/* 统计数据卡片优化 */
.stat-info .stat-trend {
  font-size: 12px;
  margin-top: 4px;
}

.stat-trend .trend-up {
  color: #67C23A;
}

.stat-trend .trend-down {
  color: #F56C6C;
}

.stat-trend .trend-stable {
  color: #909399;
}

.expired-count {
  color: #F56C6C;
  font-size: 12px;
  margin-top: 4px;
  display: block;
}

/* 图表头部 */
.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 趋势图 */
.trend-card {
  margin-top: 20px;
}

.trend-chart {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  height: 120px;
  padding: 20px 0;
  border-top: 1px solid #f0f0f0;
  overflow-x: auto;
}

.trend-bar {
  flex: 1;
  min-width: 20px;
  background-color: #409EFF;
  border-radius: 4px 4px 0 0;
  position: relative;
  transition: height 0.3s ease;
  min-height: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  padding: 4px 0;
}

.trend-bar:hover {
  opacity: 0.8;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.3);
}

.trend-label {
  font-size: 10px;
  color: #606266;
  margin-top: 4px;
  writing-mode: vertical-rl;
  transform: rotate(180deg);
  white-space: nowrap;
}

.trend-value {
  font-size: 10px;
  color: white;
  font-weight: bold;
  margin-top: 2px;
}

/* 状态标签 */
.status-label {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.status-percentage {
  font-size: 12px;
  color: #909399;
  text-align: right;
  margin-top: 4px;
}

/* 活动头部 */
.activities-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 响应式优化 */
@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
  }
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
  .user-info-content {
    flex-direction: column;
    text-align: center;
  }
  .user-stats {
    margin: 0;
  }
  .trend-bar {
    min-width: 16px;
  }
  .trend-label {
    font-size: 8px;
  }
}
</style>

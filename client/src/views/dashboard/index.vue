// client/src/views/dashboard/index.vue
<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h2>数据总览</h2>
      <p class="subtitle">系统数据统计与分析</p>
    </div>

    <!-- 统计数据卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: #409EFF;">
              <i class="el-icon-shopping-bag-1" />
            </div>
            <div class="stat-info">
              <h3>{{ statistics.total_items || 0 }}</h3>
              <p>物品总数</p>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
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
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: #E6A23C;">
              <i class="el-icon-time" />
            </div>
            <div class="stat-info">
              <h3>{{ statistics.recent_items || 0 }}</h3>
              <p>最近新增</p>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: #F56C6C;">
              <i class="el-icon-warning" />
            </div>
            <div class="stat-info">
              <h3>{{ statistics.expiring_items || 0 }}</h3>
              <p>即将过期</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="charts-row">
      <el-col :span="12">
        <el-card shadow="hover" class="chart-card">
          <div slot="header">
            <span>物品分类统计</span>
          </div>
          <div v-if="loading" class="loading-container">
            <i class="el-icon-loading" /> 加载中...
          </div>
          <div v-else class="chart-container">
            <div v-if="charts.items_by_category && charts.items_by_category.length > 0">
              <div v-for="item in charts.items_by_category" :key="item.name" class="category-item">
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
            <div v-else class="empty-chart">
              暂无分类数据
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover" class="chart-card">
          <div slot="header">
            <span>物品状态分布</span>
          </div>
          <div v-if="loading" class="loading-container">
            <i class="el-icon-loading" /> 加载中...
          </div>
          <div v-else class="chart-container">
            <div v-if="charts.items_by_status && charts.items_by_status.length > 0" class="status-chart">
              <div v-for="item in charts.items_by_status" :key="item.name" class="status-item">
                <div class="status-header">
                  <span class="status-name">{{ item.name }}</span>
                  <span class="status-count">{{ item.value }} 个</span>
                </div>
                <el-progress
                  :percentage="(item.value / totalItems) * 100"
                  :stroke-width="12"
                  :color="getStatusColor(item.name)"
                  :show-text="false"
                />
              </div>
            </div>
            <div v-else class="empty-chart">
              暂无状态数据
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 快速链接 -->
    <el-card shadow="hover" class="quick-links-card">
      <div slot="header">
        <span>快速操作</span>
      </div>
      <el-row :gutter="20">
        <el-col
          v-for="link in quickLinks"
          :key="link.title"
          :span="6"
          class="quick-link-col"
        >
          <div class="quick-link" @click="handleQuickLink(link)">
            <div class="link-icon" :style="{backgroundColor: link.color || '#409EFF'}">
              <i :class="link.icon" />
            </div>
            <p class="link-title">{{ link.title }}</p>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 最近活动 -->
    <el-card shadow="hover" class="activities-card">
      <div slot="header">
        <span>最近活动</span>
      </div>
      <div v-if="recentActivities.length > 0" class="activities-list">
        <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
          <div class="activity-icon">
            <i v-if="activity.type === 'item_added'" class="el-icon-circle-plus" style="color: #67C23A;" />
            <i v-else-if="activity.type === 'item_updated'" class="el-icon-edit" style="color: #409EFF;" />
            <i v-else class="el-icon-shopping-bag-1" style="color: #909399;" />
          </div>
          <div class="activity-content">
            <p class="activity-message">{{ activity.message }}</p>
            <p class="activity-time">{{ activity.time }}</p>
          </div>
        </div>
      </div>
      <div v-else class="empty-activities">
        暂无最近活动
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data() {
    return {
      loading: false,
      statistics: {
        total_items: 0,
        total_categories: 0,
        recent_items: 0,
        expiring_items: 0,
        expired_items: 0
      },
      charts: {
        items_by_category: [],
        items_by_status: []
      },
      quickLinks: [
        { title: '物品管理', path: '/items', icon: 'el-icon-shopping-bag-1', color: '#409EFF' },
        { title: '分类管理', path: '/categories', icon: 'el-icon-folder', color: '#67C23A' },
        { title: '用户管理', path: '/system/user', icon: 'el-icon-user', color: '#E6A23C' },
        { title: '添加物品', path: '/items?action=add', icon: 'el-icon-plus', color: '#F56C6C' }
      ],
      recentActivities: []
    }
  },
  computed: {
    totalItems() {
      return this.statistics.total_items || 1
    }
  },
  created() {
    this.fetchDashboardData()
  },
  methods: {
    // 获取仪表盘数据
    async fetchDashboardData() {
      this.loading = true
      try {
        // 尝试从后端获取数据
        const response = await this.$store.dispatch('dashboard/getDashboardData')
        if (response && response.data) {
          this.setDashboardData(response.data)
        } else {
          // 如果后端没有数据，使用模拟数据
          this.useMockData()
        }
      } catch (error) {
        console.error('获取仪表盘数据失败，使用模拟数据:', error)
        this.useMockData()
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
    },

    // 使用模拟数据
    useMockData() {
      console.log('使用模拟仪表盘数据')
      this.statistics = {
        total_items: 156,
        total_categories: 8,
        recent_items: 12,
        expiring_items: 5,
        expired_items: 3
      }
      this.charts = {
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
      this.recentActivities = [
        {
          id: 1,
          type: 'item_added',
          message: '添加了新物品：笔记本电脑',
          time: '2024-03-14 10:30:00'
        },
        {
          id: 2,
          type: 'item_updated',
          message: '更新了物品：办公椅',
          time: '2024-03-13 15:20:00'
        },
        {
          id: 3,
          type: 'category_added',
          message: '新增分类：电子产品',
          time: '2024-03-12 09:15:00'
        }
      ]
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
      return colors[name] || '#409EFF'
    },

    // 获取状态颜色
    getStatusColor(name) {
      const colors = {
        '正常': '#67C23A',
        '即将过期': '#E6A23C',
        '已过期': '#F56C6C'
      }
      return colors[name] || '#409EFF'
    },

    // 处理快速链接
    handleQuickLink(link) {
      if (link.path) {
        this.$router.push(link.path)
      }
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  background-color: #f0f2f5;
  min-height: calc(100vh - 84px);
}

.dashboard-header {
  margin-bottom: 30px;
}

.dashboard-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
}

.dashboard-header .subtitle {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

/* 统计卡片样式 */
.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  border-radius: 8px;
  border: none;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.stat-content {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.stat-icon i {
  font-size: 24px;
  color: white;
}

.stat-info h3 {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 4px 0;
}

.stat-info p {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

/* 图表区域样式 */
.charts-row {
  margin-bottom: 20px;
}

.chart-card {
  border-radius: 8px;
  border: none;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  height: 300px;
  display: flex;
  flex-direction: column;
}

.chart-card >>> .el-card__header {
  border-bottom: 1px solid #f0f0f0;
  padding: 16px 20px;
}

.chart-card >>> .el-card__body {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.loading-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #909399;
  font-size: 16px;
}

.loading-container i {
  margin-right: 8px;
  font-size: 20px;
}

.chart-container {
  height: 100%;
}

/* 分类项目样式 */
.category-item {
  margin-bottom: 20px;
}

.category-item:last-child {
  margin-bottom: 0;
}

.category-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.category-name {
  font-size: 14px;
  color: #303133;
  font-weight: 500;
}

.category-count {
  font-size: 14px;
  color: #409EFF;
  font-weight: 600;
}

/* 状态项目样式 */
.status-item {
  margin-bottom: 20px;
}

.status-item:last-child {
  margin-bottom: 0;
}

.status-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.status-name {
  font-size: 14px;
  color: #303133;
  font-weight: 500;
}

.status-count {
  font-size: 14px;
  color: #909399;
}

.empty-chart {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #909399;
  font-size: 16px;
}

/* 快速链接样式 */
.quick-links-card {
  border-radius: 8px;
  border: none;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.quick-links-card >>> .el-card__header {
  border-bottom: 1px solid #f0f0f0;
  padding: 16px 20px;
}

.quick-link-col {
  margin-bottom: 20px;
}

.quick-link {
  text-align: center;
  cursor: pointer;
  transition: transform 0.2s;
  padding: 20px 0;
}

.quick-link:hover {
  transform: translateY(-4px);
}

.link-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 12px;
  transition: all 0.3s;
}

.quick-link:hover .link-icon {
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.link-icon i {
  font-size: 28px;
  color: white;
}

.link-title {
  font-size: 16px;
  color: #303133;
  font-weight: 500;
  margin: 0;
}

/* 最近活动样式 */
.activities-card {
  border-radius: 8px;
  border: none;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.activities-card >>> .el-card__header {
  border-bottom: 1px solid #f0f0f0;
  padding: 16px 20px;
}

.activities-list {
  max-height: 300px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background-color: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  flex-shrink: 0;
}

.activity-icon i {
  font-size: 20px;
}

.activity-content {
  flex: 1;
  min-width: 0;
}

.activity-message {
  font-size: 14px;
  color: #303133;
  margin: 0 0 4px 0;
  font-weight: 500;
}

.activity-time {
  font-size: 12px;
  color: #909399;
  margin: 0;
}

.empty-activities {
  text-align: center;
  padding: 40px 0;
  color: #909399;
  font-size: 16px;
}
</style>

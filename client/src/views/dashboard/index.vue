<template>
  <div class="dashboard-container">
    <!-- 顶部卡片统计 -->
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="dashboard-card">
          <p class="card-title">物品总数</p>
          <p class="card-value">{{ overview.total_items }}</p>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="dashboard-card">
          <p class="card-title">临期物品</p>
          <p class="card-value">{{ overview.expiring_items }}</p>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="dashboard-card">
          <p class="card-title">已过期物品</p>
          <p class="card-value">{{ overview.expired_items }}</p>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="dashboard-card">
          <p class="card-title">分类数量</p>
          <p class="card-value">{{ overview.category_count }}</p>
        </el-card>
      </el-col>
    </el-row>

    <!-- 分类占比饼图 -->
    <el-row style="margin-top: 24px;">
      <el-col :span="12">
        <div id="categoryPie" class="chart"></div>
      </el-col>

      <el-col :span="12">
        <div id="expireTrend" class="chart"></div>
      </el-col>
    </el-row>

    <!-- 最近添加物品 -->
    <el-row style="margin-top: 24px;">
      <el-col :span="24">
        <el-card>
          <p class="card-title">最近添加物品</p>
          <el-table :data="recentItems" stripe>
            <el-table-column prop="name" label="名称" />
            <el-table-column prop="category" label="分类" />
            <el-table-column prop="location" label="位置" />
            <el-table-column prop="expire_date" label="保质期" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { getDashboardData } from '@/api/dashboard'

export default {
  data() {
    return {
      overview: {
        total_items: 0,
        expired_items: 0,
        expiring_items: 0,
        category_count: 0
      },
      categoryStats: [],
      expireTrend: [],
      recentItems: []
    }
  },
  mounted() {
    this.fetchDashboard()
  },
  methods: {
    fetchDashboard() {
      getDashboardData().then(res => {
        const data = res.data
        this.overview = {
          total_items: data.total_items,
          expired_items: data.expired_items,
          expiring_items: data.expiring_items,
          category_count: data.category_stats.length
        }
        this.categoryStats = data.category_stats
        this.expireTrend = data.expire_trend
        this.recentItems = data.recent_items

        this.initCategoryPie()
        this.initExpireTrend()
      })
    },
    initCategoryPie() {
      const pieChart = echarts.init(document.getElementById('categoryPie'))
      pieChart.setOption({
        title: { text: '分类占比' },
        tooltip: {},
        series: [
          {
            type: 'pie',
            radius: '50%',
            data: this.categoryStats.map(c => ({
              value: c.value,
              name: c.name
            }))
          }
        ]
      })
    },
    initExpireTrend() {
      const lineChart = echarts.init(document.getElementById('expireTrend'))

      lineChart.setOption({
        title: { text: '过期趋势' },
        tooltip: {},
        xAxis: {
          type: 'category',
          data: this.expireTrend.map(t => t.date)
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: this.expireTrend.map(t => t.count),
            type: 'line'
          }
        ]
      })
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}
.dashboard-card {
  text-align: center;
  font-size: 18px;
}
.card-title {
  font-weight: bold;
  margin-bottom: 8px;
}
.card-value {
  font-size: 28px;
  color: #409eff;
}
.chart {
  width: 100%;
  height: 350px;
}
</style>

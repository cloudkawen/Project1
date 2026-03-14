<template>
  <el-drawer
    title="系统设置"
    :visible.sync="drawerVisible"
    direction="rtl"
    size="300px"
    class="global-setting-drawer"
  >
    <div class="setting-container">
      <!-- 主题设置 -->
      <div class="setting-item">
        <h4>主题设置</h4>
        <el-radio-group v-model="theme" @change="handleThemeChange">
          <el-radio label="light">亮色主题</el-radio>
          <el-radio label="dark">深色主题</el-radio>
        </el-radio-group>
      </div>
      <!-- 布局设置 -->
      <div class="setting-item">
        <h4>布局设置</h4>
        <el-switch
          v-model="fixedHeader"
          active-text="固定头部"
          inactive-text="不固定头部"
          @change="handleFixedHeaderChange"
        />
        <el-switch
          v-model="sidebarLogo"
          active-text="显示Logo"
          inactive-text="隐藏Logo"
          @change="handleSidebarLogoChange"
        />
      </div>
      <!-- 标签页设置 -->
      <div class="setting-item">
        <h4>标签页</h4>
        <el-switch
          v-model="tagsView"
          active-text="显示标签页"
          inactive-text="隐藏标签页"
          @change="handleTagsViewChange"
        />
      </div>
      <!-- 水印设置 -->
      <div class="setting-item">
        <h4>水印设置</h4>
        <el-switch
          v-model="watermark"
          active-text="显示水印"
          inactive-text="隐藏水印"
          @change="handleWatermarkChange"
        />
      </div>
    </div>
  </el-drawer>
</template>

<script>
export default {
  name: 'GlobalSetting',
  data() {
    return {
      drawerVisible: false,
      theme: 'light',
      fixedHeader: true,
      sidebarLogo: true,
      tagsView: true,
      watermark: false
    }
  },
  mounted() {
    this.loadSettings()
  },
  methods: {
    loadSettings() {
      // 从localStorage加载设置
      const settings = JSON.parse(localStorage.getItem('settings') || '{}')
      this.theme = settings.theme || 'light'
      this.fixedHeader = settings.fixedHeader !== undefined ? settings.fixedHeader : true
      this.sidebarLogo = settings.sidebarLogo !== undefined ? settings.sidebarLogo : true
      this.tagsView = settings.tagsView !== undefined ? settings.tagsView : true
      this.watermark = settings.watermark || false
      // 应用设置
      this.applySettings()
    },
    saveSettings() {
      const settings = {
        theme: this.theme,
        fixedHeader: this.fixedHeader,
        sidebarLogo: this.sidebarLogo,
        tagsView: this.tagsView,
        watermark: this.watermark
      }
      localStorage.setItem('settings', JSON.stringify(settings))
    },
    applySettings() {
      // 应用主题
      document.documentElement.setAttribute('data-theme', this.theme)
      // 通知父组件设置变化
      this.$emit('settings-change', {
        theme: this.theme,
        fixedHeader: this.fixedHeader,
        sidebarLogo: this.sidebarLogo,
        tagsView: this.tagsView,
        watermark: this.watermark
      })
    },
    handleThemeChange(val) {
      this.theme = val
      this.saveSettings()
      this.applySettings()
    },
    handleFixedHeaderChange(val) {
      this.fixedHeader = val
      this.saveSettings()
      this.applySettings()
    },
    handleSidebarLogoChange(val) {
      this.sidebarLogo = val
      this.saveSettings()
      this.applySettings()
    },
    handleTagsViewChange(val) {
      this.tagsView = val
      this.saveSettings()
      this.applySettings()
    },
    handleWatermarkChange(val) {
      this.watermark = val
      this.saveSettings()
      this.applySettings()
    },
    // 打开设置面板
    open() {
      this.drawerVisible = true
    },
    // 关闭设置面板
    close() {
      this.drawerVisible = false
    }
  }
}
</script>

<style lang="scss" scoped>
.global-setting-drawer {
  .setting-container {
    padding: 20px;
  }
  .setting-item {
    margin-bottom: 24px;
    h4 {
      margin: 0 0 12px 0;
      font-size: 16px;
      color: #303133;
    }
    .el-switch {
      display: block;
      margin-bottom: 12px;
    }
  }
}
</style>

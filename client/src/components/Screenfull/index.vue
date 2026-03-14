<!-- client/src/components/Screenfull/index.vue -->
<template>
  <div class="screenfull-btn" @click="toggleFullScreen">
    <i
      :class="isFullscreen ? 'el-icon-close' : 'el-icon-full-screen'"
      :title="isFullscreen ? '退出全屏' : '全屏'"
    />
  </div>
</template>

<script>
export default {
  name: 'Screenfull',
  data() {
    return {
      isFullscreen: false
    }
  },
  mounted() {
    this.initFullscreenListener()
  },
  beforeDestroy() {
    this.removeFullscreenListener()
  },
  methods: {
    // 检测是否支持全屏API
    isFullscreenEnabled() {
      return (
        document.fullscreenEnabled ||
        document.webkitFullscreenEnabled ||
        document.mozFullScreenEnabled ||
        document.msFullscreenEnabled
      )
    },
    // 获取全屏元素
    getFullscreenElement() {
      return (
        document.fullscreenElement ||
        document.webkitFullscreenElement ||
        document.mozFullScreenElement ||
        document.msFullscreenElement
      )
    },
    // 切换全屏
    toggleFullScreen() {
      if (!this.isFullscreenEnabled()) {
        this.$message.warning('您的浏览器不支持全屏功能')
        return
      }
      if (!this.getFullscreenElement()) {
        this.enterFullscreen()
      } else {
        this.exitFullscreen()
      }
    },
    // 进入全屏
    enterFullscreen() {
      const el = document.documentElement
      if (el.requestFullscreen) {
        el.requestFullscreen()
      } else if (el.webkitRequestFullscreen) {
        el.webkitRequestFullscreen()
      } else if (el.mozRequestFullScreen) {
        el.mozRequestFullScreen()
      } else if (el.msRequestFullscreen) {
        el.msRequestFullscreen()
      }
    },
    // 退出全屏
    exitFullscreen() {
      if (document.exitFullscreen) {
        document.exitFullscreen()
      } else if (document.webkitExitFullscreen) {
        document.webkitExitFullscreen()
      } else if (document.mozCancelFullScreen) {
        document.mozCancelFullScreen()
      } else if (document.msExitFullscreen) {
        document.msExitFullscreen()
      }
    },
    // 更新全屏状态
    updateFullscreenStatus() {
      this.isFullscreen = !!this.getFullscreenElement()
    },
    // 初始化全屏监听
    initFullscreenListener() {
      const events = [
        'fullscreenchange',
        'webkitfullscreenchange',
        'mozfullscreenchange',
        'MSFullscreenChange'
      ]
      events.forEach(event => {
        document.addEventListener(event, this.updateFullscreenStatus)
      })
    },
    // 移除全屏监听
    removeFullscreenListener() {
      const events = [
        'fullscreenchange',
        'webkitfullscreenchange',
        'mozfullscreenchange',
        'MSFullscreenChange'
      ]
      events.forEach(event => {
        document.removeEventListener(event, this.updateFullscreenStatus)
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.screenfull-btn {
  display: inline-block;
  cursor: pointer;
  transition: all 0.3s;
  padding: 0 4px;
  font-size: 18px;
  color: #5a5e66;
  &:hover {
    color: #409eff;
  }
}
</style>

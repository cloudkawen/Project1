<template>
  <div :class="classObj" class="app-wrapper">
    <!-- 移动端遮罩层 -->
    <div v-if="device==='mobile'&&sidebar.opened" class="drawer-bg" @click="handleClickOutside" />
    <!-- 侧边栏组件 -->
    <sidebar
      class="sidebar-container"
      :is-collapse="!sidebar.opened"
      @toggle-collapse="toggleSideBar"
    />
    <!-- 主内容区域 -->
    <div :class="{'main-container': true, 'main-container-collapse': !sidebar.opened}">
      <!-- 固定顶部导航栏 -->
      <div :class="{'fixed-header': fixedHeader}">
        <navbar />
      </div>
      <!-- 主内容区 -->
      <app-main />
    </div>
  </div>
</template>

<script>
import { Navbar, Sidebar, AppMain } from './components'
import ResizeMixin from './mixin/ResizeHandler'

export default {
  name: 'Layout',
  components: {
    Navbar,
    Sidebar,
    AppMain
  },
  mixins: [ResizeMixin],
  computed: {
    sidebar() {
      return this.$store.state.app.sidebar
    },
    device() {
      return this.$store.state.app.device
    },
    fixedHeader() {
      return this.$store.state.settings.fixedHeader || true
    },
    classObj() {
      return {
        hideSidebar: !this.sidebar.opened,
        openSidebar: this.sidebar.opened,
        withoutAnimation: this.sidebar.withoutAnimation,
        mobile: this.device === 'mobile'
      }
    }
  },
  methods: {
    handleClickOutside() {
      this.$store.dispatch('app/closeSideBar', { withoutAnimation: false })
    },
    toggleSideBar() {
      this.$store.dispatch('app/toggleSideBar')
    }
  }
}
</script>

<style lang="scss" scoped>
// 使用传统的 @import 语法，避免命名空间问题
@import "~@/styles/variables.scss";

.app-wrapper {
  // 直接使用 CSS 而不是 SCSS mixin
  &:after {
    content: "";
    display: table;
    clear: both;
  }
  position: relative;
  height: 100vh;
  width: 100%;
  overflow: hidden;
  background: $bgColor;
  
  &[data-theme="dark"] {
    background: #1a1a1a;
  }
  
  &.mobile.openSidebar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
  }
}

// 移动端遮罩层
.drawer-bg {
  background: rgba(0, 0, 0, 0.3);
  opacity: 1;
  width: 100%;
  top: 0;
  left: 0;
  height: 100%;
  position: fixed;
  z-index: 1000;
  transition: opacity 0.3s;
  backdrop-filter: blur(2px);
}

// 侧边栏容器
.sidebar-container {
  transition: width 0.3s, transform 0.3s;
  width: $sidebarWidth !important;
  background-color: $menuBg;
  height: 100vh;
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  z-index: 1001;
  overflow: hidden;
  -webkit-transform: translateZ(0);
  box-shadow: 2px 0 6px rgba(0, 21, 41, 0.35);
  
  // 隐藏滚动条
  &::-webkit-scrollbar {
    width: 0;
  }
  
  // 深色主题
  [data-theme="dark"] & {
    background-color: #001529;
    box-shadow: 2px 0 6px rgba(0, 0, 0, 0.5);
  }
}

// 主内容区域
.main-container {
  min-height: 100vh;
  transition: margin-left 0.3s;
  margin-left: $sidebarWidth;
  position: relative;
  background: $bgColor;
  overflow: hidden;
  
  &[data-theme="dark"] {
    background: #141414;
  }
  
  // 移动端适配
  @media screen and (max-width: 768px) {
    margin-left: 0;
  }
}

// 侧边栏折叠时的主内容区域
.main-container-collapse {
  margin-left: $sidebarCollapseWidth;
  
  @media screen and (max-width: 768px) {
    margin-left: 0;
  }
}

// 固定头部
.fixed-header {
  position: fixed;
  top: 0;
  right: 0;
  z-index: 9;
  width: calc(100% - #{$sidebarWidth});
  transition: width 0.3s;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  background: $navBarBg;
  
  [data-theme="dark"] & {
    background: #1f1f1f;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
  }
  
  // 侧边栏折叠时的宽度
  .hideSidebar & {
    width: calc(100% - #{$sidebarCollapseWidth});
  }
  
  // 移动端适配
  .mobile & {
    width: 100%;
  }
  
  @media screen and (max-width: 768px) {
    width: 100% !important;
  }
}

// 隐藏侧边栏时的样式
.hideSidebar {
  .sidebar-container {
    width: $sidebarCollapseWidth !important;
  }
  
  .main-container {
    margin-left: $sidebarCollapseWidth;
  }
  
  .fixed-header {
    width: calc(100% - #{$sidebarCollapseWidth});
  }
}

// 移动端样式
.mobile {
  .sidebar-container {
    transition: transform 0.3s;
    width: $sidebarWidth !important;
  }
  
  &.openSidebar {
    .sidebar-container {
      transform: translate3d(0, 0, 0);
    }
    
    .main-container {
      margin-left: 0;
    }
  }
  
  &.hideSidebar {
    .sidebar-container {
      pointer-events: none;
      transform: translate3d(-$sidebarWidth, 0, 0);
    }
    
    .main-container {
      margin-left: 0;
    }
  }
  
  .fixed-header {
    width: 100%;
  }
}

// 无动画状态
.withoutAnimation {
  .main-container,
  .sidebar-container {
    transition: none;
  }
}

// 响应式适配
@media screen and (max-width: 768px) {
  .main-container {
    margin-left: 0;
  }
  
  .fixed-header {
    width: 100%;
  }
  .sidebar-container {
    transform: translate3d(-100%, 0, 0);
  }
  .openSidebar .sidebar-container {
    transform: translate3d(0, 0, 0);
  }
}
</style>

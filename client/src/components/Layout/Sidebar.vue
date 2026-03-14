<template>
  <el-aside
    :width="sidebarWidth"
    class="sidebar-container"
    :class="{ 'is-collapse': isCollapse }"
  >
    <!-- 折叠按钮 -->
    <div class="collapse-btn" @click="toggleCollapse">
      <i :class="collapseIcon" />
    </div>

    <!-- Logo区域 -->
    <div class="logo-container" :style="{ width: isCollapse ? '64px' : '200px' }">
      <div class="logo">
        <i class="el-icon-s-management logo-icon" />
        <transition name="logo-fade">
          <span v-if="!isCollapse" class="logo-title">物品管理系统</span>
        </transition>
      </div>
    </div>

    <!-- 菜单搜索（折叠时不显示） -->
    <transition name="search-fade">
      <div v-if="!isCollapse" class="menu-search">
        <el-input
          v-model="searchQuery"
          placeholder="搜索菜单"
          clearable
          size="small"
          prefix-icon="el-icon-search"
          @input="handleSearch"
        />
      </div>
    </transition>

    <!-- 菜单区域 -->
    <div class="menu-container">
      <el-scrollbar wrap-class="scrollbar-wrapper">
        <el-menu
          :default-active="activeMenu"
          :collapse="isCollapse"
          :collapse-transition="false"
          :unique-opened="true"
          :background-color="variables.menuBg"
          :text-color="variables.menuText"
          :active-text-color="variables.menuActiveText"
          mode="vertical"
        >
          <!-- 渲染菜单项 -->
          <sidebar-item
            v-for="route in filteredRoutes"
            :key="route.path"
            :item="route"
            :base-path="route.path"
            :is-collapse="isCollapse"
          />
        </el-menu>
      </el-scrollbar>
    </div>

    <!-- 侧边栏底部 -->
    <div class="sidebar-footer">
      <!-- 用户信息（折叠时不显示） -->
      <transition name="user-fade">
        <div v-if="!isCollapse" class="user-info">
          <el-avatar :size="36" :src="userAvatar" class="user-avatar">
            <i class="el-icon-user-solid" />
          </el-avatar>
          <div class="user-details">
            <div class="user-name">{{ userName }}</div>
            <div class="user-role">{{ userRole }}</div>
          </div>
        </div>
      </transition>
      <!-- 系统信息 -->
      <div class="system-info">
        <el-tooltip
          v-if="!isCollapse"
          :content="systemTime"
          placement="top"
        >
          <i class="el-icon-time" />
        </el-tooltip>
        <el-tooltip
          :content="`版本: ${version}`"
          placement="top"
        >
          <i class="el-icon-info" />
        </el-tooltip>
      </div>
    </div>
  </el-aside>
</template>

<script>
import SidebarItem from './SidebarItem'
import variables from '@/styles/variables.scss'
import { mapGetters } from 'vuex'

export default {
  name: 'Sidebar',
  components: { SidebarItem },
  props: {
    isCollapse: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      searchQuery: '',
      version: '1.0.0',
      systemTime: '',
      userAvatar: '',
      userName: '管理员',
      userRole: '系统管理员'
    }
  },
  computed: {
    ...mapGetters(['permission_routes']),
    // 侧边栏宽度
    sidebarWidth() {
      return this.isCollapse ? '64px' : '200px'
    },
    // 折叠图标
    collapseIcon() {
      return this.isCollapse ? 'el-icon-s-unfold' : 'el-icon-s-fold'
    },
    // 激活的菜单
    activeMenu() {
      const route = this.$route
      const { meta, path } = route
      if (meta.activeMenu) {
        return meta.activeMenu
      }
      return path
    },
    // 过滤后的路由（支持搜索）
    filteredRoutes() {
      if (!this.searchQuery) {
        return this.permission_routes
      }
      const query = this.searchQuery.toLowerCase()
      return this.permission_routes.filter(route => {
        // 检查主路由
        if (route.meta && route.meta.title.toLowerCase().includes(query)) {
          return true
        }
        // 检查子路由
        if (route.children) {
          return route.children.some(child =>
            child.meta &&
            child.meta.title.toLowerCase().includes(query)
          )
        }
        return false
      })
    },
    // SCSS变量
    variables() {
      return variables
    }
  },
  created() {
    this.updateSystemTime()
    this.fetchUserInfo()
    // 每分钟更新一次系统时间
    this.timeInterval = setInterval(() => {
      this.updateSystemTime()
    }, 60000)
  },
  beforeDestroy() {
    if (this.timeInterval) {
      clearInterval(this.timeInterval)
    }
  },
  methods: {
    // 切换折叠状态
    toggleCollapse() {
      this.$emit('toggle-collapse')
    },
    // 菜单搜索
    handleSearch() {
      // 搜索逻辑已由计算属性处理
    },
    // 更新系统时间
    updateSystemTime() {
      const now = new Date()
      this.systemTime = now.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      })
    },
    // 获取用户信息
    fetchUserInfo() {
      const userInfo = this.$store.getters.userInfo ||
                     JSON.parse(localStorage.getItem('userInfo')) ||
                     JSON.parse(sessionStorage.getItem('userInfo'))
      if (userInfo) {
        this.userName = userInfo.username || userInfo.name || '用户'
        this.userRole = userInfo.role || '普通用户'
        this.userAvatar = userInfo.avatar || ''
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.sidebar-container {
  position: relative;
  background-color: $menuBg;
  height: 100vh;
  transition: width 0.3s;
  box-shadow: 2px 0 6px rgba(0, 21, 41, 0.35);
  z-index: 1001;
  &.is-collapse {
    .logo-title,
    .menu-search,
    .user-details,
    .system-info i:first-child {
      display: none;
    }
  }
}

.collapse-btn {
  position: absolute;
  right: 0;
  top: 20px;
  z-index: 1002;
  width: 20px;
  height: 20px;
  background-color: $menuBg;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transform: translateX(50%);
  color: $menuText;
  transition: all 0.3s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  &:hover {
    color: $menuActiveText;
    transform: translateX(50%) scale(1.1);
  }
  i {
    font-size: 12px;
  }
}

.logo-container {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: width 0.3s;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 20px;
  width: 100%;
  height: 100%;
  text-decoration: none;
  color: $menuActiveText;
  .logo-icon {
    font-size: 24px;
    min-width: 24px;
  }
  .logo-title {
    font-size: 18px;
    font-weight: bold;
    margin-left: 12px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}

.logo-fade-enter-active,
.logo-fade-leave-active {
  transition: opacity 0.3s;
}

.logo-fade-enter,
.logo-fade-leave-to {
  opacity: 0;
}

.menu-search {
  padding: 15px 20px 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  ::v-deep .el-input__inner {
    background-color: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: $menuText;
    &::placeholder {
      color: rgba(255, 255, 255, 0.5);
    }
    &:focus {
      background-color: rgba(255, 255, 255, 0.15);
      border-color: $menuActiveText;
    }
  }
  ::v-deep .el-input__prefix {
    color: rgba(255, 255, 255, 0.5);
  }
  ::v-deep .el-input__suffix {
    .el-input__icon {
      color: rgba(255, 255, 255, 0.5);
    }
  }
}

.search-fade-enter-active,
.search-fade-leave-active {
  transition: all 0.3s;
}

.search-fade-enter,
.search-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.menu-container {
  height: calc(100vh - 180px);
  overflow: hidden;
  ::v-deep .scrollbar-wrapper {
    overflow-x: hidden !important;
    .el-scrollbar__view {
      height: 100%;
    }
  }
  ::v-deep .el-menu {
    border-right: none;
  }
}

.sidebar-footer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  background-color: rgba(0, 0, 0, 0.1);
  padding: 15px 20px;
  transition: all 0.3s;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  .user-avatar {
    flex-shrink: 0;
    margin-right: 12px;
    background-color: $menuActiveText;
  }
  .user-details {
    flex: 1;
    overflow: hidden;
    .user-name {
      color: $menuText;
      font-weight: 500;
      font-size: 14px;
      margin-bottom: 4px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .user-role {
      color: rgba(255, 255, 255, 0.7);
      font-size: 12px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  }
}

.user-fade-enter-active,
.user-fade-leave-active {
  transition: all 0.3s;
}

.user-fade-enter,
.user-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.system-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
  i {
    font-size: 16px;
    cursor: pointer;
    transition: color 0.3s;
    &:hover {
      color: $menuActiveText;
    }
  }
}
</style>

<style lang="scss">
// 全局SCSS变量
$menuBg: #304156;
$menuText: #bfcbd9;
$menuActiveText: #409eff;
</style>

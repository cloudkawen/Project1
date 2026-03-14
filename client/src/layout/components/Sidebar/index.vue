<template>
  <div :class="{'has-logo':showLogo}" class="sidebar-wrapper">
    <!-- Logo区域 -->
    <logo v-if="showLogo" :collapse="isCollapse" />
    <!-- 搜索区域（仅展开时显示） -->
    <transition name="search-fade">
      <div v-if="!isCollapse" class="menu-search-container">
        <el-input
          v-model="searchQuery"
          placeholder="搜索菜单"
          size="small"
          clearable
          @clear="handleSearchClear"
          @input="handleSearch"
        >
          <i slot="prefix" class="el-icon-search" />
        </el-input>
      </div>
    </transition>
    <!-- 侧边栏菜单 -->
    <el-scrollbar wrap-class="scrollbar-wrapper" class="sidebar-scrollbar">
      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse"
        :background-color="variables.menuBg"
        :text-color="variables.menuText"
        :unique-opened="false"
        :active-text-color="variables.menuActiveText"
        :collapse-transition="false"
        mode="vertical"
        class="sidebar-menu"
      >
        <sidebar-item
          v-for="route in filteredRoutes"
          :key="route.path"
          :item="route"
          :base-path="route.path"
          :search-query="searchQuery"
        />
      </el-menu>
    </el-scrollbar>
    <!-- 侧边栏底部 -->
    <div class="sidebar-footer">
      <!-- 用户信息（仅展开时显示） -->
      <transition name="user-fade">
        <div v-if="!isCollapse && showUserInfo" class="user-info">
          <el-avatar :size="36" :src="userAvatar" class="user-avatar">
            <i class="el-icon-user-solid" />
          </el-avatar>
          <div class="user-details">
            <div class="user-name">{{ userName }}</div>
            <div class="user-role">{{ userRole }}</div>
          </div>
        </div>
      </transition>
      <!-- 系统信息和操作 -->
      <div class="system-info">
        <!-- 系统时间 -->
        <el-tooltip
          v-if="!isCollapse"
          :content="systemTime"
          placement="top"
          class="time-tooltip"
        >
          <i class="el-icon-time time-icon" />
        </el-tooltip>
        <!-- 折叠按钮 -->
        <div class="collapse-btn" @click="toggleCollapse">
          <i :class="collapseIcon" class="collapse-icon" />
        </div>
        <!-- 系统设置 -->
        <el-tooltip
          v-if="!isCollapse"
          content="系统设置"
          placement="top"
        >
          <i class="el-icon-setting setting-icon" @click="openSettings" />
        </el-tooltip>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Logo from './Logo'
import SidebarItem from './SidebarItem'
import variables from '@/styles/variables.scss'

export default {
  name: 'Sidebar',
  components: {
    SidebarItem,
    Logo
  },
  data() {
    return {
      searchQuery: '',
      systemTime: '',
      showUserInfo: true,
      userAvatar: '',
      userName: '管理员',
      userRole: '系统管理员',
      version: '1.0.0'
    }
  },
  computed: {
    ...mapGetters([
      'permission_routes',
      'sidebar',
      'avatar',
      'name',
      'roles'
    ]),
    activeMenu() {
      const route = this.$route
      const { meta, path } = route
      // 如果设置了activeMenu，侧边栏将高亮显示您设置的路径
      if (meta.activeMenu) {
        return meta.activeMenu
      }
      return path
    },
    showLogo() {
      return this.$store.state.settings.sidebarLogo
    },
    variables() {
      return variables
    },
    isCollapse() {
      return !this.sidebar.opened
    },
    // 折叠按钮图标
    collapseIcon() {
      return this.isCollapse ? 'el-icon-s-unfold' : 'el-icon-s-fold'
    },
    // 过滤后的路由（支持搜索）
    filteredRoutes() {
      if (!this.searchQuery.trim()) {
        return this.permission_routes
      }
      const query = this.searchQuery.toLowerCase()
      return this.permission_routes.filter(route => {
        // 跳过隐藏的路由
        if (route.hidden) return false
        // 检查主路由标题
        if (route.meta && route.meta.title && route.meta.title.toLowerCase().includes(query)) {
          return true
        }
        // 检查子路由
        if (route.children) {
          return route.children.some(child =>
            !child.hidden &&
            child.meta &&
            child.meta.title &&
            child.meta.title.toLowerCase().includes(query)
          )
        }
        return false
      })
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
        this.userRole = userInfo.role || (this.roles && this.roles.length > 0 ? this.roles[0] : '普通用户')
        this.userAvatar = userInfo.avatar || this.avatar || ''
      }
    },
    // 切换侧边栏折叠状态
    toggleCollapse() {
      this.$store.dispatch('app/toggleSideBar')
    },
    // 处理搜索
    handleSearch() {
      // 搜索逻辑在计算属性filteredRoutes中处理
    },
    // 清除搜索
    handleSearchClear() {
      this.searchQuery = ''
    },
    // 打开系统设置
    openSettings() {
      this.$emit('open-settings')
    }
  }
}
</script>

<style lang="scss" scoped>
.sidebar-wrapper {
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  background-color: var(--menuBg, #304156);
  transition: all 0.3s;
}

// 搜索区域
.menu-search-container {
  padding: 12px 15px 8px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  ::v-deep .el-input__inner {
    background-color: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: var(--menuText, #bfcbd9);
    height: 32px;
    line-height: 32px;
    &::placeholder {
      color: rgba(255, 255, 255, 0.5);
    }
    &:focus {
      background-color: rgba(255, 255, 255, 0.15);
      border-color: var(--menuActiveText, #409eff);
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

// 菜单滚动区域
.sidebar-scrollbar {
  flex: 1;
  overflow: hidden;
  ::v-deep .scrollbar-wrapper {
    overflow-x: hidden !important;
  }
  ::v-deep .el-scrollbar__view {
    height: 100%;
  }
}

// 侧边栏菜单
.sidebar-menu {
  border-right: none;
  height: 100%;
  &:not(.el-menu--collapse) {
    width: 100%;
  }
}

// 侧边栏底部
.sidebar-footer {
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  background-color: rgba(0, 0, 0, 0.1);
  padding: 12px 15px;
  min-height: 60px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

// 用户信息
.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  .user-avatar {
    flex-shrink: 0;
    margin-right: 10px;
    background-color: var(--menuActiveText, #409eff);
  }
  .user-details {
    flex: 1;
    overflow: hidden;
    .user-name {
      color: var(--menuText, #bfcbd9);
      font-weight: 500;
      font-size: 13px;
      margin-bottom: 2px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .user-role {
      color: rgba(255, 255, 255, 0.7);
      font-size: 11px;
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

// 系统信息
.system-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
  .time-tooltip {
    cursor: default;
    .time-icon {
      font-size: 16px;
    }
  }
  .collapse-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border-radius: 4px;
    background-color: rgba(255, 255, 255, 0.1);
    cursor: pointer;
    transition: all 0.3s;
    &:hover {
      background-color: rgba(255, 255, 255, 0.2);
    }
    .collapse-icon {
      font-size: 16px;
      color: var(--menuText, #bfcbd9);
    }
  }
  .setting-icon {
    font-size: 16px;
    cursor: pointer;
    transition: color 0.3s;
    &:hover {
      color: var(--menuActiveText, #409eff);
    }
  }
}

// 响应式适配
@media screen and (max-width: 768px) {
  .menu-search-container {
    padding: 8px 10px 6px;
  }
  .sidebar-footer {
    padding: 8px 10px;
  }
}
</style>

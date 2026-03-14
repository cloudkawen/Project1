<template>
  <!-- 单个菜单项 -->
  <div>
    <template v-if="!item.hidden">
      <!-- 没有子菜单的菜单项 -->
      <template v-if="hasOneShowingChild(item.children, item) && (!onlyOneChild.children || onlyOneChild.noShowingChildren) && !item.alwaysShow">
        <el-menu-item
          :index="resolvePath(onlyOneChild.path)"
          :class="{'submenu-title-noDropdown': !isCollapse}"
          @click="handleClick(onlyOneChild)"
        >
          <item
            v-if="onlyOneChild.meta"
            :icon="onlyOneChild.meta.icon || (item.meta && item.meta.icon)"
            :title="onlyOneChild.meta.title"
            :badge="onlyOneChild.meta.badge"
            :badge-type="onlyOneChild.meta.badgeType"
          />
        </el-menu-item>
      </template>

      <!-- 有子菜单的菜单项 -->
      <el-submenu
        v-else
        :index="resolvePath(item.path)"
        popper-append-to-body
      >
        <template slot="title">
          <item
            v-if="item.meta"
            :icon="item.meta.icon"
            :title="item.meta.title"
            :badge="item.meta.badge"
            :badge-type="item.meta.badgeType"
          />
        </template>
        <!-- 递归渲染子菜单 -->
        <template v-for="child in item.children">
          <sidebar-item
            v-if="!child.hidden"
            :key="child.path"
            :item="child"
            :base-path="resolvePath(child.path)"
            :search-query="searchQuery"
          />
        </template>
      </el-submenu>
    </template>
  </div>
</template>

<script>
import path from 'path'
import Item from './Item'

export default {
  name: 'SidebarItem',
  components: { Item },
  props: {
    item: {
      type: Object,
      required: true
    },
    basePath: {
      type: String,
      default: ''
    },
    searchQuery: {
      type: String,
      default: ''
    }
  },
  data() {
    this.onlyOneChild = null
    return {}
  },
  computed: {
    isCollapse() {
      return this.$store.state.app.sidebar.opened
    }
  },
  methods: {
    // 检查是否只有一个显示的子菜单
    hasOneShowingChild(children = [], parent) {
      const showingChildren = children.filter(item => {
        if (item.hidden) {
          return false
        } else {
          this.onlyOneChild = item
          return true
        }
      })

      if (showingChildren.length === 1) {
        return true
      }

      if (showingChildren.length === 0) {
        this.onlyOneChild = { ...parent, path: '', noShowingChildren: true }
        return true
      }

      return false
    },
    // 解析路径
    resolvePath(routePath) {
      if (this.isExternal(routePath)) {
        return routePath
      }
      if (this.isExternal(this.basePath)) {
        return this.basePath
      }
      return path.resolve(this.basePath, routePath)
    },
    // 判断是否为外部链接
    isExternal(path) {
      return /^(https?:|mailto:|tel:)/.test(path)
    },
    // 处理点击事件
    handleClick(item) {
      if (this.isExternal(item.path)) {
        window.open(item.path, '_blank')
      } else {
        this.$router.push(this.resolvePath(item.path))
      }
    }
  }
}
</script>

<style lang="scss" scoped>
// 菜单项样式
::v-deep .el-menu-item,
::v-deep .el-submenu__title {
  position: relative;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: background-color 0.3s;
  &:hover {
    background-color: rgba(0, 0, 0, 0.1) !important;
  }
}

// 激活状态
::v-deep .el-menu-item.is-active {
  background-color: var(--menuActiveText, #409eff) !important;
  color: #fff !important;
}
</style>

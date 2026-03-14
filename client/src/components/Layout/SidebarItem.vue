<template>
  <!-- 没有子路由的菜单项 -->
  <div>
    <template v-if="!item.children || item.children.length === 0">
      <el-menu-item
        v-if="!item.meta.hidden"
        :index="resolvePath(item.path)"
        :class="{ 'submenu-title-noDropdown': !isCollapse }"
      >
        <i v-if="item.meta.icon" :class="item.meta.icon" />
        <span v-if="!isCollapse" slot="title">{{ item.meta.title }}</span>
        <!-- 徽标显示 -->
        <el-badge
          v-if="item.meta.badge && !isCollapse"
          :value="item.meta.badge"
          :max="99"
          :type="item.meta.badgeType || 'primary'"
          class="menu-badge"
        />
      </el-menu-item>
    </template>

    <!-- 有子路由的菜单项 -->
    <el-submenu
      v-else
      :index="resolvePath(item.path)"
      popper-append-to-body
    >
      <template slot="title">
        <i v-if="item.meta.icon" :class="item.meta.icon" />
        <span v-if="!isCollapse" slot="title">{{ item.meta.title }}</span>
        <!-- 徽标显示 -->
        <el-badge
          v-if="item.meta.badge && !isCollapse"
          :value="item.meta.badge"
          :max="99"
          :type="item.meta.badgeType || 'primary'"
          class="menu-badge"
        />
      </template>
      <!-- 递归渲染子菜单 -->
      <template v-for="child in item.children">
        <sidebar-item
          v-if="!child.meta.hidden"
          :key="child.path"
          :item="child"
          :base-path="resolvePath(child.path)"
          :is-collapse="isCollapse"
        />
      </template>
    </el-submenu>
  </div>
</template>

<script>
import path from 'path'

export default {
  name: 'SidebarItem',
  props: {
    item: {
      type: Object,
      required: true
    },
    basePath: {
      type: String,
      default: ''
    },
    isCollapse: {
      type: Boolean,
      default: false
    }
  },
  methods: {
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
    }
  }
}
</script>

<style lang="scss" scoped>
// 菜单项样式
::v-deep .el-menu-item,
::v-deep .el-submenu__title {
  height: 50px;
  line-height: 50px;
  position: relative;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: background-color 0.3s;
  &:hover {
    background-color: rgba(0, 0, 0, 0.1) !important;
  }
  i {
    width: 24px;
    font-size: 18px;
    text-align: center;
    margin-right: 8px;
    vertical-align: middle;
  }
  span {
    vertical-align: middle;
  }
}

// 激活状态
::v-deep .el-menu-item.is-active {
  background-color: $menuActiveText !important;
  color: #fff !important;
  i {
    color: #fff;
  }
}

// 折叠时的菜单项
::v-deep .submenu-title-noDropdown {
  &.is-active {
    background-color: $menuActiveText !important;
    color: #fff !important;
  }
}

// 徽标样式
.menu-badge {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
}
</style>

<!-- client/src/layout/components/Navbar.vue -->
<template>
  <div class="navbar">
    <div class="hamburger-container" @click="toggleSideBar">
      <i :class="hamburgerIcon" class="hamburger" />
    </div>

    <div class="breadcrumb-container">
      <span class="page-title">{{ pageTitle }}</span>
    </div>

    <div class="right-menu">
      <div class="right-menu-item">
        <i class="el-icon-user" />
        <span class="user-name">{{ name }}</span>
      </div>
      <el-dropdown class="avatar-container" trigger="click">
        <div class="avatar-wrapper">
          <img :src="avatar" class="user-avatar">
          <i class="el-icon-caret-bottom" />
        </div>
        <el-dropdown-menu slot="dropdown" class="user-dropdown">
          <router-link to="/profile">
            <el-dropdown-item>
              <i class="el-icon-user-solid" />个人中心
            </el-dropdown-item>
          </router-link>
          <router-link to="/changepassword">
            <el-dropdown-item divided>
              <i class="el-icon-edit" />修改密码
            </el-dropdown-item>
          </router-link>
          <el-dropdown-item divided @click.native="logout">
            <i class="el-icon-switch-button" />
            <span style="display:block;">退出登录</span>
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Navbar',
  computed: {
    ...mapGetters([
      'sidebar',
      'avatar',
      'name'
    ]),
    hamburgerIcon() {
      return this.sidebar.opened ? 'el-icon-s-fold' : 'el-icon-s-unfold'
    },
    pageTitle() {
      return (this.$route.meta && this.$route.meta.title) || '物品管理系统'
    }
  },
  methods: {
    toggleSideBar() {
      this.$store.dispatch('app/toggleSideBar')
    },
    async logout() {
      await this.$store.dispatch('user/logout')
      this.$router.push(`/login?redirect=${this.$route.fullPath}`)
    }
  }
}
</script>

<style lang="scss" scoped>
.navbar {
  height: 50px;
  overflow: hidden;
  position: relative;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
  display: flex;
  align-items: center;
  padding: 0 20px;

  .hamburger-container {
    line-height: 46px;
    height: 100%;
    cursor: pointer;
    transition: background .3s;
    -webkit-tap-highlight-color: transparent;
    display: flex;
    align-items: center;
    margin-right: 12px;

    &:hover {
      background: rgba(0, 0, 0, .025)
    }

    .hamburger {
      font-size: 20px;
      color: #5a5e66;
      vertical-align: middle;
    }
  }

  .breadcrumb-container {
    flex: 1;
    height: 100%;
    display: flex;
    align-items: center;
    .page-title {
      font-size: 18px;
      font-weight: bold;
      color: #303133;
    }
  }

  .right-menu {
    display: flex;
    align-items: center;
    height: 100%;
    margin-left: auto;

    .right-menu-item {
      display: flex;
      align-items: center;
      padding: 0 12px;
      height: 100%;
      font-size: 14px;
      color: #5a5e66;
      vertical-align: text-bottom;
      i {
        margin-right: 8px;
        font-size: 16px;
      }
      .user-name {
        max-width: 120px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
    }

    .avatar-container {
      .avatar-wrapper {
        display: flex;
        align-items: center;
        position: relative;
        cursor: pointer;
        padding: 4px;
        border-radius: 4px;
        transition: background .3s;

        &:hover {
          background: rgba(0, 0, 0, .025)
        }

        .user-avatar {
          cursor: pointer;
          width: 40px;
          height: 40px;
          border-radius: 10px;
        }

        .el-icon-caret-bottom {
          cursor: pointer;
          position: absolute;
          right: -20px;
          top: 25px;
          font-size: 12px;
          color: #909399;
        }
      }
    }
  }
}
</style>

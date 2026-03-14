<template>
  <section class="app-main">
    <transition name="fade-transform" mode="out-in">
      <!-- 暂时移除 keep-alive 的 include 属性 -->
      <router-view :key="key" />
    </transition>
    <!-- 回到顶部按钮 -->
    <el-backtop
      target=".app-main"
      :bottom="60"
      :right="40"
      :visibility-height="300"
    >
      <div class="back-top">
        <i class="el-icon-caret-top" />
      </div>
    </el-backtop>
  </section>
</template>

<script>
export default {
  name: 'AppMain',
  computed: {
    // 暂时注释掉 cachedViews
    // cachedViews() {
    //   return this.$store.state.tagsView.cachedViews
    // },
    key() {
      return this.$route.path
    }
  }
}
</script>

<style lang="scss" scoped>
// 使用媒体查询替代 mixin
.app-main {
  min-height: calc(100vh - 50px);
  width: 100%;
  position: relative;
  overflow: auto;
  padding: 20px;
  margin-top: 50px;
  background-color: #f0f2f5;
  &.fixed-header {
    padding-top: 50px;
  }
  // 使用直接媒体查询而不是 mixin
  @media screen and (max-width: 768px) {
    padding: 10px;
  }
}

// 页面切换动画
.fade-transform-leave-active,
.fade-transform-enter-active {
  transition: all 0.3s;
}

.fade-transform-enter {
  opacity: 0;
  transform: translateX(-30px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

// 回到顶部按钮
.back-top {
  height: 40px;
  width: 40px;
  border-radius: 50%;
  background-color: #409EFF;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s;
  &:hover {
    background-color: #66b1ff;
    transform: translateY(-2px);
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.2);
  }
  &:active {
    transform: translateY(0);
  }
}
</style>

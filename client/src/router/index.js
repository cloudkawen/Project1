import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: {
        title: '数据总览',
        icon: 'el-icon-data-line',
        affix: true
      }
    }]
  },
  {
    path: '/changepassword',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '',
        name: 'ChangePassword', // 修复：将name移到子路由
        component: () => import('@/views/system/changepassword'),
        meta: {
          title: '修改密码',
          icon: 'el-icon-edit'
        }
      }
    ]
  }
]

export const asyncRoutes = [
  // 物品管理模块
  {
    path: '/items',
    component: Layout,
    redirect: '/items/index',
    name: 'Items',
    meta: {
      title: '物品管理',
      icon: 'el-icon-shopping-bag-1',
      perms: ['items:view']
    },
    children: [
      {
        path: 'index',
        name: 'ItemsList',
        component: () => import('@/views/items/index'),
        meta: {
          title: '物品列表',
          icon: 'el-icon-list',
          perms: ['items:view']
        }
      }
    ]
  },
  {
    path: '/categories',
    component: Layout,
    redirect: '/categories/index',
    name: 'Categories',
    meta: {
      title: '分类管理',
      icon: 'el-icon-folder',
      perms: ['categories:view']
    },
    children: [
      {
        path: 'index',
        name: 'CategoriesList',
        component: () => import('@/views/categories/index'),
        meta: {
          title: '分类列表',
          icon: 'el-icon-list',
          perms: ['categories:view']
        }
      }
    ]
  },
  // 系统管理模块
  {
    path: '/system',
    component: Layout,
    redirect: '/system/user',
    name: 'System',
    meta: {
      title: '系统管理',
      icon: 'el-icon-setting',
      perms: ['system:manage']
    },
    children: [
      {
        path: 'user',
        name: 'User',
        component: () => import('@/views/system/user.vue'),
        meta: {
          title: '用户管理',
          icon: 'el-icon-user',
          perms: ['user:manage']
        }
      },
      {
        path: 'dict',
        name: 'Dict',
        component: () => import('@/views/system/dict'),
        meta: {
          title: '数据字典',
          icon: 'el-icon-collection',
          perms: ['dict:manage']
        }
      }
    ]
  },
  // 个人中心
  {
    path: '/profile',
    component: Layout,
    redirect: '/profile/index',
    meta: {
      title: '个人中心',
      icon: 'el-icon-user',
      hidden: true
    },
    children: [
      {
        path: 'index',
        name: 'ProfileIndex',
        component: () => import('@/views/profile/index'),
        meta: {
          title: '个人资料',
          icon: 'el-icon-user-solid'
        }
      }
    ]
  }
]

const createRouter = () => new Router({
  // mode: 'history', // 需要服务器支持
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher
}

export default router

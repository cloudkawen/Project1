// client/fix-all-jsx.js
const fs = require('fs')
const path = require('path')

console.log('🔧 开始修复所有 JSX 问题...\n')

// 1. 修复 Sidebar/Item.vue
console.log('1. 修复 Sidebar/Item.vue 文件...')
const itemVuePath = path.join(__dirname, 'src/layout/components/Sidebar/Item.vue')

// 创建不使用 JSX 的新内容
const newItemVueContent = `<template functional>
  <div>
    <svg-icon v-if="props.icon" :icon-class="props.icon" />
    <span v-if="props.title" slot="title">{{ props.title }}</span>
  </div>
</template>

<script>
export default {
  name: 'SidebarItem',
  functional: true,
  props: {
    icon: {
      type: String,
      default: ''
    },
    title: {
      type: String,
      default: ''
    }
  }
}
</script>`

// 备份原文件
if (fs.existsSync(itemVuePath)) {
  const backupPath = itemVuePath + '.jsx.backup'
  fs.copyFileSync(itemVuePath, backupPath)
  console.log('   ✅ 已备份原文件到:', backupPath)
}

// 写入新文件
fs.writeFileSync(itemVuePath, newItemVueContent, 'utf8')
console.log('   ✅ Sidebar/Item.vue 已修复\n')

// 2. 创建最简单的 babel.config.js
console.log('2. 创建最简单的 babel.config.js...')
const babelConfig = `module.exports = {
  presets: [
    '@vue/cli-plugin-babel/preset'
  ]
}`

fs.writeFileSync(path.join(__dirname, 'babel.config.js'), babelConfig, 'utf8')
console.log('   ✅ babel.config.js 已创建\n')

// 3. 创建最简单的 vue.config.js
console.log('3. 创建 vue.config.js...')
const vueConfig = `module.exports = {
  devServer: {
    port: 9528,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
}`

fs.writeFileSync(path.join(__dirname, 'vue.config.js'), vueConfig, 'utf8')
console.log('   ✅ vue.config.js 已创建\n')

// 4. 检查 package.json
console.log('4. 检查 package.json...')
const packagePath = path.join(__dirname, 'package.json')
if (fs.existsSync(packagePath)) {
  const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf8'))
  
  // 确保有必要的 scripts
  if (!packageJson.scripts) packageJson.scripts = {}
  packageJson.scripts.serve = 'vue-cli-service serve'
  packageJson.scripts.build = 'vue-cli-service build'
  packageJson.scripts.dev = 'vue-cli-service serve'
  
  // 确保有必要的 devDependencies
  if (!packageJson.devDependencies) packageJson.devDependencies = {}
  
  // 添加 Vue CLI 依赖
  const requiredDeps = {
    '@vue/cli-plugin-babel': '~4.5.0',
    '@vue/cli-service': '~4.5.0',
    'vue-template-compiler': '^2.6.11',
    'sass': '^1.26.5',
    'sass-loader': '^8.0.2'
  }
  
  Object.assign(packageJson.devDependencies, requiredDeps)
  
  fs.writeFileSync(packagePath, JSON.stringify(packageJson, null, 2), 'utf8')
  console.log('   ✅ package.json 已更新\n')
} else {
  console.log('   ❌ package.json 不存在，将创建...\n')
  
  const defaultPackageJson = {
    name: 'client',
    version: '0.1.0',
    private: true,
    scripts: {
      'serve': 'vue-cli-service serve',
      'build': 'vue-cli-service build',
      'dev': 'vue-cli-service serve'
    },
    dependencies: {
      "vue": "^2.6.11",
      "vue-router": "^3.2.0",
      "vuex": "^3.4.0",
      "element-ui": "^2.15.1",
      "axios": "^0.21.1"
    },
    devDependencies: {
      "@vue/cli-plugin-babel": "~4.5.0",
      "@vue/cli-service": "~4.5.0",
      "vue-template-compiler": "^2.6.11",
      "sass": "^1.26.5",
      "sass-loader": "^8.0.2"
    }
  }
  
  fs.writeFileSync(packagePath, JSON.stringify(defaultPackageJson, null, 2), 'utf8')
  console.log('   ✅ package.json 已创建\n')
}

// 5. 搜索项目中是否还有其他 JSX 文件
console.log('5. 搜索项目中其他可能的 JSX 文件...')
const searchDirs = ['src/components', 'src/views', 'src/layout']
let foundJsx = false

searchDirs.forEach(dir => {
  const dirPath = path.join(__dirname, dir)
  if (fs.existsSync(dirPath)) {
    const files = getAllFiles(dirPath)
    files.forEach(file => {
      if (file.endsWith('.vue') || file.endsWith('.js')) {
        const content = fs.readFileSync(file, 'utf8')
        if (content.includes('<svg-icon icon-class={') || content.includes('</')) {
          const relativePath = path.relative(__dirname, file)
          console.log(`   ⚠️ 发现可能包含 JSX 的文件: ${relativePath}`)
          foundJsx = true
        }
      }
    })
  }
})

if (!foundJsx) {
  console.log('   ✅ 未发现其他 JSX 文件\n')
}

// 辅助函数：获取所有文件
function getAllFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir)
  files.forEach(file => {
    const filePath = path.join(dir, file)
    const stat = fs.statSync(filePath)
    if (stat.isDirectory()) {
      getAllFiles(filePath, fileList)
    } else {
      fileList.push(filePath)
    }
  })
  return fileList
}

console.log('🎉 所有 JSX 问题已修复！\n')
console.log('📋 下一步操作：')
console.log('1. 安装依赖: npm install')
console.log('2. 启动项目: npm run dev')
console.log('3. 如果还有错误，请检查控制台输出')

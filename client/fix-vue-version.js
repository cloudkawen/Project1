// client/fix-vue-version.js
const fs = require('fs')
const path = require('path')

console.log('🔧 开始修复 Vue 版本不匹配问题...\n')

// 读取 package.json
const packagePath = path.join(__dirname, 'package.json')
if (!fs.existsSync(packagePath)) {
  console.log('❌ package.json 不存在')
  process.exit(1)
}

const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf8'))

console.log('当前版本:')
console.log(`  vue: ${packageJson.dependencies.vue}`)
console.log(`  vue-template-compiler: ${packageJson.devDependencies['vue-template-compiler']}\n`)

// 统一版本为 2.6.14（稳定版本）
const targetVersion = '2.6.14'

console.log(`✅ 将统一版本为: ${targetVersion}\n`)

// 更新版本
packageJson.dependencies.vue = targetVersion
if (packageJson.devDependencies['vue-template-compiler']) {
  packageJson.devDependencies['vue-template-compiler'] = targetVersion
}

// 写入文件
fs.writeFileSync(packagePath, JSON.stringify(packageJson, null, 2), 'utf8')
console.log('✅ package.json 已更新\n')

// 清理旧的依赖
console.log('🧹 清理旧的依赖...')
const targets = ['node_modules', 'package-lock.json', 'yarn.lock']
targets.forEach(target => {
  const targetPath = path.join(__dirname, target)
  if (fs.existsSync(targetPath)) {
    try {
      if (fs.statSync(targetPath).isDirectory()) {
        fs.rmSync(targetPath, { recursive: true, force: true })
      } else {
        fs.unlinkSync(targetPath)
      }
      console.log(`  ✅ 已删除: ${target}`)
    } catch (error) {
      console.log(`  ❌ 删除失败 ${target}:`, error.message)
    }
  }
})

console.log('\n🎉 修复完成！')
console.log('\n📋 下一步：')
console.log('1. 运行: npm install')
console.log('2. 运行: npm run dev')

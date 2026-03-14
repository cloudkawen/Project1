<template>
  <div class="app-container">
    <el-form ref="elForm" :model="formData" :rules="rules" size="medium" label-width="100px">
      <el-form-item label="旧密码" prop="old_password">
        <el-input
          v-model="formData.old_password"
          placeholder="请输入旧密码"
          clearable
          show-password
          :style="{width: '100%'}"
        />
      </el-form-item>
      <el-form-item label="新密码" prop="new_password1">
        <el-input
          v-model="formData.new_password1"
          placeholder="请输入新密码"
          clearable
          show-password
          :style="{width: '100%'}"
        />
      </el-form-item>
      <el-form-item label="新密码" prop="new_password2">
        <el-input
          v-model="formData.new_password2"
          placeholder="请再次输入新密码"
          clearable
          show-password
          :style="{width: '100%'}"
        />
      </el-form-item>
      <el-form-item size="large">
        <el-button type="primary" @click="submitForm">提交</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { changePassword } from '@/api/user'

export default {
  name: 'ChangePassword',
  data() {
    return {
      formData: {
        old_password: '',
        new_password1: '',
        new_password2: ''
      },
      rules: {
        old_password: [{
          required: true,
          message: '请输入旧密码',
          trigger: 'blur'
        }],
        new_password1: [{
          required: true,
          message: '请输入新密码',
          trigger: 'blur'
        }],
        new_password2: [{
          required: true,
          message: '请再次输入新密码',
          trigger: 'blur'
        }]
      }
    }
  },
  methods: {
    submitForm() {
      this.$refs['elForm'].validate(valid => {
        if (!valid) return
        changePassword(this.formData).then(async(res) => {
          this.$message({
            message: '密码修改成功,请重新登陆',
            type: 'success'
          })
          await this.$store.dispatch('user/logout')
          this.$router.push(`/login`)
        }).catch(error => {
          console.error('修改密码失败:', error)
          this.$message.error(error.message || '修改密码失败')
        })
      })
    },
    resetForm() {
      this.$refs['elForm'].resetFields()
    }
  }
}
</script>

<style scoped>
.app-container {
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  max-width: 500px;
  margin: 20px auto;
}
</style>

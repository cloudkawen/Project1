<template>
  <div class="items-container">
    <!-- 页面标题和操作栏 -->
    <div class="page-header">
      <h2 class="page-title">物品管理</h2>
      <div class="page-actions">
        <el-button
          type="primary"
          icon="el-icon-plus"
          @click="handleAdd"
        >
          新增物品
        </el-button>
      </div>
    </div>

    <!-- 搜索和筛选区域 -->
    <el-card shadow="never" class="filter-card">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="searchQuery"
            placeholder="搜索物品名称或位置"
            clearable
            @clear="handleSearch"
            @keyup.enter="handleSearch"
          >
            <i slot="prefix" class="el-input__icon el-icon-search" />
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-select
            v-model="categoryFilter"
            placeholder="按分类筛选"
            clearable
            style="width: 100%;"
            @change="handleSearch"
          >
            <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select
            v-model="statusFilter"
            placeholder="按状态筛选"
            clearable
            style="width: 100%;"
            @change="handleSearch"
          >
            <el-option label="正常" value="normal" />
            <el-option label="即将过期" value="expiring" />
            <el-option label="已过期" value="expired" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select
            v-model="locationFilter"
            placeholder="按位置筛选"
            clearable
            filterable
            style="width: 100%;"
            @change="handleSearch"
          >
            <el-option
              v-for="location in locations"
              :key="location"
              :label="location"
              :value="location"
            />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="yyyy-MM-dd"
            style="width: 100%;"
            @change="handleDateFilter"
          />
        </el-col>
      </el-row>
    </el-card>

    <!-- 物品表格 -->
    <el-card shadow="never" class="table-card">
      <el-table
        v-loading="loading"
        :data="list"
        stripe
        border
        style="width: 100%;"
        :default-sort="{prop: 'created_at', order: 'descending'}"
        @sort-change="handleSortChange"
      >
        <el-table-column
          prop="name"
          label="物品名称"
          min-width="150"
          sortable
        >
          <template slot-scope="scope">
            <div class="item-name">
              <span>{{ scope.row.name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column
          prop="category_name"
          label="分类"
          width="120"
          align="center"
        >
          <template slot-scope="scope">
            <el-tag v-if="scope.row.category_name" type="info" size="small">
              {{ scope.row.category_name }}
            </el-tag>
            <span v-else class="text-muted">未分类</span>
          </template>
        </el-table-column>
        <el-table-column
          label="状态"
          width="100"
          align="center"
        >
          <template slot-scope="scope">
            <el-tag
              v-if="scope.row.status === 'expired'"
              type="danger"
              effect="dark"
              size="small"
            >
              已过期
            </el-tag>
            <el-tag
              v-else-if="scope.row.status === 'expiring'"
              type="warning"
              effect="dark"
              size="small"
            >
              即将过期
            </el-tag>
            <el-tag
              v-else
              type="success"
              effect="dark"
              size="small"
            >
              正常
            </el-tag>
            <div v-if="scope.row.days_to_expire !== null" class="days-count">
              <small v-if="scope.row.days_to_expire >= 0">
                {{ scope.row.days_to_expire }}天后过期
              </small>
              <small v-else class="text-danger">
                已过期{{ -scope.row.days_to_expire }}天
              </small>
            </div>
          </template>
        </el-table-column>
        <el-table-column
          prop="location"
          label="位置"
          width="150"
        >
          <template slot-scope="scope">
            <span v-if="scope.row.location" class="text-primary">
              <i class="el-icon-location" /> {{ scope.row.location }}
            </span>
            <span v-else class="text-muted">未设置</span>
          </template>
        </el-table-column>
        <el-table-column
          prop="expire_date"
          label="过期时间"
          width="120"
          sortable
          align="center"
        >
          <template slot-scope="scope">
            <!-- 修复动态类绑定 -->
            <div
              :class="{
                'text-danger': scope.row.status === 'expired',
                'text-warning': scope.row.status === 'expiring'
              }">
              {{ scope.row.expire_date || '无' }}
            </div>
          </template>
        </el-table-column>
        <el-table-column
          prop="created_at"
          label="创建时间"
          width="150"
          sortable
          align="center"
        >
          <template slot-scope="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column
          prop="user_name"
          label="创建人"
          width="120"
          align="center"
        />
        <el-table-column
          label="操作"
          width="200"
          fixed="right"
          align="center"
        >
          <template slot-scope="scope">
            <el-button
              type="primary"
              size="mini"
              icon="el-icon-edit"
              @click="handleEdit(scope.row)"
            >
              编辑
            </el-button>
            <el-button
              type="danger"
              size="mini"
              icon="el-icon-delete"
              @click="handleDelete(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div v-if="total > 0" class="pagination-container">
        <el-pagination
          :current-page="currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pageSize"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
      <!-- 空状态 -->
      <div v-if="!loading && list.length === 0" class="empty-container">
        <i class="el-icon-box empty-icon" />
        <p class="empty-text">暂无物品数据</p>
        <el-button type="primary" @click="handleAdd">添加第一个物品</el-button>
      </div>
    </el-card>

    <!-- 新增/编辑弹窗 -->
    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      width="600px"
      :close-on-click-modal="false"
      @close="handleDialogClose"
    >
      <el-form
        ref="itemForm"
        :model="form"
        :rules="rules"
        label-width="100px"
        class="item-form"
      >
        <el-form-item label="物品名称" prop="name">
          <el-input
            v-model="form.name"
            placeholder="请输入物品名称"
            maxlength="50"
            show-word-limit
            clearable
          />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select
            v-model="form.category"
            placeholder="请选择分类"
            style="width: 100%;"
            filterable
            clearable
          >
            <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
            <el-option disabled style="text-align: center; color: #666;">
              <el-button
                type="text"
                icon="el-icon-plus"
                class="add-category-btn"
                @click.stop="showCategoryDialog = true"
              >
                添加新分类
              </el-button>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="存放位置" prop="location">
          <el-input
            v-model="form.location"
            placeholder="请输入存放位置"
            maxlength="100"
            show-word-limit
            clearable
          />
        </el-form-item>
        <el-form-item label="过期时间" prop="expire_date">
          <el-date-picker
            v-model="form.expire_date"
            type="date"
            value-format="yyyy-MM-dd"
            placeholder="选择过期日期"
            style="width: 100%;"
            :picker-options="datePickerOptions"
            clearable
          />
          <div class="form-tips">
            不设置过期时间表示永不过期
          </div>
        </el-form-item>
        <el-form-item v-if="form.user_name" label="所属用户">
          <el-input v-model="form.user_name" disabled />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button
          type="primary"
          :loading="submitting"
          @click="submitForm"
        >
          确定
        </el-button>
      </span>
    </el-dialog>

    <!-- 新增分类弹窗 -->
    <el-dialog
      title="新增分类"
      :visible.sync="showCategoryDialog"
      width="400px"
      @close="showCategoryDialog = false"
    >
      <el-form
        ref="categoryForm"
        :model="categoryForm"
        :rules="categoryRules"
        label-width="80px"
      >
        <el-form-item label="分类名称" prop="name">
          <el-input
            v-model="categoryForm.name"
            placeholder="请输入分类名称"
            maxlength="20"
            show-word-limit
            clearable
          />
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="showCategoryDialog = false">取消</el-button>
        <el-button
          type="primary"
          :loading="creatingCategory"
          @click="createCategory"
        >
          确定
        </el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { getItems, createItem, updateItem, deleteItem } from '@/api/items'
import { getCategories, createCategory } from '@/api/categories'
import { formatDate } from '@/utils/date'

export default {
  name: 'Items',
  data() {
    return {
      // 列表数据
      list: [],
      loading: false,
      categories: [],
      locations: [],
      // 搜索和筛选
      searchQuery: '',
      categoryFilter: '',
      statusFilter: '',
      locationFilter: '',
      dateRange: [],
      sortField: 'created_at',
      sortOrder: 'descending',
      // 分页
      currentPage: 1,
      pageSize: 10,
      total: 0,
      // 弹窗控制
      dialogVisible: false,
      dialogTitle: '新增物品',
      showCategoryDialog: false,
      // 表单状态
      submitting: false,
      creatingCategory: false,
      editingId: null,
      // 主表单
      form: {
        name: '',
        category: '',
        location: '',
        expire_date: '',
        user: null,
        user_name: ''
      },
      // 分类表单
      categoryForm: {
        name: ''
      },
      // 日期选择器选项
      datePickerOptions: {
        disabledDate(time) {
          return time.getTime() < Date.now() - 8.64e7
        }
      },
      // 验证规则
      rules: {
        name: [
          { required: true, message: '请输入物品名称', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
        ],
        category: [
          { required: true, message: '请选择分类', trigger: 'change' }
        ],
        location: [
          { max: 100, message: '不能超过 100 个字符', trigger: 'blur' }
        ]
      },
      categoryRules: {
        name: [
          { required: true, message: '请输入分类名称', trigger: 'blur' },
          { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.fetchData()
    this.getCurrentUser()
  },
  methods: {
    // 工具函数
    formatDate,
    // 获取当前登录用户
    getCurrentUser() {
      console.log('🔍 获取当前用户信息...')
      // 1. 从 Vuex 获取
      const userState = this.$store.state.user
      console.log('Vuex user 状态:', userState)
      if (userState && (userState.id || userState.token)) {
        this.form.user = userState.id || 1 // 如果没有 id，使用默认值
        this.form.user_name = userState.name || userState.username || '管理员'
        console.log('✅ 从 Vuex 获取到用户信息:', this.form.user_name)
        return
      }
      // 2. 从 localStorage token 中提取（如果有）
      const token = localStorage.getItem('token')
      if (token) {
        console.log('✅ 有 token，但用户信息不完整，使用默认用户')
        this.form.user = 1
        this.form.user_name = '管理员'
        return
      }
      // 3. 没有 token，重定向到登录页
      console.warn('❌ 没有用户信息，重定向到登录页')
      this.$router.push('/login')
    },
    // 获取物品列表
    async fetchData() {
      this.loading = true
      try {
        const params = {
          page: this.currentPage,
          page_size: this.pageSize,
          search: this.searchQuery,
          ordering: this.sortOrder === 'descending' ? '-' + this.sortField : this.sortField
        }
        if (this.categoryFilter) {
          params.category = this.categoryFilter
        }
        if (this.statusFilter) {
          params.status = this.statusFilter
        }
        if (this.locationFilter) {
          params.location = this.locationFilter
        }
        if (this.dateRange && this.dateRange.length === 2) {
          params.expire_date__gte = this.dateRange[0]
          params.expire_date__lte = this.dateRange[1]
        }
        const response = await getItems(params)
        this.list = response.data.results || response.data
        this.total = response.data.count || response.data.length
        // 提取位置列表用于筛选
        this.extractLocations()
      } catch (error) {
        console.error('获取物品列表失败:', error)
        this.$message.error('获取物品列表失败')
      } finally {
        this.loading = false
      }
      // 获取分类列表
      this.getCategoriesList()
    },
    // 获取分类列表
    async getCategoriesList() {
      try {
        const response = await getCategories()
        this.categories = response.data.results || response.data
      } catch (error) {
        console.error('获取分类列表失败:', error)
        this.$message.error('获取分类列表失败')
      }
    },
    // 提取位置列表
    extractLocations() {
      const locationSet = new Set()
      this.list.forEach(item => {
        if (item.location) {
          locationSet.add(item.location)
        }
      })
      this.locations = Array.from(locationSet)
    },
    // 搜索处理
    handleSearch() {
      this.currentPage = 1
      this.fetchData()
    },
    // 日期筛选处理
    handleDateFilter() {
      this.handleSearch()
    },
    // 排序处理
    handleSortChange({ column, prop, order }) {
      this.sortField = prop
      this.sortOrder = order
      this.fetchData()
    },
    // 分页处理
    handleSizeChange(val) {
      this.pageSize = val
      this.currentPage = 1
      this.fetchData()
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.fetchData()
    },
    // 新增物品
    handleAdd() {
      this.dialogTitle = '新增物品'
      this.editingId = null
      this.form = {
        name: '',
        category: '',
        location: '',
        expire_date: '',
        user: this.form.user,
        user_name: this.form.user_name
      }
      this.dialogVisible = true
      this.$nextTick(() => {
        if (this.$refs.itemForm) {
          this.$refs.itemForm.clearValidate()
        }
      })
    },
    // 编辑物品
    handleEdit(row) {
      this.dialogTitle = '编辑物品'
      this.editingId = row.id
      this.form = {
        name: row.name,
        category: row.category || '',
        location: row.location || '',
        expire_date: row.expire_date || '',
        user: row.user || this.form.user,
        user_name: row.user_name || this.form.user_name
      }
      this.dialogVisible = true
      this.$nextTick(() => {
        if (this.$refs.itemForm) {
          this.$refs.itemForm.clearValidate()
        }
      })
    },
    // 删除物品
    handleDelete(row) {
      this.$confirm(`确定删除物品 "${row.name}" 吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger',
        beforeClose: (action, instance, done) => {
          if (action === 'confirm') {
            instance.confirmButtonLoading = true
            instance.confirmButtonText = '删除中...'
            this.deleteItem(row.id).then(() => {
              done()
              instance.confirmButtonLoading = false
            }).catch(() => {
              instance.confirmButtonLoading = false
            })
          } else {
            done()
          }
        }
      }).then(async() => {
        // 删除成功后的处理在beforeClose中已执行
      }).catch(() => {})
    },
    // 实际删除物品
    async deleteItem(id) {
      try {
        await deleteItem(id)
        this.$message.success('删除成功')
        this.fetchData()
      } catch (error) {
        console.error('删除失败:', error)
        // 修复可选链操作符
        this.$message.error(
          (error.response &&
           error.response.data &&
           error.response.data.message) || '删除失败'
        )
      }
    },
    // 提交表单
    async submitForm() {
      this.$refs.itemForm.validate(async valid => {
        if (!valid) {
          return
        }
        this.submitting = true
        try {
          const submitData = {
            name: this.form.name,
            category: this.form.category || null,
            location: this.form.location,
            expire_date: this.form.expire_date,
            user: this.form.user
          }
          if (!submitData.user) {
            throw new Error('无法获取用户信息')
          }
          if (this.editingId) {
            await updateItem(this.editingId, submitData)
            this.$message.success('更新成功')
          } else {
            await createItem(submitData)
            this.$message.success('新增成功')
          }
          this.dialogVisible = false
          this.fetchData()
        } catch (error) {
          console.error('操作失败:', error)
          // 修复可选链操作符
          this.$message.error(
            (error.response &&
             error.response.data &&
             error.response.data.message) || error.message || '操作失败'
          )
        } finally {
          this.submitting = false
        }
      })
    },
    // 弹窗关闭
    handleDialogClose() {
      // 修复可选链操作符
      if (this.$refs.itemForm) {
        this.$refs.itemForm.clearValidate()
      }
    },
    // 创建分类
    async createCategory() {
      this.$refs.categoryForm.validate(async valid => {
        if (!valid) {
          return
        }
        this.creatingCategory = true
        try {
          await createCategory({ name: this.categoryForm.name })
          this.$message.success('分类创建成功')
          this.showCategoryDialog = false
          this.categoryForm.name = ''
          // 刷新分类列表
          await this.getCategoriesList()

          // 如果正在创建物品，自动选择新创建的分类
          if (this.dialogVisible) {
            const newCategory = this.categories.find(c => c.name === this.categoryForm.name)
            if (newCategory) {
              this.form.category = newCategory.id
            }
          }
        } catch (error) {
          console.error('创建分类失败:', error)
          // 修复可选链操作符
          this.$message.error(
            (error.response &&
             error.response.data &&
             error.response.data.message) || '创建分类失败'
          )
        } finally {
          this.creatingCategory = false
        }
      })
    }
  }
}
</script>

<style scoped>

.items-container {
  padding: 20px;
  background-color: #f0f2f5;
  min-height: calc(100vh - 84px);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.filter-card {
  margin-bottom: 20px;
  border-radius: 8px;
  border: 1px solid #e6e6e6;
}

.table-card {
  border-radius: 8px;
  border: 1px solid #e6e6e6;
  min-height: 500px;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
  padding: 10px 0;
  border-top: 1px solid #f0f0f0;
}

.empty-container {
  text-align: center;
  padding: 60px 0;
  color: #909399;
}

.empty-icon {
  font-size: 60px;
  margin-bottom: 20px;
  color: #c0c4cc;
}

.empty-text {
  font-size: 16px;
  margin-bottom: 20px;
  color: #606266;
}

.item-name {
  font-weight: 500;
  color: #303133;
}

.days-count {
  font-size: 12px;
  margin-top: 4px;
  color: #909399;
}

.text-primary {
  color: #409EFF;
}

.text-success {
  color: #67C23A;
}

.text-warning {
  color: #E6A23C;
}

.text-danger {
  color: #F56C6C;
}

.text-muted {
  color: #909399;
}

.item-form {
  padding: 10px 0;
}

.form-tips {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}

.add-category-btn {
  width: 100%;
  color: #409EFF;
}

.dialog-footer {
  padding: 20px 0 0;
  text-align: right;
  border-top: 1px solid #f0f0f0;
}

</style>

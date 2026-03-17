<template>
  <div class="categories-container">
    <!-- 页面标题和操作栏 -->
    <div class="page-header">
      <h2 class="page-title">分类管理</h2>
      <div class="page-actions">
        <el-button
          type="primary"
          icon="el-icon-plus"
          @click="handleAdd"
        >
          新增分类
        </el-button>
      </div>
    </div>

    <!-- 搜索区域 -->
    <el-card shadow="never" class="filter-card">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-input
            v-model="searchQuery"
            placeholder="搜索分类名称"
            clearable
            @clear="handleSearch"
            @keyup.enter="handleSearch"
          >
            <i slot="prefix" class="el-input__icon el-icon-search" />
          </el-input>
        </el-col>
      </el-row>
    </el-card>

    <!-- 分类表格 -->
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
          label="分类名称"
          min-width="150"
          sortable
        >
          <template slot-scope="scope">
            <div class="category-name">
              <i class="el-icon-folder" style="margin-right: 8px; color: #409EFF;" />
              <span>{{ scope.row.name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column
          prop="item_count"
          label="物品数量"
          width="120"
          sortable
          align="center"
        >
          <template slot-scope="scope">
            <el-tag
              v-if="scope.row.item_count > 0"
              :type="getCountTagType(scope.row.item_count)"
              size="small"
            >
              {{ scope.row.item_count }}
            </el-tag>
            <span v-else class="text-muted">0</span>
          </template>
        </el-table-column>
        <el-table-column
          prop="created_at"
          label="创建时间"
          width="180"
          sortable
          align="center"
        >
          <template slot-scope="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
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
              :disabled="scope.row.item_count > 0"
              @click="handleEdit(scope.row)"
            >
              编辑
            </el-button>
            <el-button
              type="danger"
              size="mini"
              icon="el-icon-delete"
              :disabled="scope.row.item_count > 0"
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
        <i class="el-icon-folder-opened empty-icon" />
        <p class="empty-text">暂无分类数据</p>
        <el-button type="primary" @click="handleAdd">添加第一个分类</el-button>
      </div>
    </el-card>

    <!-- 新增/编辑分类弹窗 -->
    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      width="500px"
      :close-on-click-modal="false"
      @close="handleDialogClose"
    >
      <el-form
        ref="categoryForm"
        :model="form"
        :rules="rules"
        label-width="100px"
        class="category-form"
      >
        <el-form-item label="分类名称" prop="name">
          <el-input
            v-model="form.name"
            placeholder="请输入分类名称"
            maxlength="20"
            show-word-limit
            clearable
          />
        </el-form-item>
        <el-form-item v-if="editingId" label="物品数量">
          <el-input
            :value="form.item_count || 0"
            disabled
          />
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
  </div>
</template>

<script>
import {
  getCategories,
  createCategory,
  updateCategory,
  deleteCategory
} from '@/api/categories'
import { formatDate } from '@/utils/date'

export default {
  name: 'Categories',
  data() {
    return {
      // 分类数据
      list: [],
      loading: false,
      // 搜索
      searchQuery: '',
      sortField: 'created_at',
      sortOrder: 'descending',
      // 分页
      currentPage: 1,
      pageSize: 10,
      total: 0,
      // 弹窗控制
      dialogVisible: false,
      dialogTitle: '新增分类',
      submitting: false,
      editingId: null,
      // 表单
      form: {
        name: '',
        item_count: 0
      },
      // 验证规则
      rules: {
        name: [
          { required: true, message: '请输入分类名称', trigger: 'blur' },
          { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' },
          { pattern: /^[\u4e00-\u9fa5a-zA-Z0-9]+$/, message: '只能包含中文、英文和数字', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    // 工具函数
    formatDate,
    // 获取物品数量标签类型
    getCountTagType(count) {
      if (count === 0) return 'info'
      if (count <= 5) return 'success'
      if (count <= 20) return 'warning'
      return 'danger'
    },
    // 获取分类列表
    async fetchData() {
      this.loading = true
      try {
        const params = {
          page: this.currentPage,
          page_size: this.pageSize,
          search: this.searchQuery,
          ordering: this.sortOrder === 'descending' ? '-' + this.sortField : this.sortField
        }
        const response = await getCategories(params)
        this.list = response.data.results || response.data
        this.total = response.data.count || response.data.length
      } catch (error) {
        console.error('获取分类列表失败:', error)
        this.$message.error('获取分类列表失败')
      } finally {
        this.loading = false
      }
    },
    // 搜索处理
    handleSearch() {
      this.currentPage = 1
      this.fetchData()
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
    // 新增分类
    handleAdd() {
      this.dialogTitle = '新增分类'
      this.editingId = null
      this.form = {
        name: '',
        item_count: 0
      }
      this.dialogVisible = true
      this.$nextTick(() => {
        if (this.$refs.categoryForm) {
          this.$refs.categoryForm.clearValidate()
        }
      })
    },
    // 编辑分类
    handleEdit(row) {
      this.dialogTitle = '编辑分类'
      this.editingId = row.id
      this.form = {
        name: row.name,
        item_count: row.item_count || 0
      }
      this.dialogVisible = true
      this.$nextTick(() => {
        if (this.$refs.categoryForm) {
          this.$refs.categoryForm.clearValidate()
        }
      })
    },
    // 删除分类
    handleDelete(row) {
      if (row.item_count > 0) {
        this.$message.warning('该分类下有物品，无法删除')
        return
      }
      this.$confirm(`确定删除分类 "${row.name}" 吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger',
        beforeClose: (action, instance, done) => {
          if (action === 'confirm') {
            instance.confirmButtonLoading = true
            instance.confirmButtonText = '删除中...'
            this.deleteCategory(row.id).then(() => {
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
    // 实际删除分类
    async deleteCategory(id) {
      try {
        await deleteCategory(id)
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
      this.$refs.categoryForm.validate(async valid => {
        if (!valid) {
          return
        }
        this.submitting = true
        try {
          if (this.editingId) {
            await updateCategory(this.editingId, this.form)
            this.$message.success('更新成功')
          } else {
            await createCategory(this.form)
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
      if (this.$refs.categoryForm) {
        this.$refs.categoryForm.clearValidate()
      }
    }
  }
}
</script>

<style scoped>
.categories-container {
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

.category-name {
  display: flex;
  align-items: center;
  font-weight: 500;
  color: #303133;
}

.text-muted {
  color: #909399;
}

.category-form {
  padding: 10px 0;
}

.dialog-footer {
  padding: 20px 0 0;
  text-align: right;
  border-top: 1px solid #f0f0f0;
}
</style>

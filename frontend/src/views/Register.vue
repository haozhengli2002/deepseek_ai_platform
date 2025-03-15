<template>
  <div class="login-container">
    <h2 class="login-title">用户注册</h2>
    <el-form 
      :model="form" 
      :rules="rules" 
      ref="formRef"
      label-width="80px" 
      label-position="top"
    >
      <!-- 用户名输入 -->
      <el-form-item label="用户名：" prop="username">
        <el-input
          v-model="form.username"
          placeholder="请输入用户名"
          clearable
        />
      </el-form-item>

      <!-- 密码输入 -->
      <el-form-item label="密码：" prop="password">
        <el-input
          v-model="form.password"
          type="password"
          placeholder="请输入密码"
          show-password
          clearable
        />
      </el-form-item>

      <!-- 双按钮布局 -->
      <el-form-item class="button-group">
        <el-button 
          type="primary" 
          @click="handleRegister" 
          style="width: 100%; margin-bottom: 15px;"
        >
          立即注册
        </el-button>
        <el-button 
          plain 
          @click="goToLogin" 
          style="width: 100%;"
        >
          已有账号？去登录
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { register } from '../api/api'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router' // 需要安装 vue-router

const router = useRouter()

// 表单数据绑定
const form = ref({
  username: '',
  password: ''
})

// 表单验证规则
const rules = ref({
  username: [
    { required: true, message: '用户名不能为空', trigger: 'blur' },
    { min: 4, max: 16, message: '长度在 4 到 16 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '密码不能为空', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ]
})

// 表单引用
const formRef = ref(null)

// 注册处理
const handleRegister = async () => {
  try {
    await formRef.value.validate()
    const response = await register(form.value)
    console.log('注册成功:', response.data)
    ElMessage.success('注册成功')
    router.push('/login') // 自动跳转登录页
  } catch (error) {
    console.error('注册失败:', error)
    ElMessage.error(error.response?.data?.message || '注册失败')
  }
}

// 跳转登录页
const goToLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 30px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.login-title {
  text-align: center;
  margin-bottom: 30px;
  color: #303133;
}

.el-form-item {
  margin-bottom: 22px;
}

.button-group {
  margin-top: 30px;
}

/* 调整按钮悬停效果 */
.el-button--primary:hover {
  opacity: 0.9;
}

.el-button.is-plain:hover {
  color: #409eff;
  border-color: #c6e2ff;
  background-color: #ecf5ff;
}
</style>
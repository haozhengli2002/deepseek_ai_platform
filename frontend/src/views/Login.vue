<template>
  <div class="login-container">
    <div class="header-section">
      <img 
        src="/favicon.png" 
        alt="AI Assistant"
        class="logo-image"
      />
      <h1 class="main-title">AI Assistant</h1>
      <h2 class="login-title">用户登录</h2>
    </div>
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

      <!-- 登录按钮 -->
      <el-form-item>
        <el-button 
          type="primary" 
          @click="handleLogin" 
          style="width: 100%;"
        >
          登录
        </el-button>
      </el-form-item>

      <el-form-item>
        <el-button 
          type="primary" 
          @click="goToRegister" 
          style="width: 100%;"
        >
          注册
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { login } from '../api/api'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
const router = useRouter()
// 表单数据绑定
const form = ref({
  username: '',
  password: ''
})

// 表单验证规则
const rules = ref({
  username: [
    { required: true, message: '用户名不能为空', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '密码不能为空', trigger: 'blur' }
  ]
})

// 表单引用（用于验证）
const formRef = ref(null)

// 登录处理
const handleLogin = async () => {
  try {
    // 先进行表单验证
    await formRef.value.validate()
    
    // 调用登录接口
    const response = await login({
      username: form.value.username,
      password: form.value.password
    })
    
    console.log('登录成功:', response.data)
    ElMessage.success('登录成功')
    router.push('/chat')
  } catch (error) {
    console.error('登录失败:', error)
    ElMessage.error(error.response?.data?.message || '登录失败')
  }
}



const goToRegister = () => {
  router.push('/register')
}
</script>

<style scoped>
.header-section {
  text-align: center;
  margin-bottom: 30px;
}
.main-title {
  font-size: 28px;
  color: #303133;
  margin: 10px 0;
  letter-spacing: 1px;
}
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 30px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.login-title {
  font-size: 20px;
  color: #606266;
  margin-top: 8px;
}

/* 调整表单项间距 */
.el-form-item {
  margin-bottom: 22px;
}

/* 登录容器样式 - 对应图片中的白色区域 */
.login-container {
  margin-top: 30px; /* 原50px改为30px */
}

/* 标题样式 */
.login-title {
  font-size: 24px;
  font-weight: 500;
  color: #303133; /* Element Plus 主文字颜色 */
}

/* 按钮悬停效果优化 */
.el-button--primary:hover {
  opacity: 0.9;
  transform: translateY(-1px); /* 轻微抬升效果 */
  transition: all 0.3s ease;
}
</style>

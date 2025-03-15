<template>
  <!-- 路由容器，用于显示登录/注册页面 -->
  <router-view />
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
/* 全局基础样式 - 匹配图片设计 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', Arial, sans-serif; /* 使用 Element Plus 同款字体 */
}

#app {
  min-height: 100vh;
  background-color: #f5f5f5; /* 页面背景浅灰色（图片中容器外的背景） */
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 适配图片中的白色登录容器 */
.login-container {
  width: 100%;
  max-width: 400px; /* 控制登录框最大宽度 */
  padding: 20px;
}

/* 优化移动端显示 */
@media (max-width: 480px) {
  #app {
    padding: 15px;
  }
  
  .login-container {
    padding: 15px;
  }
}
</style>
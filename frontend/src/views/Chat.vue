<template>
  <div class="main-container">
    <!-- 侧边栏 -->
    <div class="sidebar" :style="{ width: sidebarWidth }">
      <div class="sidebar-header">
        <h3 v-show="!isCollapsed">对话历史</h3>
        <div class="header-buttons">
          <el-button 
            @click="createNewConversation"
            type="primary" 
            circle
            :icon="Plus"
            size="small"
          />
          <el-button 
            @click="toggleSidebar"
            :icon="isCollapsed ? Expand : Fold"
            circle
            size="small"
          />
        </div>
      </div>

      <el-menu
        :default-active="activeConversation"
        class="conversation-list"
        :collapse="isCollapsed"
      >
        <el-menu-item 
          v-for="conv in conversations" 
          :key="conv.id"
          :index="conv.id"
          @click="selectConversation(conv.id)"
        >
          <el-icon><ChatLineRound /></el-icon>
          <template #title>
            <span class="conversation-title">{{ conv.title }}</span>
            <span class="conversation-time">{{ formatTime(conv.createTime) }}</span>
          </template>
        </el-menu-item>
      </el-menu>
    </div>

    <!-- 主聊天区域 -->
    <div class="chat-container">
      <el-scrollbar ref="scrollbar" class="message-area">
        <div 
          v-for="message in currentMessages" 
          :key="message.id"
          class="message-wrapper"
        >
          <!-- 用户消息 -->
          <div v-if="message.role === 'user'" class="user-message">
            <el-card class="message-bubble user-bubble">
              <div class="message-content">{{ message.content }}</div>
            </el-card>
          </div>

          <!-- AI 消息 -->
          <div v-else class="ai-message">
            <el-card class="message-bubble ai-bubble">
              <div class="message-content">{{ message.content }}</div>
              <div class="message-time">{{ message.time }}</div>
            </el-card>
          </div>
        </div>
      </el-scrollbar>

      <!-- 输入区域 -->
      <div class="input-area">
        <el-input
          v-model="inputText"
          placeholder="请输入消息"
          clearable
          @keyup.enter="handleSend"
          :disabled="loading"
        >
          <template #append>
            <el-button 
              type="primary" 
              @click="handleSend"
              :loading="loading"
              :icon="Promotion"
            >
              发送
            </el-button>
          </template>
        </el-input>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, watch } from 'vue'
import { 
  Fold,
  Expand,
  Promotion,
  ChatLineRound,
  Plus
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { chat } from '../api/api'

// 侧边栏状态
const isCollapsed = ref(false)
const sidebarWidth = computed(() => isCollapsed.value ? '64px' : '250px')

// 对话数据
const conversations = ref([])
const activeConversation = ref(null)

// 输入状态
const inputText = ref('')
const loading = ref(false)
const scrollbar = ref(null)

// 当前对话消息
const currentMessages = computed(() => {
  const conv = conversations.value.find(c => c.id === activeConversation.value)
  return conv ? conv.messages : []
})

// 创建新对话
const createNewConversation = () => {
  const newConv = {
    id: Date.now().toString(),
    title: '新对话',
    createTime: new Date(),
    messages: []
  }
  conversations.value.unshift(newConv)
  activeConversation.value = newConv.id
}

// 选择对话
const selectConversation = (id) => {
  activeConversation.value = id
  nextTick(scrollToBottom)
}

// 自动滚动到底部
const scrollToBottom = async () => {
  await nextTick()
  scrollbar.value?.setScrollTop(scrollbar.value.wrapRef?.scrollHeight || 0)
}

// 处理发送消息
const handleSend = async () => {
  if (!inputText.value.trim() || loading.value) return

  try {
    loading.value = true
    
    // 如果没有活动对话，创建新对话
    if (!activeConversation.value) {
      createNewConversation()
    }

    // 创建用户消息
    const userMessage = createMessage('user', inputText.value.trim())
    addMessageToConversation(userMessage)
    
    inputText.value = ''
    await scrollToBottom()

    // 获取AI响应
    const res = await chat({ prompt: userMessage.content })
    const aiMessage = createMessage('ai', res.data)
    addMessageToConversation(aiMessage)
    
    // 更新对话标题（如果是第一条消息）
    updateConversationTitle(userMessage.content)

  } catch (error) {
    ElMessage.error('发送失败: ' + (error.response?.data?.message || error.message))
  } finally {
    loading.value = false
    await scrollToBottom()
  }
}

// 创建消息对象
const createMessage = (role, content) => ({
  id: Date.now(),
  role,
  content,
  time: new Date().toLocaleTimeString()
})

// 添加消息到当前对话
const addMessageToConversation = (message) => {
  const conv = conversations.value.find(c => c.id === activeConversation.value)
  if (conv) {
    conv.messages.push(message)
  }
}

// 更新对话标题（使用第一条消息）
const updateConversationTitle = (content) => {
  const conv = conversations.value.find(c => c.id === activeConversation.value)
  if (conv && conv.messages.length === 1) { // 只有第一条消息时更新标题
    conv.title = content.substring(0, 20) || '新对话'
  }
}

// 时间格式化
const formatTime = (date) => {
  return new Date(date).toLocaleDateString() + ' ' + 
         new Date(date).toLocaleTimeString().slice(0,5)
}

// 侧边栏切换
const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
}

// 监听对话变化
watch(activeConversation, (newVal) => {
  if (newVal) {
    nextTick(scrollToBottom)
  }
})
</script>

<style scoped>
.main-container {
  display: flex;
  height: 100vh;
  background: #ffffff;
}

.sidebar {
  background: #ffffff;
  border-right: 1px solid #f0f0f0;
  transition: width 0.3s ease;
  display: flex;
  flex-direction: column;
  min-width: 80px;
}

.sidebar-header {
  padding: 8px 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  border-bottom: 1px solid #eee;
}

.header-buttons {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.conversation-list {
  flex: 1;
  border-right: none;
}

.conversation-title {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.conversation-time {
  font-size: 12px;
  color: #999;
  margin-left: 8px;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  min-width: 0;
}

.message-area {
  flex: 1;
  padding: 20px;
  background: #ffffff;
}

.message-wrapper {
  margin: 12px 0;
}

.message-bubble {
  max-width: 500px;
  border-radius: 12px;
  margin: 8px 0;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.user-message {
  display: flex;
  justify-content: flex-end;
}

.user-bubble {
  background: #409eff !important;
  color: white;
  border-radius: 12px 12px 0 12px !important;
}

.ai-message {
  display: flex;
  justify-content: flex-start;
}

.ai-bubble {
  background: #f8f8f8 !important;
  border-radius: 12px 12px 12px 0 !important;
  border: 1px solid #eee !important;
}

.message-content {
  font-size: 14px;
  line-height: 1.6;
  padding: 12px;
  white-space: pre-wrap;
}

.message-time {
  font-size: 12px;
  color: #666;
  padding: 0 12px 8px;
  text-align: right;
}

.input-area {
  padding: 20px;
  background: #ffffff;
  border-top: 1px solid #f0f0f0;
}

@media (max-width: 768px) {
  .message-bubble {
    max-width: 90% !important;
  }
  
  .sidebar-header h3 {
    display: none;
  }
}
</style>
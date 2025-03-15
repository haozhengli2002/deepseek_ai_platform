import { createApp } from 'vue'
import App from './App.vue'
import router from './router'  // 确保导入路由配置
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'


const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }
app.use(ElementPlus)
app.use(router)  // 必须挂载路由实例
app.mount('#app')
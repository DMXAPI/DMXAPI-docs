<script setup>
import { onMounted, onUnmounted } from 'vue'

let script, style

onMounted(() => {
  // 配置 Dify Chatbot
  window.difyChatbotConfig = {
    token: 'sOIIdx7n5pzJ4JXL',
    systemVariables: {
      // user_id: 'YOU CAN DEFINE USER ID HERE',
      // conversation_id: 'YOU CAN DEFINE CONVERSATION ID HERE, IT MUST BE A VALID UUID',
    },
  }

  // 动态插入 Dify 脚本
  script = document.createElement('script')
  script.src = 'https://udify.app/embed.min.js'
  script.id = 'sOIIdx7n5pzJ4JXL'
  script.defer = true
  document.body.appendChild(script)

  // 动态插入样式
  style = document.createElement('style')
  style.innerHTML = `
    #dify-chatbot-bubble-button {
      background-color: #1C64F2 !important;
    }
    #dify-chatbot-bubble-window {
      width: 24rem !important;
      height: 40rem !important;
    }
  `
  document.head.appendChild(style)
})

onUnmounted(() => {
  // 清理脚本和样式
  if (script)
    script.remove()
  if (style)
    style.remove()
  delete window.difyChatbotConfig
})
</script>

<template>
  <!-- 这里不需要内容，Dify 浮窗会自动挂载到页面 -->
  <div />
</template>

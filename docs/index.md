---
layout: page
---

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vitepress'

onMounted(() => {
  const router = useRouter()
  
  // 检查是否有保存的语言偏好
  const savedLang = localStorage.getItem('preferred-lang')
  
  if (savedLang) {
    // 如果有保存的语言偏好，直接使用
    router.go(`/${savedLang}/`)
  } else {
    // 获取浏览器语言
    const userLang = navigator.language || navigator.userLanguage
    
    // 根据浏览器语言设置默认语言
    const preferredLang = userLang.toLowerCase().includes('zh') ? 'zh' : 'en'
    
    // 保存语言偏好
    localStorage.setItem('preferred-lang', preferredLang)
    
    // 重定向到相应语言版本
    router.go(`/${preferredLang}/`)
  }
})
</script>

<template>
  <div class="redirect">
    <div class="loading-spinner"></div>
    <p>正在跳转到适合您的语言版本...</p>
    <p>Redirecting to your preferred language version...</p>
  </div>
</template>

<style scoped>
.redirect {
  padding: 100px 24px;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  margin: 20px auto;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>

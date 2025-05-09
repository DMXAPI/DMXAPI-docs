<script>
export default {
  name: 'DmxIntro',
}
</script>

<template>
  <div class="dmx-container">
    <!-- 左侧文字说明 -->
    <div class="dmx-content">
      <h1 class="title">
        海外模型低至 <span class="highlight">7 折</span>
        <br>
        模型原厂集采直供
      </h1>

      <p class="description">
        通过<strong>直接与大模型原厂合作</strong>，我们采用集中采购的方式获取资源，确保为您提供极具竞争力的价格。与传统渠道相比，我们的模式去除了中间环节，让您以更低成本享受到优质的大模型服务。无论是企业级部署还是开发者项目，我们都致力于提供高性价比的解决方案，助您实现高效创新。选择DMXAPI，轻松获得行业领先的AI模型资源，在节省预算的同时提升应用效果。
      </p>

      <ul class="feature-list">
        <li>✓ 集采直供：通过与大模型原厂合作集中采购，获得代理价格。</li>
        <li>✓ 优惠价格：让客户以更低的成本获取顶级的大模型服务。</li>
        <li>✓ 高性价比方案：专注于企业级及个性化的API服务解决方案。</li>
      </ul>
    </div>

    <!-- 右侧图片 -->
    <div class="dmx-image">
      <img src="/banner2.png" alt="DMXAPI 聚合模型展示">
    </div>
  </div>
</template>

<style scoped>
.dmx-container {
  display: flex;
  gap: 48px;
  padding: 0px;
}

.dmx-image {
  flex: 1;
}

.dmx-image img {
  width: 100%;
  border-radius: 12px;
}

.dmx-content {
  flex: 1;
  padding: 20px 0;
}

.title {
  font-size: 32px;
  margin-bottom: 16px;
}

.highlight {
  color: #FF9F43;
}

.subtitle {
  font-size: 24px;
  margin-bottom: 24px;
  opacity: 0.9;
}

.description {
  line-height: 1.6;
  margin-bottom: 24px;
  opacity: 0.8;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin-bottom: 32px;
}

.feature-list li {
  margin-bottom: 12px;
  opacity: 0.9;
}

.register-btn {
  background-color: #FF9F43;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: opacity 0.3s;
}

.register-btn:hover {
  opacity: 0.9;
}
</style>

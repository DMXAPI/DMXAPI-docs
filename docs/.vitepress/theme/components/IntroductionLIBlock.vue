<script>
export default {
  name: 'DmxIntro',
}
</script>

<template>
  <div class="dmx-container">
    <!-- 左侧图片 -->
    <div class="dmx-image">
      <img src="/banner1.png" alt="DMXAPI 聚合模型展示">
    </div>

    <!-- 右侧文字说明 -->
    <div class="dmx-content">
      <h1 class="title">
        聚合中国和全球300+<span class="highlight">多模态</span>大模型
      </h1>

      <p class="description">
        DMXAPI汇聚了国内外300+多模态大型人工智能模型，全面支持文生文、文生图、文生视频、文生音频等多种模态API。这些模型基于深度学习技术，具备强大的自然语言处理、图像识别、视频分析和音频合成能力，让您的AI应用如虎添翼。
      </p>

      <ul class="feature-list">
        <li>✓ LLM文本模型 & 文生图模型 & TTS模型 & 文生视频模型</li>
        <li>✓ 电商外贸 & AIGC & AI客服 & RAG文档问答</li>
        <li>✓ 数据标注 & 自动驾驶 & 图片理解 & 数据分析</li>
      </ul>
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

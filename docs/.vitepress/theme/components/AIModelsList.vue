<script>
export default {
  name: 'AIModelsList',
}
</script>

<template>
  <div class="models-container">
    <p class="main-title">
      主流模型全支持
    </p>
    <p class="sub-title">
      出海AI大模型列表
    </p>

    <div class="models-grid">
      <!-- OpenAI 模型 -->
      <div class="model-card">
        <h3 class="model-category">
          OpenAI 顶级大模型
        </h3>
        <p class="model-desc">
          全球顶级人工智能AI大模型
        </p>
        <p class="model-name">
          GPT-4.5
        </p>

        <div class="model-list">
          <h4>MODEL LIST:</h4>
          <div class="model-item">
            <span class="check">✓</span>
            <span class="name">o1 & o3</span>
            <span class="version">o1 / o3-mini</span>
          </div>
          <div class="model-item">
            <span class="check">✓</span>
            <span class="name">GPT-4</span>
            <span class="version">gpt-4</span>
          </div>
          <div class="model-item">
            <span class="check">✓</span>
            <span class="name">GPT-4</span>
            <span class="version">gpt-4o</span>
          </div>
          <div class="model-item">
            <span class="check">✓</span>
            <span class="name">GPT-4</span>
            <span class="version">gpt-4o-mini</span>
          </div>
          <div class="model-item">
            <span class="check">✓</span>
            <span class="name">GPT-3.5</span>
            <span class="version">gpt-3.5-turbo</span>
          </div>
          <div class="model-item">
            <span class="check">✓</span>
            <span class="name">Text-to-Image</span>
            <span class="version">dall-e-3</span>
          </div>
          <div class="model-item">
            <span class="check">✓</span>
            <span class="name">Text-to-Speech</span>
            <span class="version">whisper-1</span>
          </div>
          <div class="model-item">
            <span class="check">✓</span>
            <span class="name">More...</span>
            <span class="version" />
          </div>
        </div>
      </div>

      <!-- Anthropic 模型 -->
      <div class="model-card">
        <h3 class="model-category">
          Anthropic AI大模型
        </h3>
        <p class="model-desc">
          OpenAI的主要竞争对手，模型能力不输GPT
        </p>
        <p class="model-name">
          Claude-3.7
        </p>

        <div class="model-list">
          <h4>MODEL LIST:</h4>
          <div class="model-item">
            <span class="check">✓</span>
            <span class="name">claude-3.7</span>
            <span class="version">claude-3-7-sonnet</span>
          </div>
          <div class="model-item">
            <span class="check">✓</span>
            <span class="name">claude-3.5</span>
            <span class="version">claude-3-5-sonnet</span>
          </div>
          <div class="model-item">
            <span class="check">✓</span>
            <span class="name">claude-3</span>
            <span class="version">claude-3-opus-20240229</span>
          </div>
          <div class="model-item">
            <span class="check">✓</span>
            <span class="name">claude-3</span>
            <span class="version">claude-3-haiku-20240307</span>
          </div>
          <div class="model-item">
            <span class="check">✓</span>
            <span class="name">claude-3</span>
            <span class="version">claude-3-opus</span>
          </div>
          <div class="model-item">
            <span class="check">✓</span>
            <span class="name">claude-2.1</span>
            <span class="version">claude-2.1</span>
          </div>
          <div class="model-item">
            <span class="check">✓</span>
            <span class="name">claude-2</span>
            <span class="version">claude-2</span>
          </div>
          <div class="model-item">
            <span class="check">✓</span>
            <span class="name">More...</span>
            <span class="version" />
          </div>
        </div>
      </div>

      <!-- 开源模型 -->
      <div class="model-card">
        <h3 class="model-category">
          开源大模型
        </h3>
        <p class="model-desc">
          主流开源人工智能大模型
        </p>
        <p class="model-name">
          DeepSeek
        </p>

        <div class="model-list">
          <h4>MODEL LIST:</h4>
          <div class="model-item">
            <span class="check">✓</span>
            <span class="name">DeepSeek R1</span>
            <span class="version">deepseek-reasoner</span>
          </div>
          <div class="model-item">
            <span class="check">✓</span>
            <span class="name">DeepSeek V3</span>
            <span class="version">deepseek-chat</span>
          </div>
          <div class="model-item">
            <span class="check">✓</span>
            <span class="name">Llama3.3</span>
            <span class="version">llama-3-3-8b-instant</span>
          </div>
          <div class="model-item">
            <span class="check">✓</span>
            <span class="name">Llama3</span>
            <span class="version">llama-3-70b</span>
          </div>
          <div class="model-item">
            <span class="check">✓</span>
            <span class="name">code-llama</span>
            <span class="version">code-llama-34b</span>
          </div>
          <div class="model-item">
            <span class="check">✓</span>
            <span class="name">code-llama</span>
            <span class="version">code-llama-13b</span>
          </div>
          <div class="model-item">
            <span class="check">✓</span>
            <span class="name">mistral</span>
            <span class="version">mistral-large-latest</span>
          </div>
          <div class="model-item">
            <span class="check">✓</span>
            <span class="name">More...</span>
            <span class="version" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.models-container {
  padding: 40px 0;
  color: var(--vp-c-text-1);
}

.main-title {
  text-align: center;
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 16px;
}

.sub-title {
  text-align: center;
  font-size: 26px;
  color: #FF9F43;
  font-weight: 500;
  margin-bottom: 40px;
}

.models-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.model-card {
  background: var(--vp-c-bg-soft);
  border-radius: 12px;
  padding: 24px;
}

.model-category {
  font-size: 18px;
  margin-bottom: 8px;
}

.model-desc {
  font-size: 14px;
  opacity: 0.8;
  margin-bottom: 16px;
}

.model-name {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 24px;
}

.model-list h4 {
  font-size: 14px;
  opacity: 0.7;
  margin-bottom: 16px;
}

.model-item {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  font-size: 14px;
}

.check {
  color: #4CAF50;
  margin-right: 8px;
}

.name {
  font-weight: 500;
  margin-right: 8px;
}

.version {
  opacity: 0.6;
}

@media (max-width: 768px) {
  .models-grid {
    grid-template-columns: 1fr;
  }
}
</style>

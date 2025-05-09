<script setup>
const trustList = [
  { icon: '/icons/Page.png', name: 'OpenAI Translator' },
  { icon: '/icons/Page.png', name: 'LobeHub' },
  { icon: '/icons/Page.png', name: 'Cherry Studio' },
  { icon: '/icons/Page.png', name: 'Bob' },
  { icon: '/icons/Page.png', name: 'Pot' },
]
</script>

<template>
  <div class="trust-list">
    <h2 class="trust-title">
      开发者的信赖之选
    </h2>
    <div class="trust-items">
      <div v-for="(item, index) in trustList" :key="index" class="trust-item">
        <img :src="item.icon" :alt="item.name" class="trust-icon">
        <span class="trust-name">{{ item.name }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.trust-list {
  text-align: center;
  margin: 2rem 0;
}
.trust-title {

  font-size: 1.3rem;
  font-weight: 500;
  margin-bottom: 1.5rem;
  letter-spacing: 1px;
}
.trust-items {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 3rem;
  flex-wrap: wrap;
}
.trust-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 0.5rem;
  min-width: 150px;
}
.trust-icon {
  width: 40px;
  height: 40px;
  object-fit: contain;
}
.trust-name {
  font-size: 1.05rem;
  font-weight: 500;
  color: #222;
  white-space: nowrap;
}

.dark .trust-name {
  color: #dfdfd6; /* 或你喜欢的浅色 */
}

@media (max-width: 700px) {
  .trust-items {
    gap: 1.2rem;
  }
  .trust-item {
    min-width: 110px;
  }
  .trust-icon {
    width: 32px;
    height: 32px;
  }
}
</style>

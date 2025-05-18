<template>
  <footer class="custom-footer">
    <div class="footer-main">
      <div class="footer-col">
        <div class="footer-title">
          产品服务
        </div>
        <ul>
          <li><a href="#">Deepseek</a></li>
          <li><a href="#">OpenAI</a></li>
          <li><a href="#">Gemini</a></li>
          <li><a href="#">Grok</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-title">
          相关文档
        </div>
        <ul>
          <li><a href="#">模型价格</a></li>
          <li><a href="#">API 文档</a></li>
          <li><a href="#">服务条款</a></li>
          <li><a href="#">隐私政策</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-title">
          合作伙伴
        </div>
        <ul>
          <li><a href="#">火山引擎</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-title">
          关于我们
        </div>
        <ul>
          <li><a href="#">公司介绍</a></li>
          <li><a href="#">渠道合作</a></li>
          <li><a href="#">联系我们</a></li>
          <li><a href="#">需求反馈</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div> Copyright © 2023-2025 <a href="https://dmxapi.cn">DMXAPI</a> All Rights Reserved.</div>
    </div>
  </footer>
</template>

<style>
.custom-footer {
  width: 100vw;
  min-width: 100vw;
  position: relative;
  background: #fafbfc;
  padding: 40px 0 0 0;
  font-size: 14px;
  color: #222;
  border-top: 1px solid #f0f0f0;
}
.footer-main {
  display: flex;
  justify-content: center;
  gap: 60px;
  max-width: 1200px;
  margin: 0 auto;
  flex-wrap: wrap;
}
.footer-col {
  min-width: 180px;
  margin-bottom: 20px;
}
.footer-title {
  font-weight: 600;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  color: #222;
  font-size: 15px;
}
.footer-icon {
  font-size: 18px;
  margin-right: 6px;
}
.footer-col ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.footer-col li {
  margin-bottom: 8px;
}
.footer-col a {
  color: #222;
  text-decoration: none;
  transition: color 0.2s;
  font-size: 14px;
}
.footer-col a:hover {
  color: #1e90ff;
  text-decoration: underline;
}
.footer-bottom {
  text-align: center;
  color: #888;
  font-size: 13px;
  padding: 24px 0 12px 0;
  border-top: 1px solid #eee;
  margin-top: 16px;
  line-height: 1.8;
}
@media (max-width: 900px) {
  .footer-main {
    flex-direction: column;
    align-items: center;
    gap: 24px;
  }
  .footer-col {
    min-width: 0;
    width: 100%;
    max-width: 340px;
  }
}
.page-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.page-wrapper > *:last-child {
  margin-top: auto;
}
</style>

# 投稿

> 欢迎向**狱望**投稿监狱人文艺术相关内容。所有稿件将经过审核后发布。

<div class="submit-form-wrap">
  <div class="form-title">提交稿件</div>
  <div class="form-desc">请填写以下信息。稿件内容需与监狱人文艺术相关，我们将在 7 个工作日内完成审核并以邮件通知结果。</div>

  <form id="submitForm" action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
    <label>署名 / 笔名 *</label>
    <input type="text" name="author" placeholder="你的名字或笔名" required>

    <label>联系邮箱 *</label>
    <input type="email" name="email" placeholder="用于接收审核结果通知" required>

    <label>文章标题 *</label>
    <input type="text" name="title" placeholder="稿件标题" required>

    <label>分类</label>
    <select name="category">
      <option value="art">艺术介入监狱</option>
      <option value="photo">监狱摄影</option>
      <option value="painting">监狱绘画</option>
      <option value="poetry">监狱诗歌</option>
      <option value="travel">监狱旅游</option>
      <option value="history">监狱历史</option>
      <option value="music">监狱音乐</option>
      <option value="misc">杂谈</option>
      <option value="other">其他</option>
    </select>

    <label>正文内容 *</label>
    <textarea name="content" placeholder="在此撰写或粘贴稿件内容。支持 Markdown 格式。" required></textarea>

    <label>配图链接（可选）</label>
    <input type="url" name="images" placeholder="图片 URL，多张请换行">

    <label>来源 / 参考链接（可选）</label>
    <input type="url" name="source" placeholder="如果是编译/翻译内容，请注明来源">

    <button type="submit" class="form-submit">提交稿件</button>
  </form>

  <div class="form-note">
    <strong>投稿须知：</strong><br>
    · 稿件内容需与监狱人文艺术相关（文学、摄影、绘画、音乐、历史、改造项目等）<br>
    · 原创首发优先，编译/翻译请注明来源<br>
    · 内容需遵守相关法律法规，不含敏感或不当信息<br>
    · 投稿即授权「狱望」在 prison-art.cn 发布<br>
    · 审核通过后，内容将发布在对应分类栏目中<br>
    · 如有疑问，可发送邮件至 <a href="mailto:editor@prison-art.cn" style="color:#d4b896;">editor@prison-art.cn</a>
  </div>
</div>

<script>
  // Form submission handler with client-side validation
  document.getElementById('submitForm').addEventListener('submit', function(e) {
    // Basic content check
    var content = this.querySelector('[name="content"]').value;
    var sensitiveWords = ['暴力', '血腥', '色情', '恐怖', '极端'];
    var hasSensitive = sensitiveWords.some(function(w) {
      return content.indexOf(w) !== -1;
    });
    if (hasSensitive) {
      alert('稿件可能包含敏感内容，请检查后重新提交。如有疑问请联系编辑。');
      e.preventDefault();
      return;
    }
    // Show loading state
    var btn = this.querySelector('.form-submit');
    btn.textContent = '提交中…';
    btn.disabled = true;
  });
</script>

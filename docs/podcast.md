# 播客

狱望播客不定期更新，聊监狱、艺术、人与自由。收听请前往小宇宙。

<div id="podcast-list" style="margin-top: 24px;">
  <p style="color:#666; font-style:italic;">加载中……</p>
</div>

<a href="https://www.xiaoyuzhoufm.com/podcast/621cf7fe27b4cb4fefc0045e" target="_blank" style="display:inline-block; margin-top:16px; color:#c8001e; font-size:13px;">→ 在小宇宙订阅狱望播客</a>

<script>
(function() {
  var rss = 'https://feed.xyzfm.space/ry77fdfyrkwt';
  var proxy = 'https://api.allorigins.win/get?url=' + encodeURIComponent(rss);

  fetch(proxy)
    .then(function(r) { return r.json(); })
    .then(function(data) {
      var parser = new DOMParser();
      var xml = parser.parseFromString(data.contents, 'text/xml');
      var items = xml.querySelectorAll('item');
      var container = document.getElementById('podcast-list');
      if (!items.length) {
        container.innerHTML = '<p style="color:#666;">暂无节目</p>';
        return;
      }
      var html = '';
      items.forEach(function(item) {
        var title = item.querySelector('title') ? item.querySelector('title').textContent : '';
        var link = item.querySelector('link') ? item.querySelector('link').textContent : '#';
        var pubDate = item.querySelector('pubDate') ? item.querySelector('pubDate').textContent.slice(0, 16) : '';
        var desc = item.querySelector('description') ? item.querySelector('description').textContent.replace(/<[^>]+>/g, '').trim().slice(0, 120) + '…' : '';
        html += '<div style="border-top:1px solid #2a2520; padding:20px 0;">';
        html += '<div style="font-family:monospace; font-size:11px; color:#555; margin-bottom:6px;">' + pubDate + '</div>';
        html += '<a href="' + link + '" target="_blank" style="font-size:15px; font-weight:600; color:#f0ebe0; text-decoration:none; border:none;">' + title + '</a>';
        if (desc) html += '<p style="font-size:13px; color:#888; line-height:1.8; margin:8px 0 0;">' + desc + '</p>';
        html += '</div>';
      });
      container.innerHTML = html;
    })
    .catch(function() {
      document.getElementById('podcast-list').innerHTML =
        '<p style="color:#666;">加载失败，请直接访问 <a href="https://www.xiaoyuzhoufm.com/podcast/621cf7fe27b4cb4fefc0045e" target="_blank" style="color:#c8001e;">小宇宙</a> 收听。</p>';
    });
})();
</script>

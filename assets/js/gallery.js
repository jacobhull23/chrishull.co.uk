// Gallery: renders paintings.json as a justified grid, region filters, and a lightbox.
// All paths are relative so the site works both on *.github.io/chrishull.co.uk/ and at the apex domain.
(function () {
  'use strict';

  var gallery = document.getElementById('gallery');
  var filterButtons = Array.prototype.slice.call(document.querySelectorAll('[data-filter]'));
  var lb = document.getElementById('lightbox');
  var lbImg = document.getElementById('lb-img');
  var lbWebp = document.getElementById('lb-webp');
  var lbTitle = document.getElementById('lb-title');
  var lbMeta = document.getElementById('lb-meta');
  var lbCount = document.getElementById('lb-count');
  var lbEnquire = document.getElementById('lb-enquire');
  var lbStage = document.getElementById('lb-stage');

  var paintings = [];
  var visible = [];   // indexes into paintings for the current filter
  var current = -1;   // position within `visible`
  var lastFocus = null;

  function slug(s) { return s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''); }
  // Image variants from scripts/build-images.py: full-size JPEG/WebP plus 800px-wide copies in images/800/.
  function src(p) { return 'images/' + p.file; }
  function stem(p) { return p.file.replace(/\.jpg$/i, ''); }
  function webp(p) { return 'images/' + stem(p) + '.webp'; }
  function srcset(p, ext) {
    var small = 'images/800/' + stem(p) + ext + ' 800w';
    return p.w > 800 ? small + ', images/' + stem(p) + ext + ' ' + p.w + 'w' : small;
  }
  var TILE_SIZES = '(max-width: 700px) calc(100vw - 32px), (max-width: 1100px) 45vw, 420px';
  function altText(p) { return p.alt || ('Watercolour painting of ' + p.title); }

  function render() {
    var frag = document.createDocumentFragment();
    paintings.forEach(function (p, i) {
      var li = document.createElement('li');
      li.className = 'tile';
      li.dataset.region = slug(p.region);
      li.style.setProperty('--r', (p.w / p.h).toFixed(4));

      var a = document.createElement('a');
      a.href = src(p);
      a.dataset.index = i;

      var fig = document.createElement('figure');
      var frame = document.createElement('div');
      frame.className = 'frame';
      var pic = document.createElement('picture');
      var source = document.createElement('source');
      source.type = 'image/webp';
      source.srcset = srcset(p, '.webp');
      source.sizes = TILE_SIZES;
      var img = document.createElement('img');
      img.src = 'images/800/' + p.file;
      img.srcset = srcset(p, '.jpg');
      img.sizes = TILE_SIZES;
      img.alt = altText(p);
      img.width = p.w;
      img.height = p.h;
      img.loading = i < 8 ? 'eager' : 'lazy';
      img.decoding = 'async';
      pic.appendChild(source);
      pic.appendChild(img);
      frame.appendChild(pic);

      var cap = document.createElement('figcaption');
      cap.textContent = p.title;

      fig.appendChild(frame);
      fig.appendChild(cap);
      a.appendChild(fig);
      li.appendChild(a);
      frag.appendChild(li);
    });
    gallery.appendChild(frag);
  }

  // ---------- Filters ----------
  var counts = { all: 0 };
  function applyFilter(key) {
    if (!filterButtons.some(function (b) { return b.dataset.filter === key; })) key = 'all';
    filterButtons.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.filter === key)); });
    visible = [];
    Array.prototype.forEach.call(gallery.children, function (li, i) {
      var show = key === 'all' || li.dataset.region === key;
      li.hidden = !show;
      if (show) visible.push(i);
    });
  }
  function addCounts() {
    paintings.forEach(function (p) {
      var k = slug(p.region);
      counts[k] = (counts[k] || 0) + 1;
      counts.all++;
    });
    filterButtons.forEach(function (b) {
      var n = counts[b.dataset.filter] || 0;
      var span = document.createElement('span');
      span.className = 'count';
      span.textContent = n;
      b.appendChild(span);
    });
  }
  filterButtons.forEach(function (b) {
    b.addEventListener('click', function () {
      var key = b.dataset.filter;
      applyFilter(key);
      history.replaceState(null, '', key === 'all' ? location.pathname + location.search : '#' + key);
    });
  });

  // ---------- Lightbox ----------
  function show(pos) {
    var n = visible.length;
    current = (pos + n) % n;
    var p = paintings[visible[current]];
    lbWebp.srcset = webp(p);
    lbImg.src = src(p);
    lbImg.alt = altText(p);
    lbImg.width = p.w;
    lbImg.height = p.h;
    lbTitle.textContent = p.title;
    lbMeta.textContent = 'Original watercolour · ' + p.region;
    lbCount.textContent = (current + 1) + ' / ' + n;
    lbEnquire.href = 'contact.html?painting=' + encodeURIComponent(p.title);
    // Warm the cache for neighbours so arrowing through feels instant.
    [1, -1].forEach(function (d) {
      var q = paintings[visible[(current + d + n) % n]];
      new Image().src = webp(q);
    });
  }
  function open(index) {
    var pos = visible.indexOf(index);
    if (pos < 0) return;
    lastFocus = document.activeElement;
    show(pos);
    if (typeof lb.showModal === 'function') lb.showModal(); else lb.setAttribute('open', '');
    document.body.style.overflow = 'hidden';
    document.getElementById('lb-close').focus();
  }
  function close() {
    if (lb.open && typeof lb.close === 'function') lb.close(); else lb.removeAttribute('open');
  }
  lb.addEventListener('close', function () {
    document.body.style.overflow = '';
    if (lastFocus) lastFocus.focus();
  });

  gallery.addEventListener('click', function (e) {
    var a = e.target.closest('a[data-index]');
    if (!a || e.metaKey || e.ctrlKey || e.shiftKey || e.button === 1) return;
    e.preventDefault();
    open(Number(a.dataset.index));
  });
  document.getElementById('lb-close').addEventListener('click', close);
  document.getElementById('lb-prev').addEventListener('click', function () { show(current - 1); });
  document.getElementById('lb-next').addEventListener('click', function () { show(current + 1); });
  // Click on the empty backdrop area closes.
  lbStage.addEventListener('click', function (e) { if (e.target === lbStage) close(); });

  lb.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') { e.preventDefault(); show(current - 1); }
    else if (e.key === 'ArrowRight') { e.preventDefault(); show(current + 1); }
  });

  // Swipe (touch) — horizontal swipes change painting, vertical scrolls are left alone.
  var sx = null, sy = null;
  lbStage.addEventListener('touchstart', function (e) {
    if (e.touches.length !== 1) { sx = null; return; }
    sx = e.touches[0].clientX; sy = e.touches[0].clientY;
  }, { passive: true });
  lbStage.addEventListener('touchend', function (e) {
    if (sx === null) return;
    var dx = e.changedTouches[0].clientX - sx;
    var dy = e.changedTouches[0].clientY - sy;
    sx = null;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) show(current + (dx < 0 ? 1 : -1));
  }, { passive: true });

  // ---------- Boot ----------
  fetch('paintings.json')
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (data) {
      paintings = data;
      render();
      addCounts();
      applyFilter(location.hash.slice(1) || 'all');
    })
    .catch(function () {
      gallery.outerHTML = '<p class="gallery-empty">Sorry, the paintings could not be loaded. Please refresh the page.</p>';
    });
})();

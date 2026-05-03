(function () {
  'use strict';

  // Don't run on the landing page — it has its own entrance animations
  if (document.querySelector('.split')) return;

  var SELECTORS = [
    '.section-eyebrow',
    '.section-title',
    '.section-sub',
    '.hero-eyebrow',
    '.feature-card',
    '.service-card',
    '.stat-item',
    '.process-step',
    '.portfolio-item',
    '.gallery-item',
    '.article-card',
    '.cert-item',
    '.value-item',
    '.team-member'
  ].join(', ');

  function init() {
    if (!window.IntersectionObserver) return;
    var els = Array.prototype.slice.call(document.querySelectorAll(SELECTORS));
    if (!els.length) return;

    els.forEach(function (el) {
      // Skip if already in view on load (above the fold)
      var rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight - 40) return;

      el.classList.add('reveal');

      // Stagger sibling cards within the same parent
      var par = el.parentElement;
      if (par) {
        var cls = el.classList[0];
        var siblings = Array.prototype.slice.call(par.children).filter(function (c) {
          return c.classList.contains(cls);
        });
        var idx = siblings.indexOf(el);
        if (idx > 0 && idx <= 4) {
          el.classList.add('reveal-delay-' + idx);
        }
      }
    });

    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          obs.unobserve(entry.target);
        }
      });
    }, {
      rootMargin: '0px 0px -50px 0px',
      threshold: 0.07
    });

    els.forEach(function (el) {
      if (el.classList.contains('reveal')) obs.observe(el);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

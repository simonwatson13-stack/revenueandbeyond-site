/* Revenue & Beyond: Google Analytics 4 with a cookie consent banner.
   To switch on, put the GA4 Measurement ID below (starts with "G-").
   While it is empty, this file does nothing: no banner, no tracking.

   How it works (Google Consent Mode v2, "advanced"):
   - Analytics storage starts DENIED for everyone, so no GA cookies are set.
   - GA still receives cookieless pings, which Google uses to model visits.
   - If the visitor clicks Accept, analytics cookies are allowed and the
     choice is remembered for 6 months. Decline is remembered too.
   - Advertising signals are always denied; this site does not run ads.
   - Any element with data-cookie-settings reopens the banner. */
(function () {
  var GA_ID = 'G-SVSFC2VLL9';
  if (!GA_ID) return;
  document.documentElement.classList.add('rb-ga');

  var KEY = 'rb_consent', MAX_AGE = 182 * 864e5;
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;

  function saved() {
    try {
      var v = JSON.parse(localStorage.getItem(KEY) || 'null');
      if (v && v.t && Date.now() - v.t < MAX_AGE) return v.c;
    } catch (e) {}
    return null;
  }
  function save(c) { try { localStorage.setItem(KEY, JSON.stringify({ c: c, t: Date.now() })); } catch (e) {} }

  var choice = saved();
  gtag('consent', 'default', {
    analytics_storage: choice === 'granted' ? 'granted' : 'denied',
    ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied',
    wait_for_update: 500
  });
  gtag('js', new Date());
  gtag('config', GA_ID);

  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GA_ID);
  document.head.appendChild(s);

  function set(c) {
    save(c);
    gtag('consent', 'update', { analytics_storage: c });
    hide();
  }

  var bar;
  function css() {
    if (document.getElementById('rbCkCss')) return;
    var st = document.createElement('style');
    st.id = 'rbCkCss';
    st.textContent =
      '.rb-ck{position:fixed;left:16px;bottom:16px;z-index:60;max-width:380px;background:#fff;border:2px solid #0B363B;border-radius:16px;box-shadow:5px 5px 0 #0B363B;padding:18px 20px;font:14px/1.55 Inter,system-ui,sans-serif;color:#1C1C1C;transform:translateY(12px);opacity:0;transition:opacity .2s,transform .2s}' +
      '.rb-ck.on{transform:none;opacity:1}' +
      '.rb-ck b{display:block;color:#0B363B;font-weight:800;margin-bottom:4px}' +
      '.rb-ck p{margin:0 0 14px}' +
      '.rb-ck a{color:#0B363B;font-weight:700}' +
      '.rb-ck .row{display:flex;gap:10px;flex-wrap:wrap}' +
      '.rb-ck button{font:800 13px Inter,system-ui,sans-serif;border-radius:999px;padding:10px 18px;cursor:pointer;border:2px solid #0B363B}' +
      '.rb-ck .yes{background:#49E8B0;color:#0B363B}' +
      '.rb-ck .no{background:#fff;color:#0B363B}' +
      '.rb-ck button:focus-visible{outline:3px solid #6AD1FA;outline-offset:2px}' +
      '@media (max-width:480px){.rb-ck{left:12px;right:12px;bottom:12px;max-width:none}}';
    document.head.appendChild(st);
  }
  function show() {
    css();
    if (!bar) {
      bar = document.createElement('div');
      bar.className = 'rb-ck';
      bar.setAttribute('role', 'region');
      bar.setAttribute('aria-label', 'Cookie preferences');
      bar.innerHTML =
        '<b>Cookies</b><p>I use Google Analytics to see which pages are useful. It only sets cookies if you say yes. ' +
        '<a href="/privacy-policy.html#cookies">Privacy policy</a></p>' +
        '<div class="row"><button type="button" class="yes">Accept</button><button type="button" class="no">Decline</button></div>';
      bar.querySelector('.yes').addEventListener('click', function () { set('granted'); });
      bar.querySelector('.no').addEventListener('click', function () { set('denied'); });
      document.body.appendChild(bar);
    }
    bar.hidden = false;
    requestAnimationFrame(function () { bar.classList.add('on'); });
  }
  function hide() {
    if (!bar) return;
    bar.classList.remove('on');
    setTimeout(function () { bar.hidden = true; }, 200);
  }

  function init() {
    if (choice === null) show();
    document.addEventListener('click', function (e) {
      var t = e.target.closest && e.target.closest('[data-cookie-settings]');
      if (t) { e.preventDefault(); show(); }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();

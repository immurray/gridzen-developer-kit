(() => {
  'use strict';
  const supported = ['en', 'es', 'zh'];
  const query = new URLSearchParams(location.search);
  let lang = query.get('lang');
  if (!supported.includes(lang)) {
    try { const ref = new URL(document.referrer); if (ref.origin === location.origin) lang = /^\/(es|zh)\//.exec(ref.pathname)?.[1] || new URLSearchParams(ref.search).get('lang'); } catch (_) {}
    try { if (!supported.includes(lang)) lang = localStorage.getItem('gz-lang'); } catch (_) {}
  }
  if (!supported.includes(lang)) lang = 'en';
  document.body.dataset.locale = lang;
  window.gzGetLang = () => lang;
  window.gzOnLangChange = callback => callback();
  const dictionary = window.GZ_DEVELOPER_LOCALES[lang];
  for (const node of document.querySelectorAll('[data-i18n]')) {
    if (dictionary[node.dataset.i18n]) node.innerHTML = dictionary[node.dataset.i18n];
  }
  function localizeLinks(root) {
    for (const a of root.querySelectorAll('a[href]')) {
      const raw = a.getAttribute('href'); if (raw.startsWith('#')) continue;
      const url = new URL(raw, location.href); if (url.origin !== location.origin) continue;
      if (url.pathname.startsWith('/developers/') && !url.pathname.includes('/downloads/') && !url.pathname.includes('/api/') && !url.pathname.endsWith('.json')) url.searchParams.set('lang', lang);
      else if (/^\/(docs|trust-decision-api|contact|skills|research|guides|provider-packs|solutions)(\/|$)/.test(url.pathname) && lang !== 'en') url.pathname = '/' + lang + url.pathname;
      a.setAttribute('href', url.pathname + url.search + url.hash);
    }
  }
  localizeLinks(document);
  async function getShell(path) { const response = await fetch(path, {signal: AbortSignal.timeout(5000)}); if (!response.ok) throw Error('Shared shell unavailable'); return response.json(); }
  window.GridzenShellReady = getShell('/assets/site-shell.json').catch(() => getShell('/developers/site-shell.json')).then(shell => {
    const current = shell.languages[lang];
    document.getElementById('gz-nav').innerHTML = current.nav;
    document.getElementById('gz-foot').innerHTML = current.footer;
    for (const a of document.querySelectorAll('#gz-nav .lang a')) {
      const target = new URL(location.href); target.searchParams.set('lang', a.lang);
      a.href = target.pathname + target.search + target.hash;
    }
    // Website measurement is implemented by the main site; developer counters remain independent.
    document.querySelector('#gz-foot #measurement-toggle')?.remove();
    const subnav = document.createElement('nav'); subnav.className = 'developer-subnav'; subnav.setAttribute('aria-label', dictionary['shell.overview']);
    for (const [path, key] of [['/developers/', 'shell.overview'], ['/developers/quickstart.html', 'shell.quickstart'], ['/developers/harnesses.html', 'shell.assistant']]) {
      const a = document.createElement('a'); a.href = path + '?lang=' + lang; a.textContent = dictionary[key];
      if (location.pathname === path) a.setAttribute('aria-current', 'page'); subnav.append(a);
    }
    document.querySelector('main').prepend(subnav);
    return true;
  }).catch(() => { document.getElementById('gz-nav').innerHTML = '<nav class="site-nav"><div class="site-nav-in"><a class="brand" href="' + (lang === 'en' ? '/' : '/' + lang + '/') + '"><i></i>GridZen</a></div></nav>'; return false; });
})();

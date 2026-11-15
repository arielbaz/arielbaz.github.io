/**
 * Pages traduites (anglais, hébreu) : accueil, services, pages de service,
 * à propos, contact. Même mise en page et mêmes classes CSS que les pages
 * françaises ; seuls les textes et le sens de lecture changent.
 *
 * Le module ne dépend que de ce que le générateur lui passe (ctx), ce qui
 * permet de le tester seul.
 */
import { I18N } from './i18n-data.mjs';

export const LANGS = ['en', 'he'];
const ORDER = ['fr', 'en', 'he'];
const SHORT = { fr: 'FR', en: 'EN', he: 'עב' };
const LABEL = { fr: 'Français', en: 'English', he: 'עברית' };
const FAMILY_ICON = { electronics: 'chip', events: 'heart', web: 'globe', systems: 'layers' };

/* ----- chemins des pages équivalentes dans chaque langue ----- */
export const PATHS = {
  home: { fr: '/', en: '/en/', he: '/he/' },
  services: { fr: '/services.html', en: '/en/services.html', he: '/he/services.html' },
  about: { fr: '/apropos.html', en: '/en/about.html', he: '/he/about.html' },
  contact: { fr: '/contact.html', en: '/en/contact.html', he: '/he/contact.html' },
  filter: { fr: '/services/filtres/', en: '/en/services/filtres/', he: '/he/services/filtres/' },
  invitation: { fr: '/invitation.html', en: '/en/invitation.html', he: '/he/invitation.html' },
};
export function servicePaths(SLUG, item) {
  const s = SLUG(item.title);
  return { fr: `/services/${s}.html`, en: `/en/services/${s}.html`, he: `/he/services/${s}.html` };
}

/* ----- sélecteur de langue et balises hreflang ----- */
export function langSwitchHtml(current, paths) {
  return `<div class="lang-switch nav-lang" role="group" aria-label="Language">${ORDER.map((l) => (l === current
    ? `<span aria-current="true">${SHORT[l]}</span>`
    : `<a href="${paths[l]}" hreflang="${l}" lang="${l}" title="${LABEL[l]}">${SHORT[l]}</a>`)).join('')}</div>`;
}
export function hreflangLinks(siteUrl, paths) {
  return `${ORDER.map((l) => `<link rel="alternate" hreflang="${l}" href="${siteUrl}${paths[l]}">`).join('\n')}\n<link rel="alternate" hreflang="x-default" href="${siteUrl}${paths.fr}">`;
}

/* ----- éléments communs (menu, pied de page, bandeau, bouton WhatsApp) ----- */
function chrome(ctx, lang, active, paths) {
  const { SITE, icon, esc } = ctx;
  const T = I18N[lang].ui;
  const wa = `${SITE.waDirect}?text=${encodeURIComponent(T.waIntro)}`;
  const links = [
    [PATHS.home[lang], T.nav.home, 'home'],
    [PATHS.services[lang], T.nav.services, 'services'],
    [PATHS.contact[lang], T.nav.contact, 'contact'],
    [PATHS.about[lang], T.nav.about, 'about'],
  ];
  const nav = `<a class="skip-link" href="#contenu">${esc(T.skip)}</a>
<header class="nav">
  <div class="nav-inner">
      <button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-controls="menu" aria-label="${esc(T.menu)}">
        <svg class="i-menu" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
        <svg class="i-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>
        <span class="nav-toggle-label"><span class="l-open">${esc(T.menu)}</span><span class="l-close">${esc(T.close)}</span></span>
      </button>
    <a class="brand" href="${PATHS.home[lang]}" aria-label="${esc(T.homeAria)}">
      <img src="/assets/img/logo.svg" alt="${SITE.name}" width="100" height="27">
    </a>
    <nav class="nav-links" id="menu" aria-label="${esc(T.navAria)}">
      ${links.map(([href, label, key]) => `<a href="${href}"${active === key ? ' aria-current="page"' : ''}>${esc(label)}</a>`).join('\n      ')}
      <a class="nav-cta" href="${wa}" target="_blank" rel="noopener"><span>${esc(T.quote)}</span> ${icon('arrow-up-right', 'ico-inline')}</a>
    </nav>
    <div class="nav-actions">
      ${langSwitchHtml(lang, paths)}
      <a class="icon-btn" href="/feed.xml" aria-label="${esc(T.rss)}" title="${esc(T.rss)}">${icon('rss')}</a>
      <button class="icon-btn" type="button" data-theme-toggle aria-label="${esc(T.theme)}">${icon('sun')}</button>
    </div>
  </div>
</header>`;

  const F = T.footer;
  const footer = `<footer class="footer">
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
        <a class="brand" href="${PATHS.home[lang]}"><img src="/assets/img/logo.svg" alt="${SITE.name}" width="104" height="32"></a>
        <p>${esc(F.blurb)}</p>
      </div>
      <div class="footer-cols">
        <div class="footer-col">
          <h4>${esc(F.explore)}</h4>
          <a href="${PATHS.home[lang]}">${esc(F.home)}</a>
          <a href="${PATHS.services[lang]}">${esc(F.services)}</a>
          <a href="${PATHS.filter[lang]}">${esc(F.filter)}</a>
          <a href="${PATHS.invitation[lang]}">${esc(F.invitation)}</a>
          <a href="${PATHS.about[lang]}">${esc(F.about)}</a>
          <a href="${PATHS.contact[lang]}">${esc(F.contact)}</a>
          <a href="/feed.xml">${esc(F.rss)}</a>
        </div>
        <div class="footer-col">
          <h4>${esc(F.follow)}</h4>
          <a href="${SITE.whatsapp}" target="_blank" rel="noopener">${esc(F.channel)}</a>
          <a href="${SITE.waDirect}" target="_blank" rel="noopener">${esc(F.direct)}</a>
          <a href="mailto:${SITE.email}">${SITE.email}</a>
          <a href="${SITE.linkedin}" target="_blank" rel="noopener">LinkedIn</a>
          <a href="${SITE.github}" target="_blank" rel="noopener">GitHub</a>
        </div>
      </div>
    </div>
    <div class="footer-word" aria-hidden="true">ARIBAZ</div>
    <div class="footer-bottom">
      <span>© ${new Date().getFullYear()} ${SITE.name}. ${esc(F.bottom)}</span>
      <span><a href="/feed.xml">RSS</a> · <a href="${SITE.github}" target="_blank" rel="noopener">${esc(F.source)}</a></span>
    </div>
  </div>
</footer>
<a class="btn btn-wa wa-fab" href="${wa}" target="_blank" rel="noopener" aria-label="${esc(T.quoteAria)}">${icon('whatsapp')} ${esc(T.quote)}</a>`;

  const C = T.cta;
  const cta = `<section class="section-tight"><div class="wrap">
  <div class="cta-band reveal">
    <h2>${esc(C.title)}</h2>
    <p>${esc(C.text)}</p>
    <div class="hero-actions" style="margin-bottom:0">
      <a class="btn btn-wa" href="${SITE.whatsapp}" target="_blank" rel="noopener">${icon('whatsapp')} ${esc(C.join)}</a>
      <a class="btn btn-ghost" href="/feed.xml">${icon('rss')} ${esc(C.rss)}</a>
    </div>
  </div>
</div></section>`;
  return { nav, footer, cta, wa };
}

function shell(ctx, lang, { title, description, url, paths, extra = '' }, inner, active, ch) {
  const L = I18N[lang];
  const head = ctx.head({
    title, description, url, lang, dir: L.dir, locale: L.locale,
    extra: `${hreflangLinks(ctx.SITE.url, paths)}${extra ? '\n' + extra : ''}`,
  });
  return `${head}${ch.nav}
<main id="contenu">
${inner}
</main>
${ch.footer}
<script src="/assets/js/app.js" defer></script>
</body>
</html>`;
}

function faqJsonLd(faq) {
  const data = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faq.map(([q, a]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } })),
  };
  return `<script type="application/ld+json">${JSON.stringify(data).replace(/</g, '\\u003c')}</script>`;
}

/* ----- données : un service et sa famille dans la langue voulue ----- */
function tr(lang, item) {
  const t = I18N[lang].items[item.title];
  return t || { title: item.title, text: item.text, detail: item.text, includes: item.bullets, delai: '' };
}
function itemUrl(SLUG, lang, item) {
  if (item.href === '/services/filtres/') return PATHS.filter[lang];
  if (item.href === '/invitation.html') return PATHS.invitation[lang];
  return item.href || servicePaths(SLUG, item)[lang];
}

/* ======================================================================= */
/* Accueil                                                                  */
/* ======================================================================= */
function homePage(ctx, lang) {
  const { SITE, icon, esc, SERVICES, filterApp, articleCards } = ctx;
  const L = I18N[lang]; const H = L.home; const P = H.product;
  const ch = chrome(ctx, lang, 'home', PATHS.home);
  const cards = articleCards ? articleCards(lang) : '';
  const inner = `  <section class="hero">
    <div class="hero-bg" aria-hidden="true"><span class="blob b1"></span><span class="blob b2"></span><span class="blob b3"></span></div>
    <span class="hero-float f1" aria-hidden="true">${icon('wrench')} ${esc(H.floats[0])}</span>
    <span class="hero-float f2" aria-hidden="true">${icon('check')} ${esc(H.floats[1])}</span>
    <span class="hero-float f3" aria-hidden="true">${icon('code')} ${esc(H.floats[2])}</span>
    <div class="wrap">
      <span class="eyebrow"><span class="dot"></span>${esc(H.eyebrow)}</span>
      <h1 class="display" style="max-width:20ch">
        <span class="line"><span>${esc(H.h1a)}</span></span>
        <span class="line"><span><span class="gradient-text">${esc(H.h1b)}</span></span></span>
      </h1>
      <p class="lede">${esc(H.lede)}</p>
      <div class="hero-actions">
        <a class="btn btn-wa" href="${ch.wa}" target="_blank" rel="noopener">${icon('whatsapp')} ${esc(H.primary)}</a>
        <a class="btn btn-ghost" href="${PATHS.services[lang]}">${esc(H.secondary)} ${icon('arrow', 'arr')}</a>
      </div>
      <div class="hero-meta">
        <span>${icon('clock')} ${esc(H.meta[0])}</span>
        <span>${icon('check')} ${esc(H.meta[1])}</span>
        <span>${icon('shield')} ${esc(H.meta[2])}</span>
        <span>${icon('heart')} ${esc(H.meta[3])}</span>
      </div>
    </div>
  </section>

  <section class="section" style="padding-bottom:0">
    <div class="wrap">
      <div class="pf reveal">
        <div class="pf-body">
          <div class="pf-badges"><span class="pill">${esc(P.pill)}</span><span class="pf-new">${esc(P.badge)}</span></div>
          <h2>${esc(P.name)}</h2>
          <p class="pf-tag">${esc(P.tag)}</p>
          <p>${esc(P.text)}</p>
          <ul class="pf-chips">${P.chips.map((c) => `<li>${esc(c)}</li>`).join('')}</ul>
          <div class="hero-actions" style="margin-bottom:0;justify-content:flex-start">
            <a class="btn btn-primary" href="${PATHS.filter[lang]}">${esc(P.more)} ${icon('arrow', 'arr')}</a>
            <a class="btn btn-ghost" href="${filterApp}/">${esc(P.start)}</a>
          </div>
        </div>
        <div class="pf-art" aria-hidden="true">${icon('eye')}</div>
      </div>
    </div>
  </section>

${ctx.logoStrip ? `  <section class="section" style="padding-block:6px 0">
    <div class="wrap">
      <p class="logos-label">${esc(H.logosLabel)}</p>
      ${ctx.logoStrip()}
    </div>
  </section>

` : ''}  <section class="section">
    <div class="wrap">
      <div class="section-head">
        <div><h2>${esc(H.servicesH)}</h2><p>${esc(H.servicesSub)}</p></div>
        <a class="link-arrow" href="${PATHS.services[lang]}">${esc(H.seeAll)} ${icon('arrow', 'arr')}</a>
      </div>
      <div class="value-grid value-grid-4">
        ${SERVICES.map((f) => `<a class="value reveal" href="${PATHS.services[lang]}#${f.slug}" style="text-decoration:none;color:inherit">
          <div class="ico" style="background:var(--bg-soft)">${icon(FAMILY_ICON[f.slug] || 'layers')}</div>
          <h3>${esc(f.brand)}</h3>
          <p><strong>${esc(L.families[f.slug].tagline)}</strong> ${esc(L.families[f.slug].desc)}</p>
        </a>`).join('\n        ')}
      </div>
    </div>
  </section>
${cards ? `
  <section class="section" style="padding-top:0">
    <div class="wrap">
      <div class="section-head"><div><h2>${esc(H.articlesH)}</h2><p>${esc(H.articlesSub)}</p></div></div>
      <div class="card-grid">${cards}</div>
    </div>
  </section>
` : ''}
  <section class="section" style="padding-top:0">
    <div class="wrap">
      <div class="cta-band reveal" style="background:linear-gradient(120deg,#0a1220,#131b33 55%,#1b1030)">
        <h2>${esc(H.band.title)}</h2>
        <p>${esc(H.band.text)}</p>
        <div class="hero-actions" style="margin-bottom:0">
          <a class="btn btn-primary" href="${PATHS.services[lang]}">${esc(H.band.primary)} ${icon('arrow', 'arr')}</a>
          <a class="btn btn-ghost" href="${PATHS.services[lang]}#contact">${esc(H.band.secondary)}</a>
        </div>
      </div>
    </div>
  </section>

  ${ch.cta}`;
  return shell(ctx, lang, { title: H.title, description: H.desc, url: PATHS.home[lang], paths: PATHS.home }, inner, 'home', ch);
}

/* ======================================================================= */
/* Services                                                                 */
/* ======================================================================= */
function servicesPage(ctx, lang) {
  const { SITE, icon, esc, SLUG, SERVICES } = ctx;
  const L = I18N[lang]; const S = L.services;
  const ch = chrome(ctx, lang, 'services', PATHS.services);
  const inner = `  <section class="page-hero">
    <div class="wrap">
      <span class="eyebrow"><span class="dot"></span>${esc(S.eyebrow)}</span>
      <h1 class="display" style="font-size:clamp(36px,6vw,64px);max-width:18ch">${esc(S.h1a)} <span class="gradient-text">${esc(S.h1b)}</span></h1>
      <p class="lede" style="margin-inline:0;max-width:52ch">${esc(S.lede)}</p>
      <div class="hero-meta" style="justify-content:flex-start">
        <span>${icon('check')} ${esc(S.meta[0])}</span>
        <span>${icon('clock')} ${esc(S.meta[1])}</span>
        <span>${icon('shield')} ${esc(S.meta[2])}</span>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:26px">
    <div class="wrap">
      ${SERVICES.map((f) => `<div class="family" id="${f.slug}" style="--brand:${f.color}">
        <div class="family-head">
          <span class="brand-dot" aria-hidden="true"></span>
          <div><span class="family-num">ARIBAZ</span><h2>${esc(f.brand.replace('ARIBAZ ', ''))}</h2></div>
        </div>
        <p><strong>${esc(L.families[f.slug].tagline)}</strong> ${esc(L.families[f.slug].desc)}</p>
        <ul class="pf-chips">${(L.families[f.slug].chips || []).map((c) => `<li>${esc(c)}</li>`).join('')}</ul>
        <div class="svc-grid">
          ${f.items.map((it, i) => {
            const t = tr(lang, it);
            return `<article class="svc reveal" style="--brand:${f.color};animation-delay:${i * 70}ms">
            <div class="svc-art">
              <span class="svc-tile">${icon(it.icon)}</span>
              <span class="svc-mini mini-a">${icon('clock')}</span>
              <span class="svc-mini mini-b">${icon('check')}</span>
            </div>
            <div class="svc-body">
              <span class="svc-brand">${esc(f.brand)}</span>
              <h3>${esc(t.title)}</h3>
              <p>${esc(t.text)}</p>
              <div class="svc-foot">
                <span>${esc(it.href ? S.tile.inHouse : S.tile.onQuote)}</span>
                <span style="display:inline-flex;align-items:center;gap:14px">
                  <a class="svc-more svc-open" href="${itemUrl(SLUG, lang, it)}">${esc(it.href ? S.tile.discover : S.tile.view)} ${icon('arrow', 'arr')}</a>
                </span>
              </div>
            </div>
          </article>`;
          }).join('')}
        </div>
      </div>`).join('\n      ')}
    </div>
  </section>

  <section class="section section-soft">
    <div class="wrap">
      <div class="section-head"><div><h2>${esc(S.stepsH)}</h2><p>${esc(S.stepsSub)}</p></div></div>
      <div class="steps">
        ${S.steps.map(([h, p]) => `<div class="step"><h3>${esc(h)}</h3><p>${esc(p)}</p></div>`).join('\n        ')}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap wrap-narrow">
      <div class="section-head"><div><h2>${esc(S.dontH)}</h2><p>${esc(S.dontSub)}</p></div></div>
      <ul class="dont" style="padding:0">
        ${S.dont.map(([b, t]) => `<li>${icon('check')}<span><b>${esc(b)}</b> ${esc(t)}</span></li>`).join('\n        ')}
      </ul>
    </div>
  </section>

  <section class="section" id="faq" style="padding-top:0">
    <div class="wrap wrap-narrow">
      <div class="section-head"><div><h2>${esc(S.faqH)}</h2><p>${esc(S.faqSub)}</p></div></div>
      <div class="inv-faq">
        ${S.faq.map(([q, a]) => `<details><summary>${esc(q)}</summary><p>${esc(a)}</p></details>`).join('')}
      </div>
    </div>
  </section>

  <section class="section" id="contact" style="padding-top:0">
    <div class="wrap">
      <div class="section-head"><div><h2>${esc(S.contactH)}</h2><p>${esc(S.contactSub)}</p></div></div>
      <div class="contact-grid">
        <div class="contact-card wa">
          <h3>${icon('whatsapp')} ${esc(S.wa.title)}</h3>
          <p>${esc(S.wa.text)} ${SITE.phone}</p>
          <a class="btn btn-wa" href="${ch.wa}" target="_blank" rel="noopener">${esc(S.wa.btn)} ${icon('arrow-up-right')}</a>
        </div>
        <div class="contact-card">
          <h3>${icon('link')} ${esc(S.mail.title)}</h3>
          <p>${esc(S.mail.text)}</p>
          <a class="btn btn-primary" href="mailto:${SITE.email}">${SITE.email}</a>
        </div>
      </div>
    </div>
  </section>

  ${ch.cta}`;
  return shell(ctx, lang, { title: S.title, description: S.desc, url: PATHS.services[lang], paths: PATHS.services, extra: faqJsonLd(S.faq) }, inner, 'services', ch);
}

/* ======================================================================= */
/* Page d'un service                                                        */
/* ======================================================================= */
function servicePage(ctx, lang, family, item) {
  const { SITE, icon, esc, SLUG } = ctx;
  const L = I18N[lang]; const V = L.service;
  const t = tr(lang, item);
  const paths = servicePaths(SLUG, item);
  const ch = chrome(ctx, lang, 'services', paths);
  const fam = L.families[family.slug];
  const siblings = family.items.filter((x) => x !== item);
  const waText = encodeURIComponent(V.waText + t.title);
  const subject = encodeURIComponent(V.subject + t.title);
  const inner = `  <section class="page-hero" style="--brand:${family.color}">
    <div class="wrap">
      <a class="eyebrow" href="${PATHS.services[lang]}#${family.slug}"><span class="dot" style="background:${family.color}"></span>${esc(family.brand)} · ${esc(V.all)}</a>
      <h1 class="display" style="font-size:clamp(34px,5.6vw,60px);max-width:20ch">${esc(t.title)}</h1>
      <p class="lede" style="margin-inline:0;max-width:56ch">${esc(t.detail)}</p>
      <div class="hero-actions" style="justify-content:flex-start">
        <a class="btn btn-wa" href="${SITE.waDirect}?text=${waText}" target="_blank" rel="noopener">${icon('whatsapp')} ${esc(V.quote)}</a>
        <a class="btn btn-ghost" href="mailto:${SITE.email}?subject=${subject}">${esc(V.email)}</a>
      </div>
      <div class="hero-meta" style="justify-content:flex-start;margin-top:26px">
        <span>${icon('clock')} ${esc(V.lead)}: ${esc(t.delai)}</span>
        <span>${icon('check')} ${esc(V.free)}</span>
        <span>${icon('shield')} ${esc(V.remote)}</span>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:12px">
    <div class="wrap wrap-narrow">
      <div class="section-head"><div><h2>${esc(V.included)}</h2><p>${esc(t.text)}</p></div></div>
      <ul class="dont" style="padding:0">
        ${t.includes.map((x) => `<li>${icon('check')}<span>${esc(x)}</span></li>`).join('\n        ')}
      </ul>
    </div>
  </section>

  <section class="section section-soft">
    <div class="wrap">
      <div class="section-head"><div><h2>${esc(V.how)}</h2></div></div>
      <div class="steps">
        ${V.steps.map(([h, p]) => `<div class="step"><h3>${esc(h)}</h3><p>${esc(p)}</p></div>`).join('\n        ')}
      </div>
    </div>
  </section>
${siblings.length ? `
  <section class="section">
    <div class="wrap wrap-narrow">
      <div class="section-head"><div><h2>${esc(V.sameHouse)}</h2><p>${esc(fam.tagline)}</p></div></div>
      <ul class="dont" style="padding:0">
        ${siblings.map((s) => { const st = tr(lang, s); return `<li>${icon('check')}<span><a href="${itemUrl(SLUG, lang, s)}"><b>${esc(st.title)}</b></a> — ${esc(st.text)}</span></li>`; }).join('\n        ')}
      </ul>
    </div>
  </section>
` : ''}
  <section class="section" style="padding-top:0">
    <div class="wrap wrap-narrow">
      <a class="btn btn-ghost" href="${PATHS.services[lang]}#${family.slug}">${L.dir === 'rtl' ? '→' : '←'} ${esc(V.fromHouse)}</a>
    </div>
  </section>

  ${ch.cta}`;
  return shell(ctx, lang, { title: `${t.title} — ${family.brand}`, description: t.text, url: paths[lang], paths }, inner, 'services', ch);
}

/* ======================================================================= */
/* À propos                                                                 */
/* ======================================================================= */
function aboutPage(ctx, lang) {
  const { SITE, icon, esc } = ctx;
  const A = I18N[lang].about;
  const ch = chrome(ctx, lang, 'about', PATHS.about);
  const U = I18N[lang].ui;
  const inner = `  <section class="page-hero">
    <div class="wrap about-hero">
      <div>
        <span class="eyebrow"><span class="dot"></span>${esc(A.eyebrow)}</span>
        <h1 class="display" style="max-width:22ch">${esc(A.h1a)} <span class="gradient-text">${esc(A.h1b)}</span></h1>
        <p class="lede" style="margin-inline:0">${esc(A.lede)}</p>
      </div>
      <figure class="about-photo" style="margin:0">
        <img src="/assets/img/ariel.png" alt="${esc(A.photoAlt)}" width="520" height="520" decoding="async">
        <span class="about-pill p1">${icon('clock')} ${esc(A.pills[0])}</span>
        <span class="about-pill p2">${icon('wrench')} ${esc(A.pills[1])}</span>
      </figure>
    </div>
  </section>

  <section class="section" style="padding-top:12px">
    <div class="wrap">
      <div class="about-grid">
        <div class="prose">
          <p class="lead">${esc(A.lead)}</p>
          <p>${esc(A.p1)}</p>

          <h2>${esc(A.doH)}</h2>
          ${A.do.map(([b, t]) => `<p><strong>${esc(b)}</strong> ${esc(t)}</p>`).join('\n          ')}
          <p><a class="link-arrow" href="${PATHS.services[lang]}">${esc(A.seeServices)} ${icon('arrow', 'arr')}</a></p>

          <h2>${esc(A.workH)}</h2>
          ${A.work.map(([b, t]) => `<p><strong>${esc(b)}</strong> ${esc(t)}</p>`).join('\n          ')}

          <div class="quote-block">${esc(A.quote)}</div>

          <h2>${esc(A.believeH)}</h2>
          ${A.believe.map((p) => `<p>${esc(p)}</p>`).join('\n          ')}

          <h2>${esc(A.restH)}</h2>
          <p>${esc(A.rest)}</p>

          <h2>${esc(A.whyH)}</h2>
          ${A.why.map((p) => `<p>${esc(p)}</p>`).join('\n          ')}
        </div>

        <aside>
          <div class="fact-list">
            ${A.facts.map(([n, l]) => `<div class="fact"><span class="n" data-count-to="${esc(n)}">0</span><span class="l">${esc(l)}</span></div>`).join('\n            ')}
          </div>
          <div style="margin-top:18px;display:grid;gap:10px">
            <a class="btn btn-primary" href="${PATHS.services[lang]}" style="width:100%">${esc(A.servicesBtn)} ${icon('arrow', 'arr')}</a>
            <a class="btn btn-ghost" href="${PATHS.contact[lang]}" style="width:100%">${esc(A.contactBtn)}</a>
            <a class="btn btn-ghost" href="${SITE.linkedin}" target="_blank" rel="noopener" style="width:100%">${icon('linkedin')} LinkedIn</a>
          </div>
        </aside>
      </div>

      <div class="value-grid" style="margin-top:56px">
        ${A.values.map(([ic, h, p]) => `<div class="value reveal"><div class="ico">${icon(ic)}</div><h3>${esc(h)}</h3><p>${esc(p)}</p></div>`).join('\n        ')}
      </div>

      <div class="hero-actions" style="justify-content:flex-start;margin-top:36px">
        <a class="btn btn-wa" href="${SITE.whatsapp}" target="_blank" rel="noopener">${icon('whatsapp')} ${esc(A.channelBtn)}</a>
        <a class="btn btn-ghost" href="${SITE.linkedin}" target="_blank" rel="noopener">${icon('linkedin')} LinkedIn</a>
      </div>
    </div>
  </section>`;
  return shell(ctx, lang, { title: A.title, description: A.desc, url: PATHS.about[lang], paths: PATHS.about }, inner, 'about', ch);
}

/* ======================================================================= */
/* Contact                                                                  */
/* ======================================================================= */
function contactPage(ctx, lang) {
  const { SITE, icon, esc } = ctx;
  const C = I18N[lang].contact;
  const ch = chrome(ctx, lang, 'contact', PATHS.contact);
  const inner = `  <section class="page-hero">
    <div class="wrap">
      <span class="eyebrow"><span class="dot"></span>${esc(C.eyebrow)}</span>
      <h1 class="display" style="max-width:16ch">${esc(C.h1a)} <span class="gradient-text">${esc(C.h1b)}</span></h1>
      <p class="lede" style="margin-inline:0">${esc(C.lede)}</p>
    </div>
  </section>

  <section class="section" style="padding-top:10px">
    <div class="wrap wrap-narrow">
      <div class="stack-lg">
        <div class="contact-card wa">
          <h3>${icon('whatsapp')} ${esc(C.wa.title)}</h3>
          <p>${esc(C.wa.text)}</p>
          <a class="btn btn-wa" href="${ch.wa}" target="_blank" rel="noopener"><span dir="ltr">${SITE.phone}</span> ${icon('arrow-up-right')}</a>
        </div>
        <div class="contact-card">
          <h3>${icon('link')} ${esc(C.mail.title)}</h3>
          <p>${esc(C.mail.text)}</p>
          <a class="btn btn-ghost" href="mailto:${SITE.email}">${SITE.email}</a>
        </div>
        <div class="contact-card">
          <h3>${icon('clock')} ${esc(C.practical.title)}</h3>
          <p style="margin:0">${esc(SITE.city)} · ${esc(C.practical.text)}<br>${esc(C.practical.lines)}</p>
        </div>
        <div class="contact-card">
          <h3>${icon('link')} ${esc(C.find.title)}</h3>
          <p style="margin:0 0 14px">${esc(C.find.text)}</p>
          <div style="display:flex;gap:10px;flex-wrap:wrap">
            <a class="btn btn-ghost" href="${SITE.linkedin}" target="_blank" rel="noopener">${icon('linkedin')} LinkedIn</a>
            <a class="btn btn-ghost" href="${SITE.github}" target="_blank" rel="noopener">${icon('github')} GitHub</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  ${ch.cta}`;
  return shell(ctx, lang, { title: C.title, description: C.desc, url: PATHS.contact[lang], paths: PATHS.contact }, inner, 'contact', ch);
}

/* ======================================================================= */
/* Aribaz Filter                                                            */
/* ======================================================================= */
function filterPage(ctx, lang) {
  const { SITE, icon, esc, PLATFORMS, filterApp, filterRepo } = ctx;
  const L = I18N[lang]; const F = L.filter;
  const ch = chrome(ctx, lang, 'services', PATHS.filter);
  const waFilter = `${SITE.waDirect}?text=${encodeURIComponent(F.waText)}`;
  const state = { android: 'ok', windows: 'ok', chrome: 'ext', ios: 'soon', mac: 'soon' };
  const platformCards = Object.keys(F.platforms).map((key) => {
    const plat = PLATFORMS[key]; const [name, st] = F.platforms[key];
    const color = state[key] === 'ok' ? 'var(--green)' : state[key] === 'ext' ? 'var(--blue)' : 'var(--ink-faint)';
    return `<div class="value" style="padding:22px;display:flex;gap:14px;align-items:flex-start">
      <span class="plat ${plat.cls}" style="width:26px;height:26px;flex:none" aria-hidden="true">${plat.svg}</span>
      <div><h3 style="margin:0 0 4px">${esc(name)}</h3><p style="font-size:13px;color:${color}">${esc(st)}</p></div>
    </div>`;
  }).join('');
  const card = ([ic, t, p]) => `<div class="value reveal"><span class="ico">${icon(ic)}</span><h3>${esc(t)}</h3><p>${esc(p)}</p></div>`;
  const inner = `  <section class="page-hero">
    <div class="wrap">
      <span class="eyebrow"><span class="dot"></span>${esc(F.eyebrow)}</span>
      <h1 class="display" style="font-size:clamp(36px,6vw,64px);max-width:20ch">${esc(F.h1a)} <span class="gradient-text">${esc(F.h1b)}</span></h1>
      <p class="lede" style="margin-inline:0;max-width:56ch">${esc(F.lede)}</p>
      <div class="hero-actions" style="justify-content:flex-start">
        <a class="btn btn-primary" href="${filterApp}/">${esc(F.start)} ${icon('arrow', 'arr')}</a>
        <a class="btn btn-ghost" href="#comment">${icon('layers')} ${esc(F.how)}</a>
      </div>
      <div class="hero-meta" style="justify-content:flex-start">
        <span>${icon('check')} ${esc(F.meta[0])}</span>
        <span>${icon('shield')} ${esc(F.meta[1])}</span>
        <span>${icon('clock')} ${esc(F.meta[2])}</span>
      </div>
      <p class="muted" style="font-size:13px;margin:18px 0 0">${esc(F.note)} <a class="link-arrow" href="${filterRepo}" target="_blank" rel="noopener">${esc(F.source)} ${icon('arrow-up-right')}</a></p>
    </div>
  </section>

  <section class="section section-soft">
    <div class="wrap">
      <div class="section-head"><div><h2>${esc(F.trustH)}</h2><p>${esc(F.trustSub)}</p></div></div>
      <div class="value-grid" style="grid-template-columns:repeat(auto-fit,minmax(230px,1fr))">
        ${F.trust.map(card).join('\n        ')}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head"><div><h2>${esc(F.whyH)}</h2><p>${esc(F.whySub)}</p></div></div>
      <div class="value-grid grid-2" style="margin-top:34px">
        ${F.why.map(card).join('\n        ')}
      </div>
    </div>
  </section>

  <section class="section section-soft" id="appareils">
    <div class="wrap">
      <div class="section-head"><div><h2>${esc(F.devicesH)}</h2><p>${esc(F.devicesSub)}</p></div></div>
      <div class="value-grid" style="grid-template-columns:repeat(auto-fit,minmax(180px,1fr));margin-top:26px">
        ${platformCards}
      </div>
      <p class="muted" style="font-size:13.5px;margin-top:18px">${esc(F.devicesNote)}</p>
    </div>
  </section>

  <section class="section" id="comment">
    <div class="wrap">
      <div class="section-head"><div><h2>${esc(F.stepsH)}</h2><p>${esc(F.stepsSub)}</p></div></div>
      <div class="steps" style="grid-template-columns:repeat(auto-fit,minmax(230px,1fr))">
        ${F.steps.map(([t, p]) => `<div class="step reveal"><h3>${esc(t)}</h3><p>${esc(p)}</p></div>`).join('\n        ')}
      </div>
    </div>
  </section>

  <section class="section section-soft">
    <div class="wrap">
      <div class="section-head"><div><h2>${esc(F.whoH)}</h2><p>${esc(F.whoSub)}</p></div></div>
      <div class="value-grid" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">
        ${F.who.map(card).join('\n        ')}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap wrap-narrow">
      <div class="section-head"><div><h2>${esc(F.dontH)}</h2><p>${esc(F.dontSub)}</p></div></div>
      <ul class="dont" style="padding:0">
        ${F.dont.map(([b, t]) => `<li>${icon('check')}<span><b>${esc(b)}</b> ${esc(t)}</span></li>`).join('\n        ')}
      </ul>
    </div>
  </section>

  <section class="section-tight"><div class="wrap">
    <div class="cta-band reveal">
      <h2>${esc(F.cta.title)}</h2>
      <p>${esc(F.cta.text)}</p>
      <div class="hero-actions" style="margin-bottom:0">
        <a class="btn btn-primary" href="${filterApp}/">${esc(F.cta.protect)} ${icon('arrow', 'arr')}</a>
        <a class="btn btn-wa" href="${waFilter}" target="_blank" rel="noopener">${icon('whatsapp')} ${esc(F.cta.ask)}</a>
        <a class="btn btn-ghost" href="${filterRepo}" target="_blank" rel="noopener">${icon('github')} ${esc(F.cta.code)}</a>
      </div>
    </div>
  </div></section>

  <section class="section" style="padding-top:0">
    <div class="wrap">
      <a class="link-arrow" href="${PATHS.services[lang]}">${icon('arrow', 'arr')} ${esc(F.back)}</a>
    </div>
  </section>`;
  return shell(ctx, lang, { title: F.title, description: F.desc, url: PATHS.filter[lang], paths: PATHS.filter }, inner, 'services', ch);
}

/* ======================================================================= */
/* Invitation                                                               */
/* ======================================================================= */
function invitationPage(ctx, lang) {
  const { SITE, icon, esc } = ctx;
  const L = I18N[lang]; const V = L.invitation;
  const ch = chrome(ctx, lang, 'invitation', PATHS.invitation);
  const waInv = `${SITE.waDirect}?text=${encodeURIComponent(V.waText)}`;
  const inner = `  <section class="inv-hero">
    <div class="wrap">
      <div class="inv-hero-grid">
        <div>
          <span class="eyebrow"><span class="dot"></span>${esc(V.eyebrow)}</span>
          <h1>${esc(V.h1a)} <span class="gradient-text">${esc(V.h1b)}</span></h1>
          <p class="lede">${esc(V.lede)}</p>
          <div class="hero-actions" style="justify-content:flex-start">
            <a class="btn btn-ghost" href="/invitation/demo.html">${esc(V.demo)} ${icon('arrow', 'arr')}</a>
            <a class="btn btn-wa" href="${waInv}" target="_blank" rel="noopener">${icon('whatsapp')} ${esc(V.prepare)}</a>
          </div>
          <div class="hero-meta" style="justify-content:flex-start;margin-top:26px">
            <span>${icon('clock')} ${esc(V.meta[0])}</span>
            <span>${icon('check')} ${esc(V.meta[1])}</span>
            <span>${icon('shield')} ${esc(V.meta[2])}</span>
          </div>
        </div>
        <div class="inv-mock" aria-hidden="true">
          <div>
            <p class="m-kicker">${esc(V.mock.kicker)}</p>
            <p class="m-names">${esc(V.mock.names[0])}<br><em>&amp;</em><br>${esc(V.mock.names[1])}</p>
            <div class="m-rule"></div>
            <p class="m-date">${esc(V.mock.date)}</p>
            <p class="m-place">${esc(V.mock.place)}</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section section-soft">
    <div class="wrap">
      <div class="section-head"><div><h2>${esc(V.includedA)} <span class="accent">${esc(V.includedB)}</span></h2><p>${esc(V.includedSub)}</p></div></div>
      <div class="inv-features">
        ${V.features.map(([ic, t, d]) => `<div class="inv-feature reveal"><div class="ico">${icon(ic)}</div><h3>${esc(t)}</h3><p>${esc(d)}</p></div>`).join('')}
      </div>
      <div class="hero-actions" style="justify-content:flex-start;margin-top:34px">
        <a class="btn btn-primary" href="/invitation/demo.html">${esc(V.openDemo)} ${icon('arrow', 'arr')}</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head"><div><h2>${esc(V.howH)}</h2><p>${esc(V.howSub)}</p></div></div>
      <div class="steps">
        ${V.steps.map(([t, d]) => `<div class="step"><h3>${esc(t)}</h3><p>${esc(d)}</p></div>`).join('')}
      </div>
    </div>
  </section>

  <section class="section section-soft">
    <div class="wrap">
      <div class="section-head"><div><h2>${esc(V.eventsA)} <span class="accent">${esc(V.eventsB)}</span></h2><p>${esc(V.eventsSub)}</p></div></div>
      <div class="chips" style="gap:10px">
        ${V.events.map((t) => `<span class="chip" style="padding:10px 18px;font-size:14px">${esc(t)}</span>`).join('')}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head"><div><h2>${esc(V.pricesH)}</h2><p>${esc(V.pricesSub)}</p></div></div>
      <div class="inv-price-grid">
        ${V.prices.map((p) => `<div class="inv-price${p.main ? ' is-main' : ''}">
          ${p.tag ? `<span class="tag-main">${esc(p.tag)}</span>` : ''}
          <h3>${esc(p.t)}</h3>
          <p class="p-desc">${esc(p.d)}</p>
          <ul>${p.items.map((i) => `<li>${esc(i)}</li>`).join('')}</ul>
          <div class="p-foot"><span class="p-price">${esc(V.onQuote)}</span><a class="link-arrow" href="${SITE.waDirect}?text=${encodeURIComponent(V.quoteText + p.t)}" target="_blank" rel="noopener">${esc(V.request)} ${icon('arrow', 'arr')}</a></div>
        </div>`).join('')}
      </div>
    </div>
  </section>

  <section class="section section-soft">
    <div class="wrap">
      <div class="section-head"><div><h2>${esc(V.faqA)} <span class="accent">${esc(V.faqB)}</span></h2><p>${esc(V.faqSub)}</p></div></div>
      <div class="inv-faq">
        ${V.faq.map(([q, a]) => `<details><summary>${esc(q)}</summary><p>${esc(a)}</p></details>`).join('')}
      </div>
    </div>
  </section>

  <section class="section" id="contact">
    <div class="wrap">
      <div class="section-head"><div><h2>${esc(V.contactH)}</h2><p>${esc(V.contactSub)}</p></div></div>
      <div class="contact-grid">
        <div class="contact-card wa">
          <h3>${icon('whatsapp')} WhatsApp</h3>
          <p>${esc(V.wa.text)} <span dir="ltr">${SITE.phone}</span></p>
          <a class="btn btn-wa" href="${waInv}" target="_blank" rel="noopener">${esc(V.wa.btn)} ${icon('arrow-up-right')}</a>
        </div>
        <div class="contact-card">
          <h3>${icon('link')} Email</h3>
          <p>${esc(V.mail.text)}</p>
          <a class="btn btn-primary" href="mailto:${SITE.email}?subject=${encodeURIComponent(V.mail.subject)}">${SITE.email}</a>
        </div>
      </div>
    </div>
  </section>`;
  return shell(ctx, lang, { title: V.title, description: V.desc, url: PATHS.invitation[lang], paths: PATHS.invitation }, inner, 'invitation', ch);
}

/* ======================================================================= */
/* Toutes les pages : { 'en/services.html': '<html…>', … }                  */
/* ======================================================================= */
export function i18nPages(ctx) {
  const out = {};
  for (const lang of LANGS) {
    out[`${lang}/index.html`] = homePage(ctx, lang);
    out[`${lang}/services.html`] = servicesPage(ctx, lang);
    out[`${lang}/about.html`] = aboutPage(ctx, lang);
    out[`${lang}/contact.html`] = contactPage(ctx, lang);
    out[`${lang}/services/filtres/index.html`] = filterPage(ctx, lang);
    out[`${lang}/invitation.html`] = invitationPage(ctx, lang);
    for (const family of ctx.SERVICES) {
      for (const item of family.items.filter((it) => !it.href)) {
        out[`${lang}/services/${ctx.SLUG(item.title)}.html`] = servicePage(ctx, lang, family, item);
      }
    }
  }
  return out;
}

/** URLs des pages traduites (pour le plan du site). */
export function i18nUrls(ctx) {
  return Object.keys(i18nPages(ctx)).map((f) => '/' + f.replace(/index\.html$/, ''));
}

/**
 * Pages dédiées des services : /services/<slug>.html
 *
 * Chaque tuile de la page Services qui n'a pas déjà sa propre page (Invitation,
 * Aribaz Filter…) ouvre l'une de ces pages. Le module ne dépend que de ce que
 * le générateur lui passe (ctx), ce qui permet de le tester seul.
 */

export function servicePath(SLUG, item) {
  return `/services/${SLUG(item.title)}.html`;
}

function itemHref(SLUG, item) {
  return item.href || servicePath(SLUG, item);
}

export function servicePage(ctx, family, item) {
  const { SITE, SERVICE_DETAILS, SLUG, head, nav, footer, ctaBand, icon, esc } = ctx;
  const d = SERVICE_DETAILS[item.title] || { detail: item.text, includes: item.bullets, delai: 'sur devis' };
  const url = servicePath(SLUG, item);
  const title = `${item.title} — ${family.brand}`;
  const waText = encodeURIComponent(`Bonjour ARIBAZ, je voudrais un devis pour : ${item.title}`);
  const mailSubject = encodeURIComponent(`Devis — ${item.title}`);
  const siblings = family.items.filter((x) => x !== item);

  const body = `${nav('services', ctx.pathsFor ? ctx.pathsFor(item) : undefined)}
<main id="contenu">
  <section class="page-hero" style="--brand:${family.color}">
    <div class="wrap">
      <a class="eyebrow" href="/services.html#${family.slug}"><span class="dot" style="background:${family.color}"></span>${esc(family.brand)} · Tous les services</a>
      <h1 class="display" style="font-size:clamp(34px,5.6vw,60px);max-width:20ch">${esc(item.title)}</h1>
      <p class="lede" style="margin-inline:0;max-width:56ch">${esc(d.detail)}</p>
      <div class="hero-actions" style="justify-content:flex-start">
        <a class="btn btn-wa" href="${SITE.waDirect}?text=${waText}" target="_blank" rel="noopener">${icon('whatsapp')} Demander un devis</a>
        <a class="btn btn-ghost" href="mailto:${SITE.email}?subject=${mailSubject}">Par email</a>
      </div>
      <div class="hero-meta" style="justify-content:flex-start;margin-top:26px">
        <span>${icon('clock')} Délai : ${esc(d.delai)}</span>
        <span>${icon('check')} Devis gratuit</span>
        <span>${icon('shield')} Jérusalem &amp; à distance</span>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:12px">
    <div class="wrap wrap-narrow">
      <div class="section-head"><div><h2>Ce qui est inclus</h2><p>${esc(item.text)}</p></div></div>
      <ul class="dont" style="padding:0">
        ${d.includes.map((x) => `<li>${icon('check')}<span>${esc(x)}</span></li>`).join('\n        ')}
      </ul>
    </div>
  </section>

  <section class="section section-soft">
    <div class="wrap">
      <div class="section-head"><div><h2>Comment ça se passe</h2><p>Quatre étapes, aucune surprise.</p></div></div>
      <div class="steps">
        <div class="step"><h3>Tu racontes</h3><p>Dis-moi ce dont tu as besoin, en deux lignes. Pas de vocabulaire technique requis.</p></div>
        <div class="step"><h3>Je réponds</h3><p>Une réponse claire et un devis gratuit, sous 24 h ouvrées.</p></div>
        <div class="step"><h3>On valide</h3><p>Tu valides le prix et le délai avant que je commence.</p></div>
        <div class="step"><h3>Je livre</h3><p>Et je reste disponible pour les questions qui arrivent après.</p></div>
      </div>
    </div>
  </section>
${siblings.length ? `
  <section class="section">
    <div class="wrap wrap-narrow">
      <div class="section-head"><div><h2>Dans la même maison</h2><p>${esc(family.tagline)}</p></div></div>
      <ul class="dont" style="padding:0">
        ${siblings.map((s) => `<li>${icon('check')}<span><a href="${itemHref(SLUG, s)}"><b>${esc(s.title)}</b></a> — ${esc(s.text)}</span></li>`).join('\n        ')}
      </ul>
    </div>
  </section>
` : ''}
  <section class="section" style="padding-top:0">
    <div class="wrap wrap-narrow">
      <a class="btn btn-ghost" href="/services.html#${family.slug}">← Tous les services</a>
    </div>
  </section>

  ${ctaBand()}
</main>
${footer()}
<script src="/assets/js/app.js" defer></script>
</body>
</html>`;

  return head({ title, description: item.text, url, extra: ctx.hreflang ? ctx.hreflang(item) : '' }) + body;
}

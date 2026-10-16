#!/usr/bin/env python3
"""Add one Founder Read issue (or any Beehiiv post) to the Insights section of revenueandbeyond.com.

Edits the static site in ../site in place, so nothing else on the site changes:
  1. writes site/insights/<slug>/index.html, using an existing Insights page as the shell
  2. puts the post at the top of the list on site/insights/index.html
  3. adds the URL to site/sitemap.xml

Usage:
  python3 tools/add_insight.py post.json            (add, or refresh if the slug already exists)
  python3 tools/add_insight.py post.json --dry-run  (build into /tmp only, change nothing)

post.json fields:
  slug       Beehiiv slug, e.g. "every-deal-still-goes-through-you"
  title      post title
  subtitle   post subtitle (used as the lead and meta description)
  date       publish date, YYYY-MM-DD (UK date of the Sunday send)
  tag        Beehiiv content tag display name, e.g. "Pipeline & Sales"
  html       the post body from beehiiv get_post_content (format editor_html or html body)
  html_file  alternative to html: path to a file holding the body
Requires: beautifulsoup4.
"""
import os, re, sys, json, html as H, datetime, shutil, tempfile
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
DOMAIN = 'https://revenueandbeyond.com'
TAG_SLUG = {'Pipeline & Sales': 'pipeline-sales', 'Founder Journey': 'founder-journey',
            'Founder Dependency & Exit Value': 'founder-dependency-exit-value', 'Leadership & Team': 'leadership-team',
            'Events & Announcements': 'events-announcements', 'Market Commentary': 'market-commentary',
            'Podcasts & talks': 'podcasts-talks'}
SHELL = 'the-customers-you-d-rather-not-have'      # an existing Insights page used as the page shell
CARD_CSS_MARK = '/* founder-read cards (add_insight.py) */'
CARD_CSS = CARD_CSS_MARK + '''
.prose .nr-card{background:#fff; border:2px solid var(--teal); border-radius:16px; padding:20px 24px 6px; margin:1.6em 0 1.9em; box-shadow:6px 6px 0 var(--green)}
.prose .nr-card.sh-purple{box-shadow:6px 6px 0 var(--purple)}
.prose .nr-card.sh-sky{box-shadow:6px 6px 0 var(--sky)}
.prose .nr-card.sh-teal{box-shadow:6px 6px 0 var(--teal)}
.prose .nr-card.fill-green{background:var(--green)}
.prose .nr-card.fill-purple{background:var(--purple)}
.prose .nr-card .nr-label{font-weight:900; font-size:12px; letter-spacing:.12em; text-transform:uppercase; color:var(--teal); margin:0 0 .5em}
.prose .nr-card h2{margin:.1em 0 .45em; font-size:1.45rem}
.prose .nr-card p{margin:0 0 .9em}
.prose img.nr-img{border:0; box-shadow:none; border-radius:0}
.prose figure.nr-sign{max-width:340px}
'''
COLOURS = {'#49E8B0': 'green', '#C3A1F8': 'purple', '#6AD1FA': 'sky', '#0B363B': 'teal'}


def fmt_date(iso):
    d = datetime.date.fromisoformat(iso[:10])
    return f'{d.day} {d.strftime("%b %Y")}', d.isoformat()


def is_section(t):
    return getattr(t, 'name', None) == 'div' and (t.get('data-type') == 'section' or 'node-section' in (t.get('class') or []))


def clean(body):
    soup = BeautifulSoup(body, 'html.parser')
    # email-only furniture: masthead image, date line, greeting, forward line, name block under the sign-off
    for fig in soup.select('figure[data-type="imageBlock"]'):
        if (fig.get('data-alt') or '').startswith('The Founder Read'):
            fig.decompose()
    for p in soup.find_all('p'):
        t = p.get_text(' ', strip=True)
        if ('{{current_date' in t or re.match(r'^(Evening|Morning|Afternoon|Hi|Hello)\s*\{\{', t)
                or t.startswith('Forward this email') or re.match(r'^Simon Watson\s+Founder, Revenue', t)):
            p.decompose()
    for el in soup.select('div.node-genericEmbed, [data-type="genericEmbed"], span[data-type="emoji"]'):
        el.decompose()
    # cards: outer section = shadow colour, inner section = fill
    for sec in [s for s in soup.find_all(is_section) if not s.find_parent(is_section)]:
        txt = sec.get_text(' ', strip=True)
        if 'FREE DIAGNOSIS CALL' in txt.upper() or 'revenueandbeyond.com/book' in str(sec):
            sec.decompose(); continue          # the page already carries the booking CTA
        shadow = COLOURS.get((sec.get('data-background-color') or '').upper(), 'green')
        inner = sec.find(is_section)
        fill = COLOURS.get(((inner.get('data-background-color') if inner else '') or '').upper())
        card = soup.new_tag('aside')
        card['class'] = ['nr-card', f'sh-{shadow}'] + ([f'fill-{fill}'] if fill in ('green', 'purple') else [])
        src = inner or sec
        for child in list(src.children):
            card.append(child.extract())
        sec.replace_with(card)
    for d in soup.select('div[data-thread-id], div[data-block-thread]'):
        d.unwrap()
    for d in soup.find_all(is_section):
        d.unwrap()
    # label line at the top of each card ("A NUMBER TO CHECK")
    for card in soup.select('aside.nr-card'):
        first = card.find('p')
        if first:
            t = first.get_text(strip=True)
            if t and t.upper() == t and len(t) < 40 and not re.match(r'^\d+$', t):
                first.clear(); first.string = t; first['class'] = ['nr-label']
    # images
    for fig in soup.select('figure[data-type="imageBlock"]'):
        src = fig.get('data-src'); alt = fig.get('data-alt') or ''
        f = soup.new_tag('figure'); im = soup.new_tag('img', src=src, alt=alt, loading='lazy')
        if 'beehiiv' in (src or '') and re.search(r'/neo-[^/]*\.png', src or ''):
            im['class'] = ['nr-img']
        if 'signoff' in (src or ''):
            f['class'] = ['nr-sign']
        f.append(im)
        cap = fig.find('figcaption')
        if cap and cap.get_text(strip=True):
            c = soup.new_tag('figcaption'); c.string = cap.get_text(strip=True); f.append(c)
        fig.replace_with(f)
    for fig in soup.select('figure[data-type="blockquoteFigure"]'):
        bq = fig.find('blockquote')
        fig.replace_with(bq.extract()) if bq else fig.decompose()
    # buttons
    for a in soup.select('a[data-type="button"]'):
        a['class'] = ['btn']
    for tag in soup.find_all(['span', 'sub', 'sup', 'font']):
        tag.unwrap()
    for h in soup.find_all('h1'):
        h.name = 'h2'
    keep = {'a': ['href', 'class'], 'img': ['src', 'alt', 'loading', 'class'], 'aside': ['class'], 'p': ['class'], 'figure': ['class']}
    for t in soup.find_all(True):
        allowed = keep.get(t.name, [])
        for a in list(t.attrs):
            if a not in allowed:
                del t.attrs[a]
    for a in soup.find_all('a'):
        h = a.get('href', '')
        m = re.match(r'https?://(?:www\.)?revenueandbeyond\.com(/[^?#]*)?', h)
        if m:
            a['href'] = (m.group(1) or '/')
        elif h.startswith('http'):
            a['target'] = '_blank'; a['rel'] = 'noopener'
        if a.get('class') == ['link']:
            del a['class']
    for p in soup.find_all(['p', 'h2', 'h3', 'h4']):
        if not p.get_text().replace('\xa0', ' ').strip() and not p.find(['img']):
            p.decompose()
    out = str(soup)
    out = out.replace('{{first_name|there}}', 'there')
    out = re.sub(r'\{\{[^}]*\}\}', '', out)
    return out.strip()


def esc_attr(s):
    return H.escape(s, quote=True)


def esc_text(s):
    return H.escape(s, quote=False)


def ins_row(slug, title, sub, tag, date, with_sub=True):
    disp, iso = fmt_date(date)
    s = (f'<a class="ins" href="/insights/{slug}/" data-t="{TAG_SLUG.get(tag, "x")}">\n'
         f'  <span class="im"><time datetime="{iso}">{disp}</time><span class="it">{esc_text(tag)}</span></span>\n'
         f'  <span class="ih">{esc_text(title)}</span>\n')
    if with_sub:
        s += f'  <span class="is">{esc_text(sub)}</span>\n'
    return s + '</a>\n'


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    dry = '--dry-run' in sys.argv
    post = json.load(open(args[0], encoding='utf-8'))
    body = post.get('html') or open(post['html_file'], encoding='utf-8').read()
    slug, title, sub, tag, date = post['slug'], post['title'].strip(), (post.get('subtitle') or '').strip(), post['tag'], post['date'][:10]
    assert re.match(r'^[a-z0-9-]+$', slug), slug
    site = SITE
    if dry:
        tmp = tempfile.mkdtemp(); shutil.copytree(SITE, os.path.join(tmp, 'site')); site = os.path.join(tmp, 'site')
    disp, iso = fmt_date(date)
    prose = clean(body)

    # ---- 1. the page
    shell = open(os.path.join(site, 'insights', SHELL, 'index.html'), encoding='utf-8').read()
    url = f'/insights/{slug}/'
    old_url = f'/insights/{SHELL}/'
    m = re.search(r'<title>(.*?) \| Revenue &amp; Beyond</title>', shell); old_title = m.group(1)
    m = re.search(r'<meta name="description" content="(.*?)">', shell); old_desc = m.group(1)
    desc = sub or re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', prose)).strip()
    desc = (desc[:157].rsplit(' ', 1)[0] + '...') if len(desc) > 160 else desc
    page = shell
    page = page.replace(f'{old_title} | Revenue &amp; Beyond', f'{esc_text(title)} | Revenue &amp; Beyond')
    page = page.replace(f'content="{old_desc}"', f'content="{esc_attr(desc)}"')
    page = page.replace(DOMAIN + old_url, DOMAIN + url)
    page = page.replace(f'pg-insights-{SHELL}', f'pg-insights-{slug}')
    # JSON-LD
    ld_m = re.search(r'<script type="application/ld\+json">(.*?)</script>', page, re.S)
    ld = json.loads(ld_m.group(1))
    for g in ld['@graph']:
        if g.get('@type') == 'BlogPosting':
            g.update({'headline': title, 'description': desc, 'datePublished': iso, 'dateModified': iso,
                      'mainEntityOfPage': DOMAIN + url, 'url': DOMAIN + url, 'articleSection': tag})
        if g.get('@type') == 'BreadcrumbList':
            g['itemListElement'][2].update({'name': title, 'item': DOMAIN + url})
    page = page[:ld_m.start(1)] + json.dumps(ld, ensure_ascii=False, separators=(',', ':')) + page[ld_m.end(1):]
    # hero
    page = re.sub(r'<p class="crumb"><a href="/insights/">Insights</a> / .*?</p>',
                  f'<p class="crumb"><a href="/insights/">Insights</a> / {esc_text(tag)}</p>', page, count=1)
    page = re.sub(r'(<h1 style="font-size:clamp\(1.9rem,4.6vw,3rem\)">).*?(</h1>)', lambda m: m.group(1) + esc_text(title) + m.group(2), page, count=1, flags=re.S)
    page = re.sub(r'(<p class="lead" style="margin-top:20px;margin-bottom:12px">).*?(</p>)', lambda m: m.group(1) + esc_text(sub) + m.group(2), page, count=1, flags=re.S)
    page = re.sub(r'<p class="byline">By Simon Watson &middot; <time datetime="[^"]*">[^<]*</time></p>',
                  f'<p class="byline">By Simon Watson &middot; <time datetime="{iso}">{disp}</time></p>', page, count=1)
    # body
    a = page.index('<div class="col prose">') + len('<div class="col prose">')
    b = page.index('</article>'); b = page.rindex('</div>', a, b)
    page = page[:a] + '\n    ' + prose + '\n  ' + page[b:]
    # related posts: up to 3 others with the same tag, then the newest others
    idx = open(os.path.join(site, 'insights', 'index.html'), encoding='utf-8').read()
    rows = re.findall(r'<a class="ins" href="/insights/([^/]+)/" data-t="([^"]+)">\s*<span class="im"><time datetime="([^"]+)">([^<]+)</time><span class="it">([^<]+)</span></span>\s*<span class="ih">([^<]*)</span>', idx)
    rows = [r for r in rows if r[0] != slug]
    rel = [r for r in rows if r[1] == TAG_SLUG.get(tag)][:3]
    rel += [r for r in rows if r not in rel][:3 - len(rel)]
    rel_html = ''.join(f'<a class="ins" href="/insights/{r[0]}/"><span class="im"><time>{r[3]}</time><span class="it">{r[4]}</span></span><span class="ih">{r[5]}</span></a>' for r in rel)
    page = re.sub(r'(<p class="eyebrow">More from Insights</p><div class="inslist">).*?(</div><p class="small")', lambda m: m.group(1) + rel_html + m.group(2), page, count=1, flags=re.S)
    assert f'<link rel="canonical" href="{DOMAIN}{url}">' in page and f'pg-insights-{SHELL}"' not in page, 'shell not fully replaced'
    os.makedirs(os.path.join(site, 'insights', slug), exist_ok=True)
    open(os.path.join(site, 'insights', slug, 'index.html'), 'w', encoding='utf-8').write(page)

    # ---- 2. the list (remove any existing row for this slug, insert at the top)
    idx = re.sub(r'<a class="ins" href="/insights/' + re.escape(slug) + r'/".*?</a>\n', '', idx, flags=re.S)
    marker = '<div class="inslist" id="insList">\n'
    assert marker in idx
    idx = idx.replace(marker, marker + ins_row(slug, title, sub, tag, date), 1)
    if TAG_SLUG.get(tag) and f'data-f="{TAG_SLUG[tag]}"' not in idx:
        print('note: no filter chip exists for tag', tag)
    open(os.path.join(site, 'insights', 'index.html'), 'w', encoding='utf-8').write(idx)

    # ---- 3. sitemap
    sm_p = os.path.join(site, 'sitemap.xml'); sm = open(sm_p, encoding='utf-8').read()
    loc = f'<loc>{DOMAIN}{url}</loc>'
    today = datetime.date.today().isoformat()
    if loc not in sm:
        sm = sm.replace('</urlset>', f'  <url>{loc}<lastmod>{iso}</lastmod><priority>0.4</priority></url>\n</urlset>')
    sm = re.sub(r'(<loc>' + re.escape(DOMAIN) + r'/insights/</loc><lastmod>)[^<]*', r'\g<1>' + today, sm)
    open(sm_p, 'w', encoding='utf-8').write(sm)

    # ---- 4. card styles (once)
    css_p = os.path.join(site, 'assets', 'style.css'); css = open(css_p, encoding='utf-8').read()
    if CARD_CSS_MARK not in css:
        open(css_p, 'a', encoding='utf-8').write('\n' + CARD_CSS)
    print(('[dry run] ' if dry else '') + f'added {url} ({disp}, {tag}) -> {site}')


if __name__ == '__main__':
    main()

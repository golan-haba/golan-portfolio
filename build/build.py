"""Generates the site's HTML pages. Run:  python3 build/build.py
Edit the page content in the PAGES section below, then run again."""
import html, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = 'assets/img/'
E = html.escape

def size(key):
    with Image.open(os.path.join(ROOT, IMG + key + '.webp')) as im:
        return im.size

def img(key, alt='', cls='', lazy=True, attrs=''):
    w, h = size(key)
    return (f'<img src="{IMG}{key}.webp" width="{w}" height="{h}" alt="{E(alt)}"'
            f'{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}{" loading=" + chr(34) + "lazy" + chr(34) if lazy else ""} decoding="async"{attrs}>')

# ---------- videos ----------
# Put video files in assets/video/ with these names. Until a file exists, its image is shown instead.
VIDEOS = {
    # key: (video file, mode)   mode 'auto' = loops silently, 'click' = play button
    # 'inset' = the video plays inside the post frame: (top %, height %) of the image
    'bf/post1': ('buchman-anim-2.mp4', 'inset', (9.22, 82.97)),   # photos
    'bf/post2': ('buchman-anim-3.mp4', 'inset', (9.22, 82.97)),   # icons
    'bf/post3': ('buchman-anim-1.mp4', 'inset', (9.22, 82.97)),   # logo
    'sh/reel1': ('shira-reel-1.mp4', 'click'),
    'sh/reel2': ('shira-reel-2.mp4', 'click'),
    'sh/reel3': ('shira-reel-3.mp4', 'click'),
    'sh/reel4': ('shira-reel-4.mp4', 'click'),
    'sh/reel5': ('shira-reel-5.mp4', 'click'),
    # hover: (left %, top %, width %, height %) of the video inside the square card, as in Figma
    'hm/brand1': ('buchman-anim-1.mp4', 'hover', (-9.8, -34.4, 121.7, 162.1)),
    'hm/brand2': ('shira-logo-anim.mp4', 'hover', (0, -16.7, 100, 133.4)),
    'hm/brand3': ('lilbuns-logo-anim.mp4', 'hover', (0, 0, 100, 100)),
    'hm/brand4': ('boavida-logo-anim.mp4', 'hover', (11.6, 13.3, 76.8, 76.8)),
    'lb/web2': ('lilbuns-bun.mp4', 'box', (14.13, 25.76, 29.11, 45.29)),   # bun spinning on a finger
    'pr/msb1': ('moses-video-1.mp4', 'inset', (10.8, 81.0)),
    'pr/msb3': ('moses-video-2.mp4', 'inset', (10.9, 81.9)),
    'mo/hol1': ('holiday-1.mp4', 'click'),
    'mo/hol2': ('holiday-2.mp4', 'click'),
    'mo/hol3': ('holiday-3.mp4', 'click'),
    'il/ashmat': ('ashmat-rabim.mp4', 'click'),
    'il/final': ('final-project.mp4', 'click'),
    'il/fox360': ('fox-mask-360.mp4', 'auto'),
}
PLAY_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3l16 9-16 9z" fill="#fff"/></svg>'

def media(key, alt=''):
    if key not in VIDEOS:
        return img(key, alt)
    file, mode, *extra = VIDEOS[key]
    w, h = size(key)
    poster = f'{IMG}{key}.webp'
    if mode == 'inset':
        top, h = extra[0]
        return (f'<div class="media inset">{img(key, alt)}<video muted loop playsinline autoplay preload="none" aria-hidden="true" style="top:{top}%;height:{h}%">'
                f'<source src="assets/video/{file}" type="video/mp4"></video></div>')
    if mode == 'box':
        l, t, w_, h_ = extra[0]
        return (f'<div class="media inset">{img(key, alt)}<video muted loop playsinline autoplay preload="none" aria-hidden="true" style="left:{l}%;top:{t}%;width:{w_}%;height:{h_}%">'
                f'<source src="assets/video/{file}" type="video/mp4"></video></div>')
    if mode == 'hover':  # static logo; video plays on hover (desktop) / when on screen (mobile)
        l, t, w_, h_ = extra[0]
        return (img(key, alt) + f'<span class="hover-box"><video class="hover-vid" muted loop playsinline preload="none" aria-hidden="true" style="left:{l}%;top:{t}%;width:{w_}%;height:{h_}%">'
                f'<source src="assets/video/{file}" type="video/mp4"></video></span>')
    if mode == 'auto':
        return (f'<video width="{w}" height="{h}" poster="{poster}" muted loop playsinline autoplay preload="none" aria-label="{E(alt)}">'
                f'<source src="assets/video/{file}" type="video/mp4"></video>')
    return (f'<div class="media"><video data-click width="{w}" height="{h}" poster="{poster}" playsinline preload="none" aria-label="{E(alt)}">'
            f'<source src="assets/video/{file}" type="video/mp4"></video>'
            f'<button class="play" aria-label="Play video">{PLAY_SVG}</button></div>')

# white 0.5px outline around the creative inside a post, as in Figma: (top %, height %) of the post image
OUTLINE = {'pr/ms1': (12.7, 77.8), 'pr/ms3': (10.0, 81.7), 'pr/msb2': (10.0, 81.7)}
def outlined(key, alt=''):
    v = VIDEOS.get(key)
    top, h = v[2] if v and v[1] == 'inset' else OUTLINE[key]
    return f'<div class="ol-wrap">{media(key, alt)}<span class="ol" style="top:{top}%;height:{h}%"></span></div>'

def face_html(alt='Golan Haba', cls='', lazy=False):
    w, h = size('hm/face')
    return (f'<span class="face-anim {cls}"><img src="{IMG}hm/face.webp" width="{w}" height="{h}" alt="{E(alt)}">'
            f'<img class="wink" src="{IMG}hm/face-wink.webp" width="{w}" height="{h}" alt="" aria-hidden="true"></span>')

# ---------- building blocks ----------
def meta(): return '<div class="meta"><span>2026</span><span>the work on</span></div>'
def brand_title(name, tag='h1', id_=''):
    lines = '<br>'.join(E(p) for p in name.split('\n'))
    return f'<section class="brand-title reveal"{f" data-anchor={chr(34)}{id_}{chr(34)}" if id_ else ""}><{tag}>{lines}</{tag}></section>'
def desc(t): return f'<p class="desc reveal">{E(t)}</p>'
def intro(name, text):
    return f'<section class="intro">{meta()}{brand_title(name)}{desc(text)}</section>'
def label(l, r): return f'<div class="label"><span>{E(l)}</span><span>{E(r)}</span></div>'
DESKTOP_LOGO = {'bf/logo': 984, 'sh/logo': 603, 'lb/logo': 653, 'bv/logo': 563}  # widths in the 1728px desktop Figma frame
def logo_band(l, r, key, w):
    dw = round(DESKTOP_LOGO.get(key, w * 2) / 17.28, 2)
    return f'<section class="dark logo-sec">{label(l, r)}<div class="logo-band reveal" style="--w:{w}px;--dw:{dw}vw">{img(key, r + " logo")}</div></section>'
def icons_row(key, w=390, alt='brand icons'):
    return f'<div class="icons-row reveal" style="--w:{w}px">{img(key, alt)}</div>'

def mock(seq, alt):
    """seq: list of keys (large) or tuples (pair)."""
    out = []
    for s in seq:
        if isinstance(s, tuple):
            ar = lambda k: round(size(k)[0] / size(k)[1], 4)
            out.append(f'<div class="pair reveal">{img(s[0], alt, attrs=f" style=--ar:{ar(s[0])}")}{img(s[1], alt, attrs=f" style=--ar:{ar(s[1])}")}</div>')
        else:
            out.append(f'<div class="reveal">{img(s, alt)}</div>')
    return f'<section class="mock">{"".join(out)}</section>'

def carousel(keys, alt, web=False, cols=None, outline=()):
    cols = cols or (2 if web else min(len(keys), 3))
    items = ''.join(f'<div class="cf-item">{outlined(k, alt) if k in outline else media(k, alt)}</div>' for k in keys)
    arrows = ('<button class="cf-arrow cf-prev" aria-label="Previous">&#8592;</button>'
              '<button class="cf-arrow cf-next" aria-label="Next">&#8594;</button>')
    return f'<div class="cf{" web" if web else ""}" style="--cols:{cols}">{arrows}<div class="cf-track">{items}</div></div>'

def pair_row(keys, alt):
    return '<div class="pair-row">' + ''.join(f'<div>{media(k, alt)}</div>' for k in keys) + '</div>'

def dark(*parts, pad=True):
    return f'<section class="dark"{" style=" + chr(34) + "padding-bottom:12px" + chr(34) if pad else ""}>{"".join(parts)}</section>'

# ---------- navigation ----------
BRANDS = [('buchman feder', 'buchman-feder.html'), ('shira hadasha', 'shira-hadasha.html'),
          ('lil buns', 'lil-buns.html'), ('boa vida', 'boa-vida.html')]
PROJECTS = [('rapidos', 'projects.html#rapidos'), ('bbb', 'projects.html#bbb'), ('landmark', 'projects.html#landmark'),
            ('elbit', 'projects.html#elbit'), ('moses shop', 'projects.html#moses-shop')]
EXTRA_WORK = [('motion', 'motion.html'), ('illustration', 'illustration.html')]
BURGER = '<svg width="28" height="20" viewBox="0 0 28 20" aria-hidden="true"><path d="M2 2H26M2 10H26M2 18H26" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/></svg>'
CLOSE = '<svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5L19 19M19 5L5 19" stroke="#009476" stroke-width="2.5" stroke-linecap="round"/></svg>'

def nav_html():
    def drop(items, extra=()):
        more = ('<li class="sep" aria-hidden="true"></li>' + ''.join(f'<li><a href="{h}">{E(n)}</a></li>' for n, h in extra)) if extra else ''
        return '<ul class="drop">' + ''.join(f'<li><a href="{h}">{E(n)}</a></li>' for n, h in items) + more + '</ul>'
    return ('<ul class="nav">'
            f'<li><button aria-haspopup="true">projects</button>{drop(PROJECTS, EXTRA_WORK)}</li>'
            f'<li><button aria-haspopup="true">branding</button>{drop(BRANDS)}</li>'
            '<li><a href="index.html#about">about</a></li></ul>'
            f'<button class="burger" aria-label="Open menu" aria-expanded="false">{BURGER}</button>')

def menu_html():
    def sub(items, extra=()):
        more = ('<li class="sep" aria-hidden="true"></li>' + ''.join(f'<li><a href="{h}">{E(n)}</a></li>' for n, h in extra)) if extra else ''
        return '<ul class="menu-sub">' + ''.join(f'<li><a href="{h}">{E(n)}</a></li>' for n, h in items) + more + '</ul>'
    return ('<div class="menu" role="dialog" aria-label="Menu"><div class="menu-card">'
            f'<button class="menu-close" aria-label="Close menu">{CLOSE}</button>'
            '<ul class="menu-list">'
            '<li><a class="menu-cat" href="index.html#about">about</a></li>'
            f'<li><a class="menu-cat" href="projects.html">projects</a>{sub(PROJECTS, EXTRA_WORK)}</li>'
            f'<li><a class="menu-cat" href="index.html#branding">branding</a>{sub(BRANDS)}</li>'
            '</ul></div></div>')

def header(overlay=False):
    face = '' if overlay else f'<a class="face" href="index.html" aria-label="Home">{face_html()}</a>'
    cls = 'site-header overlay' if overlay else 'site-header mat'
    return f'<header class="{cls}"><nav aria-label="Main">{nav_html()}</nav>{face}</header>'

# Social links: put your real profile URLs here (order matches the icons in the footer).
SOCIALS = [('Email', 'mailto:golanhaba1996@gmail.com', 'mail'),
           ('WhatsApp', 'https://wa.me/972546731819', 'whatsapp'),
           ('Instagram', 'https://www.instagram.com/habagolan/', 'instagram'),
           ('LinkedIn', 'https://www.linkedin.com/in/golan-haba-23a137275/', 'linkedin')]

def footer():
    soc = ''.join(f'<li><a href="{h}" aria-label="{E(n)}" target="_blank" rel="noopener"><img src="assets/icons/{k}.svg" width="24" height="24" alt="{E(n)}"></a></li>' for n, h, k in SOCIALS)
    up = '<svg width="12" height="12" viewBox="0 0 12 12" aria-hidden="true"><path d="M6 10.5V1.5M6 1.5L2 5.5M6 1.5L10 5.5" stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>'
    return (f'<footer class="site-footer mat" id="contact"><img src="assets/img/contact.gif" width="1272" height="268" alt="Contact me" class="contact" loading="lazy">'
            f'<div class="foot-row"><div><h2>stay in touch</h2><ul class="socials">{soc}</ul></div>'
            f'<a class="to-top" href="#top">BACK TO TOP {up}</a></div></footer>')

# ---------- fonts ----------
# Futura PT comes from Adobe Fonts (included with Creative Cloud). Create a web project at
# fonts.adobe.com with "Futura PT" and "Futura PT Bold", add your site's domain, and paste the
# project ID here (the xxxxxxx in https://use.typekit.net/xxxxxxx.css). Until then Jost, a free
# Futura look-alike, is shown.
ADOBE_FONTS_KIT = 'iqo4cqp'
FONT_LINKS = ((f'<link rel="preconnect" href="https://use.typekit.net" crossorigin>\n<link rel="stylesheet" href="https://use.typekit.net/{ADOBE_FONTS_KIT}.css">\n' if ADOBE_FONTS_KIT else '') +
              '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
              '<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">')

# ---------- analytics ----------
# Google Tag Manager container. The Google Analytics (GA4) tag itself is set up inside Tag Manager.
GTM_ID = 'GTM-ZSV3VQR9'
GTM_HEAD = (f"""<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->\n""" if GTM_ID else '')
GTM_BODY = (f'<!-- Google Tag Manager (noscript) --><noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n' if GTM_ID else '')

def page(title, description, body, overlay=False):
    tiled = '<section class="desk"' in body
    return f'''<!doctype html>
<html lang="en">
<head>
{GTM_HEAD}<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(description)}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(description)}">
<meta property="og:image" content="assets/img/hm/face.webp">
<link rel="icon" href="assets/img/hm/face.webp">
{FONT_LINKS}
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body id="top"{' class="tiled"' if tiled else ''}>
{GTM_BODY}{body if overlay else header() + body}
{footer()}
{menu_html()}
<button class="fab-top" aria-label="Back to top"><svg width="20" height="20" viewBox="0 0 12 12" aria-hidden="true"><path d="M6 10.5V1.5M6 1.5L2 5.5M6 1.5L10 5.5" stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg></button>
<script src="assets/js/main.js"></script>
</body>
</html>
'''

# ================= DESKTOP (built from the 1728px desktop Figma frames) =================
import json as _json
DESK = _json.load(open(os.path.join(ROOT, 'build', 'desk.json')))
U = lambda n: f'calc(var(--u)*{n})'

def dtext(txt, x, y, w, size, cls='', align='left', color='#000', weight=None, family=None):
    st = f'left:{U(x)};top:{U(y)};width:{U(w)};font-size:{U(size)};text-align:{align};color:{color}'
    if weight: st += f';font-weight:{weight}'
    if family: st += f';font-family:{family}'
    return f'<div class="dt {cls}" style="{st}">{txt}</div>'

def dvideo(file, x, y, w, h, mode='auto'):
    st = f'left:{U(x)};top:{U(y)};width:{U(w)};height:{U(h)}'
    if mode == 'click':
        return (f'<div class="dv media" style="{st}"><video data-click playsinline preload="none"><source src="assets/video/{file}" type="video/mp4"></video>'
                f'<button class="play" aria-label="Play video">{PLAY_SVG}</button></div>')
    return f'<div class="dv" style="{st}"><video muted loop playsinline autoplay preload="none"><source src="assets/video/{file}" type="video/mp4"></video></div>'

def dclip(file, clip, r):
    """video larger than its frame, cropped to the frame as in Figma. clip/r = (x, y, w, h) in frame px"""
    cx, cy, cw, ch = clip; x, y, w, h = r
    st = f'left:{round((x-cx)/cw*100,2)}%;top:{round((y-cy)/ch*100,2)}%;width:{round(w/cw*100,2)}%;height:{round(h/ch*100,2)}%'
    return (f'<div class="dvc" style="left:{U(cx)};top:{U(cy)};width:{U(cw)};height:{U(ch)}">'
            f'<video muted loop playsinline autoplay preload="none" style="{st}"><source src="assets/video/{file}" type="video/mp4"></video></div>')

def dmeta(y): return dtext('2026', 131, y, 300, 25, 'meta-d') + dtext('the work on', 1170, y, 400, 25, 'meta-d', 'right')
def dlabel(l, r, y, x1=151, x2=1108, color='#fff', light=False):
    w = 300 if light else 800
    return dtext(E(l), x1, y, 469, 24 if not light else 25, 'lbl', 'left', color, w) + dtext(E(r), x2, y, 469, 24 if not light else 25, 'lbl', 'right', color, w)
def dtitle(t, x, y, w, size=110, align='left'):
    return dtext('<br>'.join(E(p) for p in t.split('\n')), x, y, w, size, 'ttl', align)
def ddesc(t, x, w): return dtext(E(t), x, 734, w, 24, 'dsc', 'right', '#000', 300)

def desk(slug, overlays, extra_h=0, extra=''):
    tiles = DESK[slug]
    total = tiles[-1][1] + tiles[-1][2] + extra_h
    imgs = ''.join(f'<img src="{f}" alt="" width="1728" height="{round(h)}" style="top:{U(y)};height:{U(h)}" {"" if i < 2 else "loading=lazy"} decoding="async">' for i, (f, y, h, _) in enumerate(tiles))
    return f'<section class="desk" style="height:{U(total)}">{imgs}{extra}{"".join(overlays)}</section>'

def desk_brand(slug, title, desc_text, brand_label, desc_x, desc_w, tsize=110, more=()):
    o = [dmeta(261), dtitle(title, 131, 382, 700, tsize), ddesc(desc_text, desc_x, desc_w),
         dtext('logo', 121, 1047, 300, 25, 'lbl', 'left', '#fff', 300), dtext(E(brand_label), 1170, 1047, 400, 25, 'lbl', 'right', '#fff', 300)]
    return desk(slug, o + list(more))

DESCS = {
 'bf': 'Buchman Feder is a leading Israeli packaging company with nearly a century of experience, offering advanced packaging, logistics, and technology solutions worldwide.',
 'sh': 'A contemporary modest fashion brand blending modern trends with timeless elegance, offering stylish and versatile clothing for every woman.',
 'lb': 'Lil Buns is a bold and playful brioche brand that celebrates indulgence, irresistible flavors, and carefree moments. It\u2019s all about getting messy and enjoying every bite.',
 'bv': 'Boa Vida is a premium Brazilian-inspired açaí brand that celebrates quality, authenticity, and sophistication, offering a fresh, refined, and contemporary urban experience.'}

def desk_projects():
    o = [dmeta(261), dtitle('RAPIDOS', 339, 543, 1050, 127.1, 'center'),
         dlabel('In-Store Poster Design', 'RAPIDOS', 3816), dlabel('birthday', 'RAPIDOS', 5966),
         dmeta(7092), dtitle('BBB', 339, 7342, 1050, 127.1, 'center'),
         dlabel('Stranger Things Themed Event', 'BBB', 7859, 196, 1070), dlabel('birthday', 'bbb', 10703), dlabel('other', 'bbb', 11630),
         dmeta(12536), dtitle('LANDMARK', 339, 12779, 1050, 127.1, 'center'),
         dvideo('landmark.mp4', 447.9, 13378.3, 831.6, 534.1),
         dmeta(14178), dtitle('ELBIT', 339, 14399, 1050, 127.1, 'center'),
         dmeta(18955), dtitle('MOSES\nSHOP', 339, 19121, 1050, 127.1, 'center')]
    d_ol = ('pr/ms1', 'pr/ms3', 'pr/msb1', 'pr/msb2')
    grid = ''.join(f'<div>{outlined(k, "Moses Shop post") if k in d_ol else media(k, "Moses Shop post")}</div>' for k in ['pr/ms1', 'pr/ms2', 'pr/ms3', 'pr/msb1', 'pr/msb2', 'pr/msb3'])
    anchors = ''.join(f'<span class="anc" data-anchor="{a}" style="top:{U(y)}"></span>' for a, y in
                      [('rapidos', 200), ('bbb', 7030), ('landmark', 12470), ('elbit', 14118), ('moses-shop', 18888)])
    extra = anchors + f'<div class="moses-d" style="top:{U(19568)};height:{U(1662)}"><div class="mg">{grid}</div></div>'
    return desk('pr', o, 2382, extra)

# ================= PAGES =================
def home():
    hero = (f'<section class="hero mat">{header(overlay=True)}'
            f'<div class="hero-inner">{face_html("Illustrated portrait of Golan", cls="hero-face")}'
            '<h1>golan haba</h1><p class="role">graphic designer</p></div>'
            f'<picture><source media="(max-width: 899px)" srcset="{IMG}hm/scissors-m.webp">{img("hm/scissors", "", cls="tool scissors", lazy=False)}</picture>{img("hm/ruler", "", cls="tool ruler", lazy=False)}</section>')
    about = ('<section class="about" id="about">'
             f'<div class="reveal">{img("hm/portrait", "Golan Haba", cls="portrait")}</div>'
             '<div class="block hello reveal"><h2>hello</h2><p>I’m Golan! A graphic designer specializing in motion design and animation, '
             'with two years of experience working in a design&nbsp;studio.<br><br>I’m passionate about bringing ideas to life through movement, '
             'illustration, and creative storytelling. I love fresh challenges, bold ideas, and making designs stand&nbsp;out!<br><br>'
             '<strong>LET’S CREATE SOMETHING AMAZING&nbsp;TOGETHER!</strong></p></div>'
             '<div class="col">'
             f'<div class="block reveal"><h2>skills</h2><picture><source media="(max-width: 899px)" srcset="{IMG}hm/skills-m.webp">{img("hm/skills", "After Effects, Illustrator, InDesign, ChatGPT, Figma, Photoshop, Claude", cls="skills")}</picture></div>'
             '<div class="block reveal"><h2>experience</h2><p><strong>2025-present</strong><br><br>graphic designer - idea&nbsp;studio</p></div>'
             '<div class="block reveal"><h2>education</h2><p><strong>b.design visual communication</strong><br><br>holon institute of technology (hit) | 2020&#8209;2024</p></div>'
             '</div></section>')
    cards = ''.join(
        f'<a class="brand-card reveal" href="{h}"><span class="thumb">{media("hm/brand" + str(i + 1), n)}</span>'
        f'<span class="name">{E(n)}</span><span class="num">//0{i + 1}</span></a>'
        for i, (n, h) in enumerate(BRANDS))
    branding = (f'<section class="band-title mat" id="branding"><h2>branding</h2></section>'
                f'<section class="brand-grid">{cards}</section>')
    st = dark(label('Stranger Things Themed Event', 'BBB'),
              carousel(['pr/stpost1', 'pr/stpost2', 'pr/stpost3'], 'Stranger Things event post'),
              carousel(['pr/ststory1', 'pr/ststory2', 'pr/ststory3'], 'Stranger Things event story'),
              pair_row(['pr/stmenu1', 'pr/stmenu2'], 'Stranger Things event menu'),
              '<div class="more"><a class="btn" href="projects.html#bbb">more</a><small>for more projects</small></div>', pad=False)
    rap = dark(label('In-Store Poster Design', 'RAPIDOS'),
               carousel([f'pr/poster{i}' for i in range(1, 10)], 'Rapidos in-store poster'),
               '<div class="more"><a class="btn" href="projects.html#rapidos">more</a><small>for more projects</small></div>', pad=False)
    body = hero + about + branding + f'<div id="projects">{st}{rap}</div>'
    return page('Golan Haba — Graphic Designer', 'Portfolio of Golan Haba, a graphic designer specializing in branding, motion design and animation.', body, overlay=True)

def buchman():
    body = (intro('BUCHMAN\nFEDER', 'Buchman Feder is a leading Israeli packaging company with nearly a century of experience, offering advanced packaging, logistics, and technology solutions worldwide.') +
            logo_band('logo', 'buchman feder', 'bf/logo', 342) +
            mock(['bf/l1', ('bf/p1', 'bf/p2'), 'bf/l2', 'bf/l3', 'bf/l4', 'bf/l5', 'bf/l6', 'bf/l7', 'bf/l8'], 'Buchman Feder branding') +
            icons_row('bf/icons', 312, 'Buchman Feder icon set') +
            dark(label('website', 'buchman feder'), carousel([f'bf/web{i}' for i in range(1, 5)], 'Buchman Feder website', web=True),
                 carousel([f'bf/phone{i}' for i in range(1, 4)], 'Buchman Feder mobile site'),
                 label('social', 'buchman feder'), carousel([f'bf/post{i}' for i in range(1, 4)], 'Buchman Feder social post'),
                 carousel([f'bf/col{i}' for i in range(1, 7)], 'Buchman Feder collateral')))
    body = '<div class="mob">' + body + '</div>' + desk_brand('bf', 'BUCHMAN\nFEDER', DESCS['bf'], 'buchman feder', 827, 735, 110, [dvideo('buchman-anim-2.mp4', 211, 10888, 380, 506.5), dvideo('buchman-anim-3.mp4', 674.4, 10888, 380, 506.6), dvideo('buchman-anim-1.mp4', 1122, 10888, 380, 506.6)])
    return page('Buchman Feder — Golan Haba', 'Branding for Buchman Feder, an Israeli packaging company.', body)

def shira():
    body = (intro('SHIRA\nHADASHA', 'A contemporary modest fashion brand blending modern trends with timeless elegance, offering stylish and versatile clothing for every woman.') +
            logo_band('logo', 'SHIRA HADASHA', 'sh/logo', 168) + icons_row('sh/icons', 390, 'Shira Hadasha logo variations') +
            mock(['sh/l1', ('sh/p1', 'sh/p2'), 'sh/l2', 'sh/l3', 'sh/l4', 'sh/l5', 'sh/l6', 'sh/l7'], 'Shira Hadasha branding') +
            dark(label('highlights icons', 'SHIRA HADASHA'), f'<div class="logo-band reveal" style="--w:342px">{img("sh/hl", "Instagram highlight icons")}</div>',
                 label('social', 'SHIRA HADASHA'), carousel([f'sh/post{i}' for i in range(1, 4)], 'Shira Hadasha post'),
                 carousel([f'sh/postb{i}' for i in range(1, 4)], 'Shira Hadasha post'),
                 label('AI VIDEOS', 'SHIRA HADASHA'), carousel([f'sh/reel{i}' for i in range(1, 6)], 'Shira Hadasha AI video')))
    body = '<div class="mob">' + body + '</div>' + desk_brand('sh', 'SHIRA\nHADASHA', DESCS['sh'], 'SHIRA HADASHA', 876, 686, 110, [dlabel('highlights icons', 'SHIRA HADASHA', 7288, 152, 1109), dlabel('AI VIDEOS', 'SHIRA HADASHA', 10070, 152, 1109), dvideo('shira-reel-3.mp4', 197, 9197, 379, 673, 'click'), dvideo('shira-reel-2.mp4', 674, 9197, 379, 674, 'click'), dvideo('shira-reel-1.mp4', 1154, 9197, 379, 674, 'click'), dvideo('shira-reel-5.mp4', 434, 10231, 379, 673, 'click'), dvideo('shira-reel-4.mp4', 914, 10231, 379, 673, 'click')])
    return page('Shira Hadasha — Golan Haba', 'Branding for Shira Hadasha, a contemporary modest fashion brand.', body)

def lilbuns():
    body = (intro('LIL\nBUNS', 'Lil Buns is a bold and playful brioche brand that celebrates indulgence, irresistible flavors, and carefree moments. It’s all about getting messy and enjoying every bite.') +
            logo_band('logo', 'lil buns', 'lb/logo', 227) + icons_row('lb/icons', 390, 'Lil Buns logo variations') +
            mock(['lb/l1', ('lb/p1', 'lb/p2'), 'lb/l2', ('lb/p3', 'lb/p4'), 'lb/l3', 'lb/l4', 'lb/l5'], 'Lil Buns branding') +
            dark(label('website', 'lil buns'), carousel([f'lb/web{i}' for i in range(1, 5)], 'Lil Buns website', web=True)))
    body = '<div class="mob">' + body + '</div>' + desk_brand('lb', 'LIL\nBUNS', DESCS['lb'], 'lil buns', 876, 686, 110, [dvideo('lilbuns-bun.mp4', 936.6, 7896.7, 213.4, 219.2)])
    return page('Lil Buns — Golan Haba', 'Branding for Lil Buns, a bold and playful brioche brand.', body)

def boavida():
    seq = ['bv/l1', ('bv/p1', 'bv/p2'), 'bv/l2', ('bv/p3', 'bv/p4'), 'bv/l3', ('bv/p5', 'bv/p6'), 'bv/l4', ('bv/p7', 'bv/p8'),
           'bv/l5', ('bv/p9', 'bv/p10'), ('bv/p11', 'bv/p12')]
    body = (intro('BOA\nVIDA', 'Boa Vida is a premium Brazilian-inspired açaí brand that celebrates quality, authenticity, and sophistication, offering a fresh, refined, and contemporary urban experience.') +
            logo_band('logo', 'boa vida', 'bv/logo', 157) + icons_row('bv/icons', 390, 'Boa Vida icons') +
            mock(seq, 'Boa Vida branding') +
            dark(label('social', 'boa vida'), carousel([f'bv/post{i}' for i in range(1, 4)], 'Boa Vida social post')))
    body = '<div class="mob">' + body + '</div>' + desk_brand('bv', 'BOA\nVIDA', DESCS['bv'], 'boa vida', 876, 686, 127.1, [])
    return page('Boa Vida — Golan Haba', 'Branding for Boa Vida, a premium Brazilian-inspired açaí brand.', body)

def projects():
    body = ('<div class="proj">' + meta() + brand_title('RAPIDOS', id_='rapidos') +
            mock(['pr/rl1', ('pr/rp1', 'pr/rp2'), 'pr/rl2', ('pr/rp3', 'pr/rp4')], 'Rapidos campaign') +
            dark(label('In-Store Poster Design', 'RAPIDOS'), carousel([f'pr/poster{i}' for i in range(1, 10)], 'Rapidos in-store poster'),
                 label('birthday', 'RAPIDOS'), carousel(['pr/rbday1', 'pr/rbday2', 'pr/rbday3'], 'Rapidos birthday campaign')) +
            brand_title('BBB', 'h2', 'bbb') +
            dark(label('Stranger Things Themed Event', 'BBB'),
                 carousel(['pr/stpost1', 'pr/stpost2', 'pr/stpost3'], 'Stranger Things event post'),
                 carousel(['pr/ststory1', 'pr/ststory2', 'pr/ststory3'], 'Stranger Things event story'),
                 pair_row(['pr/stmenu1', 'pr/stmenu2'], 'Stranger Things event menu'),
                 label('birthday', 'bbb'), carousel(['pr/bbday1', 'pr/bbday2', 'pr/bbday3'], 'BBB birthday campaign'),
                 label('other', 'bbb'), carousel(['pr/bother1', 'pr/bother2', 'pr/bother3'], 'BBB campaign')) +
            brand_title('LANDMARK', 'h2', 'landmark') +
            '<section class="dark"><div class="landmark-shot reveal"><div class="screen">'
            f'{img("pr/landmark", "Landmark website")}'
            '<video muted loop playsinline autoplay preload="none" aria-label="Landmark website animation"><source src="assets/video/landmark.mp4" type="video/mp4"></video>'
            '</div></div></section>' +
            brand_title('ELBIT', 'h2', 'elbit') +
            mock(['pr/el1', ('pr/ep1', 'pr/ep2'), 'pr/el2', 'pr/el3', 'pr/el4', 'pr/el5', 'pr/el6', 'pr/el7'], 'Elbit Cyclone employee event') +
            brand_title('MOSES\nSHOP', 'h2', 'moses-shop') +
            dark(label('social', 'moses shop'), carousel(['pr/ms1', 'pr/ms2', 'pr/ms3'], 'Moses Shop post'),
                 carousel(['pr/msb1', 'pr/msb2', 'pr/msb3'], 'Moses Shop post', outline=('pr/msb1', 'pr/msb2', 'pr/msb3')))) + '</div>'
    body = '<div class="mob">' + body + '</div>' + desk_projects()
    return page('Projects — Golan Haba', 'Campaigns and social content for Rapidos, BBB, Landmark, Elbit and Moses Shop.', body)


# ================= MOTION & ILLUSTRATION =================
def grid(keys, cols=2, alt=''):
    return f'<div class="mgrid" style="--cols:{cols}">' + ''.join(f'<div>{media(k, alt)}</div>' for k in keys) + '</div>'

def motion():
    logos = ''.join(
        f'<a class="brand-card reveal" href="{h}"><span class="thumb">{media("hm/brand" + str(i + 1), n)}</span>'
        f'<span class="name">{E(n)}</span><span class="num">//0{i + 1}</span></a>'
        for i, (n, h) in enumerate(BRANDS))
    body = ('<div class="proj">' + meta() + brand_title('MOTION') +
            dark(label('logo animations', 'branding'), f'<div class="brand-grid in-dark">{logos}</div>', pad=False) +
            dark(label('animations', 'buchman feder'), carousel([f'bf/post{i}' for i in range(1, 4)], 'Buchman Feder animated post'),
                 label('ai videos', 'shira hadasha'), carousel([f'sh/reel{i}' for i in range(1, 6)], 'Shira Hadasha AI video'),
                 label('holiday animations', 'rosh hashana/shavuot'), carousel(['mo/hol1', 'mo/hol2', 'mo/hol3'], 'Holiday greeting animation'),
                 label('product animation', 'lil buns'), f'<div class="mfull reveal">{media("lb/web2", "Lil Buns website with the bun animation")}</div>',
                 label('social videos', 'moses shop'), carousel(['pr/msb1', 'pr/msb2', 'pr/msb3'], 'Moses Shop video post', outline=('pr/msb1', 'pr/msb2', 'pr/msb3')),
                 label('website animation', 'landmark'),
                 '<div class="landmark-shot reveal"><div class="screen">' + img("pr/landmark", "Landmark website") +
                 '<video muted loop playsinline autoplay preload="none" aria-label="Landmark website animation"><source src="assets/video/landmark.mp4" type="video/mp4"></video></div></div>') + '</div>')
    o = [dmeta(261), dtitle('MOTION', 339, 543, 1050, 127.1, 'center'),
         dlabel('logo animations', 'branding', 986, 152, 1109), dlabel('animations', 'buchman feder', 1635, 152, 1109),
         dlabel('ai videos', 'shira hadasha', 2523, 152, 1109), dlabel('holiday animations', 'rosh hashana/shavuot', 4300, 152, 1109),
         dlabel('product animation', 'lil buns', 5293, 152, 1109), dlabel('social videos', 'moses shop', 6320, 152, 1109),
         dlabel('website animation', 'landmark', 7174, 152, 1109),
         dclip('buchman-anim-1.mp4', (109, 1105, 340, 340), (75.7, 987.7, 413.8, 551.8)),
         dclip('shira-logo-anim.mp4', (499, 1105, 340, 340), (499, 1048.2, 340, 453.6)),
         dclip('lilbuns-logo-anim.mp4', (889, 1105, 340, 340), (889, 1105, 340, 340)),
         dclip('boavida-logo-anim.mp4', (1279, 1105, 340, 340), (1318.4, 1150.2, 261.1, 261.1)),
         dclip('buchman-anim-2.mp4', (210, 1817.1, 380.8, 506.5), (211, 1732.4, 380, 675.5)),
         dvideo('buchman-anim-3.mp4', 674.4, 1817, 380, 506.6), dvideo('buchman-anim-1.mp4', 1122, 1817, 380, 506.6),
         dvideo('shira-reel-3.mp4', 197, 2642, 379, 673, 'click'), dvideo('shira-reel-2.mp4', 674, 2642, 379, 674, 'click'),
         dvideo('shira-reel-1.mp4', 1154, 2642, 379, 674, 'click'), dvideo('shira-reel-5.mp4', 434, 3426, 379, 673, 'click'),
         dvideo('shira-reel-4.mp4', 914, 3426, 379, 673, 'click'),
         dvideo('holiday-1.mp4', 197, 4419, 379, 673, 'click'), dvideo('holiday-2.mp4', 674, 4419, 379, 674, 'click'),
         dvideo('holiday-3.mp4', 1154, 4419, 379, 674, 'click'),
         dvideo('lilbuns-bun.mp4', 476.4, 5605.4, 314.1, 322.6),
         dvideo('moses-video-1.mp4', 422, 6499, 379, 474), dvideo('moses-video-2.mp4', 923, 6505, 382, 478),
         dvideo('landmark.mp4', 448, 7411, 831.6, 534.1)]
    body = '<div class="mob">' + body + '</div>' + desk('mo', o)
    return page('Motion — Golan Haba', 'Motion design: logo animations, animated posts, AI videos, holiday greetings and website animations.', body)

def illustration():
    body = ('<div class="proj">' + meta() + brand_title('ILLUSTRATION') +
            dark(label('storyboard', 'ashmat rabim'), f'<div class="mfull reveal">{media("il/ashmat", "Ashmat Rabim animated short")}</div>',
                 grid([f'il/sb{i}' for i in range(1, 7)], 2, 'Ashmat Rabim storyboard frame'),
                 label('character design', 'final project'), f'<div class="mfull reveal">{media("il/final", "Final project animated short")}</div>',
                 grid([f'il/fp{i}' for i in range(1, 7)], 2, 'Final project still'),
                 grid([f'il/ch{i}' for i in range(1, 8)], 4, 'Character design'),
                 label('character design', 'fox mask'), f'<div class="mfull reveal">{img("il/foxkey", "Fox mask character in a neon alley")}</div>',
                 f'<div class="mfull reveal">{media("il/fox360", "Fox mask character turnaround")}</div>',
                 carousel([f'il/fox{i}' for i in range(1, 8)], 'Fox mask character design'),
                 label('illustrations', 'editorial & posters'), carousel([f'il/ed{i}' for i in range(1, 5)], 'Editorial illustration')) + '</div>')
    o = [dmeta(261), dtitle('ILLUSTRATION', 164, 543, 1400, 127.1, 'center'),
         dlabel('storyboard', 'ashmat rabim', 986, 152, 1109), dlabel('character design', 'final project', 2620, 152, 1109),
         dlabel('character design', 'fox mask', 4597, 152, 1109), dlabel('illustrations', 'editorial & posters', 6672, 152, 1109),
         dvideo('ashmat-rabim.mp4', 152, 1105, 1424, 801, 'click'), dvideo('final-project.mp4', 152, 2739, 1424, 801, 'click'),
         dvideo('fox-mask-360.mp4', 152, 4716, 565, 801)]
    body = '<div class="mob">' + body + '</div>' + desk('il', o)
    return page('Illustration — Golan Haba', 'Illustration: storyboards, character design and editorial posters.', body)

# ================= INTERACTIVE (scroll-driven) VERSION =================
IX_BRANDS = [
    ('buchman-feder', 'BUCHMAN FEDER', '01', '#2f3226', 'bf/logo', DESCS['bf'],
     ['bf/l1', ('v', 'buchman-anim-2.mp4', 'bf/post1', 720, 1280), 'bf/l4', 'bf/web1', 'bf/l3', ('v', 'buchman-anim-3.mp4', 'bf/post2', 720, 960), 'bf/l5', 'bf/l8']),
    ('shira-hadasha', 'SHIRA HADASHA', '02', '#2a221e', 'sh/logo', DESCS['sh'],
     ['sh/l1', 'sh/l2', ('v', 'shira-reel-1.mp4', 'sh/reel1', 720, 1280), 'sh/l3', 'sh/l5', ('v', 'shira-reel-3.mp4', 'sh/reel3', 720, 1280), 'sh/l7']),
    ('lil-buns', 'LIL BUNS', '03', '#5b36c9', 'lb/logo', DESCS['lb'],
     ['lb/l1', ('v', 'lilbuns-bun.mp4', 'lb/p1', 640, 656), 'lb/l2', 'lb/web1', 'lb/l3', 'lb/l4', 'lb/l5']),
    ('boa-vida', 'BOA VIDA', '04', '#2b1d1e', 'bv/logo', DESCS['bv'],
     ['bv/l1', 'bv/p1', 'bv/l2', ('v', 'boavida-logo-anim.mp4', 'bv/post1', 720, 720), 'bv/l3', 'bv/p5', 'bv/l4', 'bv/l5']),
]

def ix_item(it, cls='ix-item'):
    if isinstance(it, tuple):
        _, file, poster, w, h = it
        return (f'<div class="{cls} is-video" style="--ar:{w / h:.4f}"><video muted loop playsinline preload="none" poster="{IMG}{poster}.webp" aria-hidden="true">'
                f'<source src="assets/video/{file}" type="video/mp4"></video></div>')
    w, h = size(it)
    return f'<div class="{cls}" style="--ar:{w / h:.4f}">{img(it, "")}</div>'

def interactive():
    piece = lambda cls, inner: f'<div class="ix-piece {cls}"><div class="ix-fly">{inner}</div></div>'
    nav = header(overlay=True).replace('index.html#about', '#about')
    hero = ('<section class="ix-hero" data-pin><div class="ix-stick mat">' + nav +
            piece('p-ruler', img("hm/ruler", "", lazy=False)) + piece('p-scissors', img("hm/scissors", "", lazy=False)) +
            '<div class="ix-hero-in">' + piece('p-face', face_html("Illustrated portrait of Golan", cls="ix-face")) +
            piece('p-name', '<h1 class="ix-name">golan haba</h1>') +
            piece('p-role', '<p class="ix-role">graphic designer · branding &amp; motion</p>') + '</div>'
            '<div class="ix-hint" aria-hidden="true">scroll<span></span></div></div></section>')
    about = ('<section class="ix-about" id="about" data-pin><div class="ix-stick ix-about-in">'
             f'<div class="ix-portrait">{img("hm/portrait", "Golan Haba", lazy=False)}</div>'
             '<div class="ix-about-txt">'
             '<div class="ix-step"><h2 class="ix-h2 big">hello</h2><p>I’m Golan! A graphic designer specializing in motion design and animation, with two years of experience working in a design&nbsp;studio.</p><p>I’m passionate about bringing ideas to life through movement, illustration, and creative storytelling.</p><p><strong>Let’s create something amazing&nbsp;together!</strong></p></div>'
             f'<div class="ix-step"><h2 class="ix-h2">skills</h2>{img("hm/skills", "After Effects, Illustrator, InDesign, ChatGPT, Figma, Photoshop, Claude", cls="ix-skills")}</div>'
             '<div class="ix-step ix-row"><div><h2 class="ix-h2">experience</h2><p><strong>2025 – present</strong><br>graphic designer – idea studio</p></div>'
             '<div><h2 class="ix-h2">education</h2><p><strong>b.design visual communication</strong><br>hit – holon institute of technology</p></div></div>'
             '</div></div></section>')
    band = lambda t, id_='': f'<section class="ix-band mat"{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""}><h2 class="ix-band-t">{t}</h2></section>'
    brands = ''
    for slug, name, num, color, logo, desc_, items in IX_BRANDS:
        track = ''.join(ix_item(i) for i in items) + f'<a class="ix-item ix-more" href="{slug}.html"><span>view <br>project</span><b>→</b></a>'
        brands += (f'<section class="ix-brand" data-brand style="--bg:{color}"><div class="ix-stick ix-brand-in">'
                   f'<div class="ix-cover"><div class="ix-logo">{img(logo, name + " logo", lazy=False)}</div></div>'
                   f'<div class="ix-info"><span class="ix-num">//{num}</span><h3>{E(name)}</h3><p>{E(desc_)}</p>'
                   f'<a class="ix-pill" href="{slug}.html">view the full branding →</a></div>'
                   f'<div class="ix-track-wrap"><div class="ix-track">{track}</div></div></div></section>')
    posters = ''.join(f'<div class="ix-card">{img(f"pr/poster{i}", "Rapidos in-store poster", lazy=False)}</div>' for i in range(1, 10))
    stack = ('<section class="ix-stack" data-pin><div class="ix-stick ix-stack-in">'
             '<div class="ix-stack-head"><span>in-store poster design</span><h3>RAPIDOS</h3></div>'
             f'<div class="ix-cards">{posters}</div>'
             '<a class="ix-pill" href="projects.html#rapidos">more rapidos →</a></div></section>')
    def grid(title, sub, keys, href, cls=''):
        cells = ''.join(f'<div class="rv" style="--d:{(n % 3) * 90}ms">{ix_item(k, "ix-cell")}</div>' for n, k in enumerate(keys))
        return (f'<section class="ix-show {cls}"><div class="ix-show-head rv"><span>{sub}</span><h3>{title}</h3></div>'
                f'<div class="ix-grid">{cells}</div><a class="ix-pill rv" href="{href}">see the project →</a></section>')
    shows = (grid('BBB', 'stranger things themed event', ['pr/stpost1', 'pr/stpost2', 'pr/stpost3', 'pr/ststory1', 'pr/ststory2', 'pr/ststory3'], 'projects.html#bbb') +
             grid('MOSES SHOP', 'social', ['pr/ms1', ('v', 'moses-video-1.mp4', 'pr/msb1', 720, 900), 'pr/ms3', 'pr/msb2', ('v', 'moses-video-2.mp4', 'pr/msb3', 720, 900), 'pr/ms2'], 'projects.html#moses-shop', 'light') +
             '<section class="ix-show ix-elbit"><div class="ix-show-head rv"><span>cyclone employee event</span><h3>ELBIT</h3></div>'
             '<div class="ix-par">' + ''.join(f'<div class="ix-par-i rv" data-speed="{sp}">{img(k, "Elbit Cyclone event")}</div>' for k, sp in [('pr/el1', '0'), ('pr/el3', '0.15'), ('pr/el5', '-0.1'), ('pr/el7', '0.2')]) + '</div>'
             '<a class="ix-pill rv" href="projects.html#elbit">see the project →</a></section>')
    soc = ''.join(f'<a href="{h}" target="_blank" rel="noopener"><img src="assets/icons/{k}.svg" width="28" height="28" alt="{E(n)}"></a>' for n, h, k in SOCIALS)
    contact = ('<section class="ix-contact" id="contact" data-pin><div class="ix-stick mat ix-contact-in">'
               '<div class="ix-cm"><img src="assets/img/contact.gif" width="1272" height="268" alt="Contact me"></div>'
               f'<div class="ix-end"><p>stay in touch</p><div class="ix-soc">{soc}</div>'
               '<a class="ix-pill white" href="index.html">classic version of the site</a></div></div></section>')
    head = '<div class="ix-bar" aria-hidden="true"><span></span></div>'
    body = (head + '<main>' + hero + about + band('branding', 'branding') + brands + band('projects', 'projects') + stack + shows + contact + '</main>')
    return f'''<!doctype html>
<html lang="en">
<head>
{GTM_HEAD}<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Golan Haba — Interactive Portfolio</title>
<meta name="description" content="Interactive scroll portfolio of Golan Haba, graphic designer: branding and motion.">
<meta property="og:title" content="Golan Haba — Interactive Portfolio">
<meta property="og:image" content="assets/img/hm/face.webp">
<link rel="icon" href="assets/img/hm/face.webp">
{FONT_LINKS}
<link rel="stylesheet" href="assets/css/style.css">
<link rel="stylesheet" href="assets/css/interactive.css">
</head>
<body id="top">
{GTM_BODY}{body}
{menu_html().replace('index.html#about', '#about')}
<script src="assets/js/main.js"></script>
<script src="assets/js/interactive.js"></script>
</body>
</html>
'''

PAGES = {'index.html': home, 'buchman-feder.html': buchman, 'shira-hadasha.html': shira,
         'lil-buns.html': lilbuns, 'boa-vida.html': boavida, 'projects.html': projects, 'motion.html': motion, 'illustration.html': illustration, 'interactive.html': interactive}

if __name__ == '__main__':
    for name, fn in PAGES.items():
        with open(os.path.join(ROOT, name), 'w', encoding='utf-8') as f:
            f.write(fn())
        print('built', name)

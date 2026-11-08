# -*- coding: utf-8 -*-
"""
极站 GOSITE 站点构建脚本
产出 7 个纯静态 HTML 页面（无任何后端依赖），共用一套 CSS / JS / 页头页脚。
日常改内容：直接改对应 .html；批量同步导航与页脚：改本脚本后重跑一次。
"""
import os
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = "极站 GOSITE"
SLOGAN = "快官网上线与代运营服务"
SITE_URL = "https://gd.ippi.com.cn/"

# ---------------------------------------------------------------- 图标
P = {
    "bolt": '<path d="M13 2 4.5 13.5H11l-1 8.5L19.5 10H13z"/>',
    "feather": '<path d="M20.2 12.2a6 6 0 0 0-8.5-8.5L5 10.5V19h8.5z"/><path d="M16 8 2 22M17.5 15H9"/>',
    "refresh": '<path d="M3 12a9 9 0 0 1 15.5-6.2L21 8M21 3v5h-5M21 12a9 9 0 0 1-15.5 6.2L3 16M3 21v-5h5"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "headset": '<path d="M3 14v-2a9 9 0 0 1 18 0v2"/><rect x="2" y="13" width="4" height="7" rx="2"/><rect x="18" y="13" width="4" height="7" rx="2"/><path d="M21 20a4 4 0 0 1-4 4h-3"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.5.5l2-2a5 5 0 0 0-7-7l-1 1M14 11a5 5 0 0 0-7.5-.5l-2 2a5 5 0 0 0 7 7l1-1"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 0 1 0 18 15 15 0 0 1 0-18"/>',
    "cart": '<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h2l2.5 12h12l2-8H6"/>',
    "layout": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 9v12"/>',
    "code": '<path d="m8 8-4 4 4 4M16 8l4 4-4 4M14 4l-4 16"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "check": '<path d="m4 12 5 5L20 6"/>',
    "checkcircle": '<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>',
    "pen": '<path d="M12 20h9M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4z"/>',
    "phone": '<rect x="6" y="2" width="12" height="20" rx="3"/><path d="M11 18h2"/>',
    "layers": '<path d="m12 2 9 5-9 5-9-5zM3 12l9 5 9-5M3 17l9 5 9-5"/>',
    "users": '<circle cx="9" cy="8" r="3"/><path d="M3 21v-2a6 6 0 0 1 12 0v2M16 5a3 3 0 0 1 0 6M18 21v-2a5 5 0 0 0-2-4"/>',
    "tag": '<path d="M20 12 12 20 3 11V3h8z"/><circle cx="7.5" cy="7.5" r="1.2"/>',
    "box": '<path d="m12 2 9 5v10l-9 5-9-5V7zM3 7l9 5 9-5M12 12v10"/>',
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
    "cloud": '<path d="M6 18a4 4 0 0 1 .5-8A6 6 0 0 1 18 9a4.5 4.5 0 0 1 0 9z"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "spark": '<path d="m12 3 1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 16v3M17.5 17.5h3"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "qr": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><path d="M14 14h3v3h-3zM19 19h2M14 19h2M19 14h2"/>',
    "message": '<path d="M21 12a8 8 0 0 1-11.6 7.1L3 21l1.9-6.4A8 8 0 1 1 21 12z"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM14 2v6h6M8 13h8M8 17h5"/>',
    "rocket": '<path d="M5 15c-1 2-1 5-1 5s3 0 5-1M9 15 5 11c1-5 5-9 14-9 0 9-4 13-9 14l-4-4z"/><circle cx="14.5" cy="8.5" r="1.5"/>',
    "sliders": '<path d="M4 7h10M18 7h2M4 17h2M10 17h10"/><circle cx="16" cy="7" r="2"/><circle cx="8" cy="17" r="2"/>',
    "wallet": '<rect x="2" y="6" width="20" height="14" rx="2"/><path d="M2 10h20M16 15h3"/>',
    "eye": '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "database": '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
    "gift": '<rect x="3" y="9" width="18" height="12" rx="1"/><path d="M3 13h18M12 9v12M12 9S8 3 5.5 5.5 9 9 12 9zM12 9s4-6 6.5-3.5S15 9 12 9z"/>',
    "megaphone": '<path d="M3 11v2a2 2 0 0 0 2 2h2l8 5V4L7 9H5a2 2 0 0 0-2 2zM18 9a4 4 0 0 1 0 6"/>',
    "store": '<path d="M3 9 5 3h14l2 6v2a3 3 0 0 1-6 0 3 3 0 0 1-6 0 3 3 0 0 1-6 0zM5 13v8h14v-8M10 21v-5h4v5"/>',
}


def icon(name, size=0, cls=""):
    style = ' style="width:%dpx;height:%dpx"' % (size, size) if size else ""
    return ('<svg class="%s"%s viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
            % (cls, style, P.get(name, "")))


def city_svg():
    heights = [92, 146, 112, 188, 130, 214, 160, 246, 192, 148, 224, 120, 172, 205,
               140, 182, 104, 156, 236, 132, 196, 164, 116, 208, 144, 176, 226, 124, 184, 152, 200, 118]
    rects, x, i = [], 0, 0
    while x < 1460:
        h = heights[i % len(heights)]
        w = 38 + (i % 4) * 9
        rects.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="url(#bld)"/>'
                     % (x, 330 - h, w - 7, h))
        for wy in range(330 - h + 16, 316, 24):
            rects.append('<rect x="%d" y="%d" width="%d" height="3" rx="1.5" fill="rgba(255,255,255,.5)"/>'
                         % (x + 9, wy, w - 25))
        x += w
        i += 1
    return ('<svg class="city" viewBox="0 0 1440 330" preserveAspectRatio="none" aria-hidden="true">'
            '<defs><linearGradient id="bld" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="rgba(96,164,255,.34)"/>'
            '<stop offset="1" stop-color="rgba(255,255,255,.02)"/></linearGradient></defs>'
            + "".join(rects) + '</svg>')


# ---------------------------------------------------------------- 框架
NAV = [
    ("首页", "index.html", "index"),
    ("网站建设", "website.html", "website"),
    ("商城小程序", "miniprogram.html", "miniprogram"),
    ("成功案例", "cases.html", "cases"),
    ("服务亮点", "service.html", "service"),
    ("价格套餐", "pricing.html", "pricing"),
    ("联系我们", "contact.html", "contact"),
]


def head(title, desc, keywords):
    page = PAGE_KEY
    url = SITE_URL + ("" if page == "index" else page + ".html")
    og = SITE_URL + "assets/img/og-image.png"
    org_id = SITE_URL + "#organization"
    graph = [
        {"@type": "Organization", "@id": org_id, "name": BRAND, "url": SITE_URL,
         "logo": {"@type": "ImageObject", "url": SITE_URL + "assets/img/logo.png"},
         "description": SLOGAN},
        {"@type": "WebSite", "@id": SITE_URL + "#website", "url": SITE_URL,
         "name": BRAND, "publisher": {"@id": org_id}, "inLanguage": "zh-CN"},
        {"@type": "Service", "name": "纯静态企业官网上线与代运营维护",
         "serviceType": "网站建设 / 网站代运营 / 微信商城小程序",
         "provider": {"@id": org_id}, "areaServed": "中国",
         "description": "纯静态官网最快当天上线，改稿当天发布，全年代运营维护更新；同步提供微信商城小程序搭建。",
         "offers": {"@type": "Offer", "price": "399", "priceCurrency": "CNY",
                    "description": "限时价，仅限前 10 名且资料齐全；标准价 998 元 / 年"}},
    ]
    crumbs = [{"@type": "ListItem", "position": 1, "name": "首页", "item": SITE_URL}]
    if page != "index":
        label = next((t for t, u, k in NAV if k == page), "网站地图")
        crumbs.append({"@type": "ListItem", "position": 2, "name": label, "item": url})
    graph.append({"@type": "BreadcrumbList", "itemListElement": crumbs})
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph},
                    ensure_ascii=False, separators=(",", ":"))
    d = dict(title=title, brand=BRAND, desc=desc, keywords=keywords,
             url=url, og=og, ld=ld, page=page)
    return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s | %(brand)s</title>
<meta name="description" content="%(desc)s">
<meta name="keywords" content="%(keywords)s">
<meta name="author" content="%(brand)s">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="%(url)s">
<meta property="og:type" content="website">
<meta property="og:site_name" content="%(brand)s">
<meta property="og:locale" content="zh_CN">
<meta property="og:title" content="%(title)s | %(brand)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(url)s">
<meta property="og:image" content="%(og)s">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(title)s | %(brand)s">
<meta name="twitter:description" content="%(desc)s">
<meta name="twitter:image" content="%(og)s">
<meta name="theme-color" content="#1a6bff">
<link rel="icon" href="favicon.ico" type="image/x-icon">
<link rel="apple-touch-icon" href="assets/img/icon-192.png">
<link rel="stylesheet" href="assets/css/style.css">
<script src="assets/js/main.js" defer></script>
<script type="application/ld+json">%(ld)s</script>
</head>
<body data-page="%(page)s">
''' % d


def topbar():
    return '''<div class="topbar"><div class="container">
<span><i class="spark"></i><b>限时福利</b>　399 元仅限前 10 名且资料齐全<span class="hide-sm">　|　标准价 998 元 / 年，先看设计稿满意再付款</span></span>
<a href="contact.html#consult">立即扫码咨询 &rarr;</a>
</div></div>
'''


def navbar():
    links = "".join(
        '<a href="%s" data-nav="%s">%s</a>' % (url, key, label)
        for label, url, key in NAV)
    return '''<header class="nav"><div class="container">
<a class="brand" href="index.html" aria-label="%s 首页">
<img src="assets/img/logo.png" alt="%s LOGO"><span class="brand-txt"><strong>极站</strong><span>GOSITE</span></span></a>
<nav class="nav-menu" aria-label="主导航">%s</nav>
<a class="btn btn-primary nav-cta" href="contact.html#consult">%s 扫码咨询</a>
<button class="menu-btn" aria-label="展开导航菜单" aria-expanded="false"><i></i></button>
</div></header>
''' % (BRAND, BRAND, links, icon("qr", 15))


def footer():
    cols = "".join('<li><a href="%s">%s</a></li>' % (u, t) for t, u, k in NAV if k != "index")
    friends = [
        ("广东省湖南攸县商会", "https://www.zyyous.com/"),
        ("才猎天下大数据", "https://www.91cailie.com/"),
        ("湾区（广东）数字经济研究院", "https://www.baydea.com/"),
    ]
    friend_links = "".join('<a href="%s" target="_blank" rel="noopener">%s</a>' % (u, t) for t, u in friends)
    return '''<footer class="footer"><div class="container">
<div class="footer-top">
<div>
<a class="brand" href="index.html"><img src="assets/img/logo.png" alt="%s LOGO"><span class="brand-txt"><strong>极站</strong><span>GOSITE</span></span></a>
<p class="footer-about">%s。纯静态官网最快当天上线，改稿当天发布，全年内容更新有人管；商城小程序同步搭建，让企业在微信里也能把生意做起来。</p>
<div style="margin-top:18px;display:flex;gap:8px;flex-wrap:wrap;justify-content:center">
<span class="pill" style="background:rgba(255,255,255,.12);color:#fff;border-color:rgba(255,255,255,.22)">399 元包年</span>
<span class="pill" style="background:rgba(255,255,255,.12);color:#fff;border-color:rgba(255,255,255,.22)">最快当天上线</span>
</div>
</div>
<div><h4>快速导航</h4><ul>%s</ul></div>
<div><h4>服务关键词</h4><ul>
<li><a href="website.html">纯静态企业官网</a></li><li><a href="website.html">快速上线 / 快速修改</a></li>
<li><a href="service.html">网站代运营维护</a></li><li><a href="miniprogram.html">微信商城小程序</a></li>
<li><a href="cases.html">商会 / 教育 / 研究院案例</a></li><li><a href="pricing.html">399 元包年套餐</a></li>
</ul></div>
<div><h4>咨询与合作</h4>
<img class="footer-qr" src="assets/img/qrcode.png" alt="微信扫码咨询二维码">
<p class="footer-contact"><b>微信扫码咨询</b></p>
</div>
</div>
<div class="footer-links">
<span class="fl-label">友情链接</span>
%s
<span class="fl-sep">·</span>
<a href="sitemap.html">网站地图</a>
</div>
<div class="footer-tech">
<span>网站技术服务支持：</span>
<a href="https://www.gdiis.com" target="_blank" rel="noopener"><img src="assets/img/gdiis-logo.png" alt="创享互联 GDIIS" loading="lazy"> GDIIS · 创享互联</a>
</div>
<div class="footer-bottom"><span>&copy; <span data-year>2026</span> %s · %s</span>
<span>专注中小企业：官网快上线 · 内容代运营 · 商城小程序</span></div>
</div></footer>
''' % (BRAND, SLOGAN, cols, friend_links, BRAND, SLOGAN)

def wrap(title, desc, keywords, active, body):
    global PAGE_KEY
    PAGE_KEY = active
    return (head(title, desc, keywords) + topbar() + navbar() +
            "<main>\n" + body + "\n</main>\n" + footer() + "</body>\n</html>\n")


# ---------------------------------------------------------------- 组件
def sechead(eyebrow, h2, lead="", center=True, extra=""):
    cls = "sec-head center" if center else "sec-head"
    leadhtml = '<p class="lead">%s</p>' % lead if lead else ""
    return ('<div class="%s reveal"><div class="eyebrow">%s</div><h2 class="h2">%s</h2>%s%s</div>'
            % (cls, eyebrow, h2, leadhtml, extra))


def pagehero(crumb, h1, desc, pills=None, eyebrow=""):
    ph = ""
    if pills:
        ph = '<div class="pills">' + "".join(
            '<span class="pill %s">%s</span>' % (cls, txt) for txt, cls in pills) + '</div>'
    eb = '<div class="eyebrow" style="justify-content:center">%s</div>' % eyebrow if eyebrow else ""
    return '''<section class="page-hero"><div class="container">
<div class="crumb"><a href="index.html">首页</a> / %s</div>
%s<h1>%s</h1><p>%s</p>%s
</div></section>
''' % (crumb, eb, h1, desc, ph)


def cards(items, cols="g3"):
    """items: (icon, color, title, desc)"""
    out = []
    for i, (ic, color, title, desc) in enumerate(items):
        out.append('''<article class="card glass reveal d%d"><span class="num">%02d</span>
<div class="ico %s">%s</div><h3 class="h3">%s</h3><p>%s</p></article>'''
                   % (i % 4, i + 1, color, icon(ic), title, desc))
    return '<div class="grid %s">%s</div>' % (cols, "".join(out))


def qr_card():
    return '''<div class="qr-card">
<img src="assets/img/qrcode.png" alt="微信扫码咨询二维码">
<h4>微信扫码 · 先聊需求</h4>
<p>扫码说明行业、栏目与上线时间<br>我们出方案与首页设计稿</p>
<span class="qr-badge">%s 前 10 名：设计满意再付款</span>
</div>''' % icon("message", 13)


def cta_section(title=None, desc=None):
    title = title or '官网不用等，<span style="color:#ffe27a">也不用自己管</span>'
    desc = desc or ("纯静态官网 最快当天上线，改稿当天发布；全年内容更新、栏目调整、活动页搭建由我们接手。"
                    "先在微信里把需求说清楚，设计稿满意了再谈付款。")
    checks = ["纯静态官网整站", "移动端自适应", "基础 SEO 结构", "全年代运营更新",
              "改稿当天发布", "HTTPS / CDN 托管协助", "微信内打开与分享", "域名解析协助"]
    li = "".join('<li>%s<span>%s</span></li>' % (icon("checkcircle", 17), c) for c in checks)
    return '''<section class="section tight"><div class="container">
<div class="cta-dark reveal"><div class="cta-grid">
<div>
<span class="pill" style="background:rgba(255,255,255,.16);color:#fff;border-color:rgba(255,255,255,.3)">%s 限时福利 · 限前 10 名咨询者</span>
<h2 style="margin-top:18px">%s</h2>
<div class="price-big"><span class="cur">¥</span><span class="num">399</span><span class="unit">/ 年包干</span></div>
<p style="margin-top:2px;font-weight:800">官网整站 + 全年代运营维护更新</p>
<p style="margin-top:12px">%s</p>
<ul class="cta-checks">%s</ul>
<div class="cta-actions"><a class="btn btn-white btn-lg" href="pricing.html">%s 查看套餐详情</a>
<a class="btn btn-outline btn-lg" href="contact.html#consult">%s 扫码咨询</a></div>
<p class="cta-note">标准价 998 元 / 年；399 元仅限前 10 名且资料齐全的咨询者。设计满意再付款，具体服务清单以咨询确认的方案为准。</p>
</div>
%s
</div></div></div></section>
''' % (icon("gift", 14), title, desc, li, icon("arrow", 16), icon("qr", 16), qr_card())


def faq(items):
    return '<div class="faq">' + "".join(
        '<details class="faq-item reveal"><summary>%s</summary><p>%s</p></details>' % (q, a)
        for q, a in items) + '</div>'


def case_card(img, name, url, tag, points, desc, no):
    pts = "".join('<span>%s</span>' % p for p in points)
    return '''<article class="case-card reveal">
<div class="case-shot"><div class="browser-dots"><i></i><i></i><i></i></div>
<img src="assets/cases/%s.png" alt="%s 网站首页截图" loading="lazy">
<a class="case-shot-name" href="%s" target="_blank" rel="noopener">%s %s</a></div>
<div class="case-body">
<div class="case-meta"><span class="tagx">%s</span><span class="url">%s</span></div>
<h3><a href="%s" target="_blank" rel="noopener">%s</a></h3><p>%s</p><div class="case-points">%s</div>
<div class="case-foot"><span class="no">CASE %s</span><a class="link-more" href="%s" target="_blank" rel="noopener">查看线上站点 %s</a></div>
</div></article>''' % (img, name, url, name, icon("arrow", 13), tag, url, url, name, desc, pts, no, url, icon("arrow", 14))


def flow(items):
    out = []
    for i, (title, desc, day) in enumerate(items):
        out.append('''<div class="flow-item reveal d%d"><div class="flow-dot">%02d</div>
<h4>%s</h4><p>%s</p><span class="day">%s</span></div>''' % (i % 4, i + 1, title, desc, day))
    return '<div class="flow">%s</div>' % "".join(out)


def taglist(tags):
    return '<div class="tag-list">' + "".join('<span>%s</span>' % t for t in tags) + '</div>'


def checklist(items):
    return '<ul class="check-list">' + "".join(
        '<li>%s<span>%s</span></li>' % (icon("checkcircle"), t) for t in items) + '</ul>'


def table(headers, rows):
    th = "".join('<th>%s</th>' % h for h in headers)
    tr = "".join('<tr>' + "".join('<td>%s</td>' % c for c in row) + '</tr>' for row in rows)
    return '<div class="table-wrap reveal"><table class="tbl"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (th, tr)


# ---------------------------------------------------------------- 首页
def hero_art():
    left = [("百度", "#2932e1", "百"), ("必应", "#008373", "b"), ("360", "#19b955", "3"),
            ("搜狗", "#f04b22", "S"), ("搜一搜", "#07c160", "微"), ("AI 问答", "#7a4bff", "AI")]
    right = [("公众号", "#07c160", "公"), ("小程序", "#1a6bff", "小"), ("企业微信", "#2b7bff", "企"),
             ("短视频", "#111827", "短"), ("名片码", "#e2157f", "码"), ("AI 入口", "#4d6bff", "D")]
    def chips(data):
        return "".join('<span class="chip"><i style="background:%s">%s</i>%s</span>' % (c, m, t)
                       for t, c, m in data)
    return '''<div class="hero-art" aria-hidden="true">
<div class="art-halo"></div><div class="art-ring"></div>
<div class="art-beam l"></div><div class="art-beam r"></div>
<div class="glass-panel left"><div class="panel-title">%s 搜索能搜到</div><div class="chips">%s</div></div>
<div class="glass-panel right"><div class="panel-title">%s 客户能找到</div><div class="chips">%s</div></div>
<div class="core"><div class="core-shape"></div><div class="core-inner">
<div class="core-badge">%s</div>
<div class="core-name">极站官网</div>
<div class="core-tag">快上线 · 常更新</div>
<div class="core-sub">静态架构 / 一次搭建<br>全年代运营维护</div>
</div></div>
<div class="pedestal"></div>
<span class="float-tag f1">最快当天上线</span><span class="float-tag f2">改稿当天发布</span><span class="float-tag f3">399 元包年</span>
</div>''' % (icon("search", 14), chips(left), icon("globe", 14), chips(right), icon("globe", 23))


def p_index():
    b = []
    b.append('''<section class="hero"><div class="hero-bg"><div class="glow g1"></div><div class="glow g2"></div><div class="glow g3"></div>%s</div>
<div class="container"><div class="hero-inner">
<div class="hero-copy">
<div class="hero-kicker"><span></span>AI 时代 · 企业官网快上线服务</div>
<h1><span class="l1">AI 时代，企业需要一个</span>
<span class="l2"><span class="t-blue">上得快</span>、<span class="t-pink">改得快</span>的<span class="t-grad">官网</span></span></h1>
<p class="hero-sub"><strong>纯静态架构 · 最快当天上线 · 改稿当天发布 · 全年代运营维护。</strong>不用等开发排期，不用自己改后台，官网交给一支专门做「快上线 + 长期维护」的团队。</p>
<div class="hero-actions"><a class="btn btn-primary btn-lg" href="pricing.html">%s 399 元包年 · 看套餐</a>
<a class="btn btn-ghost btn-lg" href="cases.html">%s 看真实案例</a></div>
<div class="hero-trust">
<div>%s <b>最快当天</b> 可上线</div><div>%s <b>399</b> 元包年</div>
<div>%s <b>前 10 名</b> 满意再付款</div><div>%s <b>全年</b> 有人管更新</div>
</div></div>
%s
</div></div></section>''' % (city_svg(), icon("rocket", 16), icon("arrow", 16),
                             icon("checkcircle", 15), icon("checkcircle", 15),
                             icon("checkcircle", 15), icon("checkcircle", 15), hero_art()))

    b.append('''<div class="container"><div class="stat-strip glass reveal">
<div class="stat"><b>当天<small>上线</small></b><span>资料齐备，最快当天可上线</span></div>
<div class="stat"><b>399<small>元/年</small></b><span>官网整站 + 全年维护更新</span></div>
<div class="stat"><b>当天<small>发布</small></b><span>文字图片改动即时生效</span></div>
<div class="stat"><b>2<small>大主业</small></b><span>静态官网 + 商城小程序</span></div>
</div></div>''')

    b.append('''<section class="section"><div class="container">
%s
<div class="grid g3" style="margin-top:8px">
<div class="card glass reveal"><div class="ico">%s</div><h3 class="h3">做网站，也管网站</h3><p>从栏目规划、页面设计、内容录入到上线后的更新维护，一条线做完。你只需要提供资料与确认，剩下的交给我们。</p></div>
<div class="card glass reveal d1"><div class="ico pink">%s</div><h3 class="h3">只做能快速上线的官网</h3><p>主营纯静态企业官网：结构清晰、加载快、少故障、好改好迁移，不把时间耗在复杂系统开发上。</p></div>
<div class="card glass reveal d2"><div class="ico cyan">%s</div><h3 class="h3">官网之外，补上小程序</h3><p>需要卖货、预约、会员、分销时，同步搭建微信商城小程序，让官网和微信里的生意连成一体。</p></div>
</div>
<div class="keywords">%s</div>
</div></section>''' % (sechead("ONE LINE / 一句话说清", '建站不是交付一个文件，<span class="grad">是长期有人管</span>',
                               "极站把「快速上线」和「代运营维护更新」打包成一项包年服务，适合不想养技术团队、又希望官网始终在线、内容常新的中小企业与机构。"),
                       icon("layers"), icon("bolt"), icon("cart"),
                       "".join('<span>%s</span>' % t for t in [
                           "企业官网建设", "纯静态网站", "最快当天上线", "网站快速修改优化", "网站代运营",
                           "网站维护更新", "微信商城小程序", "移动端自适应", "基础 SEO 结构", "399 元包年"])))

    b.append('''<section class="section tight"><div class="container">
%s
%s
</div></section>''' % (
        sechead("WHY GOSITE / 服务亮点", '把「快」和「有人管」<span class="blue">做进服务里</span>',
                "从参考图里「有用的官网」延伸出六条可执行的服务标准，每一条都对准中小企业最常遇到的建站痛点。"),
        cards([
            ("rocket", "", "极速上线，不等排期", "栏目和内容一次收齐，模板化设计 + 静态化产出，需求确认后 最快当天可上线，比定制开发省去大半等待。"),
            ("feather", "cyan", "纯静态，轻快又稳", "没有数据库和复杂后台，页面秒开、故障点少、安全性高，托在 CDN 上就能稳定访问。"),
            ("refresh", "pink", "随时改，改完即发布", "换文案、换图片、加栏目、上活动页，一个需求发过来，改好直接发布，不用研究后台。"),
            ("headset", "", "全年代运营维护更新", "包年服务里就包含内容更新与日常维护，官网不会上线即停更，也不用额外招人。"),
            ("search", "orange", "让客户能搜到、能看懂", "语义化结构、标题描述、站点地图、AI 可读的正文层级，搜索引擎与 AI 问答都更容易理解你是谁、做什么。"),
            ("link", "cyan", "官网与小程序一体", "官网做品牌与信任，商城小程序做交易与复购，两边内容统一维护，不重复劳动。"),
        ], "g3")))

    b.append('''<section class="section tight"><div class="container">
%s
<div class="grid g2">
<article class="biz-card glass blue reveal"><div class="radial"></div>
<div class="biz-ico">%s</div><div class="sub">FAST STATIC WEBSITE</div><h3>纯静态企业官网</h3>
<p>把企业介绍、业务板块、案例、资讯、联系方式做成结构清楚的独立页面，导航栏目各自成页，PC 与手机都好看、都好找。</p>
<ul class="biz-list">
<li>%s 最快当天上线，栏目页面一次搭齐</li><li>%s 纯静态架构，秒开、易收录、更安全</li>
<li>%s 文字图片随时改，改稿当天发布</li><li>%s 全年维护更新由我们代运营</li></ul>
<div class="biz-foot"><a class="link-more" href="website.html">了解网站建设服务 %s</a></div></article>
<article class="biz-card glass pink reveal d1"><div class="radial"></div>
<div class="biz-ico">%s</div><div class="sub">WECHAT MALL MINI PROGRAM</div><h3>微信商城小程序</h3>
<p>可视化拖拽搭建，商品、订单、会员、营销组件按需组合，覆盖卖货、预约、点餐、分销等常见经营场景。</p>
<ul class="biz-list">
<li>%s 多规格商品、订单与消息通知</li><li>%s 拼团、秒杀、优惠券、积分、分销</li>
<li>%s 会员卡、多门店、点餐与预约报名</li><li>%s 我们代搭建、代配置、代维护</li></ul>
<div class="biz-foot"><a class="link-more" href="miniprogram.html">了解商城小程序 %s</a></div></article>
</div></div></section>''' % (sechead("SERVICES / 两大主营业务", '一个做<span class="pink">门面</span>，一个做<span class="blue">生意</span>',
                                    "官网负责被找到、被信任；小程序负责被下单、被复购。两项业务可单独做，也可以一起上。"),
                             icon("layout", 30), icon("check", 15), icon("check", 15), icon("check", 15),
                             icon("check", 15), icon("arrow", 15), icon("cart", 30), icon("check", 15),
                             icon("check", 15), icon("check", 15), icon("check", 15), icon("arrow", 15)))

    b.append('''<section class="section tight"><div class="container">
%s
%s
</div></section>''' % (sechead("PROCESS / 上线流程", '从一句话需求，到<span class="grad">长期有人管</span>',
                               "流程尽量短，沟通尽量少，把企业要准备的物料压到最少。"),
                       flow([
                           ("微信聊需求", "说清行业、栏目、参考站与上线时间，我们给出方案和报价。", "第 1 步 · 10 分钟"),
                           ("出首页设计稿", "先出视觉稿与栏目结构，满意了再付款，限前 10 名咨询者。", "第 2 步 · 先看稿"),
                           ("资料一次收齐", "按清单提供文字、图片、LOGO、联系方式，我们来整理录入。", "第 3 步 · 你只提供资料"),
                           ("静态站上线", "页面制作、移动端适配、域名解析与 HTTPS 配置，最快当天可上线。", "第 4 步 · 当天"),
                           ("全年代运营", "后续改稿、加栏目、发资讯、做活动页，发需求我们来完成。", "第 5 步 · 全年"),
                       ])))

    b.append('''<section class="section tight"><div class="container">
<div class="sec-head row reveal"><div><div class="eyebrow">SELECTED WORK / 真实案例</div>
<h2 class="h2">三个不同行业，<span class="blue">同一套快上线方法</span></h2>
<p class="lead">商会组织、职业教育、研究院智库，栏目结构各不相同，但都做到了内容清楚、手机好用、后续更新方便。</p></div>
<a class="btn btn-ghost" href="cases.html">%s 查看全部案例</a></div>
<div class="grid g3">
%s
%s
%s
</div></div></section>''' % (icon("arrow", 15),
                             case_card("case-shanghui", "广东省湖南攸县商会", "https://www.zyyous.com/", "商协会门户",
                                       ["商会简介", "六大服务体系", "商会动态", "大攸商商城", "多二维码触点"],
                                       "以「抱团取暖 · 共谋发展」为主视觉，把简介、服务体系、动态资讯与线上商城入口分层呈现。", "01"),
                             case_card("case-cailie", "才猎天下大数据", "https://www.91cailie.com/", "教育实训",
                                       ["四大实训营", "核心优势", "学员故事", "常见问题", "试学转化"],
                                       "围绕课程矩阵搭建转化型首页：数据成绩、课程卡片、优势说明与咨询二维码层层递进。", "02"),
                             case_card("case-baydea", "湾区（广东）数字经济研究院", "https://www.baydea.com/", "研究院 / 智库",
                                       ["五大业务板块", "服务项目", "生态网络", "研究院动态", "合作洽谈"],
                                       "把数字经济、产业学院、跨境电商、人工智能、国际教育五大板块拆成清晰栏目与独立页面。", "03")))

    b.append(cta_section())

    b.append('''<section class="section tight"><div class="container">
<div class="split"><div>%s%s</div>
<div>%s</div></div></div></section>''' % (
        sechead("FAQ / 常见问题", '下单前，<span class="pink">先把话说清楚</span>',
                "关于价格、上线时间、后期修改，这里是最常被问到的几个问题。", center=False),
        faq([
            ("399 元包年到底包含什么？", "包含纯静态官网整站搭建（首页 + 多个栏目独立页面）、模板化设计、移动端自适应、基础 SEO 结构、域名解析与 HTTPS 协助，以及全年的内容更新代运营服务。域名、备案、第三方接口等第三方费用不含在内，具体清单以咨询确认的方案为准。"),
            ("真的能当天上线吗？", "在资料齐备、栏目结构确认的前提下，标准展示型官网最快当天即可上线。若涉及大量资料整理或额外定制页面，时间会在方案阶段一并说明。"),
            ("上线后想改内容怎么办？", "直接在微信里把要改的文字、图片或新栏目发过来，我们改好即发布，不需要你自己进后台操作，一般改动当天完成。"),
            ("「设计满意再付款」怎么算？", "前 10 名咨询者先看首页设计稿与栏目方案，确认满意后再付款进入制作；不满意可以继续沟通调整，也可以不做。"),
        ]),
        '<div class="reveal" style="display:flex;justify-content:center">' + qr_card() + '</div>'))
    return "".join(b)


# ---------------------------------------------------------------- 网站建设
def p_website():
    b = []
    b.append(pagehero("网站建设", '纯静态官网，把上线时间<span class="blue">从几周压到几天</span>',
                      "结构清楚、页面秒开、改稿即发布、全年有人维护。适合企业、商协会、研究院、培训机构等以展示与获客为主的官网需求。",
                      [("纯静态架构", ""), ("最快当天可上线", "pink"), ("导航栏目独立页面", ""), ("全年代运营", "orange")],
                      "FAST STATIC WEBSITE"))
    b.append('''<section class="section tight"><div class="container"><div class="split">
<div class="reveal"><div class="eyebrow">WHY STATIC / 为什么坚持纯静态</div>
<h2 class="h2">官网的痛点，<span class="grad">多半不在设计</span></h2>
<p class="lead">而是在等开发、等服务器、等后台改一个字。纯静态把不必要的技术环节全部拿掉，只留下企业真正需要的东西：内容清楚、打开快、能被搜索到、随时能更新。</p>
<ul class="check-list" style="margin-top:24px">
<li>%s<span><b>快</b>：不改数据库、不搭后台，页面做好即可发布，资料齐备最快当天上线。</span></li>
<li>%s<span><b>稳</b>：静态文件配合 CDN 与 HTTPS，访问稳定，日常几乎不用运维。</span></li>
<li>%s<span><b>轻</b>：首屏体积小、加载快，手机与微信里打开体验一致。</span></li>
<li>%s<span><b>安全</b>：没有数据库和后台登录入口，暴露面小、少补丁少漏洞，托管与安全更新由我们接手。</span></li>
</ul></div>
<div class="visual reveal d1">
<div class="bubble b1">%s 秒开</div><div class="bubble b2">%s 改稿当天发布</div><div class="bubble b3">暴露面小 · 更安全</div>
<div style="width:300px;background:#fff;border-radius:16px;box-shadow:0 20px 44px rgba(15,60,150,.18);overflow:hidden;border:1px solid #e6efff">
<div style="background:linear-gradient(100deg,#1668ff,#7a4bff);height:34px;display:flex;align-items:center;gap:5px;padding:0 12px"><i style="width:7px;height:7px;border-radius:50%%;background:#fff;opacity:.8"></i><i style="width:7px;height:7px;border-radius:50%%;background:#fff;opacity:.6"></i><i style="width:7px;height:7px;border-radius:50%%;background:#fff;opacity:.4"></i></div>
<div style="padding:22px"><div style="height:14px;width:62%%;border-radius:5px;background:linear-gradient(90deg,#1668ff,#e2157f)"></div>
<div style="height:8px;width:88%%;border-radius:4px;background:#e8f0ff;margin-top:14px"></div>
<div style="height:8px;width:70%%;border-radius:4px;background:#e8f0ff;margin-top:8px"></div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:20px">%s</div>
<div style="height:8px;width:48%%;border-radius:4px;background:#eef4ff;margin-top:18px"></div></div></div>
</div></div></div></section>''' % (icon("checkcircle"), icon("checkcircle"), icon("checkcircle"), icon("checkcircle"),
                                   icon("bolt", 12), icon("refresh", 12),
                                   "".join('<div style="height:52px;border-radius:9px;background:linear-gradient(140deg,#e8f1ff,#f5e9f7)"></div>' for _ in range(3))))

    b.append('''<section class="section tight"><div class="container">
%s
%s
</div></section>''' % (sechead("COMPARISON / 对比", '同样的官网，<span class="pink">少走很多弯路</span>',
                               "把常见的建站方式与极站的做法放在一起，差别一目了然。"),
                       table(["对比项", "常见定制 / 动态建站", "极站 · 纯静态官网包年"], [
                           ["上线周期", "数周至数月，需反复排期", '<span class="yes">资料齐备当天即可上线</span>'],
                           ["页面速度", "依赖数据库与服务器性能", '<span class="yes">静态文件 + CDN，秒开</span>'],
                           ["日常维护", "需自行登录后台或找技术", '<span class="yes">微信提需求，我们改完即发布</span>'],
                           ["运行稳定性", "程序、插件、数据库任一出问题都会影响访问", '<span class="yes">静态文件 + CDN，故障点少</span>'],
                           ["内容更新", "改一处常要等开发排期", '<span class="yes">全年更新包含在包年服务里</span>'],
                           ["安全与备份", "依赖原服务商环境，补丁与权限需自行打理", '<span class="yes">静态托管、定期备份，无后台暴露面，安全性更高</span>'],
                           ["费用结构", "开发费 + 服务器 + 维护费分开算", '<span class="yes">399 元 / 年，官网与维护一起算</span>'],
                       ])))

    b.append('''<section class="section tight"><div class="container">
%s
%s
</div></section>''' % (sechead("SITE MAP / 站点结构", '主导航每个栏目，<span class="blue">都有独立页面</span>',
                               "不做只有一个长页面的「假官网」。栏目各自成页，内容能被单独打开、单独收录、单独转发。"),
                       cards([
                           ("layout", "", "首页", "一句话说清你是谁、做什么、为什么选你，配主视觉与核心业务入口。"),
                           ("users", "cyan", "关于我们", "机构简介、发展历程、资质与团队，建立第一层信任。"),
                           ("grid", "pink", "业务 / 服务板块", "每项业务一个说明区或独立页，把服务内容讲明白。"),
                           ("eye", "orange", "成功案例", "案例卡片、客户场景与成果展示，可链接到线上站点。"),
                           ("file", "", "新闻 / 资讯", "动态、通知、行业内容持续更新，官网保持活跃。"),
                           ("message", "cyan", "联系我们", "电话、邮箱、地址、二维码与咨询入口，转化路径短。"),
                       ], "g3")))

    b.append('''<section class="section tight"><div class="container">
%s
<div class="grid g3">
<div class="card glass reveal"><div class="ico">%s</div><h3 class="h3">响应式布局</h3><p>PC、平板、手机自动适配，微信内打开版式不走样。</p></div>
<div class="card glass reveal d1"><div class="ico pink">%s</div><h3 class="h3">语义化 HTML</h3><p>标题层级、段落与导航结构规范，搜索引擎与 AI 问答都能读懂。</p></div>
<div class="card glass reveal d2"><div class="ico cyan">%s</div><h3 class="h3">基础 SEO 设置</h3><p>页面标题、描述、站点地图、图片替代文本与分享信息逐页配置。</p></div>
<div class="card glass reveal"><div class="ico orange">%s</div><h3 class="h3">HTTPS / CDN 托管</h3><p>协助完成域名解析、证书与静态托管配置，访问快且更安全。</p></div>
<div class="card glass reveal d1"><div class="ico">%s</div><h3 class="h3">二维码与分享物料</h3><p>官网二维码、微信内分享标题与缩略图一并配好，线下物料可直接用。</p></div>
<div class="card glass reveal d2"><div class="ico pink">%s</div><h3 class="h3">安全运维 · 托管更新</h3><p>静态托管、HTTPS 与备份由我们配置维护，日常巡检和版本更新一并接手，不用自己盯服务器。</p></div>
</div>
</div></section>''' % (sechead("TECH CHECKLIST / 交付标准", '看不见的地方，<span class="grad">也按标准做</span>',
                               "快速上线不等于粗糙。下面这些是每一套官网都会带上的基础项。"),
                       icon("phone"), icon("code"), icon("search"), icon("shield"), icon("qr"), icon("database")))

    b.append('''<section class="section tight"><div class="container">
%s
<div class="grid g2"><div class="mini-card glass reveal"><h4>%s 改一句话，怎么做</h4>
<p>微信发来「把首页第三段的电话改成新号码，加一张活动海报」，我们改好后直接发布到线上，通常当天完成，不需要你进任何后台。</p>
<div style="margin-top:16px">%s</div></div>
<div class="mini-card glass reveal d1"><h4>%s 加一个栏目，怎么做</h4>
<p>说明栏目名称与内容，我们按现有视觉规范新增独立页面并挂到主导航，保持全站风格统一，同时更新站点地图与分享信息。</p>
<div style="margin-top:16px">%s</div></div></div>
</div></section>''' % (sechead("QUICK EDIT / 快速修改优化", '官网要跟着业务走，<span class="blue">不能一年不动</span>',
                               "「快速修改优化」不是一句口号，而是包年服务里最常用的日常动作。"),
                       icon("pen"), taglist(["换文案", "换图片", "加栏目", "发资讯", "上活动页", "改联系方式"]),
                       icon("layers"), taglist(["统一视觉规范", "导航同步更新", "移动端同步", "收录信息同步"])))

    b.append('''<section class="section tight"><div class="container">%s</div></section>''' % flow([
        ("需求沟通", "确定行业、栏目、参考风格与上线时间。", "10 分钟"),
        ("设计稿确认", "先出首页视觉与栏目结构，满意再付款。", "先看稿"),
        ("资料整理录入", "文字、图片、LOGO 由我们统一整理排版。", "同步整理"),
        ("制作并上线", "静态页面、移动端适配、解析与 HTTPS。", "当天"),
        ("代运营维护", "全年内容更新、栏目调整与日常巡检。", "全年"),
    ]))
    b.append(cta_section('官网先上线，<span style="color:#ffe27a">再慢慢变好</span>',
                         "先有一套能打开、能搜到、能转发的官网，之后的文字、图片、栏目和活动页，全年由我们接着改。"))
    return "".join(b)


# ---------------------------------------------------------------- 商城小程序
def p_miniprogram():
    b = []
    b.append(pagehero("商城小程序", '把生意装进微信，<span class="pink">不用写一行代码</span>',
                      "可视化拖拽搭建 + 成熟功能组件，商品、订单、会员、营销、门店、预约按需组合；我们代搭建、代配置、代维护，官网与小程序一起管。",
                      [("商城交易", ""), ("营销插件", "pink"), ("会员门店", ""), ("代搭建代运维", "orange")],
                      "WECHAT MALL MINI PROGRAM"))

    b.append('''<section class="section tight"><div class="container">
%s
%s
</div></section>''' % (sechead("VALUE / 小程序解决什么", '客户在微信里，<span class="blue">生意也该在微信里</span>',
                               "官网负责讲清楚品牌，小程序负责把咨询变成下单、把一次性客户变成会员。"),
                       cards([
                           ("cart", "", "随时能下单", "商品、规格、购物车、订单与消息通知打通，客户看到就能买，不必跳出微信。"),
                           ("megaphone", "pink", "有工具做复购", "拼团、限时抢购、优惠券、积分签到、积分兑换、分销，常用的营销玩法都能配。"),
                           ("users", "cyan", "把客户留下来", "会员信息、会员卡折扣与积分体系，配合表单、预约与客服，把流量沉淀成可联系的人。"),
                       ], "g3")))

    groups = [
        ("商品与交易", "box", "", ["多规格商品管理", "秒杀 / 预约商品", "组图与幻灯片", "订单与消息通知", "充值与优惠规则", "内容库快速筛选"]),
        ("营销与增长", "gift", "pink", ["分销模块", "拼团商城", "限时抢购", "优惠券系统", "积分签到", "积分兑换商城"]),
        ("会员与门店", "store", "cyan", ["会员管理与会员卡", "多门店系统", "店内点餐", "付费预约", "预约报名", "万能表单"]),
        ("内容与连接", "layers", "orange", ["文章管理系统", "评论管理", "小程序跳转", "手机客服", "系统表单通知", "邮件 / 模板消息"]),
    ]
    gc = []
    for i, (title, ic, color, feats) in enumerate(groups):
        gc.append('''<article class="card glass reveal d%d"><div class="ico %s">%s</div>
<h3 class="h3">%s</h3><p>按经营需要自由组合，缺什么补什么，不必为用不上的功能买单。</p>
<div class="tag-list" style="margin-top:16px">%s</div></article>'''
                   % (i, color, icon(ic), title, "".join('<span>%s</span>' % f for f in feats)))
    b.append('''<section class="section tight"><div class="container">
%s
<div class="grid g2">%s</div>
</div></section>''' % (sechead("CAPABILITIES / 能力矩阵", '一套组件库，<span class="grad">拼出你的商城</span>',
                               "能力来自成熟的小程序搭建体系，我们按行业与经营场景做筛选、配置和界面装修。"),
                       "".join(gc)))

    b.append('''<section class="section tight"><div class="container">
%s
%s
</div></section>''' % (sechead("PLATFORM / 平台优势加工", '不用编程，<span class="pink">也不必自己摸索</span>',
                               "把搭建平台的优势，变成你这边「省心」的服务体验。"),
                       cards([
                           ("sliders", "", "拖拽式 DIY 装修", "界面模块可拖拽组合，实时预览、所见即所得，改版不用重新开发。"),
                           ("grid", "cyan", "组件自由组合", "功能组件不受行业框架限制，按场景自由搭配，定制需求响应更快。"),
                           ("layers", "pink", "行业模板一键套用", "各行业现成模板直接启用，先上线再细化，缩短从想法到可用的时间。"),
                           ("code", "", "无需技术基础", "不用写代码、不用懂服务器，日常商品与内容变更也可以交给我们代操作。"),
                           ("cloud", "orange", "服务器与问题处理", "服务器配置、环境部署、异常排查由技术侧承接，减少你的沟通成本。"),
                           ("headset", "cyan", "售后与持续支持", "售后服务群与 7×24 小时客户服务通道，配合我们的代运营，出问题有人接。"),
                       ], "g3")))

    industries = ["智慧餐饮", "智慧商城", "智慧家装", "智慧教育", "智慧美业", "婚纱摄影",
                  "智慧旅游", "同城服务", "智慧休娱", "连锁多门店"]
    b.append('''<section class="section tight"><div class="container">
<div class="split"><div class="reveal"><div class="eyebrow">INDUSTRIES / 适配行业</div>
<h2 class="h2 nowrap">从餐饮到商城，<span class="blue">场景都能对上</span></h2>
<p class="lead">按行业痛点选组件：餐饮重点在点餐与预约，零售重点在商品、拼团与分销，服务业重点在会员、表单与门店。以下为可覆盖的行业方案方向。</p>
%s
<p style="font-size:12.5px;color:var(--muted);margin-top:18px">行业方案方向依据小程序搭建平台的公开能力整理，具体功能以实际开通与配置为准。</p></div>
<div class="visual reveal d1">
<div class="bubble b1">%s 拖拽装修</div><div class="bubble b2">%s 营销插件</div><div class="bubble b3">微信内下单</div>
<div class="phone"><div class="ph-head">极站商城<small>微信小店 · 首页</small></div>
<div class="ph-body"><div class="ph-line"></div><div class="ph-box">爆款</div><div class="ph-box">新品</div>
<div class="ph-box">拼团</div><div class="ph-box">会员</div><div class="ph-line"></div><div class="ph-line short"></div></div></div>
</div></div></div></section>''' % (taglist(industries), icon("sliders", 12), icon("gift", 12)))

    b.append('''<section class="section tight"><div class="container">
%s
<div class="grid g2">
<div class="card glass reveal"><div class="ico">%s</div><h3 class="h3">官网 → 小程序</h3><p>官网里的业务介绍、案例与资讯，可以对应成小程序里的商品详情、品牌页与内容栏目，客户从了解直接走到下单。</p></div>
<div class="card glass reveal d1"><div class="ico pink">%s</div><h3 class="h3">统一代运营</h3><p>官网改文案、小程序上新品，一个微信窗口提需求，两边一起更新，不用分别找人、重复讲一遍背景。</p></div>
</div>
</div></section>''' % (sechead("TOGETHER / 官网 + 小程序", '一个窗口提需求，<span class="grad">两边一起更新</span>',
                               "这是极站和「只交付一个站点」最不一样的地方。"),
                       icon("link"), icon("refresh")))

    b.append('''<section class="section tight"><div class="container">%s
<div class="grid g2" style="margin-top:34px">
<div class="mini-card glass reveal"><h4>%s 我们负责</h4><p style="color:var(--muted);font-size:13.5px;line-height:1.9;margin-top:10px">需求梳理 · 模板选择 · 页面装修 · 组件配置 · 商品与栏目录入 · 服务器与环境配置 · 提交发布协助 · 后续内容与活动更新。</p></div>
<div class="mini-card glass reveal d1"><h4>%s 你只需提供</h4><p style="color:var(--muted);font-size:13.5px;line-height:1.9;margin-top:10px">营业执照与主体资料 · 小程序账号 · 商品图文与价格 · LOGO 与品牌色 · 客服与收款方式。资料清单会在方案阶段一次给到。</p></div>
</div></div></section>''' % (sechead("DELIVERY / 交付方式", '搭建、配置、维护，<span class="blue">我们接手</span>',
                                    "商城小程序首年 9980 元起（含设计与上线），次年续费 3980 元；可与官网包年一起做。"),
                            icon("checkcircle"), icon("file")))
    b.append('''<section class="section tight"><div class="container">
%s
<div class="grid g2" style="margin-top:8px">
<div class="card glass reveal"><span class="pill pink">%s 首年</span>
<h3 class="h3" style="font-size:24px;margin-top:18px">9980 元起 · 含设计与上线</h3>
<p>按功能范围与页面数量确定最终报价。首年费用包含商城界面设计、组件配置、商品与栏目录入、提交上线，先把能卖货的版本跑起来。</p>
<div style="margin-top:16px">%s</div></div>
<div class="card glass reveal d1"><span class="pill">%s 次年起</span>
<h3 class="h3" style="font-size:24px;margin-top:18px">3980 元 / 年 · 续费维护</h3>
<p>后续每年续费 3980 元，覆盖技术维护、服务器与环境配置、问题排查与日常更新支持，商城不用自己养技术。</p>
<div style="margin-top:16px">%s</div></div>
</div>
<p style="font-size:12.5px;color:var(--muted);margin-top:18px;text-align:center">具体功能清单与报价以咨询确认的方案为准；第三方费用（微信认证、支付接口、短信等）另计。</p>
</div></section>''' % (sechead("PRICING / 商城小程序定价", '首年<span class="pink">9980 元起</span>，次年续费 3980 元',
                               "设计、上线、维护分开写清楚，方便按预算做决定。"),
                       icon("cart", 13), checklist([
                           "商城界面设计与首页装修", "功能组件配置与商品录入",
                           "服务器与环境配置、提交上线协助", "按功能范围确定最终报价",
                       ]), icon("refresh", 13), checklist([
                           "技术维护与问题排查", "服务器与环境持续支持",
                           "日常内容与商品更新支持", "按年续费，费用提前说明",
                       ])))

    mall_items = [
        ("mall-01.jpg", "商城首页", "首页装修 · 搜索 · 优惠券 · 分类入口"),
        ("mall-02.jpg", "商品分类", "左侧分类导航 + 右侧商品列表"),
        ("mall-03.jpg", "商品详情", "详情图文 · 价格 · 拼团 · 下单"),
        ("mall-04.jpg", "商品列表", "多规格商品与分类筛选"),
        ("mall-05.jpg", "服务商城", "服务类目 · 课程 · 推荐位"),
        ("mall-06.jpg", "分类页面", "服务型商城的分类与报价展示"),
    ]
    stack = "".join('<a class="ms-item" style="--i:%d" href="assets/mall/%s" target="_blank" rel="noopener"><img src="assets/mall/%s" alt="%s 界面样板" loading="lazy"></a>' % (i, f, f, t)
                    for i, (f, t, _) in enumerate(mall_items))
    grid = "".join('<a class="mall-cell" href="assets/mall/%s" target="_blank" rel="noopener"><img src="assets/mall/%s" alt="%s 界面样板" loading="lazy"><h4>%s</h4><p>%s</p></a>' % (f, f, t, t, d)
                   for f, t, d in mall_items)
    b.append('''<section class="section tight"><div class="container">
%s
<div class="mall-stack reveal">%s</div>
<div class="mall-grid" style="margin-top:26px">%s</div>
<p style="font-size:12.5px;color:var(--muted);margin-top:18px;text-align:center">以上为常见小程序商城界面版式示意，用于展示可搭建的页面样式；点击任意图片可查看大图。</p>
</div></section>''' % (sechead("SHOWCASE / 商城界面样板", '商城长什么样，<span class="grad">先看这些版式</span>',
                               "首页、分类、列表、详情、服务型商城——不同行业的页面结构，都可以用组件搭出来。"), stack, grid))

    b.append(cta_section('官网 + 小程序，<span style="color:#ffe27a">一次说清需求</span>',
                         "官网 399 元包年；商城小程序首年 9980 元起（含设计上线），次年续费 3980 元。微信扫码聊清楚场景，我们给出可落地的组合建议。"))
    return "".join(b)


# ---------------------------------------------------------------- 成功案例
def p_cases():
    b = []
    b.append(pagehero("成功案例", '三种行业，<span class="blue">同一套上线方法</span>',
                      "以下为可公开访问的线上站点案例。每个案例都围绕「内容讲清楚、栏目独立成页、手机好用、后续好更新」来组织。",
                      [("商协会门户", ""), ("教育实训", "pink"), ("研究院智库", ""), ("可点击访问", "orange")],
                      "SELECTED WORK"))
    b.append('''<section class="section tight"><div class="container"><div class="grid g3">
%s
%s
%s
</div></div></section>''' % (
        case_card("case-shanghui", "广东省湖南攸县商会", "https://www.zyyous.com/", "商协会门户",
                  ["商会简介", "六大服务体系", "商会动态", "大攸商商城", "多二维码触点"],
                  "成立于 2013 年的异地商会门户。首页用「抱团取暖 · 共谋发展」立住主旨，向下依次是数据成绩、商会简介、六大服务体系、动态资讯、官方线上商城与多触点二维码。", "01"),
        case_card("case-cailie", "才猎天下大数据", "https://www.91cailie.com/", "教育实训 / 转化型官网",
                  ["四大实训营", "核心优势", "学员故事", "常见问题", "试学预约"],
                  "2008 年创立于深圳的 AI 人才实训基地。站点以四大实训营卡片为主线，配合就业数据、核心优势、学员故事与 FAQ，最终落到试学预约与咨询二维码。", "02"),
        case_card("case-baydea", "湾区（广东）数字经济研究院", "https://www.baydea.com/", "研究院 / 智库",
                  ["五大业务板块", "服务项目", "生态网络", "研究院动态", "合作洽谈"],
                  "面向政校企的数字经济研究院。把数字经济、产业学院、跨境电商、人工智能、国际教育拆成五大板块与独立页面，服务项目、生态网络、动态与合作入口层层展开。", "03")))

    b.append('''<section class="section tight"><div class="container">
%s
<div class="grid g3">
<div class="card glass reveal"><div class="ico">%s</div><h3 class="h3">先定栏目，再做页面</h3><p>商会的六大服务体系、研究院的五大板块、培训机构的四大课程，都先拆成清晰的信息骨架，再落到视觉设计。</p></div>
<div class="card glass reveal d1"><div class="ico pink">%s</div><h3 class="h3">每个栏目独立成页</h3><p>主导航不是锚点跳转，而是各自有独立页面与独立标题描述，便于收录、便于转发、便于后续单独改版。</p></div>
<div class="card glass reveal d2"><div class="ico cyan">%s</div><h3 class="h3">把转化入口做短</h3><p>咨询二维码、联系电话、预约试学、合作洽谈、线上商城入口都放在用户做决定的位置，而不是埋在页脚。</p></div>
</div></div></section>''' % (sechead("METHOD / 案例里的共同点", '不是三套设计，<span class="grad">是三个行业的内容结构</span>',
                                    "行业不同，方法一致：结构先行、页面独立、更新方便。"),
                            icon("grid"), icon("layers"), icon("qr")))

    b.append('''<section class="section tight"><div class="container">
%s
<div class="mini-card glass reveal"><h4 style="margin-bottom:6px">%s 小程序可覆盖的经营场景</h4>
<p style="color:var(--muted);font-size:13.5px;line-height:1.9">餐饮点餐、零售商城、家政同城、教育培训、美业预约、婚纱摄影、旅游攻略、健身休闲、连锁多门店、社区团购等，均可按组件组合出对应的商城或预约小程序。</p>
%s
<p style="font-size:12.5px;color:var(--muted);margin-top:16px">以上为行业方案方向（依据小程序搭建平台公开能力整理），并非本站自有客户名单。</p></div>
</div></section>''' % (sechead("SCENES / 场景参考", '需要交易时，<span class="pink">官网可以接上小程序</span>',
                               "展示型官网与商城小程序的常见组合方向。"),
                       icon("store", 18),
                       taglist(["商品多规格", "拼团 / 秒杀", "优惠券 / 积分", "分销裂变", "会员卡", "多门店",
                                "店内点餐", "预约报名", "万能表单", "手机客服"])))
    galleries = [
        ("广东省湖南攸县商会", "case-shanghui", "商协会门户"),
        ("才猎天下大数据", "case-cailie", "教育实训"),
        ("湾区（广东）数字经济研究院", "case-baydea", "研究院 / 智库"),
    ]
    gal = []
    for gname, stem, gtag in galleries:
        shots = [(stem + ".png", "PC 首页", "wide"), (stem + "-pc2.jpg", "PC 内页", "wide"),
                 (stem + "-m1.jpg", "手机首页", "phone"), (stem + "-m2.jpg", "手机内页", "phone")]
        imgs = "".join('<a class="shot %s" href="assets/cases/%s" target="_blank" rel="noopener"><img src="assets/cases/%s" alt="%s %s" loading="lazy"><span>%s</span></a>' % (cls, f, f, gname, label, label)
                       for f, label, cls in shots)
        gal.append('<div class="gallery-item glass reveal"><div class="gallery-head"><span class="pill">%s</span><h3 class="h3">%s</h3></div><div class="gallery-grid">%s</div></div>' % (gtag, gname, imgs))
    b.append('''<section class="section tight"><div class="container">
%s
%s
</div></section>''' % (sechead("SCREENS / 多端实拍", 'PC 与手机，<span class="grad">都经得起看</span>',
                               "每个案例都附 PC 端与手机端实拍截图，点击可查看原图，看看栏目在两种屏幕上怎么落地。"),
                       "".join(gal)))

    b.append(cta_section('你的官网，<span style="color:#ffe27a">也可以这样清楚</span>',
                         "扫码发来行业、参考栏目与资料，我们按同样的结构方法出首页设计稿，满意再付款。"))
    return "".join(b)


# ---------------------------------------------------------------- 服务亮点
def p_service():
    b = []
    b.append(pagehero("服务亮点", '快，是上线速度；<span class="blue">有人管，是长期价值</span>',
                      "把参考图里「有用的官网」拆成八条服务标准：既能快速上线，也能在上线之后持续被修改、被更新、被找到。",
                      [("8 条服务标准", ""), ("全年代运营", "pink"), ("改稿当天发布", ""), ("399 元包年", "orange")],
                      "WHY GOSITE"))
    b.append('''<section class="section tight"><div class="container">
%s
%s
</div></section>''' % (sechead("HIGHLIGHTS / 亮点提炼", '整体服务亮点，<span class="grad">一次讲明白</span>',
                               "不做堆功能的清单，只保留客户真正能感受到的八件事。"),
                       cards([
                           ("rocket", "", "01 极速上线", "需求确认、资料齐备后 最快当天可上线，把等待排期的时间还给业务。"),
                           ("feather", "cyan", "02 纯静态轻快", "无数据库、无复杂后台，页面秒开、故障点少、安全性更高。"),
                           ("refresh", "pink", "03 修改即发布", "文字、图片、栏目、活动页随时提需求，改好直接上线，一般当天完成。"),
                           ("headset", "", "04 全年代运营", "内容更新与日常维护写在包年服务里，官网不会上线即停更。"),
                           ("search", "orange", "05 搜索与 AI 友好", "语义化结构、标题描述、站点地图、清晰正文，让搜索引擎与 AI 问答读得懂。"),
                           ("phone", "cyan", "06 多端一致", "PC、手机、平板与微信内打开都适配，分享出去版式不走样。"),
                           ("link", "pink", "07 官网 + 小程序", "一个窗口提需求，官网与商城小程序同步更新，不重复沟通。"),
                           ("database", "", "08 安全运维 · 托管更新", "静态托管、定期备份与版本更新由我们接手，不用自己盯服务器与补丁。"),
                       ], "g4")))

    b.append('''<section class="section tight"><div class="container">
%s
%s
</div></section>''' % (sechead("OPERATION / 代运营维护清单", '包年之后，<span class="pink">我们具体做什么</span>',
                               "代运营不是「有问题再联系」，而是把官网当成一项需要长期打理的资产。"),
                       table(["服务项目", "频率 / 时效", "说明"], [
                           ["文字与图片更新", "随时提需求，一般当天完成", "改电话、改简介、换 Banner、换团队照片、调整表述"],
                           ["栏目与页面调整", "按需，随提随做", "新增业务页、活动页、招聘页，导航与站点地图同步更新"],
                           ["资讯与动态发布", "按客户提供的内容随时发布", "新闻、通知、案例、文章整理排版后上线"],
                           ["营销活动页", "按活动节奏", "促销、报名、会议、招生专题页快速搭建"],
                           ["基础 SEO 维护", "随页面更新同步", "标题、描述、图片替代文本、站点地图与分享信息"],
                           ["微信与二维码物料", "按需", "官网二维码、分享标题与缩略图、线下物料适配"],
                           ["访问与安全巡检", "定期", "链接可用性、HTTPS 状态、页面加载、异常排查"],
                           ["整站备份与交付", "按需 / 到期可打包", "静态文件完整备份，可随时迁移或自行托管"],
                       ])))

    b.append('''<section class="section tight"><div class="container">
%s
%s
</div></section>''' % (sechead("COST / 算一笔账", '不用为「改一个字」<span class="blue">再养一个岗位</span>',
                               "对多数中小企业来说，官网不需要专职技术，需要的是有人随叫随到。"),
                       table(["对比项", "自己维护 / 临时找人", "极站 399 元包年"], [
                           ["首年投入", "建站费、服务器、维护分别计价", '<span class="yes">官网 + 全年维护一起算</span>'],
                           ["日常改稿", "找人、报价、排期", '<span class="yes">微信提需求，改完即发布</span>'],
                           ["人员成本", "需有人懂后台或长期外包", '<span class="yes">无需专人，零学习成本</span>'],
                           ["响应速度", "视对方排期而定", '<span class="yes">一般改动当天完成</span>'],
                           ["长期维护", "容易停更、链接失效没人管", '<span class="yes">全年持续更新与巡检</span>'],
                       ])))

    b.append('''<section class="section tight"><div class="container">
%s
<div class="grid g4">
<div class="card glass reveal"><div class="ico">%s</div><h3 class="h3">随时</h3><p>日常改稿、加内容，微信发来需求即可处理。</p></div>
<div class="card glass reveal d1"><div class="ico pink">%s</div><h3 class="h3">每月</h3><p>检查链接、页面加载、二维码与分享信息是否正常。</p></div>
<div class="card glass reveal d2"><div class="ico cyan">%s</div><h3 class="h3">每季度</h3><p>回看栏目结构、内容时效与收录情况，给出优化建议。</p></div>
<div class="card glass reveal d3"><div class="ico orange">%s</div><h3 class="h3">活动节点</h3><p>招生、展会、年会、促销前，快速搭好专题与活动页。</p></div>
</div></div></section>''' % (sechead("RHYTHM / 服务节奏", '什么时候找我们，<span class="grad">都有人接</span>',
                                    "把维护做成固定节奏，而不是等网站出问题才想起来。"),
                            icon("message"), icon("chart"), icon("eye"), icon("megaphone")))
    b.append(cta_section())
    return "".join(b)


# ---------------------------------------------------------------- 价格套餐
def p_pricing():
    b = []
    b.append(pagehero("价格套餐", '<span class="pink">399 元包年</span>，官网和全年维护一起算',
                      "价格简单，服务不打折。标准价 998 元 / 年；399 元仅限前 10 名且资料齐全的咨询者，先看设计稿，满意再付款。",
                      [("399 元 / 年", ""), ("标准价 998 / 年", ""), ("设计满意再付款", "pink"), ("前 10 名且资料齐全", "orange")],
                      "PRICING"))

    b.append('''<section class="section tight"><div class="container">
<div class="grid g3 plan-grid">
<article class="card glass reveal" style="padding:32px 26px;border:1.5px solid rgba(26,107,255,.32);background:linear-gradient(165deg,rgba(255,255,255,.94),rgba(230,241,255,.72))">
<span class="pill">%s 主推套餐</span>
<h3 class="h3" style="font-size:23px;margin-top:18px">极站官网包年 · 限时价</h3>
<div class="price-big" style="color:var(--blue-deep);margin-top:6px"><span class="cur">¥</span><span class="num" style="background:linear-gradient(100deg,#1668ff,#e2157f);-webkit-background-clip:text;background-clip:text;color:transparent">399</span><span class="unit" style="color:var(--muted)">/ 年</span></div>
<p class="price-std">标准价 <s>¥998 / 年</s></p>
<span class="pill orange" style="margin-top:10px">仅限前 10 名且资料齐全</span>
<p style="color:var(--muted);font-size:13px;margin-top:14px">官网整站搭建 + 全年代运营维护更新</p>
<div style="margin-top:20px">%s</div>
<div style="margin-top:24px"><a class="btn btn-primary btn-lg" href="contact.html#consult">%s 微信扫码咨询</a></div>
<p style="font-size:12px;color:var(--muted);margin-top:12px">具体服务清单以咨询确认的方案为准；第三方费用另计。</p>
</article>
<article class="card glass reveal d1" style="padding:32px 26px">
<span class="pill pink">%s 标准价</span>
<h3 class="h3" style="font-size:23px;margin-top:18px">极站官网包年 · 标准版</h3>
<div class="price-big" style="color:var(--ink-2);margin-top:6px"><span class="cur">¥</span><span class="num" style="background:linear-gradient(100deg,#0a1e3c,#1a6bff);-webkit-background-clip:text;background-clip:text;color:transparent">998</span><span class="unit" style="color:var(--muted)">/ 年</span></div>
<p class="price-std">不限名额 · 资料可分批补齐</p>
<p style="color:var(--muted);font-size:13px;margin-top:14px">与限时价相同的官网整站与全年维护，适合错过名额或资料尚在准备的单位。</p>
<div style="margin-top:20px">%s</div>
<div style="margin-top:24px"><a class="btn btn-ghost btn-lg" href="contact.html#consult">咨询标准套餐</a></div>
</article>
<article class="card glass reveal d2" style="padding:32px 26px">
<span class="pill">%s 商城定价</span>
<h3 class="h3" style="font-size:23px;margin-top:18px">微信商城小程序</h3>
<div class="price-big" style="color:var(--ink-2);margin-top:6px"><span class="cur">¥</span><span class="num" style="font-size:56px;background:linear-gradient(100deg,#e2157f,#7a4bff);-webkit-background-clip:text;background-clip:text;color:transparent">9980</span><span class="unit" style="color:var(--muted)">起 / 首年</span></div>
<p class="price-std">首年含设计与上线　·　次年续费 <b>¥3980 / 年</b></p>
<p style="color:var(--muted);font-size:13px;margin-top:14px">按功能范围与页面数量出方案：商品订单、营销插件、会员门店、预约点餐、分销拼团等组件按需组合。</p>
<div style="margin-top:18px">%s</div>
<div style="margin-top:24px"><a class="btn btn-ghost btn-lg" href="miniprogram.html">%s 查看小程序能力</a></div>
</article>
</div></div></section>''' % (icon("gift", 13), checklist([
        "纯静态官网整站（首页 + 多个栏目独立页面）", "模板化视觉设计与移动端自适应",
        "文字、图片、LOGO 等资料整理录入", "域名解析、HTTPS 与 CDN 静态托管协助",
        "基础 SEO 结构：标题 / 描述 / 站点地图", "全年内容更新代运营与访问巡检",
        "微信分享物料、官网二维码与整站备份",
    ]), icon("qr", 16), icon("tag", 13), checklist([
        "官网整站与全年代运营，交付内容同限时价", "资料不齐可先搭框架、后补内容",
        "不限前 10 名，随时可咨询开通", "域名解析、HTTPS 与基础 SEO 协助",
        "可与商城小程序组合成整体方案",
    ]), icon("cart", 13), checklist([
        "可视化拖拽装修，界面自由 DIY", "行业模板 + 功能组件，快速搭起可用版本",
        "服务器配置、问题排查由技术侧承接", "可与官网包年一起做，统一代运营",
        "次年续费 3980 元 / 年",
    ]), icon("arrow", 15)))

    b.append('''<section class="section tight"><div class="container">
%s
<div class="grid g3">
<div class="card glass reveal"><span class="num">01</span><div class="ico">%s</div><h3 class="h3">先沟通，不先收钱</h3><p>微信说清行业、栏目、参考站与上线时间，我们给方案和报价。</p></div>
<div class="card glass reveal d1"><span class="num">02</span><div class="ico pink">%s</div><h3 class="h3">先看设计稿</h3><p>出首页视觉稿与栏目结构，前 10 名咨询者确认满意后再付款。</p></div>
<div class="card glass reveal d2"><span class="num">03</span><div class="ico cyan">%s</div><h3 class="h3">满意再做全站</h3><p>进入资料整理、页面制作与上线流程，后续维护按包年服务执行。</p></div>
</div>
<div class="mini-card glass reveal" style="margin-top:22px;text-align:center">
<p style="font-size:14px;color:var(--ink-2)"><b>设计满意再付款 · 限前 10 名咨询者。</b> 名额以微信咨询先后为准，设计稿阶段可继续沟通调整；不涉及任何预付款或捆绑消费。</p>
</div>
</div></section>''' % (sechead("PROMOTION / 限时福利规则", '把风险放在<span class="blue">我们这一边</span>',
                               "先看稿、再付款，是为了让第一次合作不必靠猜。"),
                       icon("message"), icon("pen"), icon("rocket")))

    b.append('''<section class="section tight"><div class="container">
%s
%s
</div></section>''' % (sechead("SCOPE / 费用边界", '包含什么、不包含什么，<span class="pink">写清楚</span>',
                               "避免合作过程中出现「这个要另外加钱」的尴尬。"),
                       table(["项目", "399 元包年", "说明"], [
                           ["官网页面制作", '<span class="yes">包含</span>', "首页及约定的栏目独立页面，按确认的栏目结构交付"],
                           ["全年内容更新", '<span class="yes">包含</span>', "文字、图片、栏目、资讯与活动页的日常更新"],
                           ["移动端与基础 SEO", '<span class="yes">包含</span>', "响应式适配、标题描述、站点地图与分享信息"],
                           ["域名 / 备案", '<span class="no">第三方费用另计</span>', "可协助操作，费用由第三方收取"],
                           ["商城小程序", '<span class="no">另出方案</span>', "按功能范围单独报价，可与官网一起做"],
                           ["支付 / 短信 / 接口", '<span class="no">第三方费用另计</span>', "仅在实际需要时产生，方案阶段会提前说明"],
                           ["定制开发功能", '<span class="no">另行沟通</span>', "超出静态展示范围的需求单独评估"],
                       ])))

    b.append('''<section class="section tight"><div class="container">
%s
%s
</div></section>''' % (sechead("FAQ / 价格相关", '关于 399 包年，<span class="blue">常被问到</span>'),
                       faq([
                           ("399 元和 998 元有什么区别？", "服务内容一致，都是官网整站 + 全年代运营维护更新。399 元是限时价，仅限前 10 名且资料齐全的咨询者；标准价 998 元 / 年不限名额，资料可以分批补齐，先搭框架、后补内容。"),
                           ("399 元是首年价还是每年都一样？", "按年计费，续费价格与当年服务范围会在方案里一次说清，不做低价引流后临时加价。"),
                           ("一年里能改多少次？", "日常内容更新不限按次计费，按实际需求随时提；涉及大规模改版或新增大量页面的情况，会在方案阶段说明处理方式。"),
                           ("设计稿不满意怎么办？", "前 10 名咨询者先看稿再付款，设计稿阶段可以继续沟通调整，也可以选择不做，不产生费用。"),
                           ("可以先只做官网，之后再加小程序吗？", "可以。官网先上线，后续需要交易、预约、会员时再按功能范围出小程序方案，两边内容可统一维护。"),
                           ("需要提供什么资料？", "企业简介、业务与栏目文字、图片素材、LOGO、联系方式与参考站点；清单会在沟通后一次给到，整理录入由我们完成。"),
                       ])))
    b.append(cta_section())
    return "".join(b)


# ---------------------------------------------------------------- 联系我们
def p_contact():
    b = []
    b.append(pagehero("联系我们", '先聊 10 分钟，<span class="blue">把官网的事定下来</span>',
                      "微信扫码说明行业、栏目与上线时间，我们出方案与首页设计稿；前 10 名咨询者设计满意再付款。",
                      [("微信扫码咨询", ""), ("先看设计稿", "pink"), ("最快当天可上线", ""), ("工作日响应", "orange")],
                      "CONTACT"))

    b.append('''<section class="section tight" id="consult"><div class="container">
<div class="split"><div class="reveal">
<div class="eyebrow">ABOUT / 关于极站</div><h2 class="h2">名字里的「极」，<span class="grad">是极速，也是极致省心</span></h2>
<p class="lead">%s 是一项面向中小企业的快官网上线服务：用纯静态架构把上线时间压到最快当天，用包年代运营把上线之后的修改、更新、维护一并接住，需要交易时再接上微信商城小程序。</p>
<p class="lead">我们不做庞大复杂的系统，只把企业官网最常用、最影响获客的部分做扎实：结构清楚、打开够快、手机好用、能被搜到、内容常新。</p>
%s
</div>
<div style="display:flex;justify-content:center" class="reveal d1">%s</div>
</div></div></section>''' % (BRAND, taglist([
        "企业官网建设", "纯静态网站", "最快当天上线", "网站快速修改优化", "网站代运营",
        "网站维护更新", "微信商城小程序", "399 元包年", "设计满意再付款", "改稿当天发布",
    ]), qr_card()))

    b.append('''<section class="section tight"><div class="container">
%s
<div class="grid g2">
<div class="card glass reveal"><div class="ico">%s</div><h3 class="h3">咨询时，请顺手说清</h3>
<ul class="check-list" style="margin-top:18px">
<li>%s<span>行业与主营业务，想让客户看完做什么</span></li>
<li>%s<span>需要的栏目（没有想法我们可以给结构建议）</span></li>
<li>%s<span>参考网站或喜欢的风格，以及期望上线时间</span></li>
<li>%s<span>现有 LOGO、图片、文字资料是否齐备</span></li>
</ul></div>
<div class="card glass reveal d1"><div class="ico pink">%s</div><h3 class="h3">我们会回给你</h3>
<ul class="check-list" style="margin-top:18px">
<li>%s<span>栏目结构与页面清单</span></li>
<li>%s<span>首页设计稿与视觉方向</span></li>
<li>%s<span>明确报价、上线时间与资料清单</span></li>
<li>%s<span>后续更新维护怎么提需求、多久生效</span></li>
</ul></div>
</div></div></section>''' % (sechead("BEFORE YOU WRITE / 沟通清单", '少来回几轮，<span class="blue">上线就更快</span>',
                                    "把下面这些信息一次发来，方案能出得更准。"),
                            icon("message"), icon("checkcircle"), icon("checkcircle"),
                            icon("checkcircle"), icon("checkcircle"), icon("file"),
                            icon("checkcircle"), icon("checkcircle"), icon("checkcircle"), icon("checkcircle")))

    b.append('''<section class="section tight"><div class="container">%s</div></section>''' % flow([
        ("扫码加微信", "说明需求，确认是否在前 10 名名额内。", "10 分钟"),
        ("出方案与设计稿", "栏目结构 + 首页视觉，满意再付款。", "先看稿"),
        ("资料一次收齐", "按清单提供文字图片，我们来整理。", "同步整理"),
        ("官网制作上线", "静态页面、移动端、解析与 HTTPS。", "当天"),
        ("长期代运营", "改稿、加栏目、发资讯，全年有人管。", "全年"),
    ]))

    b.append('''<section class="section tight"><div class="container">
<div class="grid g3">
<div class="mini-card glass reveal"><h4>%s 咨询方式</h4><p>微信扫码，工作日 9:00–18:00 响应；紧急改动会优先处理。</p></div>
<div class="mini-card glass reveal d1"><h4>%s 服务范围</h4><p>纯静态企业官网、官网代运营维护更新、微信商城小程序搭建与配置。</p></div>
<div class="mini-card glass reveal d2"><h4>%s 适合谁</h4><p>中小企业、商协会、研究院、培训机构等，希望官网快速上线又不想养技术团队的机构。</p></div>
</div></div></section>''' % (icon("qr", 18), icon("layers", 18), icon("users", 18)))
    b.append(cta_section())
    return "".join(b)


def p_sitemap():
    b = []
    b.append(pagehero("网站地图", '全站页面，<span class="blue">一页看全</span>',
                      "这里列出极站 GOSITE 的全部栏目页面，方便快速查找，也方便搜索引擎收录。",
                      [("7 个主栏目", ""), ("独立页面", "pink"), ("XML 站点地图", "")], "SITE MAP"))
    entries = [
        ("首页", "index.html", "品牌主张、两大主营业务、服务亮点、真实案例与限时套餐", "layout"),
        ("网站建设", "website.html", "纯静态官网、对比表、站点结构、交付标准与上线流程", "code"),
        ("商城小程序", "miniprogram.html", "能力矩阵、平台优势、行业场景与官网联动", "cart"),
        ("成功案例", "cases.html", "商会 / 教育实训 / 研究院三个线上站点案例", "eye"),
        ("服务亮点", "service.html", "八条服务标准、代运营清单与成本对比", "spark"),
        ("价格套餐", "pricing.html", "399 限时价、998 标准价、商城小程序按需报价", "tag"),
        ("联系我们", "contact.html", "品牌介绍、沟通清单、上线流程与微信扫码咨询", "message"),
        ("网站地图", "sitemap.html", "本页：全站页面入口与搜索引擎文件", "grid"),
    ]
    cells = "".join('''<a class="card glass reveal d%d" href="%s" style="display:block">
<div class="ico">%s</div><h3 class="h3">%s</h3><p>%s</p></a>''' % (i % 4, url, icon(ic), title, desc)
                    for i, (title, url, desc, ic) in enumerate(entries))
    b.append('''<section class="section tight"><div class="container">
%s
<div class="grid g4">%s</div>
<div class="mini-card glass reveal" style="margin-top:24px;text-align:center">
<h4>给搜索引擎的文件</h4>
<p style="color:var(--muted);font-size:13.5px;margin-top:8px"><a href="sitemap.xml" style="color:var(--blue);font-weight:800">sitemap.xml</a>　·　<a href="robots.txt" style="color:var(--blue);font-weight:800">robots.txt</a></p>
</div></div></section>''' % (sechead("SITE MAP / 全部页面", '每个栏目，<span class="grad">都有独立页面</span>',
                              "点击任意卡片进入对应栏目；也可以直接访问 XML 站点地图与 robots 文件。"), cells))
    b.append(cta_section())
    return "".join(b)


# ---------------------------------------------------------------- 输出
PAGES = [
    ("index.html", "AI时代企业官网快上线｜纯静态网站·代运营维护·399元包年",
     "极站 GOSITE：纯静态企业官网 最快当天上线，改稿当天发布，全年代运营维护更新；同步提供微信商城小程序搭建。399 元包年，设计满意再付款限前 10 名咨询者。",
     "企业官网建设,纯静态网站,快速上线,网站代运营,网站维护更新,商城小程序,399元包年", "index", p_index),
    ("website.html", "纯静态企业网站建设｜最快当天上线·快速修改优化",
     "纯静态企业官网建设服务：结构清楚、页面秒开、改稿当天发布，主导航每个栏目独立成页，全年代运营维护更新。",
     "纯静态官网,企业网站建设,快速上线,网站快速修改,响应式官网,基础SEO", "website", p_website),
    ("miniprogram.html", "微信商城小程序搭建｜商品·营销·会员·门店",
     "微信商城小程序可视化搭建：多规格商品、拼团秒杀、优惠券积分、分销、会员卡、多门店、点餐预约与万能表单，我们代搭建代维护。",
     "商城小程序,微信商城,小程序开发,拼团,分销,会员卡,多门店,点餐预约", "miniprogram", p_miniprogram),
    ("cases.html", "网站案例｜商会·教育实训·数字经济研究院",
     "网站案例：广东省湖南攸县商会、才猎天下大数据、湾区（广东）数字经济研究院，展示不同行业的栏目结构与官网上线方法。",
     "网站案例,商协会官网,教育机构官网,研究院官网,企业官网案例", "cases", p_cases),
    ("service.html", "服务亮点｜官网快上线与全年代运营维护",
     "极站服务亮点：最快当天上线、纯静态轻快、修改即发布、全年代运营、搜索与 AI 友好、多端一致、官网小程序一体、安全运维托管更新。",
     "网站代运营,网站维护更新,快速上线,搜索优化,官网维护", "service", p_service),
    ("pricing.html", "价格套餐｜官网399元包年·设计满意再付款",
     "极站官网包年 399 元：官网整站 + 全年代运营维护更新；设计满意再付款限前 10 名咨询者；商城小程序按需报价。",
     "399元包年,网站价格,建站套餐,设计满意付款,官网包年", "pricing", p_pricing),
    ("contact.html", "联系我们｜微信扫码咨询·先看设计稿",
     "微信扫码咨询极站 GOSITE，说明行业、栏目与上线时间，我们出方案与首页设计稿；前 10 名咨询者设计满意再付款。",
     "扫码咨询,官网建设咨询,微信咨询,设计满意付款", "contact", p_contact),
    ("sitemap.html", "网站地图｜极站 GOSITE 全部页面入口",
     "极站 GOSITE 网站地图：首页、网站建设、商城小程序、成功案例、服务亮点、价格套餐、联系我们全部页面入口，另提供 sitemap.xml 与 robots.txt。",
     "网站地图,站点地图,sitemap,极站 GOSITE", "sitemap", p_sitemap),
]


def main():
    for filename, title, desc, kw, active, builder in PAGES:
        html = wrap(title, desc, kw, active, builder())
        with open(os.path.join(ROOT, filename), "w", encoding="utf-8") as f:
            f.write(html)
        print("generated", filename, len(html), "bytes")


if __name__ == "__main__":
    main()

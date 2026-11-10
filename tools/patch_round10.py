# -*- coding: utf-8 -*-
"""第十轮：左 PC 上下 + 右手机并列；7 个案例设计讲解详情页；入口/站点地图/SEO 同步"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
log = []


def edit(path, pairs, label=""):
    s = io.open(path, encoding="utf-8").read()
    for old, new in pairs:
        n = s.count(old)
        log.append((label or os.path.basename(path), old[:36], n))
        if n:
            s = s.replace(old, new, 1)
    io.open(path, "w", encoding="utf-8", newline="\n").write(s)
    return s


# ---------------- build_site.py ----------------
BS = os.path.join(HERE, "build_site.py")
s = io.open(BS, encoding="utf-8").read()

# 1. 引入案例讲解数据
pairs = [("import json\n", "import json\nfrom case_details import CASE_DETAILS\n")]
log.append(("build_site", "import CASE_DETAILS", 1))
s = s.replace(*pairs[0], 1)

# 2. case_card 底部入口：查看线上站点 -> 设计讲解（指向详情页）
old_foot = '''<div class="case-foot"><span class="no">CASE %s</span><a class="link-more" href="%s" target="_blank" rel="noopener">查看线上站点 %s</a></div>'''
new_foot = '''<div class="case-foot"><span class="no">CASE %s</span><a class="link-more" href="%s.html">设计讲解 %s</a></div>'''
log.append(("build_site", "卡片入口文案", s.count(old_foot)))
s = s.replace(old_foot, new_foot, 1)
old_args = '''pts, no, url, icon("arrow", 14))'''
new_args = '''pts, no, img, icon("arrow", 14))'''
log.append(("build_site", "卡片参数", s.count(old_args)))
s = s.replace(old_args, new_args, 1)

# 3. JSON-LD 面包屑：详情页显示案例名
old_lb = '''        label = next((t for t, u, k in NAV if k == page), "网站地图")'''
new_lb = '''        label = (next((c["name"] for c in CASES if c["stem"] == page), None)
                 or next((t for t, u, k in NAV if k == page), "网站地图"))'''
log.append(("build_site", "面包屑 label", s.count(old_lb)))
s = s.replace(old_lb, new_lb, 1)

# 4. 新函数：case_gallery / p_case_detail
NEW_FUNCS = '''def case_gallery(c, show_head=True):
    """左侧两张 PC 上下叠放，右侧两张手机并列"""
    stem = c["stem"]
    pc = [(stem + ".png", "PC 首页"), (stem + "-pc2.jpg", "PC 内页")]
    mb = [(stem + "-m1.jpg", "手机首页"), (stem + "-m2.jpg", "手机内页")]

    def shot(f, label, cls):
        return ('<a class="shot %s" href="assets/cases/%s" target="_blank" rel="noopener">'
                '<img src="assets/cases/%s" alt="%s %s" loading="lazy"><span>%s</span></a>'
                % (cls, f, f, c["name"], label, label))

    head = ('<div class="gallery-head"><span class="pill">%s</span><h3 class="h3">%s</h3></div>'
            % (c["gtag"], c["name"])) if show_head else ""
    return \'\'\'<div class="gallery-item glass reveal">%s
<div class="gallery-grid">
<div class="gallery-side gallery-pc">%s</div>
<div class="gallery-side gallery-mobile">%s</div>
</div></div>\'\'\' % (head,
        "".join(shot(f, l, "wide") for f, l in pc),
        "".join(shot(f, l, "mobile") for f, l in mb))


def p_case_detail(c):
    d = CASE_DETAILS[c["stem"]]
    b = []
    b.append(pagehero("设计讲解", c["name"] + ' <span class="blue">设计讲解</span>',
                      d["lead"],
                      [(c["gtag"], ""), ("PC / 手机实拍", "pink"), ("构思 · 框架 · 风格 · 配色 · SEO", "")],
                      "CASE STUDY"))
    b.append(\'\'\'<div class="container" style="text-align:center;margin-top:-16px">
<a class="btn btn-ghost" href="%s" target="_blank" rel="noopener">%s 访问 %s 官网</a></div>\'\'\'
              % (c["url"], icon("arrow", 15), c["name"]))

    b.append(\'\'\'<section class="section tight"><div class="container">
%s
%s
</div></section>\'\'\' % (sechead("SCREENS / 站点实拍", 'PC 与手机，<span class="grad">一起看</span>',
                               "左侧为 PC 端首页与内页，右侧为手机端首页与内页，点击可查看原图。"),
                       case_gallery(c, show_head=False)))

    items = [
        ("构思与定位", "rocket", "", d["idea"]),
        ("框架结构", "layout", "cyan", d["frame"]),
        ("设计风格", "pen", "pink", d["style"]),
        ("色彩搭配", "spark", "orange", d["color"]),
        ("SEO 与收录", "search", "", d["seo"]),
        ("整体剖析", "eye", "cyan", d["review"]),
    ]
    cells = "".join(\'\'\'<article class="card glass reveal d%d"><div class="ico %s">%s</div>
<h3 class="h3">%s</h3><p>%s</p></article>\'\'\'
                    % (i % 4, color, icon(ic), title, text)
                    for i, (title, ic, color, text) in enumerate(items))
    b.append(\'\'\'<section class="section tight"><div class="container">
%s
<div class="grid g2">%s</div>
</div></section>\'\'\' % (sechead("ANALYSIS / 设计剖析", '把一个网站，<span class="grad">拆开来看</span>',
                               "从构思到框架、风格、配色与 SEO，逐项拆解这个站点为什么这样做。"), cells))

    b.append(\'\'\'<section class="section tight"><div class="container">
<div class="mini-card glass reveal" style="text-align:center">
<h4 style="margin-bottom:12px">%s 站点关键点</h4>
%s
<div style="margin-top:24px;display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
<a class="btn btn-ghost" href="cases.html">返回全部案例</a>
<a class="btn btn-primary" href="%s" target="_blank" rel="noopener">访问原站</a>
</div></div></div></section>\'\'\' % (icon("tag", 18), taglist(c["points"]), c["url"]))
    b.append(cta_section())
    return "".join(b)


'''
anchor = "# ---------------------------------------------------------------- 成功案例\ndef p_cases():"
log.append(("build_site", "新函数插入", s.count(anchor)))
s = s.replace(anchor, NEW_FUNCS + anchor, 1)

# 5. 案例页 gallery 生成改用 case_gallery
start = s.index("    galleries = [(c[\"name\"], c[\"stem\"], c[\"gtag\"]) for c in CASES]")
end = s.index('                       "".join(gal)))', start) + len('                       "".join(gal)))')
NEW_GAL = '''    gal = "".join(case_gallery(c) for c in CASES)
    b.append(\'\'\'<section class="section tight"><div class="container">
%s
%s
</div></section>\'\'\' % (sechead("SCREENS / 多端实拍", 'PC 与手机，<span class="grad">都经得起看</span>',
                               "每个案例都附 PC 端首页/内页与手机端首页/内页实拍，点击可查看原图。"), gal))'''
s = s[:start] + NEW_GAL + s[end:]
log.append(("build_site", "案例页 gallery", 1))

# 6. 站点地图页增加 7 个设计讲解入口
old_sm = '''    b.append(cta_section())
    return "".join(b)


# ---------------------------------------------------------------- 输出'''
new_sm = '''    detail_links = "".join('<span><a href="%s.html">%s · 设计讲解</a></span>' % (c["stem"], c["name"])
                           for c in CASES)
    b.append(\'\'\'<section class="section tight"><div class="container">
%s
<div class="mini-card glass reveal" style="text-align:center">
<div class="tag-list" style="justify-content:center">%s</div>
</div></div></section>\'\'\' % (sechead("CASE STUDIES / 设计讲解", '逐个案例，<span class="blue">拆开看</span>',
                               "7 个站点的构思、框架结构、设计风格、色彩搭配、SEO 与整体剖析。"), detail_links))
    b.append(cta_section())
    return "".join(b)


# ---------------------------------------------------------------- 输出'''
log.append(("build_site", "站点地图讲解入口", s.count(old_sm)))
s = s.replace(old_sm, new_sm, 1)

# 7. PAGES 追加 7 个详情页
old_main = '''def main():
    for filename, title, desc, kw, active, builder in PAGES:'''
new_main = '''for _i, _c in enumerate(CASES):
    PAGES.append((
        _c["stem"] + ".html",
        _c["name"] + " 网站设计讲解｜构思·框架·风格·配色·SEO｜极站 GOSITE",
        _c["name"] + " 网站设计讲解：站点构思、框架结构、设计风格、色彩搭配与 SEO 拆解，附 PC 端与手机端实拍截图。",
        "网站设计讲解,网站剖析,框架结构,色彩搭配,SEO," + _c["name"],
        _c["stem"],
        (lambda i=_i: p_case_detail(CASES[i])),
    ))


def main():
    for filename, title, desc, kw, active, builder in PAGES:'''
log.append(("build_site", "PAGES 追加", s.count(old_main)))
s = s.replace(old_main, new_main, 1)

io.open(BS, "w", encoding="utf-8", newline="\n").write(s)

# ---------------- 其他脚本 ----------------
STEMS = ["case-shanghui", "case-cailie", "case-baydea", "case-jianzhuo",
         "case-guanxiang", "case-niling", "case-leiyiming"]
extra_pages = "PAGES += [%s]\n" % ", ".join('"%s.html"' % x for x in STEMS)

edit(os.path.join(HERE, "build_seo.py"),
     [("]\n\nFONT_BOLD", "]\n" + extra_pages + "\nFONT_BOLD")], "build_seo")
edit(os.path.join(HERE, "validate.py"),
     [('NAV = set(PAGES) | {"sitemap.xml", "robots.txt", "CNAME"}',
       extra_pages + 'NAV = set(PAGES) | {"sitemap.xml", "robots.txt", "CNAME"}')], "validate")
edit(os.path.join(HERE, "package_site.py"),
     [("import datetime\n", "import datetime\nimport glob\n"),
      ("site_files = set(PAGES)",
       'site_files = set(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "*.html")))')],
     "package_site")

# ---------------- CSS ----------------
css = os.path.join(ROOT, "assets", "css", "style.css")
with open(css, "a", encoding="utf-8", newline="\n") as f:
    f.write('''
/* ---------- 第十轮：左 PC 上下 / 右手机并列 + 案例讲解页 ---------- */
.gallery-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:14px;align-items:stretch}
.gallery-side{display:grid;gap:14px;min-width:0}
.gallery-pc{grid-template-rows:auto auto}
.gallery-mobile{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
.shot.wide{aspect-ratio:1440 / 940;height:auto;align-self:start}
.shot.wide img{object-fit:cover;object-position:center}
.shot.mobile{height:auto;align-self:stretch}
.shot.mobile img{object-fit:contain;object-position:center}
.tag-list a{color:var(--blue-deep);font-weight:700}
.tag-list a:hover{text-decoration:underline}
@media(max-width:640px){
  .gallery-grid{grid-template-columns:1fr;gap:9px}
  .gallery-side{gap:9px}
  .gallery-mobile{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
  .shot.mobile{height:220px}
  .shot.mobile img{object-fit:cover;object-position:top center}
}
''')
log.append(("style.css", "第十轮布局", 1))

for label, key, n in log:
    print(("OK  " if n else "MISS"), "%-22s" % label, n, key)

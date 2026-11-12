# -*- coding: utf-8 -*-
"""第十二轮：404 页 + 三个友情链接 + robots / sitemap 优化。

遵循写死规则：404.html 由服务器返回 404 状态、noindex,follow、无自动跳转、
无 canonical / OG / 结构化数据；不进 sitemap.xml；robots 不 Disallow 它。
robots 显式放行 * / Baiduspider / Googlebot 抓取 /assets/，并带 Host 与 Sitemap。
"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, "tools")
BUILD = os.path.join(T, "build_site.py")
SEO = os.path.join(T, "build_seo.py")
VALID = os.path.join(T, "validate.py")


def load(p):
    return io.open(p, encoding="utf-8").read()


def save(p, s):
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)


def apply(s, pairs, tag):
    for old, new in pairs:
        n = s.count(old)
        if n != 1:
            raise SystemExit("[%s] 命中 %d 次（应为 1）: %s" % (tag, n, old[:70]))
        s = s.replace(old, new)
        print("  [%s] OK %s" % (tag, old[:48].replace("\n", " ")))
    return s


EXTRA_FRIENDS_BLOCK = '''EXTRA_FRIENDS = [
    ("AI建站-跨境极站", "https://www.gosite.com.cn/"),
    ("莞促集团", "https://www.guancu.com/"),
    ("东莞市常平个体私营企业协会", "https://www.ichangping.cn/"),
]


'''

PAGE_404_BLOCK = '''def head_404():
    """404 专用页头：noindex,follow，不写 canonical / OG / JSON-LD，不做自动跳转。"""
    return \'\'\'<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>页面未找到 | 极站 GOSITE</title>
<meta name="description" content="访问的页面不存在，可返回首页或通过网站地图继续浏览极站 GOSITE 的栏目与案例。">
<meta name="robots" content="noindex,follow">
<link rel="icon" href="favicon.ico" type="image/x-icon">
<link rel="stylesheet" href="assets/css/style.css">
<script src="assets/js/main.js" defer></script>
</head>
<body data-page="404">
\'\'\'


def p_404():
    entries = [
        ("返回首页", "index.html"), ("网站地图", "sitemap.html"),
        ("网站建设", "website.html"), ("商城小程序", "miniprogram.html"),
        ("成功案例", "cases.html"), ("服务亮点", "service.html"),
        ("价格套餐", "pricing.html"), ("联系我们", "contact.html"),
    ]
    links = "".join(\'<a class="btn btn-ghost" href="%s" style="margin:5px">%s</a>\' % (u, t)
                    for t, u in entries)
    body = \'\'\'<section class="section"><div class="container">
<div class="mini-card glass reveal" style="text-align:center;padding:64px 30px">
<div class="eyebrow">404 / PAGE NOT FOUND</div>
<div style="font-size:96px;font-weight:900;line-height:1.1;background:linear-gradient(100deg,#1a6bff,#e2157f);-webkit-background-clip:text;background-clip:text;color:transparent;margin:10px 0 6px">404</div>
<h1 class="h2">这个页面没有找到</h1>
<p class="lead" style="margin:14px auto 0;max-width:620px">链接可能已调整或地址输入有误。可以从下面的入口继续浏览，也可以在网站地图里查看全部栏目与案例。</p>
<div style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:28px">%s</div>
</div></div></section>\'\'\' % links
    return (head_404() + topbar() + navbar() + "<main>\\n" + body +
            "\\n</main>\\n" + footer() + "</body>\\n</html>\\n")


'''

NEW_ROBOTS_MAIN = '''def file_lastmod(path):
    """按页面文件的真实修改日期写 lastmod；全站页脚同步后重跑生成器即为生成当天。"""
    p = os.path.join(ROOT, path or "index.html")
    if os.path.exists(p):
        return datetime.date.fromtimestamp(os.path.getmtime(p)).isoformat()
    return TODAY


def main():
    make_og_image()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, priority, freq in PAGES:
        lines.append("  <url><loc>%s%s</loc><lastmod>%s</lastmod>"
                     "<changefreq>%s</changefreq><priority>%s</priority></url>"
                     % (SITE, path, file_lastmod(path), freq, priority))
    lines.append("</urlset>")
    write_text("sitemap.xml", "\\n".join(lines) + "\\n")

    # 显式放行通用爬虫、百度、谷歌抓取 /assets/；404.html 与站长验证文件不屏蔽
    agent_block = ("User-agent: %s\\n"
                   "Allow: /\\n"
                   "Allow: /assets/\\n"
                   "Disallow: /tools/\\n"
                   "Disallow: /dist/\\n")
    robots = "\\n".join(agent_block % ua for ua in ("*", "Baiduspider", "Googlebot"))
    robots += "\\nSitemap: %ssitemap.xml\\nHost: %s\\n" % (SITE, SITE.rstrip("/"))
    write_text("robots.txt", robots)
    write_text("CNAME", "gd.ippi.com.cn\\n")
    write_text(".nojekyll", "")


'''

EXTRA_VALIDATE = '''
# ---------------------------------------------------------------- 第十二轮：404 / robots / 友链
FRIEND_LINKS = [
    ("AI建站-跨境极站", "https://www.gosite.com.cn/"),
    ("莞促集团", "https://www.guancu.com/"),
    ("东莞市常平个体私营企业协会", "https://www.ichangping.cn/"),
]
p404 = os.path.join(ROOT, "404.html")
if not os.path.exists(p404):
    problems.append("缺 404.html")
else:
    s404 = open(p404, encoding="utf-8").read()
    if 'name="robots" content="noindex,follow"' not in s404:
        problems.append("404.html 缺 noindex,follow")
    for bad in ['rel="canonical"', 'property="og:', 'name="twitter:',
                'application/ld+json', 'http-equiv="refresh"',
                'location.href', 'location.replace', '<meta http-equiv']:
        if bad in s404:
            problems.append("404.html 含禁止元素 %s" % bad)
    for need in ['href="index.html"', 'href="sitemap.html"', 'rel="icon"']:
        if need not in s404:
            problems.append("404.html 缺入口/资源 %s" % need)
    if s404.count("<h1") != 1:
        problems.append("404.html 的 h1 数量不是 1")
    for name, url in FRIEND_LINKS:
        if url not in s404 or name not in s404:
            problems.append("404.html 页脚缺友情链接 " + name)

for ua in ["User-agent: *", "User-agent: Baiduspider", "User-agent: Googlebot"]:
    if ua not in robots:
        problems.append("robots.txt 缺 " + ua)
if robots.count("Allow: /assets/") != 3:
    problems.append("robots.txt 未对三个 UA 显式放行 /assets/")
for kw in ["Host: https://gd.ippi.com.cn", "Sitemap: " + SITE_URL + "sitemap.xml"]:
    if kw not in robots:
        problems.append("robots.txt 缺 " + kw)
if "Disallow: /404" in robots or "404.html" in robots:
    problems.append("robots.txt 不应屏蔽或特别提及 404.html")
if "404.html" in xml_raw or "googled740" in xml_raw:
    problems.append("sitemap.xml 不应包含 404 页或站长验证文件")

page_html = {name: open(os.path.join(ROOT, name), encoding="utf-8").read() for name in PAGES}
for name, url in FRIEND_LINKS:
    missing = [p for p, s in page_html.items() if url not in s or name not in s]
    if missing:
        problems.append("友情链接 %s 未同步页面: %s" % (name, missing[:4]))

'''


def main():
    print("== 1/3 build_site.py ==")
    s = load(BUILD)
    s = apply(s, [
        ("def head(title, desc, keywords):", EXTRA_FRIENDS_BLOCK + "def head(title, desc, keywords):"),
        ('    friend_links = "".join(\'<a href="%s" target="_blank" rel="noopener">%s</a>\' % (c["url"], c["name"])\n'
         '                            for c in CASES)\n',
         '    friend_links = "".join(\'<a href="%s" target="_blank" rel="noopener">%s</a>\' % (c["url"], c["name"])\n'
         '                            for c in CASES)\n'
         '    friend_links += "".join(\'<a href="%s" target="_blank" rel="noopener">%s</a>\' % (u, t)\n'
         '                            for t, u in EXTRA_FRIENDS)\n'),
        ("# ---------------------------------------------------------------- 输出",
         PAGE_404_BLOCK + "# ---------------------------------------------------------------- 输出"),
        ('        print("generated", filename, len(html), "bytes")',
         '        print("generated", filename, len(html), "bytes")\n'
         '    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:\n'
         '        f.write(p_404())\n'
         '    print("generated 404.html (noindex,follow / 无 canonical·OG·JSON-LD)")'),
    ], "site")
    save(BUILD, s)

    print("== 2/3 build_seo.py ==")
    e = load(SEO)
    a = e.index("def file_lastmod(")
    b = e.index('if __name__ == "__main__":', a)
    e = e[:a] + NEW_ROBOTS_MAIN + e[b:]
    print("  [seo] robots 生成段已替换为三段 UA")
    save(SEO, e)

    print("== 3/3 validate.py ==")
    v = load(VALID)
    if "第十二轮：404 / robots / 友链" in v:
        raise SystemExit("validate.py 已打过补丁")
    v = v.replace('\nprint("页面数:", len(PAGES))', EXTRA_VALIDATE + '\nprint("页面数:", len(PAGES))')
    save(VALID, v)
    print("补丁完成")


if __name__ == "__main__":
    main()

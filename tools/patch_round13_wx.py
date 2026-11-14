# -*- coding: utf-8 -*-
"""第十三轮：微信分享卡片静态兜底。

只改生成器与 CSS：详情页切换 og 图为 400×400 方图、补 itemprop、body 首行隐藏方图；
首页 / 栏目页 / 404 页保持原有基础 OG，不误带。
不动 sitemap.xml / robots.txt / 404.html 的生成逻辑，不重跑 SEO 生成器。
"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, "tools")
BUILD = os.path.join(T, "build_site.py")
CSS = os.path.join(ROOT, "assets", "css", "style.css")
VALID = os.path.join(T, "validate.py")
PACKAGE = os.path.join(T, "package_site.py")


def load(p):
    return io.open(p, encoding="utf-8").read()


def save(p, s):
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)


def apply(s, pairs, tag):
    for old, new in pairs:
        n = s.count(old)
        if n != 1:
            raise SystemExit("[%s] 命中 %d 次（应为 1）: %s" % (tag, n, old[:80]))
        s = s.replace(old, new)
        print("  [%s] OK %s" % (tag, old[:52].replace("\n", " ")))
    return s


HELPERS = '''def share_image_url(page):
    """详情页方形分享图的 HTTPS 绝对地址。"""
    return SITE_URL + "assets/cases/share-" + page[len("case-"):] + ".jpg"


def share_summary(desc, limit=60):
    """摘要取描述前 60 字，并去掉结尾标点。"""
    return desc[:limit].rstrip("，。；、：！？,.;:!? 　")


'''

EXTRA_VALIDATE = '''
# ---------------------------------------------------------------- 第十三轮：微信分享卡片静态兜底
from PIL import Image

SHARE_STEMS = ["shanghui", "cailie", "baydea", "jianzhuo", "guanxiang", "niling", "leiyiming"]
detail_pages = [p for p in PAGES if p.startswith("case-")]
plain_pages = [p for p in PAGES if not p.startswith("case-")] + ["404.html"]

if len(detail_pages) != len(SHARE_STEMS):
    problems.append("详情页数量与方图数量不一致: %d / %d" % (len(detail_pages), len(SHARE_STEMS)))
for stem in SHARE_STEMS:
    p = os.path.join(ROOT, "assets", "cases", "share-%s.jpg" % stem)
    if not os.path.exists(p):
        problems.append("缺方形分享图 " + p)
        continue
    im = Image.open(p)
    if im.size != (400, 400) or im.format != "JPEG":
        problems.append("方图规格不对 %s %s %s" % (p, im.size, im.format))
    if os.path.getsize(p) > 100 * 1024:
        problems.append("方图超过 100KB " + p)
    if im.getexif():
        problems.append("方图含 EXIF " + p)

for name in detail_pages:
    s = open(os.path.join(ROOT, name), encoding="utf-8").read()
    for tag in ['property="og:title"', 'property="og:description"', 'property="og:image"',
                'property="og:image:width" content="400"',
                'property="og:image:height" content="400"',
                'itemprop="name"', 'itemprop="description"', 'itemprop="image"',
                'name="twitter:card" content="summary_large_image"',
                'class="wx-share-thumb"', 'aria-hidden="true"', 'width="300" height="300"']:
        if tag not in s:
            problems.append("%s 缺 %s" % (name, tag))
    for tag in ['property="og:image"', 'itemprop="image"', 'class="wx-share-thumb"']:
        if s.count(tag) != 1:
            problems.append("%s 重复输出 %s" % (name, tag))
    for tag in ['<title>', 'rel="canonical"', '<meta name="description"', 'application/ld+json']:
        if tag not in s:
            problems.append("%s 丢失保留项 %s" % (name, tag))
    urls = []
    for pat in [r'<meta property="og:image" content="([^"]+)"',
                r'<meta itemprop="image" content="([^"]+)"',
                r'<img class="wx-share-thumb" src="([^"]+)"']:
        m = re.search(pat, s)
        if m:
            urls.append(m.group(1))
    if len(urls) != 3 or len(set(urls)) != 1 or not all(u.startswith("https://") for u in urls):
        problems.append("%s 三处方图地址不一致或不是 HTTPS 绝对地址: %s" % (name, urls))
    else:
        rel = urls[0].replace(SITE_URL, "")
        if not os.path.exists(os.path.join(ROOT, rel)):
            problems.append("%s 方图本地文件不存在 %s" % (name, rel))
    if not re.search(r'<body[^>]*>\\s*<img class="wx-share-thumb"', s):
        problems.append("%s 方图不在 body 第一行" % name)
    if "display:none" in s or re.search(r'wx-share-thumb[^>]*loading=', s):
        problems.append("%s 首图用了 display:none 或 loading=lazy" % name)

for name in plain_pages:
    p = os.path.join(ROOT, name)
    if not os.path.exists(p):
        problems.append("缺非详情页 " + name)
        continue
    s = open(p, encoding="utf-8").read()
    if "itemprop=" in s or "wx-share-thumb" in s:
        problems.append("非详情页误带 itemprop / 首图: " + name)
verify_file = os.path.join(ROOT, "googled740806788de8245.html")
if os.path.exists(verify_file):
    vs = open(verify_file, encoding="utf-8").read()
    if "itemprop=" in vs or "wx-share-thumb" in vs:
        problems.append("验证文件误带 itemprop / 首图")

'''


def main():
    print("== 1/4 build_site.py ==")
    s = load(BUILD)
    s = apply(s, [
        ("import os\nimport json\nimport datetime\nfrom case_details import CASE_DETAILS",
         "import os\nimport json\nimport datetime\nimport html\nfrom case_details import CASE_DETAILS"),
        ("def head(title, desc, keywords):", HELPERS + "def head(title, desc, keywords):"),
        ('    d = dict(title=title, brand=BRAND, desc=desc, keywords=keywords,\n'
         '             url=url, og=og, ld=ld, page=page,\n'
         '             ogtype="article" if is_case else "website",\n'
         '             ogalt=title + " | " + BRAND)\n',
         '    share_url = share_image_url(page) if is_case else ""\n'
         '    short_desc = share_summary(desc) if is_case else desc\n'
         '    esc_short = html.escape(short_desc, quote=True) if is_case else desc\n'
         '    og_img = share_url if is_case else og\n'
         '    og_w, og_h = ("400", "400") if is_case else ("1200", "630")\n'
         '    og_itype = "image/jpeg" if is_case else "image/png"\n'
         '    itemprop = ""\n'
         '    if is_case:\n'
         '        itemprop = (\'<meta itemprop="name" content="%s">\\n\'\n'
         '                    \'<meta itemprop="description" content="%s">\\n\'\n'
         '                    \'<meta itemprop="image" content="%s">\\n\'\n'
         '                    % (html.escape(title + " | " + BRAND, quote=True),\n'
         '                       esc_short, share_url))\n'
         '    d = dict(title=title, brand=BRAND, desc=desc, keywords=keywords,\n'
         '             url=url, og=og, ld=ld, page=page,\n'
         '             ogtype="article" if is_case else "website",\n'
         '             ogalt=title + " | " + BRAND,\n'
         '             ogdesc=esc_short, ogimg=og_img, ogw=og_w, ogh=og_h,\n'
         '             ogitype=og_itype, itemprop=itemprop)\n'),
        ('<meta property="og:description" content="%(desc)s">',
         '<meta property="og:description" content="%(ogdesc)s">'),
        ('<meta property="og:image" content="%(og)s">\n'
         '<meta property="og:image:type" content="image/png">\n'
         '<meta property="og:image:width" content="1200">\n'
         '<meta property="og:image:height" content="630">\n',
         '<meta property="og:image" content="%(ogimg)s">\n'
         '<meta property="og:image:type" content="%(ogitype)s">\n'
         '<meta property="og:image:width" content="%(ogw)s">\n'
         '<meta property="og:image:height" content="%(ogh)s">\n'),
        ('<meta property="og:image:alt" content="%(ogalt)s">\n'
         '<meta name="twitter:card" content="summary_large_image">',
         '<meta property="og:image:alt" content="%(ogalt)s">\n'
         '%(itemprop)s<meta name="twitter:card" content="summary_large_image">'),
        ('<meta name="twitter:description" content="%(desc)s">\n'
         '<meta name="twitter:image" content="%(og)s">',
         '<meta name="twitter:description" content="%(ogdesc)s">\n'
         '<meta name="twitter:image" content="%(ogimg)s">'),
        ('def wrap(title, desc, keywords, active, body):\n'
         '    global PAGE_KEY\n'
         '    PAGE_KEY = active\n'
         '    return (head(title, desc, keywords) + topbar() + navbar() +\n'
         '            "<main>\\n" + body + "\\n</main>\\n" + footer() + "</body>\\n</html>\\n")',
         'def wrap(title, desc, keywords, active, body):\n'
         '    global PAGE_KEY\n'
         '    PAGE_KEY = active\n'
         '    thumb = ""\n'
         '    if active.startswith("case-"):\n'
         '        thumb = (\'<img class="wx-share-thumb" src="%s" alt="" width="300" height="300" aria-hidden="true">\\n\'\n'
         '                 % share_image_url(active))\n'
         '    return (head(title, desc, keywords) + thumb + topbar() + navbar() +\n'
         '            "<main>\\n" + body + "\\n</main>\\n" + footer() + "</body>\\n</html>\\n")'),
    ], "site")
    save(BUILD, s)

    print("== 2/4 style.css ==")
    c = load(CSS)
    if ".wx-share-thumb" in c:
        raise SystemExit("CSS 已含 .wx-share-thumb")
    c += ("\n/* 微信分享卡片首图：移出视口但不隐藏，供爬虫抓图，不改可见布局 */\n"
          ".wx-share-thumb{position:absolute;top:0;left:-9999px;width:300px;height:300px;"
          "pointer-events:none;z-index:-1}\n")
    save(CSS, c)
    print("  [css] 追加 .wx-share-thumb")

    print("== 3/4 package_site.py ==")
    p = load(PACKAGE)
    p = apply(p, [(
        '# 含个人信息的二维码原图不打包\nsite_files.discard("assets/img/qrcode-source.png")',
        '# 微信分享方图使用 HTTPS 绝对地址，无法被标签属性收集，显式补入\n'
        'for _p in glob.glob(os.path.join(ROOT, "assets", "cases", "share-*.jpg")):\n'
        '    site_files.add(os.path.relpath(_p, ROOT).replace("\\\\", "/"))\n\n'
        '# 含个人信息的二维码原图不打包\nsite_files.discard("assets/img/qrcode-source.png")'),
    ], "package")
    save(PACKAGE, p)

    print("== 4/4 validate.py ==")
    v = load(VALID)
    if "第十三轮：微信分享卡片静态兜底" in v:
        raise SystemExit("validate.py 已打过补丁")
    v = v.replace('\nprint("页面数:", len(PAGES))', EXTRA_VALIDATE + '\nprint("页面数:", len(PAGES))')
    save(VALID, v)
    print("补丁完成")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""第十四轮：全站微信分享统一为一张固定图。

只换图片来源并把分享标签扩展到所有正常内容页；404 与站长验证文件按写死规则不带任何分享标签。
"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, "tools")
BUILD = os.path.join(T, "build_site.py")
PACKAGE = os.path.join(T, "package_site.py")
VALID = os.path.join(T, "validate.py")


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
        print("  [%s] OK %s" % (tag, old[:54].replace("\n", " ")))
    return s


NEW_VALIDATE = '''# ---------------------------------------------------------------- 第十四轮：全站统一固定分享图
from PIL import Image

SHARE_URL = SITE_URL + "assets/img/share-site.jpg"
share_path = os.path.join(ROOT, "assets", "img", "share-site.jpg")
if not os.path.exists(share_path):
    problems.append("缺全站固定分享图")
else:
    im = Image.open(share_path)
    if im.size != (400, 400) or im.format != "JPEG":
        problems.append("固定分享图规格不对 %s %s" % (im.size, im.format))
    if os.path.getsize(share_path) > 100 * 1024:
        problems.append("固定分享图超过 100KB")
    if im.getexif():
        problems.append("固定分享图含 EXIF")

for name in PAGES:
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
    if len(urls) != 3 or len(set(urls)) != 1 or urls[0] != SHARE_URL:
        problems.append("%s 分享图地址不是全站固定图: %s" % (name, urls))
    if not re.search(r'<body[^>]*>\\s*<img class="wx-share-thumb"', s):
        problems.append("%s 固定图不在 body 第一行" % name)
    if "display:none" in s or re.search(r'wx-share-thumb[^>]*loading=', s):
        problems.append("%s 首图用了 display:none 或 loading=lazy" % name)
    if re.search(r'assets/cases/share-[a-z]+\\.jpg', s):
        problems.append("%s 仍引用旧的详情页专属方图" % name)

# 404 与站长验证文件按规范不带任何分享标签
for name in ["404.html", "googled740806788de8245.html"]:
    p = os.path.join(ROOT, name)
    if not os.path.exists(p):
        continue
    s = open(p, encoding="utf-8").read()
    if "itemprop=" in s or "wx-share-thumb" in s or 'property="og:' in s:
        problems.append("%s 误带分享标签" % name)

'''


def main():
    print("== 1/3 build_site.py ==")
    s = load(BUILD)
    s = apply(s, [
        ('def share_image_url(page):\n'
         '    """详情页方形分享图的 HTTPS 绝对地址。"""\n'
         '    return SITE_URL + "assets/cases/share-" + page[len("case-"):] + ".jpg"',
         'SHARE_IMAGE_URL = SITE_URL + "assets/img/share-site.jpg"\n\n\n'
         'def share_image_url(page=None):\n'
         '    """全站统一固定分享图的 HTTPS 绝对地址。"""\n'
         '    return SHARE_IMAGE_URL'),
        ('    share_url = share_image_url(page) if is_case else ""\n'
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
         '                       esc_short, share_url))\n',
         '    share_url = share_image_url()\n'
         '    short_desc = share_summary(desc) if is_case else desc\n'
         '    esc_short = html.escape(short_desc, quote=True)\n'
         '    ogdesc = esc_short if is_case else desc\n'
         '    og_img = share_url\n'
         '    og_w, og_h = "400", "400"\n'
         '    og_itype = "image/jpeg"\n'
         '    itemprop = (\'<meta itemprop="name" content="%s">\\n\'\n'
         '                \'<meta itemprop="description" content="%s">\\n\'\n'
         '                \'<meta itemprop="image" content="%s">\\n\'\n'
         '                % (html.escape(title + " | " + BRAND, quote=True),\n'
         '                   esc_short, share_url))\n'),
        ('             ogdesc=esc_short, ogimg=og_img, ogw=og_w, ogh=og_h,',
         '             ogdesc=ogdesc, ogimg=og_img, ogw=og_w, ogh=og_h,'),
        ('    thumb = ""\n'
         '    if active.startswith("case-"):\n'
         '        thumb = (\'<img class="wx-share-thumb" src="%s" alt="" width="300" height="300" aria-hidden="true">\\n\'\n'
         '                 % share_image_url(active))',
         '    thumb = (\'<img class="wx-share-thumb" src="%s" alt="" width="300" height="300" aria-hidden="true">\\n\'\n'
         '             % share_image_url())'),
    ], "site")
    save(BUILD, s)

    print("== 2/3 package_site.py ==")
    p = load(PACKAGE)
    p = apply(p, [(
        '# 微信分享方图使用 HTTPS 绝对地址，无法被标签属性收集，显式补入\n'
        'for _p in glob.glob(os.path.join(ROOT, "assets", "cases", "share-*.jpg")):\n'
        '    site_files.add(os.path.relpath(_p, ROOT).replace("\\\\", "/"))',
        '# 全站统一微信分享图使用 HTTPS 绝对地址，无法被标签属性收集，显式补入\n'
        'if os.path.isfile(os.path.join(ROOT, "assets", "img", "share-site.jpg")):\n'
        '    site_files.add("assets/img/share-site.jpg")'),
    ], "package")
    save(PACKAGE, p)

    print("== 3/3 validate.py ==")
    v = load(VALID)
    a = v.index("# ---------------------------------------------------------------- 第十三轮")
    b = v.index('print("页面数:", len(PAGES))', a)
    v = v[:a] + NEW_VALIDATE + v[b:]
    print("  [validate] 第十三轮断言已替换为全站固定图断言")
    save(VALID, v)
    print("补丁完成")


if __name__ == "__main__":
    main()

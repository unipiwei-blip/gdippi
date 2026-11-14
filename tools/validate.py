# -*- coding: utf-8 -*-
"""静态站点自检：资源、链接、导航、SEO 元信息、关键营销文案"""
import os
import re
from bs4 import BeautifulSoup

ROOT = r"D:\项目管理文件夹\2026-11-08-11-48-17"
PAGES = ["index.html", "website.html", "miniprogram.html", "cases.html",
         "service.html", "pricing.html", "contact.html", "sitemap.html"]
PAGES += ["case-shanghui.html", "case-cailie.html", "case-baydea.html", "case-jianzhuo.html", "case-guanxiang.html", "case-niling.html", "case-leiyiming.html"]
NAV = set(PAGES) | {"sitemap.xml", "robots.txt", "CNAME"}
ALL_CASE_SITES = ["zyyous.com", "91cailie.com", "baydea.com", "dgjzkj.com",
                  "touzs.com", "365ls.cn", "oals.cn"]
problems = []

for name in PAGES:
    path = os.path.join(ROOT, name)
    soup = BeautifulSoup(open(path, encoding="utf-8").read(), "html.parser")

    # 资源文件
    for tag, attr in [("img", "src"), ("link", "href"), ("script", "src")]:
        for el in soup.find_all(tag):
            src = el.get(attr, "")
            if not src or src.startswith(("http", "data:", "#")):
                continue
            if not os.path.exists(os.path.join(ROOT, src.split("#")[0])):
                problems.append("%s: 资源缺失 %s" % (name, src))

    # 本地链接目标
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith(("http", "mailto:", "tel:")):
            continue
        target, _, anchor = href.partition("#")
        if not target:
            continue
        if target.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg",
                                    ".xml", ".txt", ".pdf", ".ico")):
            if not os.path.exists(os.path.join(ROOT, target)):
                problems.append("%s: 资源链接缺失 %s" % (name, href))
            continue
        if target not in NAV:
            problems.append("%s: 链接目标不存在 %s" % (name, href))
        if target and os.path.exists(os.path.join(ROOT, target)) and anchor:
            other = BeautifulSoup(open(os.path.join(ROOT, target), encoding="utf-8").read(),
                                  "html.parser")
            if not other.find(id=anchor):
                problems.append("%s: 锚点不存在 %s" % (name, href))

    # 导航 7 项
    links = {a.get("data-nav") for a in soup.select(".nav-menu a")}
    if len(links) != 7:
        problems.append("%s: 主导航栏目数 %d（应为 7）" % (name, len(links)))

    # SEO 元信息
    if not soup.title or "极站 GOSITE" not in soup.title.string:
        problems.append("%s: 标题缺失" % name)
    for key in ["description", "keywords"]:
        el = soup.find("meta", attrs={"name": key})
        if not el or not el.get("content"):
            problems.append("%s: meta %s 缺失" % (name, key))

    # 二维码 / ICO
    for need in ["assets/img/qrcode.png", "assets/img/logo.png", "favicon.ico",
                 "assets/img/og-image.png", "assets/img/gdiis-logo.png",
                 "sitemap.xml", "robots.txt", "CNAME", ".nojekyll"]:
        if not os.path.exists(os.path.join(ROOT, need)):
            problems.append("%s: 缺文件 %s" % (name, need))
    for tag in ['rel="canonical"', "application/ld+json", 'property="og:image"',
                'name="twitter:card"', "https://gd.ippi.com.cn/"]:
        if tag not in open(path, encoding="utf-8").read():
            problems.append("%s: SEO 标签缺失 %s" % (name, tag))

# 关键营销信息全站覆盖检查
index = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
for kw in ["399", "前 10 名", "设计满意再付款", "最快当天上线", "代运营", "纯静态", "商城小程序",
           "zyyous.com", "91cailie.com", "baydea.com", "footer-qr"]:
    if kw not in index:
        problems.append("首页缺失关键信息: %s" % kw)

# 案例页三站链接
cases = open(os.path.join(ROOT, "cases.html"), encoding="utf-8").read()
for site in ALL_CASE_SITES:
    if "https://www.%s/" % site not in cases:
        problems.append("案例页缺失: %s" % site)
if cases.count('class="case-card reveal"') != 7:
    problems.append("案例页卡片数不是 7")
if cases.count('class="shot ') != 28:
    problems.append("案例页多端截图数不是 28（7 组 × 4 张）")
if cases.count('>设计讲解 ') != 7 or index.count('>设计讲解 ') != 6:
    problems.append("案例卡设计讲解入口数不对")
for stem in [c for c in ("case-shanghui", "case-cailie", "case-baydea", "case-jianzhuo",
                         "case-guanxiang", "case-niling", "case-leiyiming")]:
    if not os.path.exists(os.path.join(ROOT, stem + ".html")):
        problems.append("缺少设计讲解页: " + stem)
if "GDiis" not in index or "brand-slogan" not in index:
    problems.append("LOGO GDiis / 广告词缺失")
if "每月前 10 名" not in index:
    problems.append("每月前 10 名顾客口径缺失")
if index.count('class="case-card reveal"') != 6:
    problems.append("首页案例卡片数不是 6")

# 标准价套餐与页脚链接
pricing = open(os.path.join(ROOT, "pricing.html"), encoding="utf-8").read()
for kw in ["998", "标准价", "每月前 10 名顾客", "标准版"]:
    if kw not in pricing:
        problems.append("价格页缺失: %s" % kw)
for site in ALL_CASE_SITES:
    if "https://www.%s/" % site not in index:
        problems.append("首页友情链接缺失: %s" % site)
if "https://www.gdiis.com" not in index:
    problems.append("首页技术支持链接缺失")
if "说明行业与栏目需求" in index or "工作日 9:00" in index:
    problems.append("页脚旧文案未删除")
if "footer-links" not in index or "网站地图" not in index:
    problems.append("页脚链接条/网站地图链接缺失")
if "footer-tech" not in index or "网站技术服务支持" not in index or "gdiis-logo.png" not in index:
    problems.append("技术支持 LOGO 区块缺失")

# 小程序页能力覆盖
mini = open(os.path.join(ROOT, "miniprogram.html"), encoding="utf-8").read()
for kw in ["分销模块", "拼团", "限时抢购", "积分", "会员", "多门店", "店内点餐",
           "预约报名", "万能表单", "智慧餐饮", "同城服务"]:
    if kw not in mini:
        problems.append("小程序页缺失能力: %s" % kw)

# ---------------------------------------------------------------- 第十一轮：SEO / 网站地图深度校验
import json

DISALLOWED = ["独立成页", "独立页面", "独立详情页", "各自成页", "单独成页", "各有专页",
              "每项都有专页", "点击任意", "进入详情页", "上线前建议", "匿名化示例",
              "本页", "本站", "本栏目", "一句话说清", "一句话讲清", "按需进入",
              "写清能做什么", "都有独立页面", "页面独立", "假官网"]
SITE_URL = "https://gd.ippi.com.cn/"

xml_raw = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
xml_urls = re.findall(r"<loc>(.*?)</loc>", xml_raw)
expect_urls = {SITE_URL} | {SITE_URL + p for p in PAGES if p != "index.html"}
if len(xml_urls) != len(expect_urls) or set(xml_urls) != expect_urls:
    problems.append("sitemap.xml 的 URL 集合与实际页面不一致（%d 条）" % len(xml_urls))
robots = open(os.path.join(ROOT, "robots.txt"), encoding="utf-8").read()
if "Sitemap: " + SITE_URL + "sitemap.xml" not in robots or "Allow: /assets/" not in robots:
    problems.append("robots.txt 缺少 Sitemap / assets 放行规则")

# 站长平台验证文件：必须原样放在根目录、可被公开抓取，但不写入 sitemap（避免被索引）
verify_files = [f for f in os.listdir(ROOT) if re.match(r"^google[a-f0-9]+\.html$", f)]
for vf in verify_files:
    content = open(os.path.join(ROOT, vf), encoding="utf-8").read().strip()
    if content != "google-site-verification: " + vf:
        problems.append("%s: 站长验证文件内容不正确" % vf)
    if SITE_URL + vf in xml_urls:
        problems.append("%s: 验证文件不应写入 sitemap.xml" % vf)
    if "Disallow: /" + vf in robots:
        problems.append("%s: robots.txt 不可屏蔽验证文件" % vf)

for name in PAGES:
    raw = open(os.path.join(ROOT, name), encoding="utf-8").read()
    soup = BeautifulSoup(raw, "html.parser")
    canon = soup.find("link", rel="canonical")
    want = SITE_URL + ("" if name == "index.html" else name)
    if not canon or canon.get("href") != want:
        problems.append("%s: canonical 不正确" % name)
    d = soup.find("meta", attrs={"name": "description"})
    if d and not (70 <= len(d.get("content", "")) <= 200):
        problems.append("%s: description 长度 %d，建议 70-200" % (name, len(d.get("content", ""))))
    if len(soup.find_all("h1")) != 1:
        problems.append("%s: h1 数量不是 1" % name)
    for im in soup.find_all("img"):
        # 装饰性图片允许 alt=""（配合 aria-hidden），只要求属性存在
        if im.get("alt") is None:
            problems.append("%s: 图片缺 alt 属性 %s" % (name, im.get("src", "")))
    txt_soup = BeautifulSoup(raw, "html.parser")
    for sc in txt_soup.find_all("script"):
        sc.decompose()
    visible = txt_soup.get_text(" ") + " " + (d.get("content", "") if d else "")
    for w in DISALLOWED:
        if w in visible:
            problems.append("%s: 文案含禁用表述「%s」" % (name, w))
    ld = soup.find("script", attrs={"type": "application/ld+json"})
    if not ld:
        problems.append("%s: 缺 JSON-LD" % name)
        continue
    graph = json.loads(ld.string).get("@graph", [])
    types = {g.get("@type") for g in graph}
    for need in ["Organization", "WebSite", "Service", "WebPage", "BreadcrumbList"]:
        if need not in types:
            problems.append("%s: JSON-LD 缺 %s" % (name, need))
    if name.startswith("case-"):
        ogt = soup.find("meta", attrs={"property": "og:type"})
        if not ogt or ogt.get("content") != "article":
            problems.append("%s: 案例页 og:type 应为 article" % name)
        bc = next((g for g in graph if g.get("@type") == "BreadcrumbList"), {})
        if len(bc.get("itemListElement", [])) != 3:
            problems.append("%s: 面包屑应为 3 级" % name)
    if name in ("index.html", "pricing.html") and "FAQPage" not in types:
        problems.append("%s: 缺 FAQPage 结构化数据" % name)


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


# ---------------------------------------------------------------- 第十四轮：全站统一固定分享图
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
    if not re.search(r'<body[^>]*>\s*<img class="wx-share-thumb"', s):
        problems.append("%s 固定图不在 body 第一行" % name)
    if "display:none" in s or re.search(r'wx-share-thumb[^>]*loading=', s):
        problems.append("%s 首图用了 display:none 或 loading=lazy" % name)
    if re.search(r'assets/cases/share-[a-z]+\.jpg', s):
        problems.append("%s 仍引用旧的详情页专属方图" % name)

# 404 与站长验证文件按规范不带任何分享标签
for name in ["404.html", "googled740806788de8245.html"]:
    p = os.path.join(ROOT, name)
    if not os.path.exists(p):
        continue
    s = open(p, encoding="utf-8").read()
    if "itemprop=" in s or "wx-share-thumb" in s or 'property="og:' in s:
        problems.append("%s 误带分享标签" % name)

print("页面数:", len(PAGES))
print("问题数:", len(problems))
for p in problems:
    print(" -", p)
if not problems:
    print("全部校验通过：资源、链接、导航、SEO、营销信息齐全。")

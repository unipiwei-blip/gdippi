# -*- coding: utf-8 -*-
"""静态站点自检：资源、链接、导航、SEO 元信息、关键营销文案"""
import os
import re
from bs4 import BeautifulSoup

ROOT = r"D:\项目管理文件夹\2026-11-08-11-48-17"
PAGES = ["index.html", "website.html", "miniprogram.html", "cases.html",
         "service.html", "pricing.html", "contact.html", "sitemap.html"]
NAV = set(PAGES) | {"sitemap.xml", "robots.txt", "CNAME"}
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
for site in ["zyyous.com", "91cailie.com", "baydea.com"]:
    if site not in cases:
        problems.append("案例页缺失: %s" % site)

# 标准价套餐与页脚链接
pricing = open(os.path.join(ROOT, "pricing.html"), encoding="utf-8").read()
for kw in ["998", "标准价", "仅限前 10 名且资料齐全", "标准版"]:
    if kw not in pricing:
        problems.append("价格页缺失: %s" % kw)
for site in ["zyyous.com", "91cailie.com", "baydea.com"]:
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

print("页面数:", len(PAGES))
print("问题数:", len(problems))
for p in problems:
    print(" -", p)
if not problems:
    print("全部校验通过：资源、链接、导航、SEO、营销信息齐全。")

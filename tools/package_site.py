# -*- coding: utf-8 -*-
"""打包交付：① 可直接部署的静态网站 ② 商城上架素材
网站包只包含运行所需文件，自动从 HTML 引用收集资源，排除个人信息原图、工具脚本与缓存。
"""
import io
import os
import zipfile
from bs4 import BeautifulSoup

ROOT = r"D:\项目管理文件夹\2026-11-08-11-48-17"
DIST = os.path.join(ROOT, "dist")
os.makedirs(DIST, exist_ok=True)

PAGES = ["index.html", "website.html", "miniprogram.html", "cases.html",
         "service.html", "pricing.html", "contact.html", "sitemap.html"]

site_files = set(PAGES)
for page in PAGES:
    soup = BeautifulSoup(io.open(os.path.join(ROOT, page), encoding="utf-8").read(),
                         "html.parser")
    for tag, attr in [("img", "src"), ("link", "href"), ("script", "src"), ("a", "href")]:
        for el in soup.find_all(tag):
            value = el.get(attr, "")
            if not value or value.startswith(("http", "#", "mailto:", "tel:", "data:")):
                continue
            rel = value.split("#")[0]
            if rel and os.path.isfile(os.path.join(ROOT, rel)):
                site_files.add(rel)

# 发布与 SEO 文件（meta 中的绝对 URL 无法被标签属性收集，显式补上）
for extra in ["favicon.ico", "CNAME", ".nojekyll", "robots.txt", "sitemap.xml",
              "assets/img/og-image.png"]:
    if os.path.isfile(os.path.join(ROOT, extra)):
        site_files.add(extra)

# 含个人信息的二维码原图不打包
site_files.discard("assets/img/qrcode-source.png")

missing = [f for f in site_files if not os.path.isfile(os.path.join(ROOT, f))]
if missing:
    raise SystemExit("缺失文件: %s" % missing)

site_zip = os.path.join(DIST, "极速建站-网站完整包-20261108.zip")
with zipfile.ZipFile(site_zip, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for rel in sorted(site_files):
        z.write(os.path.join(ROOT, rel), arcname=rel)
print("网站包:", len(site_files), "个文件")

shop_root = os.path.join(ROOT, "assets", "shop")
shop_files = []
for base, _dirs, files in os.walk(shop_root):
    for f in files:
        if f.lower().endswith((".png", ".jpg", ".jpeg")):
            full = os.path.join(base, f)
            arc = os.path.relpath(full, shop_root).replace("\\", "/")
            shop_files.append((full, arc))

shop_zip = os.path.join(DIST, "极速建站-商品素材包-20261108.zip")
with zipfile.ZipFile(shop_zip, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for full, arc in sorted(shop_files, key=lambda x: x[1]):
        z.write(full, arcname=arc)
print("素材包:", len(shop_files), "个文件")

for path in (site_zip, shop_zip):
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
        total = sum(i.file_size for i in z.infolist())
        print(os.path.basename(path), "| 校验:", "OK" if bad is None else bad,
              "| 原始大小: %.2f MB" % (total / 1024 / 1024),
              "| 压缩包: %.2f MB" % (os.path.getsize(path) / 1024 / 1024))

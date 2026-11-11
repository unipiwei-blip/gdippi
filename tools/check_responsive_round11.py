# -*- coding: utf-8 -*-
"""第十一轮响应式与版式校验：15 页 × 4 宽度 + 网站地图新布局实拍"""
import os
from playwright.sync_api import sync_playwright

ROOT = r"D:\项目管理文件夹\2026-11-08-11-48-17"
OUT = os.path.join(ROOT, ".tmp", "preview")
os.makedirs(OUT, exist_ok=True)
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
WIDTHS = [390, 768, 1024, 1440]
PAGES = ["index.html", "website.html", "miniprogram.html", "cases.html",
         "service.html", "pricing.html", "contact.html", "sitemap.html",
         "case-shanghui.html", "case-cailie.html", "case-baydea.html",
         "case-jianzhuo.html", "case-guanxiang.html", "case-niling.html",
         "case-leiyiming.html"]


def url(name):
    return "file:///" + os.path.join(ROOT, name).replace("\\", "/")


def ready(pg):
    pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
    pg.evaluate("document.querySelectorAll('img').forEach(i=>{i.loading='eager';i.src=i.src})")
    pg.wait_for_timeout(450)


problems = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EDGE, headless=True,
                          args=["--no-sandbox", "--disable-gpu"])
    for name in PAGES:
        for w in WIDTHS:
            pg = b.new_page(viewport={"width": w, "height": 900})
            pg.goto(url(name), wait_until="load")
            pg.wait_for_timeout(180)
            ready(pg)
            over = pg.evaluate("Math.max(0, document.documentElement.scrollWidth - window.innerWidth)")
            if over > 1:
                problems.append("%s @%dpx 横向溢出 %dpx" % (name, w, over))
            broken = pg.evaluate("Array.from(document.images).filter(i=>!i.complete||i.naturalWidth===0).length")
            if broken:
                problems.append("%s @%dpx 图片未加载 %d 张" % (name, w, broken))
            pg.close()

    # 网站地图新布局实拍
    for w, tag in [(1440, "pc"), (390, "mobile")]:
        pg = b.new_page(viewport={"width": w, "height": 1000},
                        is_mobile=(w == 390), has_touch=(w == 390))
        pg.goto(url("sitemap.html"), wait_until="load")
        pg.wait_for_timeout(400)
        ready(pg)
        grids = pg.locator("section .grid.g4")
        counts = [grids.nth(i).locator("a.card").count() for i in range(grids.count())]
        print("网站地图 @%dpx: g4 网格 %d 组，每组卡片 %s" % (w, grids.count(), counts))
        if counts != [8, 8]:
            problems.append("sitemap.html @%dpx 卡片分组不是 8+8: %s" % (w, counts))
        pg.screenshot(path=os.path.join(OUT, "r11-sitemap-%s.png" % tag), full_page=True)
        pg.close()

    # 首页与案例页同步抽查
    for name, tag in [("index.html", "home"), ("cases.html", "cases")]:
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        pg.goto(url(name), wait_until="load")
        pg.wait_for_timeout(300)
        ready(pg)
        pg.screenshot(path=os.path.join(OUT, "r11-%s.png" % tag), full_page=False)
        pg.close()
    b.close()

print("页面 %d × 宽度 %d = %d 组，问题: %d" % (len(PAGES), len(WIDTHS), len(PAGES) * len(WIDTHS), len(problems)))
for x in problems:
    print(" -", x)

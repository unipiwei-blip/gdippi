# -*- coding: utf-8 -*-
"""第五轮视觉校验：套餐顺序、单行标题、商城样板、案例多端截图、页脚"""
import os
from playwright.sync_api import sync_playwright

ROOT = r"D:\项目管理文件夹\2026-11-08-11-48-17"
OUT = os.path.join(ROOT, ".tmp", "preview")
os.makedirs(OUT, exist_ok=True)
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def url(name):
    return "file:///" + os.path.join(ROOT, name).replace("\\", "/")


with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EDGE, headless=True,
                          args=["--no-sandbox", "--disable-gpu"])

    # 价格页：三卡视觉顺序
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(url("pricing.html"), wait_until="load")
    pg.wait_for_timeout(600)
    pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
    pg.wait_for_timeout(350)
    order = pg.evaluate("""() => [...document.querySelectorAll('.plan-grid > article')]
      .map(a => ({x: a.getBoundingClientRect().x, t: a.querySelector('h3').innerText}))
      .sort((a,b) => a.x - b.x).map(o => o.t)""")
    print("套餐从左到右:", " | ".join(order))
    pg.locator(".plan-grid").screenshot(path=os.path.join(OUT, "r5-plans.png"))
    pg.close()

    # 小程序页：单行标题 + 样板堆叠 + 网格
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(url("miniprogram.html"), wait_until="load")
    pg.wait_for_timeout(700)
    pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
    pg.wait_for_timeout(350)
    info = pg.evaluate("""() => { const e=document.querySelector('.h2.nowrap');
      const lh=parseFloat(getComputedStyle(e).lineHeight);
      return {height:e.getBoundingClientRect().height, lineHeight:lh}; }""")
    print("行业标题高度/行高:", info, "单行:", info["height"] <= info["lineHeight"] * 1.5)
    pg.locator(".mall-stack").screenshot(path=os.path.join(OUT, "r5-mall-stack.png"))
    pg.locator(".mall-grid").screenshot(path=os.path.join(OUT, "r5-mall-grid.png"))
    pg.close()

    # 案例页多端截图区
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(url("cases.html"), wait_until="load")
    pg.wait_for_timeout(700)
    pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
    pg.wait_for_timeout(350)
    print("案例截图数量:", pg.locator(".gallery-grid .shot").count())
    pg.evaluate("document.querySelectorAll('img').forEach(i=>{i.loading='eager'; i.src=i.src})")
    pg.wait_for_timeout(1500)
    pg.locator(".gallery-item").first.screenshot(path=os.path.join(OUT, "r5-gallery.png"))
    pg.close()

    # 页脚（桌面 / 手机）
    for width, label in [(1440, "pc"), (390, "mobile")]:
        pg = b.new_page(viewport={"width": width, "height": 900})
        pg.goto(url("index.html"), wait_until="load")
        pg.wait_for_timeout(600)
        pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
        pg.wait_for_timeout(350)
        second = pg.evaluate("""() => document.querySelectorAll('.footer-top > div')[1].innerText.replace(/\\s+/g,' ')""")
        print("页脚第二栏(%s):" % label, second.strip())
        pg.locator(".footer").screenshot(path=os.path.join(OUT, "r5-footer-" + label + ".png"))
        pg.close()

    # 手机端商城网格与案例截图
    pg = b.new_page(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    pg.goto(url("miniprogram.html"), wait_until="load")
    pg.wait_for_timeout(700)
    pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
    pg.wait_for_timeout(350)
    pg.locator(".mall-grid").screenshot(path=os.path.join(OUT, "r5-mall-mobile.png"))
    pg.close()
    b.close()

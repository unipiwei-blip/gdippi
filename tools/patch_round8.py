# -*- coding: utf-8 -*-
"""第八轮：案例实拍 1 PC + 2 手机 / LOGO GDiis + 广告词 / 每月前 10 名顾客口径"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
log = []


def patch(path, reps, label):
    s = io.open(path, encoding="utf-8").read()
    for old, new in reps:
        n = s.count(old)
        if n:
            s = s.replace(old, new)
        log.append((label, old[:34], n))
    io.open(path, "w", encoding="utf-8", newline="\n").write(s)


BS = os.path.join(HERE, "build_site.py")
s = io.open(BS, encoding="utf-8").read()

# ---------- 1. 案例实拍：1 张完整 PC + 2 张手机 ----------
old_shots = '''        shots = [(stem + ".png", "PC 首页", "wide"), (stem + "-pc2.jpg", "PC 内页", "wide"),
                 (stem + "-m1.jpg", "手机首页", "phone"), (stem + "-m2.jpg", "手机内页", "phone")]'''
new_shots = '''        shots = [(stem + ".png", "PC 完整首屏", "wide"),
                 (stem + "-m1.jpg", "手机首页", "phone"), (stem + "-m2.jpg", "手机内页", "phone")]'''
log.append(("案例实拍 3 张", "shots", s.count(old_shots)))
s = s.replace(old_shots, new_shots, 1)

old_lead = '"7 个案例，每个都附 PC 端与手机端实拍截图，点击可查看原图，看看栏目在两种屏幕上怎么落地。"'
new_lead = '"每个案例都附完整 PC 首屏与两张手机页面实拍，点击可查看原图，看看栏目在两种屏幕上怎么落地。"'
log.append(("实拍导语", "lead", s.count(old_lead)))
s = s.replace(old_lead, new_lead, 1)

# ---------- 2. LOGO：GOSITE → GDiis，导航后加广告词 ----------
old_bt = "<strong>极站</strong><span>GOSITE</span>"
log.append(("LOGO GDiis", old_bt, s.count(old_bt)))
s = s.replace(old_bt, "<strong>极站</strong><span>GDiis</span>")
old_nav = '''<span class="brand-txt"><strong>极站</strong><span>GDiis</span></span></a>
<nav class="nav-menu"'''
new_nav = '''<span class="brand-txt"><strong>极站</strong><span>GDiis</span></span></a>
<span class="brand-slogan">官网快上线 · 全年有人管</span>
<nav class="nav-menu"'''
log.append(("导航广告词", "brand-slogan", s.count(old_nav)))
s = s.replace(old_nav, new_nav, 1)

# ---------- 3. 399 口径：每月前 10 名顾客（保留资料齐全条件） ----------
PRICE_REPS = [
    ("不限前 10 名，随时可咨询开通", "不限名额，随时可咨询开通"),
    ("前 10 名且资料齐全的咨询者", "每月前 10 名顾客且资料齐全"),
    ("限前 10 名咨询者", "每月限前 10 名顾客"),
    ("前 10 名咨询者", "每月前 10 名顾客"),
    ("前 10 名且资料齐全", "每月前 10 名顾客且资料齐全"),
    ("前 10 名", "每月前 10 名"),
]
for old, new in PRICE_REPS:
    n = s.count(old)
    if n:
        s = s.replace(old, new)
    log.append(("399 口径", old[:30], n))

io.open(BS, "w", encoding="utf-8", newline="\n").write(s)

# ---------- 4. 商品素材脚本同步价格口径 ----------
SHOP_REPS = [
    ("399 元 / 年 · 仅限前 10 名且资料齐全", "399 元 / 年 · 每月仅限前 10 名顾客"),
    ("399 元为限时价，仅限前 10 名且资料齐全的咨询者", "399 元为限时价，每月仅限前 10 名顾客且资料齐全"),
    ("399 元为限时价，仅限前 10 名且资料齐全的客户", "399 元为限时价，每月仅限前 10 名顾客且资料齐全"),
    ("限前 10 名且资料齐全的咨询者", "每月限前 10 名顾客且资料齐全"),
    ("限前 10 名且资料齐全的客户", "每月限前 10 名顾客且资料齐全"),
    ("前 10 名", "每月前 10 名"),
]
for name in ["build_shop_assets.py", "build_shop_clean.py", "build_shop_v3.py"]:
    p = os.path.join(HERE, name)
    t = io.open(p, encoding="utf-8").read()
    for old, new in SHOP_REPS:
        n = t.count(old)
        if n:
            t = t.replace(old, new)
        log.append((name, old[:28], n))
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)

p = os.path.join(HERE, "build_share_5x4.py")
t = io.open(p, encoding="utf-8").read()
for old, new in [("399 元/年 · 仅限前 10 名且资料齐全", "399 元/年 · 每月仅限前 10 名顾客"),
                 ("前 10 名", "每月前 10 名")]:
    n = t.count(old)
    if n:
        t = t.replace(old, new)
    log.append(("build_share_5x4.py", old[:28], n))
io.open(p, "w", encoding="utf-8", newline="\n").write(t)

for label, key, n in log:
    print(("OK  " if n else "MISS"), "%-22s" % label, n, key)

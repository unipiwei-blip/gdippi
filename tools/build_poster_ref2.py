# -*- coding: utf-8 -*-
"""参考两张图各做一版 399 建站海报，均压成 1080×1920 手机竖版。

A · longform：仿长图文的淡蓝紫底 / 白卡分节 / 数据卡 / 深蓝矩阵 / 亮蓝 CTA + 官网二维码
B · geo     ：仿科技蓝横幅的浅蓝白主视觉 / 六边形发光核心 / 玻璃面板 / 城市天际线，无二维码
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

from build_poster_399 import f, center, make_qr, ROOT, W, H

OUT = os.path.join(ROOT, "assets", "poster")
os.makedirs(OUT, exist_ok=True)

INK = (22, 34, 62)
MUTED = (104, 122, 158)
BLUE = (37, 92, 235)
PURPLE = (122, 68, 235)
PINK = (226, 21, 127)
CYAN = (16, 178, 172)
GOLD = (255, 205, 92)
WHITE = (255, 255, 255)
PALE = (226, 236, 255)


def ov_new():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def grad_bg(stops):
    """纵向多段渐变背景。stops: [(pos, (r,g,b)), ...]"""
    y = np.linspace(0, 1, H)[:, None]
    arr = np.tile(np.array(stops[0][1], dtype=float), (H, 1, 1))
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        k = np.clip((y - p0) / (p1 - p0), 0, 1)[..., None]
        seg = np.array(c0, dtype=float) + (np.array(c1, dtype=float) - np.array(c0, dtype=float)) * k
        arr = np.where((y >= p0)[..., None], seg, arr)
    tile = np.repeat(arr, W, axis=1).clip(0, 255).astype("uint8")
    return Image.fromarray(tile, "RGB").convert("RGBA")


def light_beams(d, color=(255, 255, 255, 120)):
    d.polygon([(0, 120), (300, 0), (120, 1920), (0, 1920)], fill=color)
    d.polygon([(1080, 80), (820, 0), (960, 1920), (1080, 1920)], fill=color)


def sec_title(d, y, text, color=INK, accent=(BLUE, CYAN)):
    """居中分节标题，两侧短渐变线（参考长图）。"""
    fnt = f(34, True)
    tw = d.textlength(text, font=fnt)
    cx = W / 2
    d.rounded_rectangle((cx - tw / 2 - 62, y + 18, cx - tw / 2 - 16, y + 22),
                        radius=2, fill=accent[0] + (255,))
    d.rounded_rectangle((cx + tw / 2 + 16, y + 18, cx + tw / 2 + 62, y + 22),
                        radius=2, fill=accent[1] + (255,))
    d.text((cx - tw / 2, y), text, font=fnt, fill=color + (255,) if len(color) == 3 else color)


def grad_text(img, y, text, fnt, c0, c1):
    """横向/纵向渐变文字（贴片 + 掩码）。"""
    w = int(fnt.getlength(text)) + 40
    h = int(fnt.size * 1.55)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).text((20, 0), text, font=fnt, fill=255)
    patch = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pd = ImageDraw.Draw(patch)
    for j in range(h):
        k = j / max(1, h - 1)
        pd.line((0, j, w, j), fill=tuple(int(c0[i] + (c1[i] - c0[i]) * k) for i in range(3)) + (255,))
    img.paste(patch, ((W - w) // 2, y), mask)


def pill(d, box, text, fnt, fill, outline, tcolor):
    d.rounded_rectangle(box, radius=(box[3] - box[1]) // 2, fill=fill, outline=outline, width=2)
    tw = d.textlength(text, font=fnt)
    d.text(((box[0] + box[2] - tw) / 2, (box[1] + box[3]) / 2 - fnt.size * 0.62),
           text, font=fnt, fill=tcolor)


def hex_pts(cx, cy, r):
    return [(cx + r * math.cos(math.radians(60 * k - 30)),
             cy + r * math.sin(math.radians(60 * k - 30))) for k in range(6)]


def browser_shot(img, box, path):
    """把真实案例 PC 截图放进带浏览器顶栏的圆角框。"""
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle((x0, y0, x1, y1), radius=20, fill=(255, 255, 255, 255),
                        outline=(206, 222, 250, 255), width=2)
    bar = 30
    d.rounded_rectangle((x0, y0, x1, y0 + bar + 16), radius=20, fill=(232, 241, 255, 255))
    d.rectangle((x0, y0 + bar, x1, y0 + bar + 16), fill=(232, 241, 255, 255))
    for i, c in enumerate([(255, 108, 108), (255, 198, 92), (96, 206, 148)]):
        cx = x0 + 22 + i * 20
        d.ellipse((cx, y0 + 12, cx + 10, y0 + 22), fill=c + (255,))
    sw, sh = x1 - x0 - 16, y1 - y0 - bar - 24
    shot = Image.open(path).convert("RGB")
    shot = ImageOps.fit(shot, (sw, sh), Image.LANCZOS, centering=(0.5, 0.0))
    mask = Image.new("L", (sw, sh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, sw, sh), radius=12, fill=255)
    img.paste(shot, (x0 + 8, y0 + bar + 16), mask)


# ---------------------------------------------------------------- A · 长图文压缩版
def make_longform():
    img = grad_bg([(0.0, (238, 242, 255)), (0.45, (244, 247, 255)),
                   (1.0, (232, 238, 255))])
    base = ov_new()
    light_beams(ImageDraw.Draw(base), (255, 255, 255, 105))
    img = Image.alpha_composite(img, base)

    ov = ov_new()
    d = ImageDraw.Draw(ov)

    # 品牌条
    logo = Image.open(os.path.join(ROOT, "assets", "img", "logo.png")).convert("RGBA")
    logo.thumbnail((64, 64), Image.LANCZOS)
    img.alpha_composite(logo, (60, 52))
    d.text((138, 54), "极站 GOSITE", font=f(34, True), fill=INK + (255,))
    d.text((138, 94), "GDiis · 官网快上线", font=f(19), fill=MUTED + (255,))
    pill(d, (720, 58, 1020, 108), "399 元/年 企业官网包年", f(22, True),
         (37, 92, 235, 255), (37, 92, 235, 255), (255, 255, 255, 255))

    # 标题
    d.text(((W - d.textlength("好官网，不用等", font=f(66, True))) / 2, 158),
           "好官网，不用等", font=f(66, True), fill=INK + (255,))
    grad_text(ov, 240, "最快当天上线", f(66, True), (60, 92, 240), (16, 178, 172))
    center(d, 330, "纯静态官网整站 + 全年代运营维护更新", f(27), MUTED + (255,))
    center(d, 368, "SEO + GEO 双优化，让客户能搜到，让 AI 能推荐", f(23), MUTED + (255,))

    # 两枚标签
    pill(d, (250, 410, 520, 460), "资料齐备即可上线", f(22, True),
         (255, 255, 255, 220), (190, 208, 245, 255), BLUE + (255,))
    pill(d, (560, 410, 830, 460), "每月前 10 名顾客", f(22, True),
         (255, 255, 255, 220), (190, 208, 245, 255), PURPLE + (255,))

    # 数据卡
    d.rounded_rectangle((60, 494, 1020, 676), radius=28, fill=(255, 255, 255, 250),
                        outline=(222, 232, 252, 255), width=2)
    sec_title(d, 510, "服务底座 · 站点实况")
    stats = [("当天", "最快可上线", BLUE), ("12 个月", "全年维护更新", CYAN),
             ("7 个", "线上站点案例", PURPLE)]
    for i, (num, lab, col) in enumerate(stats):
        x = 84 + i * 302
        d.rounded_rectangle((x, 566, x + 278, 654), radius=18,
                            fill=(246, 249, 255, 255), outline=(226, 235, 252, 255), width=2)
        nw = d.textlength(num, font=f(42, True))
        d.text((x + (278 - nw) / 2, 574), num, font=f(42, True), fill=col + (255,))
        d.rounded_rectangle((x + 20, 626, x + 258, 630), radius=2, fill=col + (90,))
        lw = d.textlength(lab, font=f(21))
        d.text((x + (278 - lw) / 2, 634), lab, font=f(21), fill=MUTED + (255,))

    # 分节 1：左侧三条说明 + 右侧真实案例 PC 截图
    d.rounded_rectangle((60, 700, 1020, 1042), radius=28, fill=(255, 255, 255, 250),
                        outline=(222, 232, 252, 255), width=2)
    sec_title(d, 716, "官网能带来什么")
    items = [("快", "最快当天上线", "资料齐备，页面做好即可发布"),
             ("稳", "纯静态更安全", "静态文件 + CDN，秒开少故障"),
             ("省", "全年有人维护", "改稿、加栏目、发资讯由服务团队完成")]
    for i, (tag, title, sub) in enumerate(items):
        y = 782 + i * 82
        d.rounded_rectangle((96, y, 152, y + 56), radius=14, fill=(231, 240, 255, 255))
        tw = d.textlength(tag, font=f(28, True))
        d.text((124 - tw / 2, y + 10), tag, font=f(28, True), fill=BLUE + (255,))
        d.text((170, y - 2), title, font=f(26, True), fill=(36, 74, 190, 255))
        d.text((170, y + 32), sub, font=f(19), fill=MUTED + (255,))
    browser_shot(ov, (552, 776, 992, 1016),
                 os.path.join(ROOT, "assets", "cases", "case-shanghui.png"))

    # 分节 2：深蓝交付标准矩阵
    d.rounded_rectangle((60, 1066, 1020, 1370), radius=28, fill=(18, 44, 96, 255))
    center(d, 1088, "交付标准", f(34, True), (255, 255, 255, 255))
    center(d, 1132, "快速上线不等于粗糙", f(21), (176, 202, 248, 255))
    grid = ["响应式布局", "语义化 HTML", "基础 SEO", "HTTPS · CDN", "分享物料", "安全运维"]
    for i, t in enumerate(grid):
        col, row = i % 3, i // 3
        x = 86 + col * 302
        y = 1174 + row * 92
        d.rounded_rectangle((x, y, x + 278, y + 76), radius=16,
                            fill=(46, 84, 156, 255), outline=(110, 156, 226, 255), width=2)
        tw = d.textlength(t, font=f(24, True))
        d.text((x + (278 - tw) / 2, y + 22), t, font=f(24, True), fill=(255, 255, 255, 255))

    # 分节 3：栏目清单
    d.rounded_rectangle((60, 1394, 1020, 1582), radius=28, fill=(255, 255, 255, 250),
                        outline=(222, 232, 252, 255), width=2)
    sec_title(d, 1410, "栏目清晰，内容好找")
    cols = ["首页", "关于我们", "业务服务", "成功案例",
            "资讯动态", "联系我们", "商城入口", "二维码"]
    for i, t in enumerate(cols):
        col, row = i % 4, i // 4
        x = 88 + col * 230
        y = 1462 + row * 52
        d.rounded_rectangle((x, y, x + 210, y + 44), radius=12,
                            fill=(240, 245, 255, 255), outline=(220, 231, 250, 255), width=1)
        tw = d.textlength(t, font=f(21))
        d.text((x + (210 - tw) / 2, y + 10), t, font=f(21), fill=INK + (255,))

    # 底部亮蓝 CTA + 官网二维码
    d.rounded_rectangle((60, 1606, 1020, 1900), radius=28, fill=(48, 106, 246, 255))
    d.rounded_rectangle((760, 1636, 992, 1868), radius=18, fill=(255, 255, 255, 255))
    ov.paste(make_qr().convert("RGBA").resize((176, 176), Image.NEAREST), (788, 1648))
    qw = d.textlength("扫码访问官网", font=f(19, True))
    d.text((760 + (232 - qw) / 2, 1832), "扫码访问官网", font=f(19, True),
           fill=(30, 70, 140, 255))
    d.text((96, 1640), "399 元 / 年", font=f(62, True), fill=(255, 255, 255, 255))
    std = "标准价 998 元 / 年"
    d.text((98, 1720), std, font=f(23), fill=(206, 224, 255, 255))
    sw = d.textlength(std, font=f(23))
    d.line((98, 1734, 98 + sw, 1734), fill=(206, 224, 255, 255), width=2)
    d.text((96, 1760), "企业官网包年 · 全年代运营维护更新", font=f(25, True), fill=(255, 255, 255, 255))
    d.text((96, 1804), "每月前 10 名顾客且资料齐全", font=f(23), fill=(226, 238, 255, 255))
    d.text((96, 1844), "设计满意再付款 · gd.ippi.com.cn", font=f(22, True),
           fill=(255, 255, 255, 255))

    return Image.alpha_composite(img, ov)


# ---------------------------------------------------------------- B · 科技蓝 GEO 主视觉
def make_geo():
    img = grad_bg([(0.0, (228, 242, 255)), (0.5, (246, 251, 255)),
                   (1.0, (214, 232, 255))])
    base = ov_new()
    bd = ImageDraw.Draw(base)
    # 城市天际线（淡蓝剪影）
    bars = [(0, 1240, 78, 260), (86, 1300, 62, 200), (156, 1190, 96, 310),
            (260, 1280, 70, 220), (338, 1150, 108, 350), (454, 1270, 64, 230),
            (526, 1210, 92, 290), (626, 1300, 58, 200), (692, 1170, 100, 330),
            (800, 1260, 74, 240), (882, 1220, 90, 280), (980, 1290, 100, 210)]
    for x, y, w, _h in bars:
        bd.rectangle((x, y, x + w, H), fill=(168, 202, 248, 90))
    bd.ellipse((300, 380, 780, 860), fill=(150, 205, 255, 60))
    light_beams(bd, (255, 255, 255, 95))
    img = Image.alpha_composite(img, base.filter(ImageFilter.GaussianBlur(2)))

    ov = ov_new()
    d = ImageDraw.Draw(ov)

    # 品牌条
    logo = Image.open(os.path.join(ROOT, "assets", "img", "logo.png")).convert("RGBA")
    logo.thumbnail((62, 62), Image.LANCZOS)
    img.alpha_composite(logo, (60, 50))
    d.text((136, 52), "极站 GOSITE", font=f(33, True), fill=(16, 52, 110, 255))
    d.text((136, 92), "GDiis · 官网快上线 · 全年有人管", font=f(19), fill=(96, 128, 178, 255))
    pill(d, (790, 56, 1020, 106), "399 元 / 年", f(24, True),
         (37, 92, 235, 255), (37, 92, 235, 255), (255, 255, 255, 255))

    # 标题（仿横幅的双色强调）
    center(d, 166, "AI 时代，企业需要一个", f(42, True), (24, 46, 88, 255))
    y = 224
    fnt = f(60, True)
    parts = [("有用的", (24, 46, 88, 255)), ("GEO", None), ("官网", (37, 92, 235, 255))]
    total = sum(d.textlength(t, font=fnt) for t, _ in parts)
    x = (W - total) / 2
    for t, col in parts:
        if col is None:
            grad_text_at(ov, x, y, t, fnt, (226, 21, 127), (122, 68, 235))
        else:
            d.text((x, y), t, font=fnt, fill=col)
        x += d.textlength(t, font=fnt)
    center(d, 312, "SEO + GEO 双优化，让客户能搜到，让 AI 能推荐", f(25), (86, 116, 166, 255))

    # 左右玻璃面板
    panels = [(48, 430, 336, 848, "搜索平台",
               [("百度", (48, 106, 235)), ("必应", (16, 150, 190)),
                ("360 搜索", (76, 176, 80)), ("搜狗", (226, 110, 40))]),
              (744, 430, 1032, 848, "AI 问答",
               [("DeepSeek", (76, 106, 235)), ("豆包", (16, 160, 190)),
                ("Kimi", (40, 44, 70)), ("文心", (226, 60, 90))])]
    for x0, y0, x1, y1, title, tags in panels:
        d.rounded_rectangle((x0, y0, x1, y1), radius=26,
                            fill=(255, 255, 255, 170), outline=(255, 255, 255, 235), width=3)
        tw = d.textlength(title, font=f(25, True))
        d.text((x0 + (x1 - x0 - tw) / 2, y0 + 22), title, font=f(25, True), fill=(20, 62, 130, 255))
        d.line((x0 + 30, y0 + 68, x1 - 30, y0 + 68), fill=(190, 216, 248, 255), width=2)
        for i, (name, col) in enumerate(tags):
            cx, cy = (x0 + 22 + (i % 2) * 138, y0 + 108 + (i // 2) * 148)
            d.rounded_rectangle((cx - 10, cy - 12, cx + 122, cy + 112), radius=16,
                                fill=(255, 255, 255, 210), outline=(214, 232, 252, 255), width=2)
            d.ellipse((cx + 34, cy + 8, cx + 78, cy + 52), fill=col + (46,))
            d.ellipse((cx + 44, cy + 18, cx + 68, cy + 42), fill=col + (255,))
            nw = d.textlength(name, font=f(18, True))
            d.text((cx + 56 - nw / 2, cy + 68), name, font=f(18, True), fill=(30, 58, 104, 255))

    # 光束指向核心
    d.polygon([(340, 600), (470, 660), (470, 700), (340, 720)], fill=(226, 60, 110, 46))
    d.polygon([(740, 600), (610, 660), (610, 700), (740, 720)], fill=(40, 120, 255, 46))

    # 六边形发光核心
    cx, cy = 540, 646
    for r, a in ((238, 40), (196, 70), (158, 110)):
        pts = hex_pts(cx, cy, r)
        d.line(pts + [pts[0]], fill=(70, 150, 255, a), width=4, joint="curve")
    inner = hex_pts(cx, cy, 152)
    d.polygon(inner, fill=(58, 128, 240, 232))
    d.line(inner + [inner[0]], fill=(190, 226, 255, 255), width=4, joint="curve")
    # 地球网格图标
    d.ellipse((cx - 42, cy - 118, cx + 42, cy - 34), outline=(226, 240, 255, 255), width=3)
    d.ellipse((cx - 20, cy - 118, cx + 20, cy - 34), outline=(226, 240, 255, 220), width=2)
    d.line((cx - 42, cy - 76, cx + 42, cy - 76), fill=(226, 240, 255, 220), width=2)
    d.arc((cx - 42, cy - 100, cx + 42, cy - 52), 0, 180, fill=(226, 240, 255, 200), width=2)
    center(d, cy - 18, "GEO 官网", f(38, True), (255, 255, 255, 255))
    center(d, cy + 36, "AI 可见入口", f(24, True), (222, 238, 255, 255))
    # 发光底座
    for rw, a in ((210, 60), (160, 90), (112, 130)):
        d.ellipse((cx - rw, cy + 150 - 26, cx + rw, cy + 150 + 26),
                  outline=(60, 150, 255, a), width=7)

    # 价格卡
    d.rounded_rectangle((60, 900, 1020, 1178), radius=28,
                        fill=(255, 255, 255, 232), outline=(255, 255, 255, 255), width=3)
    d.text((96, 920), "399", font=f(88, True), fill=(37, 92, 235, 255))
    d.text((342, 958), "元 / 年  ·  企业官网包年", font=f(34, True), fill=(20, 46, 92, 255))
    d.text((98, 1024), "标准价 998 元 / 年   ·   每月前 10 名顾客且资料齐全",
           font=f(23), fill=(104, 130, 172, 255))
    chips = ["最快当天上线", "全年代运营", "设计满意再付款"]
    for i, t in enumerate(chips):
        x = 96 + i * 300
        d.rounded_rectangle((x, 1080, x + 278, 1142), radius=16, fill=(232, 242, 255, 255))
        tw = d.textlength(t, font=f(23, True))
        d.text((x + (278 - tw) / 2, 1098), t, font=f(23, True), fill=(37, 92, 235, 255))

    # 底部深蓝收尾（无二维码、无网址）
    d.rounded_rectangle((60, 1210, 1020, 1910), radius=28, fill=(16, 46, 104, 255))
    center(d, 1260, "极站 GOSITE", f(48, True), (255, 255, 255, 255))
    center(d, 1332, "官网快上线 · 全年有人管", f(29), (186, 214, 255, 255))
    d.line((300, 1392, 780, 1392), fill=(255, 255, 255, 60), width=2)
    center(d, 1424, "纯静态官网 · 搜索与 AI 都能读懂", f(30, True), (255, 255, 255, 255))
    center(d, 1484, "SEO + GEO 双优化 · 内容清楚 · 持续更新", f(23), (176, 206, 250, 255))
    center(d, 1544, "399 元 / 年 · 设计满意再付款", f(30, True), (255, 205, 92, 255))
    for i, t in enumerate(["最快当天上线", "全年代运营", "每月前 10 名顾客"]):
        x = 110 + i * 290
        d.rounded_rectangle((x, 1620, x + 270, 1682), radius=16,
                            fill=(46, 84, 156, 255), outline=(110, 156, 226, 255), width=2)
        tw = d.textlength(t, font=f(22, True))
        d.text((x + (270 - tw) / 2, 1638), t, font=f(22, True), fill=(226, 238, 255, 255))
    center(d, 1736, "结构清楚、事实可核验，官网才能被长期看见", f(24), (176, 206, 250, 255))
    center(d, 1786, "极站 GOSITE  ·  企业官网包年服务", f(22, True), (140, 180, 240, 255))

    return Image.alpha_composite(img, ov)


def grad_text_at(img, x, y, text, fnt, c0, c1):
    """在指定 x 位置贴渐变文字（用于一行内的多段混排）。"""
    w = int(fnt.getlength(text)) + 12
    h = int(fnt.size * 1.55)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).text((6, 0), text, font=fnt, fill=255)
    patch = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pd = ImageDraw.Draw(patch)
    for j in range(h):
        k = j / max(1, h - 1)
        pd.line((0, j, w, j), fill=tuple(int(c0[i] + (c1[i] - c0[i]) * k) for i in range(3)) + (255,))
    img.paste(patch, (int(x), int(y)), mask)


def main():
    for stem, builder in [("poster-399-longform", make_longform),
                          ("poster-399-geo", make_geo)]:
        img = builder().convert("RGB")
        p_png = os.path.join(OUT, stem + ".png")
        p_jpg = os.path.join(OUT, stem + ".jpg")
        img.save(p_png, "PNG", optimize=True)
        img.save(p_jpg, "JPEG", quality=90, optimize=True, subsampling=0)
        print(stem, "|", img.size,
              "| PNG %.0fKB" % (os.path.getsize(p_png) / 1024),
              "| JPG %.0fKB" % (os.path.getsize(p_jpg) / 1024))


if __name__ == "__main__":
    main()

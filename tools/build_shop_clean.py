# -*- coding: utf-8 -*-
"""极站官网包年（399 元）商城上架素材：主图 / 4 张副图 / 详情长图
只围绕「企业官网包年」这一项服务，价格 399 元，不涉及其他产品与服务。
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = r"D:\项目管理文件夹\2026-11-08-11-48-17"
OUT = os.path.join(ROOT, "assets", "shop", "clean")
os.makedirs(OUT, exist_ok=True)

FB = "C:/Windows/Fonts/msyhbd.ttc"
FR = "C:/Windows/Fonts/msyh.ttc"
BLUE = (22, 104, 255)
PINK = (226, 21, 127)
INK = (10, 30, 60)
MUTED = (92, 113, 146)
WHITE = (255, 255, 255)


def font(size, bold=False):
    return ImageFont.truetype(FB if bold else FR, size)


def gradient(w, h, top=(11, 71, 214), mid=(105, 70, 235), bottom=(226, 21, 127)):
    yy = np.linspace(0, 1, h)[:, None, None]
    xx = np.linspace(0, 1, w)[None, :, None]
    t = np.clip(0.65 * xx + 0.35 * yy, 0, 1)
    a = np.array(top, dtype=float) + (np.array(mid, dtype=float) - np.array(top, dtype=float)) * np.clip(t / 0.55, 0, 1)
    b = np.array(mid, dtype=float) + (np.array(bottom, dtype=float) - np.array(mid, dtype=float)) * np.clip((t - 0.55) / 0.45, 0, 1)
    arr = np.where(t < 0.55, a, b).clip(0, 255).astype("uint8")
    return Image.fromarray(arr, "RGB").convert("RGBA")


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur); cur = ""; continue
        if draw.textlength(cur + ch, font=fnt) <= max_w:
            cur += ch
        elif ch in "，。！？、；：）" and cur:
            cur += ch
            lines.append(cur); cur = ""
        else:
            lines.append(cur); cur = ch
    if cur:
        lines.append(cur)
    return lines


def put_lines(d, lines, x, y, fnt, fill, lh):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def rounded(d, box, radius, fill, outline=None, width=1):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def base_square():
    img = gradient(800, 800)
    glow = Image.new("RGBA", (800, 800), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    g.ellipse((500, -180, 1000, 320), fill=(255, 255, 255, 46))
    g.ellipse((-180, 500, 300, 950), fill=(80, 200, 255, 40))
    img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(80)))
    d = ImageDraw.Draw(img)
    rounded(d, (34, 34, 766, 766), 40, (255, 255, 255, 246))
    return img, d


def logo(img, xy=(76, 74), size=76):
    im = Image.open(os.path.join(ROOT, "assets", "img", "logo.png")).convert("RGBA")
    im.thumbnail((size, size), Image.LANCZOS)
    img.alpha_composite(im, xy)


def brand(d, x=168, y=88):
    d.text((x, y), "极站 GOSITE", font=font(30, True), fill=INK)
    d.text((x, y + 38), "企业官网快上线服务", font=font(17), fill=MUTED)


def footer_line(d, y=710):
    d.line((76, y - 22, 724, y - 22), fill=(225, 234, 248), width=2)
    d.text((76, y), "极站 GOSITE  ·  企业官网包年", font=font(19), fill=MUTED)
    d.text((520, y), "399 元 / 年", font=font(20, True), fill=BLUE)


def make_main():
    img, d = base_square()
    logo(img); brand(d)
    d.text((76, 182), "企业官网包年", font=font(62, True), fill=INK)
    d.text((76, 268), "¥", font=font(44, True), fill=BLUE)
    d.text((118, 246), "399", font=font(108, True), fill=BLUE)
    d.text((372, 292), "/ 年", font=font(30, True), fill=MUTED)
    rounded(d, (76, 382, 724, 386), 2, (232, 240, 255))
    sub = wrap(d, "纯静态官网 · 最快当天上线 · 全年代运营维护更新", font(26), 640)
    y = put_lines(d, sub, 76, 410, font(26), INK, 40)
    tags = ["最快当天上线", "改稿当天发布", "设计满意再付款"]
    x = 76
    for t in tags:
        w = d.textlength(t, font=font(21, True)) + 34
        rounded(d, (x, y + 18, x + w, y + 62), 22, (235, 244, 255))
        d.text((x + 17, y + 26), t, font=font(21, True), fill=BLUE)
        x += w + 14
    d.text((76, 648), "399 元 / 年 · 仅限前 10 名且资料齐全", font=font(21, True), fill=PINK)
    footer_line(d)
    img.convert("RGB").save(os.path.join(OUT, "main.png"), "PNG", optimize=True)
    print("main.png")


def make_sub(idx, kicker, title, highlight, bullets, note):
    img, d = base_square()
    logo(img); brand(d)
    d.text((76, 178), "0%d" % idx, font=font(22, True), fill=PINK)
    d.text((128, 174), kicker, font=font(22, True), fill=BLUE)
    d.text((76, 224), title, font=font(46, True), fill=INK)
    d.text((76, 296), highlight, font=font(64, True), fill=BLUE)
    d.line((76, 392, 724, 392), fill=(225, 234, 248), width=2)
    y = 424
    for b in bullets:
        d.ellipse((78, y + 12, 92, y + 26), fill=BLUE)
        lines = wrap(d, b, font(24), 600)
        y = put_lines(d, lines, 108, y, font(24), INK, 36) + 16
    d.text((76, 650), note, font=font(20, True), fill=PINK)
    footer_line(d)
    img.convert("RGB").save(os.path.join(OUT, "sub-%02d.png" % idx), "PNG", optimize=True)
    print("sub-%02d.png" % idx)


def make_detail():
    W = 750
    H = 5600
    img = Image.new("RGBA", (W, H), (244, 249, 255, 255))
    d = ImageDraw.Draw(img)

    # 头图
    head = gradient(W, 720)
    img.alpha_composite(head, (0, 0))
    d = ImageDraw.Draw(img)
    logo(img, (52, 56), 82)
    d.text((150, 60), "极站 GOSITE", font=font(32, True), fill=WHITE)
    d.text((150, 102), "企业官网快上线服务", font=font(19), fill=(220, 232, 255))
    d.text((52, 190), "企业官网包年", font=font(64, True), fill=WHITE)
    d.text((52, 278), "¥ 399", font=font(104, True), fill=WHITE)
    d.text((370, 336), "/ 年", font=font(30, True), fill=(226, 236, 255))
    d.text((52, 420), "纯静态官网 · 最快当天上线 · 全年代运营维护更新", font=font(25), fill=(232, 240, 255))
    for i, t in enumerate(["最快当天上线", "改稿当天发布", "设计满意再付款"]):
        x = 52 + i * 225
        rounded(d, (x, 486, x + 208, 540), 26, (255, 255, 255, 235))
        d.text((x + 20, 499), t, font=font(20, True), fill=BLUE)
    d.text((52, 618), "399 元 / 年 · 仅限前 10 名且资料齐全", font=font(24, True), fill=(255, 226, 122))
    y = 720

    def section(eyebrow, title, y, subtitle=None):
        d.text((52, y), eyebrow, font=font(19, True), fill=BLUE)
        y += 34
        d.text((52, y), title, font=font(38, True), fill=INK)
        y += 58
        if subtitle:
            lines = wrap(d, subtitle, font(22), 640)
            y = put_lines(d, lines, 52, y, font(22), MUTED, 34) + 12
        return y + 10

    def card(y, title, lines_, accent=BLUE):
        wrapped_all = [wrap(d, line, font(22), 590) for line in lines_]
        total = sum(len(w) for w in wrapped_all)
        h = 92 + total * 34 + len(lines_) * 12
        rounded(d, (36, y, 714, y + h), 24, (255, 255, 255, 250))
        rounded(d, (36, y, 44, y + h), 6, accent)
        d.text((66, y + 26), title, font=font(28, True), fill=INK)
        yy = y + 78
        for wrapped in wrapped_all:
            d.ellipse((70, yy + 12, 82, yy + 24), fill=accent)
            yy = put_lines(d, wrapped, 96, yy, font(22), MUTED, 34) + 12
        return y + h + 24

    y = section("01 / 为什么需要", "官网不用等，也不用自己管", y + 46,
                "很多企业的官网卡在等开发、等服务器、等后台改一个字。极站把上线和后续维护打包成一项包年服务。")
    y = card(y, "常见困扰", [
        "定制开发排期长，官网迟迟上不了线",
        "上线后改一句文案也要找人、等排期",
        "后台、插件、数据库都要自己盯",
        "内容长期停更，客户看到的是旧信息",
    ], PINK)
    y = card(y, "极站的做法", [
        "纯静态官网，资料齐备最快当天上线",
        "改稿当天发布，不用自己进后台",
        "全年内容更新代运营，发需求即可",
        "没有数据库和后台入口，暴露面更小",
    ])

    y = section("02 / 服务包含", "399 元包年，包含这些", y + 30)
    y = card(y, "官网整站交付", [
        "首页 + 多个栏目独立页面，一次搭齐",
        "模板化视觉设计，PC / 手机自适应",
        "文字、图片、LOGO 等资料整理录入",
        "域名解析、HTTPS 与 CDN 静态托管协助",
    ])
    y = card(y, "上线后的维护", [
        "基础 SEO 结构：标题、描述、站点地图",
        "全年内容更新：改稿、加栏目、发资讯、活动页",
        "微信内打开与分享适配、官网二维码物料",
        "访问巡检、整站备份，随时可打包迁移",
    ], PINK)

    y = section("03 / 纯静态", "快、稳、轻，也更安全", y + 30)
    y = card(y, "四个特点", [
        "快：页面做好即可发布，不搭数据库和后台",
        "稳：静态文件配合 CDN 与 HTTPS，故障点少",
        "轻：首屏体积小，手机和微信里打开都快",
        "安全：无后台登录入口，少补丁少漏洞",
    ])

    y = section("04 / 上线流程", "五步，把官网交出去", y + 30)
    steps = ["需求沟通：说清行业、栏目与上线时间",
             "出首页设计稿：先看稿，满意再付款",
             "资料一次收齐：文字图片由我们整理录入",
             "制作并上线：移动端适配、解析与 HTTPS",
             "全年代运营：后续改稿加栏目，随时提需求"]
    for i, st in enumerate(steps, 1):
        rounded(d, (36, y, 714, y + 78), 18, (255, 255, 255, 250))
        d.text((60, y + 18), "0%d" % i, font=font(28, True), fill=BLUE)
        d.text((124, y + 22), st, font=font(22), fill=INK)
        y += 90
    y += 24

    y = section("05 / 价格与保障", "399 元 / 年，先看设计稿", y + 16)
    y = card(y, "价格说明", [
        "一口价 399 元 / 年：官网整站 + 全年维护更新",
        "399 元为限时价，仅限前 10 名且资料齐全的客户",
        "先看首页设计稿，满意后再付款",
        "域名、备案等第三方费用另计，方案阶段一次说清",
    ], PINK)

    y = section("06 / 常见问题", "下单前先把话说清楚", y + 30)
    y = card(y, "真的能当天上线吗？", [
        "资料齐备、栏目结构确认后，标准展示型官网最快当天可上线；资料较多或需额外页面时，方案阶段会说明时间。",
    ])
    y = card(y, "上线后想改内容怎么办？", [
        "把要改的文字、图片或新栏目发过来，我们改好即发布，一般改动当天完成。",
    ])
    y = card(y, "整站文件归谁？", [
        "纯静态文件可随时打包备份与迁移，不被平台绑定。",
    ])

    y = section("07 / 下单之后", "按流程开始，不用等", y + 30)
    y = card(y, "开始后你会经历", [
        "提供企业资料：简介、栏目文字、图片与 LOGO",
        "确认首页设计稿，满意后再进入制作",
        "官网上线后，全年改稿与更新按需提交",
        "整站文件可随时打包备份，归属清晰",
    ])

    rounded(d, (0, y, W, y + 150), 0, (10, 30, 74, 255))
    d.text((52, y + 36), "极站 GOSITE", font=font(32, True), fill=WHITE)
    d.text((52, y + 86), "企业官网包年 · 399 元 / 年 · 极站 GOSITE", font=font(20), fill=(180, 205, 245))
    y += 150

    out = os.path.join(OUT, "detail.png")
    img.crop((0, 0, W, y)).convert("RGB").save(out, "PNG", optimize=True)
    print("detail.png height", y)


if __name__ == "__main__":
    make_main()
    make_sub(1, "极速上线", "不用等排期", "最快当天上线",
             ["栏目和内容一次收齐，模板化设计加静态化产出",
              "资料齐备、结构确认后，官网最快当天可上线",
              "比定制开发省去大半等待时间"],
             "先看设计稿，满意再付款")
    make_sub(2, "技术架构", "轻快又省心", "纯静态更安全",
             ["没有数据库和后台登录入口，暴露面更小",
              "静态文件配合 CDN 与 HTTPS，访问稳定",
              "首屏体积小，手机与微信里打开都快",
              "整站是文件，可随时备份与迁移"],
             "少补丁、少漏洞，日常几乎不用运维")
    make_sub(3, "代运营维护", "上线只是开始", "全年有人管",
             ["文字、图片、栏目、活动页随时提需求",
              "改稿当天发布，不用自己研究后台",
              "资讯动态、联系方式、二维码同步更新",
              "访问巡检与整站备份一并接手"],
             "官网不会上线即停更")
    make_sub(4, "合作保障", "先看到再决定", "设计满意再付款",
             ["沟通需求后，先出首页视觉稿与栏目结构",
              "确认满意后再付款进入制作",
              "限前 10 名且资料齐全的客户",
              "第三方费用在方案阶段一次说清"],
             "399 元 / 年 · 官网整站 + 全年维护")
    make_detail()

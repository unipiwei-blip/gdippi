# -*- coding: utf-8 -*-
"""第五轮网站内容补丁：页脚 / 套餐顺序 / 小程序定价与样板 / 案例多端截图"""
import io
import os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools", "build_site.py")
s = io.open(P, encoding="utf-8").read()
log = []


def rep(old, new, tag):
    global s
    c = s.count(old)
    log.append((tag, c))
    if c:
        s = s.replace(old, new, 1)


# 1. 页脚快速导航去掉「首页」
rep("""    cols = "".join('<li><a href="%s">%s</a></li>' % (u, t) for t, u, _ in NAV)""",
    """    cols = "".join('<li><a href="%s">%s</a></li>' % (u, t) for t, u, k in NAV if k != "index")""",
    "页脚去首页")

# 2. 价格页三卡容器加 plan-grid（由 CSS order 把主推 399 放到中间）
rep("""<div class="grid g3">
<article class="card glass reveal" style="padding:32px 26px;border:1.5px solid rgba(26,107,255,.32)""",
    """<div class="grid g3 plan-grid">
<article class="card glass reveal" style="padding:32px 26px;border:1.5px solid rgba(26,107,255,.32)""",
    "套餐容器加 class")

# 3. 价格页小程序卡：9980 起 / 3980 续费
rep("""<span class="pill">%s 按需报价</span>""",
    """<span class="pill">%s 商城定价</span>""", "小程序卡标签")
rep("""<h3 class="h3" style="font-size:23px;margin-top:18px">微信商城小程序</h3>
<p style="color:var(--muted);font-size:13.5px;line-height:1.9;margin-top:14px">按功能范围与页面数量出方案：商品与订单、营销插件、会员门店、预约点餐、分销拼团等组件按需组合。</p>""",
    """<h3 class="h3" style="font-size:23px;margin-top:18px">微信商城小程序</h3>
<div class="price-big" style="color:var(--ink-2);margin-top:6px"><span class="cur">¥</span><span class="num" style="font-size:56px;background:linear-gradient(100deg,#e2157f,#7a4bff);-webkit-background-clip:text;background-clip:text;color:transparent">9980</span><span class="unit" style="color:var(--muted)">起 / 首年</span></div>
<p class="price-std">首年含设计与上线　·　次年续费 <b>¥3980 / 年</b></p>
<p style="color:var(--muted);font-size:13px;margin-top:14px">按功能范围与页面数量出方案：商品订单、营销插件、会员门店、预约点餐、分销拼团等组件按需组合。</p>""",
    "小程序卡定价")
rep("""        "咨询后出功能清单与明确报价",
    ]), icon("arrow", 15)))""",
    """        "次年续费 3980 元 / 年",
    ]), icon("arrow", 15)))""",
    "小程序卡清单")

# 4. 小程序页：标题单行、口径、CTA
rep("""<h2 class="h2">从餐饮到商城，<span class="blue">场景都能对上</span></h2>""",
    """<h2 class="h2 nowrap">从餐饮到商城，<span class="blue">场景都能对上</span></h2>""",
    "行业标题单行")
rep("""                                    "商城小程序按功能范围单独出方案报价，可与官网包年一起做。"),""",
    """                                    "商城小程序首年 9980 元起（含设计与上线），次年续费 3980 元；可与官网包年一起做。"),""",
    "交付方式口径")
rep("""                         "官网 399 元包年；商城小程序按功能范围另出方案。微信扫码聊清楚场景，我们给出可落地的组合建议。"))""",
    """                         "官网 399 元包年；商城小程序首年 9980 元起（含设计上线），次年续费 3980 元。微信扫码聊清楚场景，我们给出可落地的组合建议。"))""",
    "小程序页 CTA")

# 5. 小程序页新增「定价」与「商城界面样板」两个板块
NEW_MINI = '''    b.append(\'\'\'<section class="section tight"><div class="container">
%s
<div class="grid g2" style="margin-top:8px">
<div class="card glass reveal"><span class="pill pink">%s 首年</span>
<h3 class="h3" style="font-size:24px;margin-top:18px">9980 元起 · 含设计与上线</h3>
<p>按功能范围与页面数量确定最终报价。首年费用包含商城界面设计、组件配置、商品与栏目录入、提交上线，先把能卖货的版本跑起来。</p>
<div style="margin-top:16px">%s</div></div>
<div class="card glass reveal d1"><span class="pill">%s 次年起</span>
<h3 class="h3" style="font-size:24px;margin-top:18px">3980 元 / 年 · 续费维护</h3>
<p>后续每年续费 3980 元，覆盖技术维护、服务器与环境配置、问题排查与日常更新支持，商城不用自己养技术。</p>
<div style="margin-top:16px">%s</div></div>
</div>
<p style="font-size:12.5px;color:var(--muted);margin-top:18px;text-align:center">具体功能清单与报价以咨询确认的方案为准；第三方费用（微信认证、支付接口、短信等）另计。</p>
</div></section>\'\'\' % (sechead("PRICING / 商城小程序定价", '首年<span class="pink">9980 元起</span>，次年续费 3980 元',
                               "设计、上线、维护分开写清楚，方便按预算做决定。"),
                       icon("cart", 13), checklist([
                           "商城界面设计与首页装修", "功能组件配置与商品录入",
                           "服务器与环境配置、提交上线协助", "按功能范围确定最终报价",
                       ]), icon("refresh", 13), checklist([
                           "技术维护与问题排查", "服务器与环境持续支持",
                           "日常内容与商品更新支持", "按年续费，费用提前说明",
                       ])))

    mall_items = [
        ("mall-01.jpg", "商城首页", "首页装修 · 搜索 · 优惠券 · 分类入口"),
        ("mall-02.jpg", "商品分类", "左侧分类导航 + 右侧商品列表"),
        ("mall-03.jpg", "商品详情", "详情图文 · 价格 · 拼团 · 下单"),
        ("mall-04.jpg", "商品列表", "多规格商品与分类筛选"),
        ("mall-05.jpg", "服务商城", "服务类目 · 课程 · 推荐位"),
        ("mall-06.jpg", "分类页面", "服务型商城的分类与报价展示"),
    ]
    stack = "".join(\'<a class="ms-item" style="--i:%d" href="assets/mall/%s" target="_blank" rel="noopener"><img src="assets/mall/%s" alt="%s 界面样板" loading="lazy"></a>\' % (i, f, f, t)
                    for i, (f, t, _) in enumerate(mall_items))
    grid = "".join(\'<a class="mall-cell" href="assets/mall/%s" target="_blank" rel="noopener"><img src="assets/mall/%s" alt="%s 界面样板" loading="lazy"><h4>%s</h4><p>%s</p></a>\' % (f, f, t, t, d)
                   for f, t, d in mall_items)
    b.append(\'\'\'<section class="section tight"><div class="container">
%s
<div class="mall-stack reveal">%s</div>
<div class="mall-grid" style="margin-top:26px">%s</div>
<p style="font-size:12.5px;color:var(--muted);margin-top:18px;text-align:center">以上为常见小程序商城界面版式示意，用于展示可搭建的页面样式；点击任意图片可查看大图。</p>
</div></section>\'\'\' % (sechead("SHOWCASE / 商城界面样板", '商城长什么样，<span class="grad">先看这些版式</span>',
                               "首页、分类、列表、详情、服务型商城——不同行业的页面结构，都可以用组件搭出来。"), stack, grid))

'''
anchor = """    b.append(cta_section('官网 + 小程序，<span style="color:#ffe27a">一次说清需求</span>',"""
if anchor not in s:
    raise SystemExit("小程序 CTA 锚点未找到")
s = s.replace(anchor, NEW_MINI + anchor, 1)
log.append(("小程序定价+样板板块", 1))

# 6. 案例页新增 PC / 手机多端实拍
NEW_GALLERY = '''    galleries = [
        ("广东省湖南攸县商会", "case-shanghui", "商协会门户"),
        ("才猎天下大数据", "case-cailie", "教育实训"),
        ("湾区（广东）数字经济研究院", "case-baydea", "研究院 / 智库"),
    ]
    gal = []
    for gname, stem, gtag in galleries:
        shots = [(stem + ".png", "PC 首页", "wide"), (stem + "-pc2.jpg", "PC 内页", "wide"),
                 (stem + "-m1.jpg", "手机首页", "phone"), (stem + "-m2.jpg", "手机内页", "phone")]
        imgs = "".join(\'<a class="shot %s" href="assets/cases/%s" target="_blank" rel="noopener"><img src="assets/cases/%s" alt="%s %s" loading="lazy"><span>%s</span></a>\' % (cls, f, f, gname, label, label)
                       for f, label, cls in shots)
        gal.append(\'<div class="gallery-item glass reveal"><div class="gallery-head"><span class="pill">%s</span><h3 class="h3">%s</h3></div><div class="gallery-grid">%s</div></div>\' % (gtag, gname, imgs))
    b.append(\'\'\'<section class="section tight"><div class="container">
%s
%s
</div></section>\'\'\' % (sechead("SCREENS / 多端实拍", 'PC 与手机，<span class="grad">都经得起看</span>',
                               "每个案例都附 PC 端与手机端实拍截图，点击可查看原图，看看栏目在两种屏幕上怎么落地。"),
                       "".join(gal)))

'''
anchor2 = """    b.append(cta_section('你的官网，<span style="color:#ffe27a">也可以这样清楚</span>',"""
if anchor2 not in s:
    raise SystemExit("案例 CTA 锚点未找到")
s = s.replace(anchor2, NEW_GALLERY + anchor2, 1)
log.append(("案例多端截图", 1))

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
for tag, c in log:
    print(("OK  " if c else "MISS"), tag, c)

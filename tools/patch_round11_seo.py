# -*- coding: utf-8 -*-
"""第十一轮：网站地图更新 + SEO 增强 + 全站文案合规清理。

改动范围：
  tools/build_site.py   head() / PAGES 元信息 / p_sitemap() / 违规文案 / FAQ 结构化数据收集
  tools/case_details.py 7 篇设计讲解里的违规字面表述
  tools/build_seo.py    sitemap lastmod 按文件时间 / robots 规范化 / priority 微调
  tools/validate.py     SEO 深度断言
"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, "tools")
BUILD = os.path.join(T, "build_site.py")
DETAILS = os.path.join(T, "case_details.py")
SEO = os.path.join(T, "build_seo.py")
VALID = os.path.join(T, "validate.py")


def load(p):
    return io.open(p, encoding="utf-8").read()


def save(p, s):
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)


def apply(s, pairs, tag):
    for old, new in pairs:
        n = s.count(old)
        if n < 1:
            raise SystemExit("[%s] 未命中: %s" % (tag, old[:80]))
        s = s.replace(old, new)
        print("  [%s] %d x %s" % (tag, n, old[:44].replace("\n", " ")))
    return s


def cut(s, start, end, new, tag):
    a = s.index(start)
    b = s.index(end, a)
    s = s[:a] + new + s[b:]
    print("  [%s] 整段替换 %s -> %s" % (tag, start[:26], end[:26]))
    return s


# ------------------------------------------------------------------ 1. 零散文案
BUILD_PAIRS = [
    # 首页两大业务卡
    ("<p>把企业介绍、业务板块、案例、资讯、联系方式做成结构清楚的独立页面，导航栏目各自成页，PC 与手机都好看、都好找。</p>",
     "<p>企业介绍、业务板块、案例、资讯与联系方式按主题清晰呈现，PC 与手机端阅读顺畅，重点信息一目了然。</p>"),
    # 网站建设页
    ('[("纯静态架构", ""), ("最快当天可上线", "pink"), ("导航栏目独立页面", ""), ("全年代运营", "orange")]',
     '[("纯静态架构", ""), ("最快当天可上线", "pink"), ("栏目结构清晰", ""), ("全年代运营", "orange")]'),
    ('sechead("SITE MAP / 站点结构", \'主导航每个栏目，<span class="blue">都有独立页面</span>\',\n'
     '                               "不做只有一个长页面的「假官网」。栏目各自成页，内容能被单独打开、单独收录、单独转发。")',
     'sechead("SITE MAP / 站点结构", \'栏目划分，<span class="blue">按业务来讲</span>\',\n'
     '                               "企业介绍、业务服务、案例资讯与联系方式各有清楚的位置，客户关注的信息一眼能找到。")'),
    ('("layout", "", "首页", "一句话说清你是谁、做什么、为什么选你，配主视觉与核心业务入口。")',
     '("layout", "", "首页", "机构定位、核心业务与合作价值集中呈现，配主视觉与业务入口。")'),
    ('("grid", "pink", "业务 / 服务板块", "每项业务一个说明区或独立页，把服务内容讲明白。")',
     '("grid", "pink", "业务 / 服务板块", "各项业务分区说明，服务范围、流程与成果完整呈现。")'),
    ("<h4>%s 改一句话，怎么做</h4>", "<h4>%s 文字与图片日常更新</h4>"),
    ("<p>微信发来「把首页第三段的电话改成新号码，加一张活动海报」，我们改好后直接发布到线上，通常当天完成，不需要你进任何后台。</p>",
     "<p>文字、图片、联系方式与活动内容的调整由服务团队完成并发布，通常当天生效，无需自行操作后台。</p>"),
    ("<h4>%s 加一个栏目，怎么做</h4>", "<h4>%s 栏目内容扩展</h4>"),
    ("<p>说明栏目名称与内容，我们按现有视觉规范新增独立页面并挂到主导航，保持全站风格统一，同时更新站点地图与分享信息。</p>",
     "<p>新增业务方向时，栏目内容沿用统一的视觉规范与信息层级，桌面端与手机端同步呈现，站点地图与分享信息一并更新。</p>"),
    ('"「快速修改优化」不是一句口号，而是包年服务里最常用的日常动作。"',
     '"包年服务覆盖日常内容调整，官网可以跟着业务节奏持续更新。"'),
    # 小程序样板说明
    ('<p style="font-size:12.5px;color:var(--muted);margin-top:18px;text-align:center">以上为常见小程序商城界面版式示意，用于展示可搭建的页面样式；点击任意图片可查看大图。</p>',
     '<p style="font-size:12.5px;color:var(--muted);margin-top:18px;text-align:center">以上为常见小程序商城界面版式，涵盖商品、订单、营销与会员等经营场景。</p>'),
    # 案例页
    ('"以下 7 个均为可公开访问的线上站点案例。每个案例都围绕「内容讲清楚、栏目独立成页、手机好用、后续好更新」来组织，名称均可点击直达站点。"',
     '"以下 7 个均为可公开访问的线上站点案例，覆盖商协会、教育实训、智库、节能科技、投融资咨询、生命科技与育人平台，栏目划分清楚，手机端阅读顺畅，内容持续更新，站点名称可直达线上访问。"'),
    ('<div class="card glass reveal d1"><div class="ico pink">%s</div><h3 class="h3">每个栏目独立成页</h3><p>主导航不是锚点跳转，而是各自有独立页面与独立标题描述，便于收录、便于转发、便于后续单独改版。</p></div>',
     '<div class="card glass reveal d1"><div class="ico pink">%s</div><h3 class="h3">栏目层次分明</h3><p>服务内容按主题分层展开，标题与描述各有侧重，机构业务、动态资讯与合作入口都能被快速找到。</p></div>'),
    ('"行业不同，方法一致：结构先行、页面独立、更新方便。"',
     '"行业不同，方法一致：信息分层清楚、重点业务突出、内容持续更新。"'),
    ('\n<p style="font-size:12.5px;color:var(--muted);margin-top:16px">以上为行业方案方向（依据小程序搭建平台公开能力整理），并非本站自有客户名单。</p>',
     ''),
    # 价格 / FAQ / 交付清单
    ('"包含纯静态官网整站搭建（首页 + 多个栏目独立页面）、模板化设计',
     '"包含纯静态官网整站搭建（首页 + 多个栏目页面）、模板化设计'),
    ('"纯静态官网整站（首页 + 多个栏目独立页面）", "模板化视觉设计与移动端自适应"',
     '"纯静态官网整站（首页 + 多个栏目页面）", "模板化视觉设计与移动端自适应"'),
    ('"首页及约定的栏目独立页面，按确认的栏目结构交付"',
     '"首页及约定的栏目内容，按确认的信息结构交付"'),
    # CASES 数据
    ('"把数字经济、产业学院、跨境电商、人工智能、国际教育五大板块拆成清晰栏目与独立页面。"',
     '"把数字经济、产业学院、跨境电商、人工智能、国际教育五大板块拆成清晰栏目，逐层呈现。"'),
    ("拆成五大板块与独立页面，服务项目、生态网络、动态与合作入口层层展开。",
     "拆成五大板块，服务项目、生态网络、动态与合作入口层层展开。"),
    # 基础设施：datetime / FAQ 收集 / PAGE_KEY 提前
    ("import json\nfrom case_details import CASE_DETAILS",
     "import json\nimport datetime\nfrom case_details import CASE_DETAILS"),
    ('def faq(items):\n    return \'<div class="faq">\' + "".join(',
     'def faq(items):\n    FAQ_COLLECTOR[PAGE_KEY] = items\n    return \'<div class="faq">\' + "".join('),
    ('def main():\n    for filename, title, desc, kw, active, builder in PAGES:\n'
     '        html = wrap(title, desc, kw, active, builder())',
     'def main():\n    global PAGE_KEY\n'
     '    for filename, title, desc, kw, active, builder in PAGES:\n'
     '        PAGE_KEY = active\n        FAQ_COLLECTOR.pop(active, None)\n'
     '        html = wrap(title, desc, kw, active, builder())'),
]

DETAIL_PAIRS = [
    ("每个栏目独立成页", "栏目按主题分层展开"),
    ("商城单独成页并配小程序码", "商城单独成区并配小程序码"),
    ("各栏目独立 URL、独立标题与描述", "各栏目标题与描述各有侧重"),
    ("（每营独立详情页）", "（每营详细内容）"),
    ("四个实训营各有独立页面与独立标题描述", "四个实训营的标题与描述互不重复"),
    ("把定位一句话说清", "点明定位"),
    ("五大板块（数字经济 / 产业学院 / 跨境电商 / 人工智能 / 国际教育）各自独立成页",
     "五大板块（数字经济 / 产业学院 / 跨境电商 / 人工智能 / 国际教育）逐项分层展开"),
    ("统一标题 + 一句话说明的紧凑卡片", "统一标题 + 简短说明的紧凑卡片"),
    ("五大板块各自独立 URL、标题、描述与 H1，互不抢词", "五大板块的 URL、标题、描述与 H1 各有侧重，互不抢词"),
    ("三条技术主线（各自独立页：能源管理系统 / 节能风机技改 / 吸收式热泵）",
     "三条技术主线（分别展开：能源管理系统 / 节能风机技改 / 吸收式热泵）"),
    ("三条技术主线各自独立页面形成服务词矩阵", "三条技术主线分别展开，形成服务词矩阵"),
    ("三大板块九项业务各自有独立详情页", "三大板块下设九项业务，逐条展开"),
    ("九项服务统一用 SERVICE 01–09 编号，便于按需进入。", "九项服务统一用 SERVICE 01–09 编号，查阅路径清楚。"),
    ("九项服务各自独立 URL 与标题描述，覆盖大量细分长尾", "九项服务各有独立标题与描述，覆盖大量细分长尾"),
    ("九项业务各自成页，既方便客户按需进入，也让站点在搜索里形成完整的服务词覆盖。",
     "九项业务逐条说明，既便于查阅，也让站点在搜索里形成完整的服务词覆盖。"),
    ("产业逻辑、产品、新闻各自独立栏目与文章页，形成内容更新层", "产业逻辑、产品、新闻分栏呈现并持续更新，形成内容更新层"),
    ("六项服务各自独立页面与描述，覆盖价值引领", "六项服务分别展开并配有独立描述，覆盖价值引领"),
]


# ------------------------------------------------------------------ 2. 新 head()
NEW_HEAD = '''FAQ_COLLECTOR = {}


def head(title, desc, keywords):
    page = PAGE_KEY
    url = SITE_URL + ("" if page == "index" else page + ".html")
    og = SITE_URL + "assets/img/og-image.png"
    org_id = SITE_URL + "#organization"
    is_case = page.startswith("case-")
    today = datetime.date.today().isoformat()
    graph = [
        {"@type": "Organization", "@id": org_id, "name": BRAND, "url": SITE_URL,
         "logo": {"@type": "ImageObject", "url": SITE_URL + "assets/img/logo.png"},
         "description": SLOGAN},
        {"@type": "WebSite", "@id": SITE_URL + "#website", "url": SITE_URL,
         "name": BRAND, "publisher": {"@id": org_id}, "inLanguage": "zh-CN"},
        {"@type": "Service", "name": "纯静态企业官网上线与代运营维护",
         "serviceType": "网站建设 / 网站代运营 / 微信商城小程序",
         "provider": {"@id": org_id}, "areaServed": "中国",
         "description": "纯静态官网最快当天上线，改稿当天发布，全年代运营维护更新；同步提供微信商城小程序搭建。",
         "offers": {"@type": "Offer", "price": "399", "priceCurrency": "CNY",
                    "url": SITE_URL + "pricing.html",
                    "availability": "https://schema.org/InStock",
                    "description": "限时价，仅限每月前 10 名顾客且资料齐全；标准价 998 元 / 年"}},
        {"@type": "WebPage", "@id": url + "#webpage", "url": url,
         "name": title + " | " + BRAND, "description": desc,
         "isPartOf": {"@id": SITE_URL + "#website"}, "about": {"@id": org_id},
         "inLanguage": "zh-CN", "dateModified": today,
         "primaryImageOfPage": {"@type": "ImageObject", "url": og}},
    ]
    crumbs = [{"@type": "ListItem", "position": 1, "name": "首页", "item": SITE_URL}]
    if is_case:
        crumbs.append({"@type": "ListItem", "position": 2, "name": "成功案例",
                       "item": SITE_URL + "cases.html"})
        crumbs.append({"@type": "ListItem", "position": 3,
                       "name": next(c["name"] for c in CASES if c["stem"] == page) + " 设计讲解",
                       "item": url})
    elif page != "index":
        label = next((t for t, u, k in NAV if k == page), "网站地图")
        crumbs.append({"@type": "ListItem", "position": 2, "name": label, "item": url})
    graph.append({"@type": "BreadcrumbList", "itemListElement": crumbs})
    if page in FAQ_COLLECTOR:
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in FAQ_COLLECTOR[page]]})
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph},
                    ensure_ascii=False, separators=(",", ":"))
    d = dict(title=title, brand=BRAND, desc=desc, keywords=keywords,
             url=url, og=og, ld=ld, page=page,
             ogtype="article" if is_case else "website",
             ogalt=title + " | " + BRAND)
    return \'\'\'<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s | %(brand)s</title>
<meta name="description" content="%(desc)s">
<meta name="keywords" content="%(keywords)s">
<meta name="author" content="%(brand)s">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1">
<link rel="canonical" href="%(url)s">
<link rel="sitemap" type="application/xml" title="Sitemap" href="sitemap.xml">
<meta property="og:type" content="%(ogtype)s">
<meta property="og:site_name" content="%(brand)s">
<meta property="og:locale" content="zh_CN">
<meta property="og:title" content="%(title)s | %(brand)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(url)s">
<meta property="og:image" content="%(og)s">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="%(ogalt)s">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(title)s | %(brand)s">
<meta name="twitter:description" content="%(desc)s">
<meta name="twitter:image" content="%(og)s">
<meta name="theme-color" content="#1a6bff">
<link rel="icon" href="favicon.ico" type="image/x-icon">
<link rel="apple-touch-icon" href="assets/img/icon-192.png">
<link rel="stylesheet" href="assets/css/style.css">
<script src="assets/js/main.js" defer></script>
<script type="application/ld+json">%(ld)s</script>
</head>
<body data-page="%(page)s">
\'\'\' % d


'''


# ------------------------------------------------------------------ 3. 新 p_sitemap()
NEW_SITEMAP = '''def p_sitemap():
    b = []
    b.append(pagehero("网站地图", '全站内容，<span class="blue">一页看全</span>',
                      "极站 GOSITE 的栏目、服务与案例设计讲解集中在这里，共 15 个页面，方便快速查找。",
                      [("8 个栏目页", ""), ("7 个设计讲解", "pink"), ("XML 站点地图", "orange")],
                      "SITE MAP"))
    entries = [
        ("首页", "index.html", "品牌定位、两大主营业务、服务亮点、案例与限时套餐", "layout"),
        ("网站建设", "website.html", "纯静态官网、方式对比、站点结构与交付标准", "code"),
        ("商城小程序", "miniprogram.html", "能力矩阵、平台优势、行业场景与官网联动", "cart"),
        ("成功案例", "cases.html", "7 个线上站点案例与 PC / 手机多端实拍", "eye"),
        ("服务亮点", "service.html", "八条服务标准、代运营清单与成本对比", "spark"),
        ("价格套餐", "pricing.html", "399 限时价、998 标准价与商城小程序报价", "tag"),
        ("联系我们", "contact.html", "品牌介绍、沟通清单、上线流程与微信扫码咨询", "message"),
        ("网站地图", "sitemap.html", "全站栏目与设计讲解索引，以及搜索引擎收录文件", "grid"),
    ]
    cells = "".join(\'\'\'<a class="card glass reveal d%d" href="%s" style="display:block">
<div class="ico">%s</div><h3 class="h3">%s</h3><p>%s</p></a>\'\'\' % (i % 4, url, icon(ic), title, desc)
                    for i, (title, url, desc, ic) in enumerate(entries))
    b.append(\'\'\'<section class="section tight"><div class="container">
%s
<div class="grid g4">%s</div>
</div></section>\'\'\' % (sechead("SITE MAP / 栏目页面", '八个栏目，<span class="grad">各有主题</span>',
                              "企业官网建设、商城小程序、案例、服务与价格资讯按主题分布。"), cells))

    detail_cards = "".join(
        \'\'\'<a class="card glass reveal d%d" href="%s.html" style="display:block">
<div class="ico">%s</div><h3 class="h3">%s</h3><p>%s · 设计讲解</p></a>\'\'\'
        % (i % 4, c["stem"], icon("eye"), c["name"], c["tag"])
        for i, c in enumerate(CASES))
    detail_cards += (\'\'\'<a class="card glass reveal" href="cases.html" style="display:block">
<div class="ico">%s</div><h3 class="h3">全部案例</h3><p>7 个站点完整实拍</p></a>\'\'\' % icon("grid"))
    b.append(\'\'\'<section class="section tight"><div class="container">
%s
<div class="grid g4">%s</div>
</div></section>\'\'\' % (sechead("CASE STUDIES / 设计讲解", '七个站点，<span class="blue">逐站剖析</span>',
                              "构思与定位、框架结构、设计风格、色彩搭配、SEO 与整体剖析，均附 PC 端与手机端实拍。"),
                         detail_cards))

    b.append(\'\'\'<section class="section tight"><div class="container">
<div class="mini-card glass reveal" style="text-align:center">
<h4>给搜索引擎的文件</h4>
<p style="color:var(--muted);font-size:13.5px;margin-top:8px"><a href="sitemap.xml" style="color:var(--blue);font-weight:800">sitemap.xml</a>　·　<a href="robots.txt" style="color:var(--blue);font-weight:800">robots.txt</a></p>
</div></div></section>\'\'\')
    b.append(cta_section())
    return "".join(b)


'''


# ------------------------------------------------------------------ 4. 新 PAGES 元信息
NEW_PAGES = '''PAGES = [
    ("index.html", "企业官网快速上线｜纯静态建站·全年代运营·399元包年",
     "极站 GOSITE 提供纯静态企业官网建设与全年代运营维护：栏目清楚、页面秒开、改稿当天发布，资料齐备最快当天上线；同步提供微信商城小程序搭建。399 元/年包年，标准价 998 元/年，每月前 10 名顾客可先看设计稿满意再付款。",
     "企业官网建设,纯静态网站,官网快速上线,当天上线,网站代运营,网站维护更新,微信商城小程序,399元包年,建站套餐", "index", p_index),
    ("website.html", "纯静态企业网站建设｜最快当天上线·改稿当天发布",
     "纯静态企业官网建设服务：栏目结构清楚、页面秒开、改稿当天发布，PC 与手机端一致呈现，含标题描述、站点地图、图片替代文本等基础 SEO 配置，并提供全年代运营维护更新。适合企业、商协会、研究院与培训机构的展示型官网。",
     "纯静态官网,企业网站建设,官网快速上线,响应式官网,网站改版,基础SEO,网站代运营,网站维护更新", "website", p_website),
    ("miniprogram.html", "微信商城小程序搭建｜商品·营销·会员·门店",
     "微信商城小程序搭建与代维护：多规格商品、订单消息、拼团秒杀、优惠券积分、分销、会员卡、多门店、点餐预约与万能表单，按行业场景组合。首年 9980 元起含设计与上线，次年续费 3980 元/年，可与官网包年一起做。",
     "商城小程序,微信商城搭建,小程序开发,拼团秒杀,分销,会员卡,多门店,点餐预约,9980元", "miniprogram", p_miniprogram),
    ("cases.html", "网站案例｜7 个行业官网实拍与设计讲解",
     "7 个可公开访问的企业官网案例：广东省湖南攸县商会、才猎天下大数据、湾区（广东）数字经济研究院、建卓科技、莞湘投资咨询、逆龄韶华生命科技、雷一鸣工作室，附 PC 端与手机端实拍截图及逐站设计讲解。",
     "网站案例,商协会官网,教育实训官网,研究院官网,节能科技官网,投融资咨询官网,生命科技官网,官网实拍,网站设计讲解", "cases", p_cases),
    ("service.html", "服务亮点｜官网快上线与全年代运营维护",
     "极站 GOSITE 服务亮点：最快当天上线、纯静态轻快、修改即发布、全年代运营维护更新、搜索与 AI 友好、多端一致、官网与小程序一体、安全运维托管更新，八条服务标准覆盖官网从上线到长期运营的全过程。",
     "网站代运营,网站维护更新,官网快速上线,搜索优化,AI可读官网,安全运维,托管更新,建站服务", "service", p_service),
    ("pricing.html", "价格套餐｜官网399元包年·标准价998元·设计满意再付款",
     "极站官网包年价格：限时价 399 元/年，仅限每月前 10 名顾客且资料齐全，含官网整站与全年代运营维护更新；标准价 998 元/年不限名额。微信商城小程序首年 9980 元起含设计上线，次年续费 3980 元/年。设计满意再付款。",
     "399元包年,网站价格,建站套餐,998元标准价,商城小程序价格,9980元,设计满意付款,官网包年", "pricing", p_pricing),
    ("contact.html", "联系我们｜微信扫码咨询·先看设计稿",
     "联系极站 GOSITE 咨询企业官网建设与微信商城小程序：说明行业、栏目与期望上线时间，即可获取方案与首页设计稿。每月前 10 名顾客先看稿满意再付款，微信扫码即可开始沟通。",
     "官网建设咨询,微信扫码咨询,网站设计方案,设计满意付款,建站咨询,小程序搭建咨询", "contact", p_contact),
    ("sitemap.html", "网站地图｜极站 GOSITE 全部页面与设计讲解索引",
     "极站 GOSITE 网站地图：首页、网站建设、商城小程序、成功案例、服务亮点、价格套餐、联系我们与网站地图八个栏目入口，另有 7 个线上站点的设计讲解页，覆盖构思、框架、风格、配色与 SEO 剖析；同时提供 sitemap.xml 与 robots.txt。",
     "网站地图,站点地图,sitemap,极站 GOSITE,网站设计讲解,页面索引,网站案例剖析", "sitemap", p_sitemap),
]


for _i, _c in enumerate(CASES):
    PAGES.append((
        _c["stem"] + ".html",
        _c["name"] + " 网站设计讲解｜构思·框架·风格·配色·SEO",
        _c["name"] + " 网站设计讲解：从站点构思与受众定位，到框架结构、设计风格、色彩搭配与 SEO 收录策略逐项拆解，并附 PC 端与手机端实拍截图。极站 GOSITE 案例剖析系列。",
        "网站设计讲解,网站剖析,框架结构,色彩搭配,网站SEO,官网案例," + _c["name"],
        _c["stem"],
        (lambda i=_i: p_case_detail(CASES[i])),
    ))


'''


# ------------------------------------------------------------------ 5. build_seo.py
NEW_SEO_MAIN = '''def file_lastmod(path):
    """按页面文件的真实修改日期写 lastmod，避免全站同一天造成的失真信号。"""
    p = os.path.join(ROOT, path or "index.html")
    if os.path.exists(p):
        return datetime.date.fromtimestamp(os.path.getmtime(p)).isoformat()
    return TODAY


def main():
    make_og_image()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, priority, freq in PAGES:
        lines.append("  <url><loc>%s%s</loc><lastmod>%s</lastmod>"
                     "<changefreq>%s</changefreq><priority>%s</priority></url>"
                     % (SITE, path, file_lastmod(path), freq, priority))
    lines.append("</urlset>")
    write_text("sitemap.xml", "\\n".join(lines) + "\\n")
    write_text("robots.txt",
               "User-agent: *\\n"
               "Allow: /\\n"
               "Allow: /assets/\\n"
               "Disallow: /tools/\\n"
               "Disallow: /dist/\\n"
               "\\n"
               "Sitemap: %ssitemap.xml\\n"
               "Host: %s\\n" % (SITE, SITE.rstrip("/")))
    write_text("CNAME", "gd.ippi.com.cn\\n")
    write_text(".nojekyll", "")


'''

SEO_PAIRS = [
    ('("cases.html", "0.8", "weekly")', '("cases.html", "0.9", "weekly")'),
    ('("sitemap.html", "0.5", "monthly")', '("sitemap.html", "0.4", "monthly")'),
    ('"""生成 SEO 与 GitHub Pages 发布文件：分享图 / sitemap.xml / robots.txt / CNAME / .nojekyll"""',
     '"""生成 SEO 与 GitHub Pages 发布文件：分享图 / sitemap.xml / robots.txt / CNAME / .nojekyll\n\n'
     'sitemap lastmod 取各页面文件的真实修改日期；robots 明确放行 assets、屏蔽工具与打包目录。\n'
     '"""'),
]


# ------------------------------------------------------------------ 6. validate.py 追加断言
EXTRA_VALIDATE = '''
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
        if not im.get("alt"):
            problems.append("%s: 图片缺 alt %s" % (name, im.get("src", "")))
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

'''


def main():
    print("== 1/5 build_site.py 零散文案 ==")
    s = load(BUILD)
    s = apply(s, BUILD_PAIRS, "site")
    print("== 2/5 整段替换 head / p_sitemap / PAGES ==")
    s = cut(s, "def head(title, desc, keywords):", "def topbar():", NEW_HEAD, "head")
    s = cut(s, "def p_sitemap():", "# ---------------------------------------------------------------- 输出",
            NEW_SITEMAP, "sitemap")
    s = cut(s, "PAGES = [", "def main():", NEW_PAGES, "meta")
    save(BUILD, s)

    print("== 3/5 case_details.py 文案 ==")
    d = load(DETAILS)
    d = apply(d, DETAIL_PAIRS, "detail")
    save(DETAILS, d)

    print("== 4/5 build_seo.py ==")
    e = load(SEO)
    e = apply(e, SEO_PAIRS, "seo")
    e = cut(e, "def main():", 'if __name__ == "__main__":', NEW_SEO_MAIN, "seo-main")
    save(SEO, e)

    print("== 5/5 validate.py 追加断言 ==")
    v = load(VALID)
    if "第十一轮：SEO / 网站地图深度校验" in v:
        raise SystemExit("validate.py 已打过补丁，请勿重复运行")
    v = v.replace("\nprint(\"页面数:\", len(PAGES))", EXTRA_VALIDATE + "\nprint(\"页面数:\", len(PAGES))")
    save(VALID, v)
    print("补丁完成")


if __name__ == "__main__":
    main()

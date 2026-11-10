# -*- coding: utf-8 -*-
"""第七轮：案例扩为 7 个（统一数据源 CASES），同步首页预览 / 案例页 / 友情链接 / 站点地图"""
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


# 1. 统一案例数据源
CASES = '''CASES = [
    {
        "stem": "case-shanghui", "name": "广东省湖南攸县商会", "url": "https://www.zyyous.com/",
        "tag": "商协会门户", "gtag": "商协会门户",
        "points": ["商会简介", "六大服务体系", "商会动态", "大攸商商城", "多二维码触点"],
        "short": "以「抱团取暖 · 共谋发展」为主视觉，把简介、服务体系、动态资讯与线上商城入口分层呈现。",
        "desc": "成立于 2013 年的异地商会门户。首页用「抱团取暖 · 共谋发展」立住主旨，向下依次是数据成绩、商会简介、六大服务体系、动态资讯、官方线上商城与多触点二维码。",
    },
    {
        "stem": "case-cailie", "name": "才猎天下大数据", "url": "https://www.91cailie.com/",
        "tag": "教育实训 / 转化型官网", "gtag": "教育实训",
        "points": ["四大实训营", "核心优势", "学员故事", "常见问题", "试学预约"],
        "short": "围绕课程矩阵搭建转化型首页：数据成绩、课程卡片、优势说明与咨询二维码层层递进。",
        "desc": "2008 年创立于深圳的 AI 人才实训基地。站点以四大实训营卡片为主线，配合就业数据、核心优势、学员故事与 FAQ，最终落到试学预约与咨询二维码。",
    },
    {
        "stem": "case-baydea", "name": "湾区（广东）数字经济研究院", "url": "https://www.baydea.com/",
        "tag": "研究院 / 智库", "gtag": "研究院 / 智库",
        "points": ["五大业务板块", "服务项目", "生态网络", "研究院动态", "合作洽谈"],
        "short": "把数字经济、产业学院、跨境电商、人工智能、国际教育五大板块拆成清晰栏目与独立页面。",
        "desc": "面向政校企的数字经济研究院。把数字经济、产业学院、跨境电商、人工智能、国际教育拆成五大板块与独立页面，服务项目、生态网络、动态与合作入口层层展开。",
    },
    {
        "stem": "case-jianzhuo", "name": "建卓科技", "url": "https://www.dgjzkj.com/",
        "tag": "综合节能服务", "gtag": "节能科技",
        "points": ["节能减排", "能源管理系统", "节能风机技改", "吸收式热泵", "项目案例"],
        "short": "以「节能降碳、降本增效」为主旨，把一体服务链、六步流程与三条技术主线拆成清晰栏目。",
        "desc": "面向企业用能场景的综合节能服务商。首页以「节能降碳、降本增效」立住主旨，依次展开节能数据、企业定位、六步服务流程、三条技术主线（能源管理系统 / 节能风机技改 / 吸收式热泵）、项目案例与常见问题。",
    },
    {
        "stem": "case-guanxiang", "name": "莞湘投资咨询", "url": "https://www.touzs.com/",
        "tag": "投融资咨询", "gtag": "投融资咨询",
        "points": ["三大板块", "九项业务", "六步闭环", "客户反馈", "合规说明"],
        "short": "把三大板块、九项标准化业务与六步服务流程做成结构化页面，信息密度高但不乱。",
        "desc": "立足东莞的投融资咨询服务机构。站点以「让每一笔资金都找到最优路径」开篇，把个人融资、企业融资、投资咨询三大板块与九项标准化业务逐项展开，配六步服务闭环、客户反馈与合规 FAQ。",
    },
    {
        "stem": "case-niling", "name": "逆龄韶华生命科技", "url": "https://www.365ls.cn/",
        "tag": "生命科技 / 健康产业", "gtag": "生命科技",
        "points": ["负熵科学", "四层产业逻辑", "负熵小米", "发展脉络", "新闻资讯"],
        "short": "从科学底座、产业逻辑到核心主食产品与品牌动态，用清晰层级讲清一个新品类。",
        "desc": "以负熵科学为理论底座的生命科技企业。首页用「以负熵重构生命秩序」立题，向下依次是科学底座、六条竞争优势、四层产业逻辑链、核心产品负熵小米、发展脉络、新闻资讯与合作入口。",
    },
    {
        "stem": "case-leiyiming", "name": "雷一鸣工作室", "url": "https://www.oals.cn/",
        "tag": "教育 / 育人平台", "gtag": "教育工作室",
        "points": ["三育人模式", "六项服务", "五步育人路径", "主理人", "工作室实景"],
        "short": "以「立德树人 · 陪伴成长」为主旨，把育人特色、服务方向、路径与工作室实景分层呈现。",
        "desc": "以大学生思想政治教育为核心的综合性育人平台。站点围绕「立德树人 · 陪伴成长」，展开平台概览、六条育人特色、两类服务方向、五步育人路径、六项服务体系、主理人介绍与工作室实景。",
    },
]

'''
rep('SITE_URL = "https://gd.ippi.com.cn/"\n', 'SITE_URL = "https://gd.ippi.com.cn/"\n' + CASES, "案例数据源")

# 2. 页脚友情链接跟随 CASES
rep('''    friends = [
        ("广东省湖南攸县商会", "https://www.zyyous.com/"),
        ("才猎天下大数据", "https://www.91cailie.com/"),
        ("湾区（广东）数字经济研究院", "https://www.baydea.com/"),
    ]
    friend_links = "".join('<a href="%s" target="_blank" rel="noopener">%s</a>' % (u, t) for t, u in friends)''',
'''    friend_links = "".join('<a href="%s" target="_blank" rel="noopener">%s</a>' % (c["url"], c["name"])
                            for c in CASES)''', "页脚友情链接")

# 3. 首页案例区：6 张精选卡 + 查看全部 7 个
NEW_HOME = '''    b.append(\'\'\'<section class="section tight"><div class="container">
<div class="sec-head row reveal"><div><div class="eyebrow">SELECTED WORK / 真实案例</div>
<h2 class="h2">七个不同行业，<span class="blue">同一套快上线方法</span></h2>
<p class="lead">商协会、教育实训、研究院智库、节能科技、投融资咨询、生命科技与育人工作室，栏目结构各不相同，但都做到了内容清楚、手机好用、后续更新方便。</p></div>
<a class="btn btn-ghost" href="cases.html">%s 查看全部 7 个案例</a></div>
<div class="grid g3">
%s
</div></div></section>\'\'\' % (icon("arrow", 15),
        "".join(case_card(c["stem"], c["name"], c["url"], c["tag"], c["points"], c["short"], "%02d" % i)
                for i, c in enumerate(CASES[:6], 1))))
'''
start = s.index('''    b.append(\'\'\'<section class="section tight"><div class="container">
<div class="sec-head row reveal">''')
end = s.index('"03")))\n', start) + len('"03")))\n')
s = s[:start] + NEW_HOME + s[end:]
log.append(("首页案例区", 1))

# 4. 案例页头部与卡片区
rep('''    b.append(pagehero("成功案例", '三种行业，<span class="blue">同一套上线方法</span>',
                      "以下为可公开访问的线上站点案例。每个案例都围绕「内容讲清楚、栏目独立成页、手机好用、后续好更新」来组织。",
                      [("商协会门户", ""), ("教育实训", "pink"), ("研究院智库", ""), ("可点击访问", "orange")],
                      "SELECTED WORK"))''',
'''    b.append(pagehero("成功案例", '七类机构，<span class="blue">同一套上线方法</span>',
                      "以下 7 个均为可公开访问的线上站点案例。每个案例都围绕「内容讲清楚、栏目独立成页、手机好用、后续好更新」来组织，名称均可点击直达站点。",
                      [("7 个线上案例", ""), ("PC / 手机实拍", "pink"), ("可点击访问", "orange")],
                      "SELECTED WORK"))''', "案例页头部")

NEW_CARDS = '''    b.append(\'\'\'<section class="section tight"><div class="container">
<div class="case-index">%s</div>
<div class="grid g3">
%s
</div></div></section>\'\'\' % (
        "".join(\'<a class="pill" href="%s" target="_blank" rel="noopener">%s &nearr;</a>\' % (c["url"], c["name"])
                for c in CASES),
        "".join(case_card(c["stem"], c["name"], c["url"], c["tag"], c["points"], c["desc"], "%02d" % i)
                for i, c in enumerate(CASES, 1))))
'''
start = s.index('''    b.append(\'\'\'<section class="section tight"><div class="container"><div class="grid g3">''')
end = s.index('"03")))\n', start) + len('"03")))\n')
s = s[:start] + NEW_CARDS + s[end:]
log.append(("案例页卡片区", 1))

# 5. 共性总结文案
rep('''sechead("METHOD / 案例里的共同点", '不是三套设计，<span class="grad">是三个行业的内容结构</span>',''',
'''sechead("METHOD / 案例里的共同点", '不是七套设计，<span class="grad">是同一套内容结构</span>',''',
    "共性标题")
rep("商会的六大服务体系、研究院的五大板块、培训机构的四大课程，都先拆成清晰的信息骨架，再落到视觉设计。",
    "商会的六大服务体系、研究院的五大板块、节能企业的一体服务链、咨询公司的九项业务，都先拆成清晰的信息骨架，再落到视觉设计。",
    "共性卡片")

# 6. 多端实拍跟随 CASES
rep('''    galleries = [
        ("广东省湖南攸县商会", "case-shanghui", "商协会门户"),
        ("才猎天下大数据", "case-cailie", "教育实训"),
        ("湾区（广东）数字经济研究院", "case-baydea", "研究院 / 智库"),
    ]''',
'''    galleries = [(c["name"], c["stem"], c["gtag"]) for c in CASES]''', "多端实拍数据")
rep('"每个案例都附 PC 端与手机端实拍截图，点击可查看原图，看看栏目在两种屏幕上怎么落地。"',
    '"7 个案例，每个都附 PC 端与手机端实拍截图，点击可查看原图，看看栏目在两种屏幕上怎么落地。"',
    "多端实拍导语")

# 7. 站点地图页描述
rep('("成功案例", "cases.html", "商会 / 教育实训 / 研究院三个线上站点案例", "eye"),',
    '("成功案例", "cases.html", "7 个线上站点案例与 PC / 手机多端实拍", "eye"),', "站点地图条目")

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
for tag, c in log:
    print(("OK  " if c else "MISS"), tag, c)

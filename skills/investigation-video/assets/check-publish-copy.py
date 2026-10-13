#!/usr/bin/env python3
"""校验 八平台发布文案-v<N>.md 是否符合固定模板（2026-09-15 定版）。
用法: check-publish-copy.py <文案.md>
检查：顶部"对应："与"共用免责段"块；八个平台顺序固定为 抖音、快手、B站、视频号、小红书（弱化品牌名）、YouTube、知乎、公众号；
每个平台含 主推标题/备选标题/正文/（共用免责段）；标题字数硬限制（含标点）：小红书≤20，抖音/快手/视频号/公众号≤30，B站/YouTube/知乎≤40；顶部须有"标题公式（dbs-xhs-title）："行；B站与 YouTube 含"章节："；B站含"本期结构："；抖音/快手/B站/视频号/小红书含"置顶评论："；公众号含"摘要："。
"""
import sys,re
from title_symbols import VIDEO_CHANNEL_SYMBOLS, VIDEO_CHANNEL_SEQUENCES, invalid_title_characters
raytalk = '--raytalk' in sys.argv
args = [a for a in sys.argv[1:] if a != '--raytalk']
if not args or args[0] in ('-h','--help'):print('用法: python3 check-publish-copy.py [--raytalk] <发布文案.md>（--raytalk 检查当前四平台）');sys.exit(2)
s=open(args[0],encoding='utf-8-sig').read();bad=[];warn=[]
# RayTalk current four-platform mode; default mode remains compatible with historical packages.
if raytalk:
    current_order=['抖音','哔哩哔哩','小红书','微信视频号']
    current_heads=re.findall(r'^## (.+)$',s,re.M)
    if current_heads!=current_order: bad.append(f'当前只交四平台，顺序应为{current_order}，实际{current_heads}')
    if not re.search(r'^对应：',s,re.M): bad.append('缺顶部对应版本说明')
    if not re.search(r'^标题策略：',s,re.M): bad.append('缺标题策略记录（数字/关键词/情绪点与平台钩子）')
    sections=re.split(r'^## .+$',s,flags=re.M)[1:]
    limits={'抖音':30,'哔哩哔哩':40,'小红书':20,'微信视频号':16}
    for name,body in zip(current_heads,sections):
        for field in ('主推标题','备选标题'):
            m=re.search(r'^'+field+r'：([^\n]+)',body,re.M)
            if not m or not m.group(1).strip(): bad.append(f'{name}缺{field}')
            else:
                title=m.group(1).strip()
                if '<' in title or '>' in title: bad.append(f'{name}{field}仍为模板')
                if name in limits and len(title)>limits[name]: bad.append(f'{name}{field}超过{limits[name]}字')
                if name=='小红书' and 'raytalk' in title.lower(): bad.append('小红书标题不写品牌名')
                if name=='微信视频号':
                    invalid=invalid_title_characters(title,VIDEO_CHANNEL_SYMBOLS,VIDEO_CHANNEL_SEQUENCES)
                    if invalid: bad.append(f'{name}{field}含不支持的特殊字符{invalid!r}；逗号请改为空格')
        m=re.search(r'^正文：(.*)',body,re.M|re.S)
        if not m or not m.group(1).strip(): bad.append(f'{name}缺正文')
        elif re.search(r'<[^>]+>',m.group(1)): bad.append(f'{name}正文含未填写模板')
    print('COPY_OK' if not bad else 'COPY_FAIL\n  '+'\n  '.join(bad))
    sys.exit(1 if bad else 0)
if not re.search(r'^对应：',s,re.M): bad.append('缺顶部"对应："说明块')
if '共用免责段（各平台正文末尾）' not in s: bad.append('缺顶部"共用免责段（各平台正文末尾）"')
if '标题公式（dbs-xhs-title）：' not in s: bad.append('缺顶部"标题公式（dbs-xhs-title）："行，标题必须先过 /dbs-xhs-title 公式')
order=['抖音','快手','B站','视频号','小红书（弱化品牌名）','YouTube','知乎','公众号']
heads=re.findall(r'^## (.+)$',s,re.M)
# 公众号与微信公众号是同一平台，保留历史稿件兼容。
heads=['公众号' if h=='微信公众号' else h for h in heads]
if heads!=order: bad.append(f'平台顺序/集合不对: {heads}')
secs=re.split(r'^## .+$',s,flags=re.M)[1:]
for name,body in zip(heads,secs):
    for f in ['主推标题：','备选标题：']:
        if f not in body: bad.append(f'{name} 缺 {f}')
    if name!='公众号':
        if '正文：' not in body: bad.append(f'{name} 缺 正文：')
        if '（共用免责段）' not in body: bad.append(f'{name} 缺 （共用免责段）')
    if name in ['B站','YouTube'] and '章节：' not in body: bad.append(f'{name} 缺 章节：')
    if name=='B站' and '本期结构：' not in body: bad.append('B站 缺 本期结构：')
    if name in ['抖音','快手','B站','视频号','小红书（弱化品牌名）'] and '置顶评论：' not in body: bad.append(f'{name} 缺 置顶评论：')
    if name=='公众号' and '摘要：' not in body: bad.append('公众号 缺 摘要：')
    for m in re.finditer(r'(主推标题|备选标题)：(.+)',body):
        L=len(m.group(2).strip())
        lim={'抖音':30,'快手':30,'视频号':30,'小红书（弱化品牌名）':20,'公众号':30,'B站':40,'YouTube':40,'知乎':40}[name]
        if L>lim: bad.append(f'{name} {m.group(1)} {L}字 > {lim}（硬限制，含标点）')
print('COPY_OK' if not bad else 'COPY_FAIL\n  '+'\n  '.join(bad))
if warn: print('标题超长提示:\n  '+'\n  '.join(warn))
sys.exit(1 if bad else 0)

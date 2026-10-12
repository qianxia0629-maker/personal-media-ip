import sys
import re,json
from pathlib import Path
KB=Path(sys.argv[1])  # 口播稿 markdown 路径
t=KB.read_text()
items=[];chapter='';ctitle=''
for line in t.split('\n'):
    h=re.match(r'^##\s+(.+?)｜(.+)$',line.strip())
    if h: ctitle=h.group(1); chapter=ctitle; srcs=h.group(2); continue
    m=re.match(r'^\[(s\d+[a-z]?)\]\s*(.+)$',line.strip())
    if not m: continue
    sid,txt=m.group(1),m.group(2).strip()
    tts=txt.replace('〇','零').replace('GB','G B').replace('CEO','C E O')
    items.append({'id':sid,'text':txt,'tts':tts,'chapter':chapter,'chapterTitle':ctitle,'sources':srcs})
json.dump(items,open(Path(__file__).parent/'sentences.json','w'),ensure_ascii=False,indent=1)
n=sum(len(re.sub(r'\s','',i['text'])) for i in items)
print(f"{len(items)} 句，{n} 字，预计 {n*0.156/60:.1f} 分钟")

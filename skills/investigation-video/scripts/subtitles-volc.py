# 字幕对齐：优先用火山 TTS 返回的字级时间戳(audio-manifest 里每句的 words)，没有 words 的句子回退到 asr/<id>.json(whisper)。
# 用法: python3 subtitles-volc.py [manifest.json]   默认 audio-manifest-s20.json；输出 renderer/subtitles.json、subtitles.srt、alignment-audit.json
from pathlib import Path
import json,re,sys
p=Path(__file__).parent
t=json.loads((p/'renderer/timeline.json').read_text())
manifest={x['id']:x for x in json.loads((p/(sys.argv[1] if len(sys.argv)>1 else 'audio-manifest-s20.json')).read_text())}
normal=lambda s: ''.join(c.lower() for c in s if c.isalnum())
def char_times_from_words(words):
 # 每个 word 条目可含多个字符(如"底，"), 按字符均分区间; 标点不计入 normal 字符
 aa=[];at=[]
 for w in words:
  cc=normal(w['word']);n=len(cc)
  for k,c in enumerate(cc):aa.append(c);at.append((w['startTime']+(w['endTime']-w['startTime'])*k/n,w['startTime']+(w['endTime']-w['startTime'])*(k+1)/n))
 return aa,at
subs=[];audit=[]
for x in t['scenes']:
 words=manifest.get(x['id'],{}).get('words') or []
 src='volc'
 if not words:
  r=json.loads((p/'asr'/f"{x['id']}.json").read_text());src='whisper'
  words=[w for seg in r['segments'] for w in seg.get('words',[])];words=[dict(word=w['word'],startTime=w['start'],endTime=w['end']) for w in words]
 aa,at=char_times_from_words(words)
 a=normal(x['text']);b=''.join(aa);n,m=len(a),len(b)
 dp=[[0]*(m+1) for _ in range(n+1)]
 for i in range(n+1):dp[i][0]=i
 for j in range(m+1):dp[0][j]=j
 for i in range(1,n+1):
  for j in range(1,m+1):dp[i][j]=min(dp[i-1][j]+1,dp[i][j-1]+1,dp[i-1][j-1]+(a[i-1]!=b[j-1]))
 mapped={};i,j=n,m
 while i or j:
  if i and j and dp[i][j]==dp[i-1][j-1]+(a[i-1]!=b[j-1]):mapped[i-1]=at[j-1];i-=1;j-=1
  elif i and dp[i][j]==dp[i-1][j]+1:i-=1
  else:j-=1
 for i in range(n):
  if i in mapped:continue
  lo=max([k for k in mapped if k<i],default=-1);hi=min([k for k in mapped if k>i],default=n)
  start=mapped[lo][1] if lo>=0 else .04;end=mapped[hi][0] if hi<n else x['duration']-.15
  dt=(end-start)/(hi-lo);mapped[i]=(start+dt*(i-lo-1),start+dt*(i-lo))
 raw=re.findall(r'[^，。？！：；、]+[，。？！：；、]?',x['text']);groups=[];acc=''
 for cl in raw:
  if acc and len(normal(acc+cl))>22:groups.append(acc);acc=''
  acc+=cl
  if cl[-1] in '。？！' or len(normal(acc))>=17:groups.append(acc);acc=''
 if acc:groups.append(acc)
 cursor=0;local=[]
 for g in groups:
  num=len(normal(g));s=max(0,min(x['duration']-.1,mapped[cursor][0]));e=max(s+.18,min(x['duration'],mapped[cursor+num-1][1]+.12))
  local.append(dict(text=g.strip('，。：；、'),start=s,end=e));cursor+=num
 for k,q in enumerate(local):
  if k+1<len(local):q['end']=max(q['start']+.1,min(q['end'],local[k+1]['start']))
  subs.append(dict(scene=x['id'],text=q['text'],start=round(x['start']+q['start']*30),end=min(x['end'],round(x['start']+q['end']*30))))
 audit.append(dict(scene=x['id'],source=src,editRate=round(dp[n][m]/max(n,1),3),mappedCharacters=len(mapped),characters=n))
(p/'renderer/subtitles.json').write_text(json.dumps(subs,ensure_ascii=False,indent=2));(p/'alignment-audit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False))
def tc(fr):
 ms=round(fr/30*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(p/'subtitles.srt').write_text('\n\n'.join(f'{i+1}\n{tc(s["start"])} --> {tc(s["end"])}\n{s["text"]}' for i,s in enumerate(subs))+'\n')
assert all(s['end']>s['start'] for s in subs)
assert ''.join(normal(s['text']) for s in subs)==''.join(normal(x['text']) for x in t['scenes'])
print('captions',len(subs),'volc',sum(a['source']=='volc' for a in audit),'whisper',sum(a['source']=='whisper' for a in audit),'maxEdit',max(a['editRate'] for a in audit))

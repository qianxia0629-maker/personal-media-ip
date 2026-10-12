import json,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).parent;A=P/'renderer/public/assets';O=P/'clip-check';O.mkdir(exist_ok=True)
FF='ffmpeg'
tl=json.loads((P/'renderer/timeline.json').read_text())
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Unicode.ttf',15)
items=[]
for s in tl['scenes']:
  v=s['visual']
  if v['kind']!='film':continue
  for c in v['clips']:items.append((s['id'],c))
only=set(sys.argv[1:])
if only: items=[x for x in items if x[0] in only]
tw=300;cells=[]
for sid,c in items:
  out=O/(c['file']+'.jpg')
  if not out.exists():
    subprocess.run([FF,'-nostdin','-v','error','-y','-ss',f"{c['frames']/30*0.5:.2f}",'-i',str(A/c['file']),'-frames:v','1','-vf',f'scale={tw}:-2',str(out)],check=True)
  cells.append((sid,c,Image.open(out).convert('RGB')))
cols=6;rowh=max(im.height for *_,im in cells)+36
pages=[cells[i:i+36] for i in range(0,len(cells),36)]
for k,pg in enumerate(pages):
  rows=(len(pg)+cols-1)//cols;sh=Image.new('RGB',(cols*tw,rows*rowh),'#111');d=ImageDraw.Draw(sh)
  for i,(sid,c,im) in enumerate(pg):
    x=(i%cols)*tw;y=(i//cols)*rowh;sh.paste(im,(x,y+34))
    d.text((x+3,y+1),f"{sid} {c['credit'][:18]}",fill='yellow',font=font);d.text((x+3,y+17),f"{c['frames']/30:.1f}s",fill='cyan',font=font)
  sh.save(O/f'sheet-{k+1}.jpg',quality=78);print(O/f'sheet-{k+1}.jpg',sh.size)

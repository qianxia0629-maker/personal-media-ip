import sys
import json,subprocess,hashlib,concurrent.futures
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).parent;Q=P/'qa';(Q/'frames').mkdir(parents=True,exist_ok=True)
FF='ffmpeg';F=Path(sys.argv[1]) if len(sys.argv)>1 else P/'renders/final.mp4'
tl=json.loads((P/'renderer/timeline.json').read_text());res={}
p=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(F)]))
v=[s for s in p['streams'] if s['codec_type']=='video'][0];a=[s for s in p['streams'] if s['codec_type']=='audio'][0]
res['分辨率']=f"{v['width']}x{v['height']}";res['帧率']=v['r_frame_rate'];res['视频帧数']=int(v['nb_frames']);res['timeline帧数']=tl['durationInFrames']
res['帧数一致']=abs(int(v['nb_frames'])-tl['durationInFrames'])<=2;res['音频']=f"{a['codec_name']} {a['sample_rate']}Hz {a['channels']}ch";res['时长']=round(float(p['format']['duration']),2);res['体积MB']=round(int(p['format']['size'])/1048576,1)
r=subprocess.run([FF,'-nostdin','-v','info','-i',str(F),'-vf','blackdetect=d=0.3:pix_th=0.06','-af','silencedetect=n=-45dB:d=1.5','-f','null','-'],capture_output=True,text=True)
res['解码错误']=[l for l in r.stderr.split('\n') if 'error' in l.lower()][:5] or '无'
res['黑帧段']=[l.split('] ')[-1] for l in r.stderr.split('\n') if 'black_start' in l] or '无'
res['长静音段(>1.5s,-45dB)']=[l.split('] ')[-1] for l in r.stderr.split('\n') if 'silence_start' in l] or '无'
subs=json.loads((P/'renderer/subtitles.json').read_text());res['字幕条数']=len(subs)
res['字幕越界']=[s['scene'] for s in subs if s['end']>tl['durationInFrames']] or '无'
res['字幕最长字数']=max(len(s['text']) for s in subs)
res['sha256']=hashlib.sha256(F.read_bytes()).hexdigest()
pts=[(s['id'],(s['start']+min(s['end']-s['start']-3,max(40,int((s['end']-s['start'])*.6))))/30) for s in tl['scenes']]
def fr(q):
 k,sec=q;subprocess.run([FF,'-nostdin','-v','error','-y','-ss',f'{sec:.3f}','-i',str(F),'-frames:v','1','-vf','scale=640:360',str(Q/'frames'/f'{k}.jpg')],check=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(fr,pts))
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',20)
for pg in range((len(pts)+11)//12):
 sh=Image.new('RGB',(1920,4*384),'#111');d=ImageDraw.Draw(sh)
 for j,(k,sec) in enumerate(pts[pg*12:pg*12+12]):
  sh.paste(Image.open(Q/'frames'/f'{k}.jpg'),((j%3)*640,(j//3)*384));d.text(((j%3)*640+8,(j//3)*384+362),f'{k} {sec:.1f}s',fill='yellow',font=font)
 sh.save(Q/f'contact-{pg+1}.jpg',quality=80)
(Q/'report.json').write_text(json.dumps(res,ensure_ascii=False,indent=1));print(json.dumps(res,ensure_ascii=False,indent=1))

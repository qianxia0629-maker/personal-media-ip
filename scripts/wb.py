"""Cross-platform whiteboard entrypoint with explicit voice routing."""
from pathlib import Path
from datetime import date
import subprocess,sys,argparse,json
from apply_config import ROOT,apply,resolve,load

def run(*args):
 argv=[str(x) for x in args]
 if argv[0]=='node' and (ROOT/'.env').exists():argv.insert(1,'--env-file='+str(ROOT/'.env'))
 subprocess.run(argv,check=True,cwd=ROOT/'skills/whiteboard-video')
def project(arg,c):
 p=Path(arg)
 if p.is_dir():return p.resolve()
 parent=resolve(c['dirs']['projects']);hits=sorted(x for x in parent.iterdir() if x.is_dir() and arg.lower() in x.name.lower())
 if len(hits)!=1:raise ValueError('Specify one exact episode path; found '+str(len(hits))+' matches')
 return hits[0]
def ensure_external(p,c):
 wb=ROOT/'skills/whiteboard-video';d=load(wb/'config.json')
 out=Path(d['dirs']['build'])/p.name/'work/audio'
 for scene in load(p/'scenes/script.json'):
  meta=out/(scene['name']+'.json');wav=out/(scene['name']+'.wav')
  if not meta.exists() or not wav.exists():raise ValueError('External voice missing: use scripts/import_narration.py with real audio and timestamps first')
  m=load(meta)
  if m.get('segments')!=scene['segments'] or m.get('speed')!=c['tts']['speed']:raise ValueError('Narration is stale after script/speed changes; regenerate and reimport it')
  if not m.get('wordList') or m.get('estimated'):raise ValueError('External narration requires actual aligned timing, not estimates')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('command',choices=['new','list','scenes','stills','tts','render','mix','cover','build']);ap.add_argument('episode',nargs='?');ap.add_argument('extra',nargs='*');a=ap.parse_args()
 c=apply();wb=ROOT/'skills/whiteboard-video'
 if a.command=='list':
  for p in sorted(resolve(c['dirs']['projects']).iterdir()):
   if p.is_dir():print(p.name)
  return
 if not a.episode:ap.error('episode/title required')
 if a.command=='new':
  if '/' in a.episode or '\\' in a.episode:raise ValueError('Title must not contain path separators')
  p=resolve(c['dirs']['projects'])/(date.today().isoformat()+' '+a.episode);p.mkdir(exist_ok=False)
  text=(wb/'templates/scenes.js').read_text(encoding='utf-8').replace('__TITLE__',a.episode).replace('__WB_ROOT__',wb.as_posix())
  (p/'scenes.js').write_text(text,encoding='utf-8');print(p);return
 p=project(a.episode,c)
 if a.command in {'build','scenes','stills','cover','tts'}:run('node',p/'scenes.js')
 if a.command in {'tts','build'}:
  if c['tts']['engine']=='volc':run('node',wb/'lib/tts-volc.mjs',p,*a.extra)
  else:ensure_external(p,c)
 if a.command=='stills':run('node',wb/'lib/render.js',p,'--stills',*a.extra)
 if a.command in {'render','build'}:run('node',wb/'lib/render.js',p,*a.extra)
 if a.command in {'mix','build'}:run('node',wb/'lib/mix-bgm.mjs',p,*a.extra)
 if a.command in {'cover','build'}:run('node',wb/'lib/render.js',p,'--cover')
if __name__=='__main__':main()

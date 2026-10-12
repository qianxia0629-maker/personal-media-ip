"""Synchronize the portable account profile into the two production modes."""
from pathlib import Path
import json, shutil, argparse

ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,data):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def resolve(p):
 path=Path(p).expanduser()
 return path if path.is_absolute() else (ROOT/path).resolve()
def apply(config=None):
 source=Path(config).resolve() if config else ROOT/'config.json'
 c=load(source)
 if c['tts']['engine'] not in {'external','chatcut','volc'}:raise ValueError('tts.engine must be external, chatcut, or volc')
 if not 0.5<=float(c['tts']['speed'])<=2:raise ValueError('tts.speed must be between 0.5 and 2')
 b=c['brand'];graphic=b.get('graphic',{})
 if graphic.get('type') not in {'sparkle','none','logo'}:raise ValueError('brand.graphic.type must be sparkle, none, or logo')
 if graphic.get('type')=='logo' and not b.get('logo'):raise ValueError('logo graphic requires brand.logo')
 for key in ('accent','ink'):
  import re
  if not re.fullmatch(r'#[0-9a-fA-F]{6}',b[key]):raise ValueError('brand.'+key+' requires #RRGGBB')
 wb=ROOT/'skills/whiteboard-video'
 d=load(wb/'config.defaults.json')
 for key in ('render','captions','cover','tts'):d[key]=c[key]
 d['dirs']={k:str(resolve(c['dirs'][k])) for k in ('projects','build')}
 d['brand']=json.loads(json.dumps(b));d['bgm']=json.loads(json.dumps(c['bgm']))
 d['bgm']['file']=str(resolve(c['bgm']['file'])) if c['bgm'].get('enabled',True) else ''
 d['bgm']['enabled']=c['bgm'].get('enabled',True)
 d['brand']['watermark']['sparkle']=graphic.get('type')=='sparkle' and graphic.get('sparkle',True)
 d['brand']['watermark']['underline']=graphic.get('underline',True)
 investigation=ROOT/'skills/investigation-video/template/remotion'
 profile={'brand':{'signature':b['name'],'wordmark':b['name'],'accent':b['accent'],'ink':b['ink'],
                    'fontFamily':'WorkflowBrand','sparkle':d['brand']['watermark']['sparkle'],
                    'underline':d['brand']['watermark']['underline']},'tts':c['tts'],'bgm':d['bgm']}
 for key,label in [('font','BrandFont'),('bodyFont','BodyFont')]:
  font=resolve(b[key]['file'])
  if not font.is_file() or font.suffix.lower() not in {'.ttf','.otf','.woff','.woff2'}:raise ValueError(f'Invalid font file: {font}')
  target=wb/'assets/fonts'/(label+font.suffix.lower());target.parent.mkdir(parents=True,exist_ok=True)
  if font.resolve()!=target.resolve():shutil.copy2(font,target)
  d['brand'][key]['url']='../assets/fonts/'+target.name
  (investigation/'public').mkdir(parents=True,exist_ok=True)
  shutil.copy2(font,investigation/'public'/target.name)
  profile['brand']['fontFile' if key=='font' else 'bodyFontFile']=target.name
 if b.get('logo'):
  logo=resolve(b['logo'])
  if not logo.is_file() or logo.suffix.lower()!='.png':raise ValueError('brand.logo must point to an existing transparent PNG')
  d['brand']['logo']=str(logo)
  shutil.copy2(logo,investigation/'public'/'brand-logo.png');profile['brand']['logoFile']='brand-logo.png'
 save(wb/'config.json',d);save(investigation/'profile.json',profile)
 for path in c['dirs'].values():resolve(path).mkdir(parents=True,exist_ok=True)
 wpath=ROOT/c['writing']['workflowFile'];w=load(wpath)
 w['videoScript']['style']=c['writing']['videoStyle'];w['wechatArticle']['style']=c['writing']['wechatStyle']
 save(wpath,w)
 print('CONFIG_APPLIED: profile, fonts, brand, voice, music, and writing styles synchronized')
 return c
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--config');a=p.parse_args();apply(a.config)

"""Validate the configured publication platform set and title lengths."""
import argparse,re,json
from pathlib import Path
from apply_config import ROOT,load
from title_symbols import invalid_title_characters
def check(text,platforms,brand_name="RayTalk"):
 errors=[];names=[p['name'] for p in platforms]
 heads=re.findall(r'^## (.+)$',text,re.M)
 if heads!=names:errors.append('Platform order/set must be '+', '.join(names))
 bodies=re.split(r'^## .+$',text,flags=re.M)[1:]
 for name,body in zip(heads,bodies):
  cfg=next((p for p in platforms if p['name']==name),None)
  if cfg is None:continue
  for field in ['主推标题','备选标题']:
   m=re.search(r'^'+field+r'：([^\n]+)',body,re.M)
   if not m or not m[1].strip():errors.append(name+' missing '+field);continue
   title=m[1].strip()
   if '<' in title or '>' in title or '〔' in title:errors.append(name+' unfilled title')
   if len(title)>cfg['titleMaxChars']:errors.append(name+' title longer than '+str(cfg['titleMaxChars']))
   if 'titleAllowedSymbols' in cfg:
    invalid=invalid_title_characters(title,cfg['titleAllowedSymbols'],cfg.get('titleAllowedSymbolSequences',[]))
    if invalid:errors.append(name+' '+field+' unsupported title characters: '+repr(''.join(invalid))+'（逗号请改为空格）')
   if cfg.get('titleContainsBrand') is False and brand_name and brand_name.lower() in title.lower():errors.append(name+' title contains demo brand')
  m=re.search(r'^正文：(.*)',body,re.M|re.S)
  if not m or not m[1].strip():errors.append(name+' missing body')
  elif re.search(r'<[^>]+>|〔[^〕]+〕',m[1]):errors.append(name+' unfilled body')
 return errors
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('file');a=ap.parse_args()
 profile=load(ROOT/'workflow/文案编写配置.json');errors=check(Path(a.file).read_text(encoding='utf-8-sig'),profile['platforms'],load(ROOT/'config.json')['brand']['name'])
 print('COPY_OK' if not errors else 'COPY_FAIL\n'+'\n'.join(errors));raise SystemExit(bool(errors))

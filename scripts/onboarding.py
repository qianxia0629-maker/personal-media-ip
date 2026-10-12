"""Local, resumable state for an Agent-led, one-question-at-a-time setup."""
from pathlib import Path
import argparse, copy, json, hashlib, math
from apply_config import ROOT, load, save, apply

META={'_note','note','source','scope','implementation','draftingStage','missingInput','delivery','formatReference'}
LABELS={
 'brand.name':('品牌名','你的账号或品牌叫什么名字？'),
 'writing.videoStyle':('视频口播风格','视频口播希望是什么风格？例如自然科普、专业解读或辛辣评论。'),
 'writing.wechatStyle':('公众号笔风','公众号文章希望是什么笔风？默认辛辣锐评，也可以改成温和评论等。'),
 'platforms':('视频发布平台','视频准备发到哪些平台？请按顺序说出名称。'),
 'brand.font.family':('品牌字体名称','品牌名想用什么字体？可保留免费小赖手写体。'),
 'brand.font.file':('品牌字体文件','这款品牌字体的文件在哪里？用免费小赖字体可保留默认。'),
 'brand.bodyFont.family':('正文字体名称','视频正文想用什么字体？'),
 'brand.bodyFont.file':('正文字体文件','正文字体文件在哪里？可保留默认。'),
 'brand.graphic.type':('品牌图形','品牌图形选择星芒、无图形，还是自己的透明Logo？'),
 'brand.graphic.sparkle':('星芒开关','品牌星芒要显示吗？'),
 'brand.graphic.underline':('品牌下划线','品牌名下面的手绘下划线要保留吗？'),
 'brand.accent':('品牌色','品牌主色用什么颜色？可以说颜色或提供HEX色号。'),
 'brand.ink':('正文颜色','视频正文和品牌墨色用什么颜色？'),
 'brand.logo':('透明Logo','有自己的透明PNG Logo吗？有就提供本机路径，没有可留空。'),
 'brand.slogan':('品牌口号','需要固定品牌口号吗？没有可留空。'),
 'brand.endCard.cta':('片尾引导语','片尾需要什么引导语？没有可留空。'),
 'tts.engine':('旁白来源','旁白选火山引擎、ChatCut克隆音色，还是其他服务的音轨？'),
 'tts.voice':('火山音色ID','选择哪个火山音色ID？API密钥请只写入本机.env，不要发在对话里。'),
 'tts.resourceId':('火山资源ID','火山资源ID使用官方2.0还是声音复刻资源？'),
 'tts.voiceName':('旁白音色名称','你想使用的旁白音色叫什么名字？'),
 'tts.customVoiceId':('ChatCut音色','连接你自己的ChatCut后，选择哪个ready音色？由Agent查询真实ID，不猜ID。'),
 'tts.speed':('旁白语速','旁白语速用几倍？默认1.2倍，可选0.5到2倍。'),
 'tts.externalManifest':('外部音轨清单','外部音轨与真实时间戳的清单放在哪里？可先留空，制作时再提供。'),
 'bgm.enabled':('是否配乐','视频需要背景配乐吗？'),
 'bgm.file':('配乐文件','你的配乐文件在哪里？没有音乐可以先关闭配乐。'),
 'bgm.gain':('配乐总音量','配乐总音量倍率用多少？默认0.5。'),
 'bgm.speak':('说话时配乐','说话时配乐压低到多少倍率？默认0.1。'),
 'bgm.gap':('停顿时配乐','停顿时配乐回升到多少倍率？默认0.22。'),
 'bgm.trim':('配乐截取','使用整首音乐，还是只用某个秒数区间？整首填写空数组。'),
 'writing.workflowFile':('写作配置位置','写作配置文件保留默认位置吗？'),
 'writing.scopeNotes':('范围说明','材料范围等说明只放在画面，还是希望在口播里说？'),
 'writing.reviewSkills':('审校技能顺序','保留Humanizer-zh、stop-slop、taste-skill三轮审校吗？也可指定顺序。'),
 'writing.optionalTitleAudit':('附加标题审核','是否保留可选dbs-xhs-title审核？该依赖需自行安装并遵守许可。'),
 'dirs.projects':('白板工程位置','白板每期源文件放在哪里？默认仓库workspace内。'),
 'dirs.build':('白板成片位置','白板中间文件和成片放在哪里？'),
 'dirs.investigation':('调查工程位置','调查视频工程和成片放在哪里？'),
}
TERMS={'watermark':'白板水印','endCard':'片尾品牌卡','pen':'绘笔','enabled':'开关','position':'位置','opacity':'透明度','size':'字号','margin':'边距','drawInSeconds':'画入时长','seconds':'时长','holdSeconds':'停留时长','color':'颜色','fps':'帧率','workers':'渲染并行数','leadSeconds':'提前停留','speed':'速度','fillSpeed':'填充速度','minSeconds':'最短绘制时间','gapSeconds':'抬笔间隔','charSeconds':'每字绘制时间范围','overflow':'跨段绘制比例','travelMax':'抬笔移动最长时间','fillMaxSeconds':'填充最长时间','fontSize':'字幕字号','baselineY':'字幕基线','safeTop':'字幕安全区起点','minChars':'最少字数','maxChars':'最多字数','tailSeconds':'结束延后','ratios':'封面比例','seriesTag':'封面系列标签','frame':'封面边框','frameColor':'封面边框色','rampSeconds':'配乐过渡时长','tailFadeSeconds':'配乐淡出时长','titleMaxChars':'标题字数上限','titleStrategy':'标题策略','format':'格式','bodyCharsReference':'正文参考字数','titleContainsBrand':'标题是否写品牌名','lengthRule':'口播篇幅规则','shortScriptReferenceChars':'短视频脚本参考字数','separateScreenNotes':'口播与画面注记分开','cta':'互动引导规则','candidatesPerPlatform':'主推/备选标题数量','strategy':'标题吸引力策略','audit':'标题审核方式','outputFields':'交付字段','deliverables':'输出文件名','abstractOutput':'是否附摘要','tagsOutput':'是否附标签','commentsOutput':'是否附评论','ctaRequired':'是否强制CTA','approach':'文章评论方式','txtPreservesMarkdown':'TXT保留Markdown','formatRules':'Markdown排版规则','templateFile':'公众号模板文件','promptFile':'写稿提示词文件','reviewFile':'审校流程文件','publishAction':'是否仅制作备稿'}
PRIORITY=['config:brand.name','config:writing.videoStyle','config:writing.wechatStyle','workflow:platforms',
 'config:brand.font.family','config:brand.font.file','config:brand.bodyFont.family','config:brand.bodyFont.file',
 'config:brand.graphic.type','config:brand.graphic.sparkle','config:brand.graphic.underline','config:brand.logo',
 'config:brand.accent','config:brand.ink','config:brand.slogan','config:brand.endCard.cta',
 'config:tts.engine','config:tts.voiceName','config:tts.voice','config:tts.resourceId','config:tts.customVoiceId','config:tts.speed','config:tts.externalManifest','config:bgm.enabled','config:bgm.file']

def get(data,path):
 for key in path.split('.'):data=data[int(key)] if isinstance(data,list) else data[key]
 return data
def set_value(data,path,value):
 keys=path.split('.');node=data
 for key in keys[:-1]:node=node[int(key)] if isinstance(node,list) else node[key]
 if isinstance(node,list):node[int(keys[-1])]=value
 else:node[keys[-1]]=value
def leaves(data,prefix=''):
 for key,value in data.items():
  if key in META:continue
  path=f'{prefix}.{key}' if prefix else key
  if isinstance(value,dict):yield from leaves(value,path)
  else:yield path,value
def steps(c,w):
 result=[]
 for path,value in leaves(c):
  # Derived duplicates are controlled by brand.graphic rather than asked twice.
  if path in {'brand.watermark.sparkle','brand.watermark.underline'}:continue
  result.append({'id':'config:'+path,'file':'config','path':path,'value':value})
 for path,value in leaves(w):
  if path in {'videoScript.style','wechatArticle.style','reviewSequence'}:continue
  if path=='platforms':
   result.append({'id':'workflow:platforms','file':'workflow','path':path,'value':[p['name'] for p in value]})
   for i,platform in enumerate(value):
    for sub,sv in leaves(platform):
     if sub in {'name','type'}:continue
     p=f'platforms.{i}.{sub}'
     result.append({'id':'workflow:'+p,'file':'workflow','path':p,'value':sv,'platform':platform['name']})
   continue
  if path=='wechatArticle.name' or path=='wechatArticle.type':continue
  result.append({'id':'workflow:'+path,'file':'workflow','path':path,'value':value})
 order={x:i for i,x in enumerate(PRIORITY)}
 return sorted(result,key=lambda s:order.get(s['id'],len(PRIORITY)))
def active(step,c):
 p=step['path'];engine=c['tts']['engine']
 if step['file']=='workflow':return True
 if p in {'tts.voice','tts.resourceId'}:return engine=='volc'
 if p=='tts.customVoiceId':return engine=='chatcut'
 if p=='tts.voiceName':return engine!='volc'
 if p=='tts.externalManifest':return engine in {'chatcut','external'}
 if p.startswith('bgm.') and p!='bgm.enabled':return c['bgm']['enabled']
 if p=='brand.graphic.sparkle':return c['brand']['graphic']['type']=='sparkle'
 if p.startswith('brand.watermark.') and p!='brand.watermark.enabled':return c['brand']['watermark']['enabled']
 if p.startswith('brand.endCard.') and p!='brand.endCard.enabled':return c['brand']['endCard']['enabled']
 return True
def describe(step):
 path=step['path'];title,question=LABELS.get(path,(None,None))
 if not title:
  pieces=[TERMS.get(x,x) for x in path.split('.') if not x.isdigit()]
  title=(step.get('platform','')+' '+ ' / '.join(pieces)).strip()
  question=f'{title}要怎么设置？可以明确说“保留默认”。'
 return {'id':step['id'],'title':title,'question':question,'current':step['value'],'configFile':'config.json' if step['file']=='config' else 'workflow/文案编写配置.json','path':path}
def fingerprint(c,w):return hashlib.sha256(json.dumps([c,w],sort_keys=True,ensure_ascii=False).encode()).hexdigest()

class Wizard:
 def __init__(self,root=ROOT):
  self.root=Path(root).resolve();self.statefile=self.root/'.local/onboarding.json'
 def read(self):
  if self.statefile.exists():return load(self.statefile)
  c=load(self.root/'config.json');w=load(self.root/c['writing']['workflowFile'])
  state={'version':1,'status':'in_progress','config':c,'workflow':w,'reviewed':{},'baseFingerprint':fingerprint(c,w)}
  self.persist(state);return state
 def persist(self,s):save(self.statefile,s)
 def pending(self,s):return [x for x in steps(s['config'],s['workflow']) if active(x,s['config']) and x['id'] not in s['reviewed']]
 def next(self):
  s=self.read();remaining=self.pending(s)
  return {'status':s['status'],'reviewed':len(s['reviewed']),'remaining':len(remaining),'next':describe(remaining[0]) if remaining else None,
          'instruction':'Ask ONLY this item and wait for an explicit answer. Do not synthesize or render during setup.' if remaining else 'Show final summary; finish saves and synchronizes the draft.'}
 def validate(self,step,value,s):
  old=step['value'];p=step['path']
  if p=='platforms':
   if not isinstance(value,list) or not value or not all(isinstance(x,str) and x.strip() for x in value) or len(set(value))!=len(value):raise ValueError('Platforms need a nonempty unique list of names')
   return
  if isinstance(old,bool) and not isinstance(value,bool):raise ValueError('Expected boolean')
  if isinstance(old,(int,float)) and (isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value)):raise ValueError('Expected finite number')
  if isinstance(old,int) and not isinstance(value,int):raise ValueError('Expected integer')
  if isinstance(old,str) and not isinstance(value,str):raise ValueError('Expected text')
  if isinstance(old,list) and not isinstance(value,list):raise ValueError('Expected array')
  if p=='tts.engine' and value not in {'volc','chatcut','external'}:raise ValueError('Unknown voice engine')
  if p=='tts.speed' and not .5<=value<=2:raise ValueError('Voice speed must be between 0.5 and 2')
  if p=='brand.graphic.type' and value not in {'sparkle','none','logo'}:raise ValueError('Unknown graphic type')
  if p in {'brand.accent','brand.ink','brand.pen.color','cover.frameColor'}:
   import re
   if not re.fullmatch(r'#[0-9a-fA-F]{6}',value):raise ValueError('Expected #RRGGBB')
  if p in {'brand.watermark.opacity','bgm.gain','bgm.speak','bgm.gap'} and not 0<=value<=1:raise ValueError('Use a value from 0 to 1')
  if p.endswith('titleMaxChars') and value<1:raise ValueError('Title length must be positive')
  if p in {'render.fps','render.workers','captions.fontSize','brand.watermark.size'} and value<=0:raise ValueError('Expected positive value')
  if p.endswith(('bodyCharsReference','shortScriptReferenceChars','charSeconds')) and (len(value)!=2 or any(isinstance(x,bool) or not isinstance(x,(int,float)) or x<0 for x in value) or value[0]>value[1]):raise ValueError('Expected [minimum, maximum]')
  if p=='bgm.trim' and value and (len(value)!=2 or any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) for x in value) or not 0<=value[0]<value[1]):raise ValueError('Expected [] or [start, end]')
  if p=='brand.logo':
   if s['config']['brand']['graphic']['type']=='logo' and not value:raise ValueError('Provide a PNG logo or revise the graphic choice to sparkle/none')
   if value:
    f=Path(value).expanduser();f=f if f.is_absolute() else self.root/f
    if not f.is_file() or f.suffix.lower()!='.png':raise ValueError('An existing transparent PNG path is required')
  if p in {'brand.font.file','brand.bodyFont.file'}:
   f=Path(value).expanduser();f=f if f.is_absolute() else self.root/f
   if not f.is_file():raise ValueError('Font file missing; supply its actual path or keep the bundled font')
  if p=='writing.scopeNotes' and value not in {'screen-only','spoken'}:raise ValueError('Use screen-only or spoken')
  if p=='brand.watermark.position' and value not in {'top-right','top-left','bottom-right','bottom-left'}:raise ValueError('Unknown watermark position')
 def answer(self,step_id,value=None,keep=False):
  s=self.read()
  if s['status']=='completed':raise ValueError('Use reset to configure again; completed setup is not reopened automatically')
  pending=self.pending(s)
  if not pending or pending[0]['id']!=step_id:raise ValueError('Answer only the currently pending item')
  step=pending[0]
  if keep:value=step['value']
  self.validate(step,value,s)
  if step['path']=='platforms':
   byname={p['name']:p for p in s['workflow']['platforms']}
   s['workflow']['platforms']=[byname.get(name,{'name':name,'type':'video_publish_copy','titleMaxChars':30,'titleStrategy':'具体对象与问题，有依据的数字、关键词与情绪点','format':'按平台受众自然表达'}) for name in value]
   s['reviewed']={k:v for k,v in s['reviewed'].items() if not k.startswith('workflow:platforms.')}
  else:set_value(s[step['file']],step['path'],value)
  s['reviewed'][step_id]={'choice':'keep' if keep else 'changed'}
  self.persist(s);return self.next()
 def keep_remaining(self,confirmed=False):
  if not confirmed:raise ValueError('Only after the user explicitly says to keep all remaining defaults')
  s=self.read()
  for step in self.pending(s):s['reviewed'][step['id']]={'choice':'keep_remaining'}
  self.persist(s);return self.next()
 def revise(self,step_id,value):
  s=self.read()
  if s['status']=='completed':raise ValueError('Use reset for a completed setup')
  step=next((x for x in steps(s['config'],s['workflow']) if x['id']==step_id),None)
  if not step or step_id not in s['reviewed']:raise ValueError('Revise only an already answered item')
  self.validate(step,value,s)
  if step['path']=='platforms':
   byname={p['name']:p for p in s['workflow']['platforms']}
   s['workflow']['platforms']=[byname.get(name,{'name':name,'type':'video_publish_copy','titleMaxChars':30,'titleStrategy':'具体对象与问题','format':'按平台受众自然表达'}) for name in value]
   s['reviewed']={k:v for k,v in s['reviewed'].items() if not k.startswith('workflow:platforms.')}
  else:set_value(s[step['file']],step['path'],value)
  s['reviewed'][step_id]={'choice':'revised'};self.persist(s);return self.next()
 def finish(self):
  s=self.read()
  if s['status']=='completed':return {'status':'completed','instruction':'Already configured; do not ask the setup questions again.'}
  if self.pending(s):raise ValueError('Unanswered items remain')
  original=load(self.root/'config.json');old_workflow=load(self.root/original['writing']['workflowFile'])
  if fingerprint(original,old_workflow)!=s['baseFingerprint']:raise ValueError('Config changed outside this draft; reconcile it before finishing, do not overwrite other edits')
  if s['config']['brand']['graphic']['type']=='logo' and not s['config']['brand']['logo']:raise ValueError('Logo mode needs a file; return to setup with reset or use a valid draft logo')
  # Drafts are committed only once setup has been explicitly answered.
  backup=self.root/'.local/onboarding-backup';save(backup/'config.json',original);save(backup/'workflow.json',old_workflow)
  save(self.root/'config.json',s['config']);save(self.root/s['config']['writing']['workflowFile'],s['workflow'])
  try:
   import subprocess,sys
   subprocess.run([sys.executable,str(self.root/'scripts/apply_config.py')],cwd=self.root,check=True)
  except Exception:
   save(self.root/'config.json',original);save(self.root/original['writing']['workflowFile'],old_workflow)
   raise
  s['status']='completed';self.persist(s)
  return {'status':'completed','reviewed':len(s['reviewed']),'instruction':'Summarize the saved account settings; separately check assets, services and runtime readiness before production.'}

def main():
 p=argparse.ArgumentParser();sub=p.add_subparsers(dest='action',required=True)
 for name in ('next','status','summary','finish','reset'):sub.add_parser(name)
 a=sub.add_parser('answer');a.add_argument('--id',required=True);group=a.add_mutually_exclusive_group(required=True);group.add_argument('--value-json');group.add_argument('--keep',action='store_true')
 a=sub.add_parser('keep-remaining');a.add_argument('--confirmed-by-user',action='store_true')
 a=sub.add_parser('revise');a.add_argument('--id',required=True);a.add_argument('--value-json',required=True)
 args=p.parse_args();w=Wizard()
 if args.action in {'next','status'}:result=w.next()
 elif args.action=='answer':result=w.answer(args.id,json.loads(args.value_json) if args.value_json is not None else None,args.keep)
 elif args.action=='keep-remaining':result=w.keep_remaining(args.confirmed_by_user)
 elif args.action=='revise':result=w.revise(args.id,json.loads(args.value_json))
 elif args.action=='summary':
  s=w.read();result={'status':s['status'],'config':s['config'],'workflow':s['workflow'],'remaining':len(w.pending(s))}
 elif args.action=='finish':result=w.finish()
 else:
  if w.statefile.exists():w.statefile.unlink()
  result=w.next()
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()

import unittest,sys,tempfile,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from import_narration import align
from check_publish import check
from apply_config import load
from title_symbols import VIDEO_CHANNEL_SYMBOLS

class WorkflowTests(unittest.TestCase):
 def test_real_word_bounds_and_segment_alignment(self):
  starts,words=align(['先看资料。','再核对来源。'],[
   {'word':'先看资料','startTime':.2,'endTime':1.0},
   {'word':'再核对来源','startTime':1.1,'endTime':2.0}],2.1)
  self.assertEqual(starts,[0,1.1]);self.assertEqual(words[-1]['e'],2.0)
  self.assertEqual(''.join(w['w'] for w in words),'先看资料。再核对来源。')
 def test_wrong_transcript_cannot_silently_render(self):
  with self.assertRaisesRegex(ValueError,'mismatch'):
   align(['核对来源'],[{'word':'随意编造','startTime':0,'endTime':1}],1)
 def test_timestamp_outside_audio_is_rejected(self):
  with self.assertRaisesRegex(ValueError,'outside'):
   align(['资料'],[{'word':'资料','startTime':0,'endTime':10}],2)
 def text(self,title):
  out='# 发布稿\n'
  for name in ['抖音','哔哩哔哩','小红书','微信视频号']:
   out+=f'\n## {name}\n主推标题：'+(title if name=='微信视频号' else '先核对资料')+'\n备选标题：先看来源\n正文：\n先核对资料，再写稿。\n'
  return out
 def test_sixteen_char_boundary(self):
  platforms=load(ROOT/'workflow/文案编写配置.json')['platforms']
  self.assertEqual(check(self.text('字'*16),platforms),[])
  self.assertTrue(any('longer' in e for e in check(self.text('字'*17),platforms)))
 def test_removed_platform_rejected(self):
  platforms=load(ROOT/'workflow/文案编写配置.json')['platforms']
  self.assertTrue(check(self.text('核对资料')+'\n## 快手\n正文：额外平台',platforms))
 def test_custom_brand_is_used_in_title_validation(self):
  platforms=load(ROOT/'workflow/文案编写配置.json')['platforms']
  text=self.text('核对资料').replace('## 小红书\n主推标题：先核对资料','## 小红书\n主推标题：NewBrand教你核对')
  self.assertTrue(any('brand' in e for e in check(text,platforms,'NewBrand')))
 def test_custom_title_limit_is_read_from_config(self):
  platforms=load(ROOT/'workflow/文案编写配置.json')['platforms']
  platforms[-1]['titleMaxChars']=4
  self.assertTrue(any('longer' in e for e in check(self.text('这是五个字'),platforms)))
 def test_allowed_video_channel_symbols(self):
  platforms=load(ROOT/'workflow/文案编写配置.json')['platforms']
  for symbol in VIDEO_CHANNEL_SYMBOLS:
   with self.subTest(symbol=symbol):self.assertEqual(check(self.text('资料'+symbol+'核对'),platforms),[])
  for title in ['温度25℃','温度25°C','AI资料 核对50%','《资料》：有误吗？']:
   with self.subTest(title=title):self.assertEqual(check(self.text(title),platforms),[])
 def test_unsupported_video_channel_symbols_rejected(self):
  platforms=load(ROOT/'workflow/文案编写配置.json')['platforms']
  for symbol in ['，',',','。','.','！','!','、','；',';','（','）','(',')','#','@','/','_','-','—','…','★','🔥','°','①','\u200b','\t','\u00a0','\ufe0f','\u20e3']:
   with self.subTest(symbol=symbol):self.assertTrue(any('unsupported' in e for e in check(self.text('资料'+symbol+'核对'),platforms)))
 def test_backup_title_uses_same_symbol_rule(self):
  platforms=load(ROOT/'workflow/文案编写配置.json')['platforms']
  text=self.text('核对资料').replace('## 微信视频号\n主推标题：核对资料\n备选标题：先看来源','## 微信视频号\n主推标题：核对资料\n备选标题：先看来源！')
  self.assertTrue(any('备选标题' in e and 'unsupported' in e for e in check(text,platforms)))
 def test_symbol_rule_does_not_restrict_other_platforms_or_body(self):
  platforms=load(ROOT/'workflow/文案编写配置.json')['platforms']
  text=self.text('核对资料').replace('主推标题：先核对资料','主推标题：先核对资料！')
  self.assertEqual(check(text,platforms),[])
 def test_spaces_count_toward_sixteen_character_limit(self):
  platforms=load(ROOT/'workflow/文案编写配置.json')['platforms']
  self.assertEqual(check(self.text('字'*7+' '+'字'*8),platforms),[])
  self.assertTrue(any('longer' in e for e in check(self.text('字'*8+' '+'字'*8),platforms)))
 def test_symbol_allowlist_is_configurable(self):
  platforms=load(ROOT/'workflow/文案编写配置.json')['platforms']
  platforms[-1]['titleAllowedSymbols']+='!'
  self.assertEqual(check(self.text('核对资料!'),platforms),[])
 def test_standalone_skill_checker_enforces_symbols(self):
  with tempfile.TemporaryDirectory(dir=ROOT/'.local') as folder:
   path=Path(folder)/'copy.md'
   header='对应：测试\n标题策略：关键词\n'
   for title,expected in [('资料 核对?',0),('资料，核对',1)]:
    path.write_text(header+self.text(title),encoding='utf-8')
    result=subprocess.run([sys.executable,str(ROOT/'skills/investigation-video/assets/check-publish-copy.py'),'--raytalk',str(path)],capture_output=True,text=True,encoding='utf-8')
    self.assertEqual(result.returncode,expected,result.stdout+result.stderr)

if __name__=='__main__':unittest.main()

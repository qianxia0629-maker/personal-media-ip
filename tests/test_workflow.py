import unittest,sys,tempfile,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from import_narration import align
from check_publish import check
from apply_config import load

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

if __name__=='__main__':unittest.main()

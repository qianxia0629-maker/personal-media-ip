"""Import cloned-voice audio plus measured word timestamps into whiteboard scenes."""
from pathlib import Path
import argparse,subprocess,json,re
from apply_config import ROOT,load,apply,resolve,save

def norm(text):return ''.join(re.findall(r'[\u4e00-\u9fffA-Za-z0-9]',text)).lower()
def align(segments,words,duration):
 if not words:raise ValueError('No real word timestamps; synthesize/transcribe the audio first')
 chars=[];last=0.0
 for w in words:
  start=float(w['startTime']);end=float(w['endTime']);text=norm(w['word'])
  if start<last-0.02 or start<0 or end<start or end>duration+0.1:raise ValueError('Timestamp is unordered/outside source audio')
  last=end
  for i,ch in enumerate(text):chars.append((ch,start+(end-start)*i/len(text),start+(end-start)*(i+1)/len(text)))
 expected=norm(''.join(segments))
 if not expected or ''.join(x[0] for x in chars)!=expected:raise ValueError('Transcript/script mismatch: correct pronunciation or transcription before import')
 starts=[];wordlist=[];index=0
 for segment in segments:
  starts.append(chars[index][1])
  for ch in segment:
   if norm(ch):
    _,s,e=chars[index];index+=1;wordlist.append({'w':ch,'s':s,'e':e})
   elif wordlist and ch.strip():wordlist[-1]['w']+=ch
 starts[0]=0
 return starts,wordlist
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project',required=True);ap.add_argument('--manifest',required=True);a=ap.parse_args()
 c=apply();p=Path(a.project).resolve();manifest=Path(a.manifest).resolve();items=load(manifest)['scenes'];scenes=load(p/'scenes/script.json')
 target=resolve(c['dirs']['build'])/p.name/'work/audio';target.mkdir(parents=True,exist_ok=True)
 byname={i['name']:i for i in items}
 if len(byname)!=len(items):raise ValueError('Duplicate scene name')
 speed=float(c['tts']['speed'])
 for sc in scenes:
  item=byname[sc['name']];audio=Path(item['audio']);audio=audio if audio.is_absolute() else manifest.parent/audio
  if not audio.is_file():raise ValueError('Missing source audio: '+str(audio))
  duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(audio)]))
  if duration<=0:raise ValueError('Empty source audio')
  starts,words=align(sc['segments'],item['words'],duration)
  wav=target/(sc['name']+'.wav')
  subprocess.run(['ffmpeg','-v','error','-y','-i',str(audio),'-af',f'atempo={speed}','-ar','48000','-ac','1',str(wav)],check=True)
  actual=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(wav)]))
  for w in words:w['s']=round(w['s']/speed,3);w['e']=round(w['e']/speed,3)
  save(target/(sc['name']+'.json'),{'name':sc['name'],'duration':actual,'segmentStarts':[x/speed for x in starts],'segments':sc['segments'],
       'wordList':words,'speed':speed,'voice':c['tts']['voiceName'],'alignmentSource':'provider/ASR word timestamps; exact normalized transcript match; characters interpolated within measured word bounds'})
 print('NARRATION_IMPORTED: audio, script, and measured timing matched')
if __name__=='__main__':main()

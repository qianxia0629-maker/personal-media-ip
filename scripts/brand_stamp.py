"""Apply the configurable account mark to a cover; no model-generated lettering."""
from pathlib import Path
import argparse
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageColor
from apply_config import ROOT,load,resolve
def make_mark(width,c,dark=False):
 b=c['brand'];g=b['graphic'];scale=width/320
 if b.get('logo'):
  im=Image.open(resolve(b['logo'])).convert('RGBA');im.thumbnail((width,int(width*.45)));return im
 im=Image.new('RGBA',(width,int(92*scale)),(0,0,0,0));d=ImageDraw.Draw(im)
 ink='#FAFAF8' if dark else b['ink'];accent=b['accent']
 fontpath=resolve(b['font']['file']);size=int(55*scale);font=ImageFont.truetype(str(fontpath),max(size,1))
 while d.textbbox((0,0),b['name'],font=font)[2]>width-int(40*scale) and size>8:
  size-=1;font=ImageFont.truetype(str(fontpath),size)
 if g.get('type')=='sparkle' and g.get('sparkle',True):
  points=[(20,0),(24,15),(40,20),(24,25),(20,40),(16,25),(0,20),(16,15)]
  d.polygon([(x*.6*scale,(y*.6+5)*scale) for x,y in points],fill=accent)
 d.text((30*scale,2*scale),b['name'],font=font,fill=ink)
 if g.get('underline',True):d.line([(30*scale,75*scale),(175*scale,79*scale),(310*scale,73*scale)],fill=accent,width=max(1,int(4*scale)))
 return im
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('output');p.add_argument('--width',type=float,default=.22);p.add_argument('--dark',action='store_true');a=p.parse_args()
 if not 0<a.width<=1:p.error('--width must be between 0 and 1')
 base=Image.open(a.input).convert('RGBA');mark=make_mark(int(base.width*a.width),load(ROOT/'config.json'),a.dark)
 x=base.width-mark.width-int(base.width*.04);y=int(base.height*.03)
 base.alpha_composite(mark,(x,y));base.convert('RGB').save(a.output);print('BRAND_STAMPED')

#!/usr/bin/env python3
"""封面字标固定合成。

用法: brand-stamp.py <in.png> <out.png> [--pos top-right|bottom-right|bottom-left] [--width 0.22] [--text "Your Brand"]
默认: 右上角，字标宽 = 图宽 22%，右边距 = 图宽 4%，上边距 = 图高 3%。
几何与 assets/BrandStamp.jsx 一致：星芒 + SignPainter 白字签名 + 甩笔底划，默认强调色 #10C46F。签名文字用 --text 传入，或改 TEXT 常量。
需要 macOS SignPainter (/System/Library/Fonts/Supplemental/SignPainter.ttc) 与 Pillow。
生图提示词里不要再让模型画签名；右上角留净空。
"""
import sys,argparse
from PIL import Image,ImageDraw,ImageFont,ImageFilter
FONT='/System/Library/Fonts/Supplemental/SignPainter.ttc'
ACCENT=(16,196,111,255);INK=(250,250,248,255);TEXT='Your Brand'
def wordmark(width,text=TEXT):
    # 参照 JSX: 容器 265×84，星 24@ (0,1)，文字 left 24 fontSize 55，底划 224×15 @ (27,57)
    S=width/265.0;W=int(265*S);H=int(84*S)+int(8*S)
    im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
    # star: viewBox 40 → 24px
    k=24*S/40;ox,oy=0,1*S
    pts=[(20,0),(24,15),(40,20),(24,25),(20,40),(16,25),(0,20),(16,15)]
    d.polygon([(ox+x*k,oy+y*k) for x,y in pts],fill=ACCENT)
    font=ImageFont.truetype(FONT,int(55*S))
    # SignPainter 行高 1.05；PIL 基线对齐用 anchor 'la'
    d.text((24*S,-2*S),text,font=font,fill=INK,anchor='la')
    # swoosh: viewBox 320×22 → 224×15 @ (27,57)，用贝塞尔采样
    def bez(p0,p1,p2,p3,n=40):
        return [((1-t)**3*p0[0]+3*(1-t)**2*t*p1[0]+3*(1-t)*t**2*p2[0]+t**3*p3[0],(1-t)**3*p0[1]+3*(1-t)**2*t*p1[1]+3*(1-t)*t**2*p2[1]+t**3*p3[1]) for t in [i/n for i in range(n+1)]]
    top=bez((4,15),(70,6),(220,2),(316,7));bot=bez((316,7),(230,8),(100,13),(12,19))
    sx,sy=224*S/320,15*S/22
    poly=[(27*S+x*sx,57*S+y*sy) for x,y in top+bot]
    d.polygon(poly,fill=ACCENT)
    return im
def stamp(src,dst,pos='top-right',wr=0.20,text=TEXT):
    base=Image.open(src).convert('RGBA');W,H=base.size
    wm=wordmark(int(W*wr),text)
    mx,my=int(W*0.04),int(H*0.03)
    x={'top-right':W-wm.width-mx,'bottom-right':W-wm.width-mx,'bottom-left':mx}[pos]
    y={'top-right':my,'bottom-right':H-wm.height-my,'bottom-left':H-wm.height-my}[pos]
    # 柔和投影保证浅底可读
    sh=Image.new('RGBA',base.size,(0,0,0,0));a=wm.split()[3]
    shl=Image.new('RGBA',wm.size,(0,0,0,140));shl.putalpha(a)
    sh.paste(shl,(x,y+int(wm.height*0.04)),shl);sh=sh.filter(ImageFilter.GaussianBlur(radius=max(2,wm.width//60)))
    base=Image.alpha_composite(base,sh);base.paste(wm,(x,y),wm)
    base.convert('RGB').save(dst,quality=95);print('stamped',dst,base.size,'wordmark',wm.size,'at',(x,y))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('src');ap.add_argument('dst');ap.add_argument('--pos',default='top-right');ap.add_argument('--width',type=float,default=0.22);ap.add_argument('--text',default=TEXT)
    a=ap.parse_args();stamp(a.src,a.dst,a.pos,a.width,a.text)

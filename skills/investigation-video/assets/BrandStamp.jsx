import React from 'react';
import {staticFile} from 'remotion';

// 签名字标：四角星芒 + 手写体签名 + 甩笔底划。signature / accent / wordmark 由 brand 配置传入，这里的默认值只是占位。
// Pass the generated brand profile; WorkflowBrand is registered by the composition.
export function BrandStamp({brand={},dark=false,right=75,top=33,scale=1}) {
  const accent=brand.accent || '#A5B0E3';
  const signature=brand.signature || 'RayTalk';
  if(brand.logoFile)return <img alt={signature} src={staticFile(brand.logoFile)} style={{position:'absolute',right,top,width:265*scale,objectFit:'contain'}}/>;
  return <div aria-label={brand.wordmark || 'RayTalk'} style={{position:'absolute',right,top,width:265,height:84,color:dark?'#fafaf8':(brand.ink || '#20262d'),transform:`scale(${scale})`,transformOrigin:'top right',pointerEvents:'none'}}>
    {brand.sparkle !== false && <svg viewBox="0 0 40 40" style={{position:'absolute',left:0,top:1,width:24,height:24}}><path d="M20 0 L24 15 L40 20 L24 25 L20 40 L16 25 L0 20 L16 15 Z" fill={accent}/></svg>}
    <div style={{position:'absolute',left:24,top:0,fontFamily:brand.fontFamily || 'WorkflowBrand',fontSize:55,fontWeight:600,lineHeight:1.05,letterSpacing:1,textShadow:dark?'0 2px 6px #0007':'none'}}>{signature}</div>
    {brand.underline !== false && <svg viewBox="0 0 320 22" preserveAspectRatio="none" style={{position:'absolute',left:27,top:57,width:224,height:15}}><path d="M4 15 C 70 6 220 2 316 7 C 230 8 100 13 12 19 Z" fill={accent}/></svg>}
  </div>;
}

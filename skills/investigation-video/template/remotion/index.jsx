import React from 'react';
import {AbsoluteFill,Composition,registerRoot,useCurrentFrame,interpolate,staticFile} from 'remotion';
import {BrandStamp} from '../../assets/BrandStamp.jsx';
import profile from './profile.json';
function Demo(){
 const f=useCurrentFrame();const v=interpolate(f,[0,60],[0,1],{extrapolateRight:'clamp'});
 return <AbsoluteFill style={{background:'#f3f4f6',color:profile.brand.ink,fontFamily:'WorkflowBody',padding:100}}>
  <style>{`@font-face{font-family:WorkflowBrand;src:url('${staticFile(profile.brand.fontFile)}')}@font-face{font-family:WorkflowBody;src:url('${staticFile(profile.brand.bodyFontFile)}')}`}</style>
  <h1 style={{fontSize:70,color:profile.brand.accent,marginTop:100}}>调查画面模板</h1>
  <p style={{fontSize:38}}>这里替换本期真实素材、来源与动态图解。</p>
  <div style={{width:1100,height:36,background:'#ddd',marginTop:60}}><div style={{width:v*900,height:36,background:profile.brand.accent}}/></div>
  <p style={{fontSize:30}}>动画仅用于布局演示，不包含真实统计或案件结论。</p>
  <BrandStamp brand={profile.brand}/>
 </AbsoluteFill>;
}
registerRoot(()=> <Composition id="InvestigationVisual" component={Demo} width={1920} height={1080} fps={30} durationInFrames={180}/>);

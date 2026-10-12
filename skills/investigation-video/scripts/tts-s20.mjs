import fs from 'node:fs';
import path from 'node:path';
try{process.loadEnvFile(new URL('../.env',import.meta.url).pathname)}catch{}  // 仓库根目录 .env，见 .env.example
delete process.env.TTS_ENGINE;
process.env.VOLC_TTS_SPEED='20';   // 语速 +20 ≈ 1.2x
const {synthesize}=await import('./tts.mjs');
const base=import.meta.dirname;
const items=JSON.parse(fs.readFileSync(path.join(base,'sentences.json'),'utf8'));
let next=0, failed=false;
async function worker(){
 while(next<items.length&&!failed){
  const x=items[next++];
  const wav=path.join(base,'audio-s20',x.id+'.wav'), js=path.join(base,'audio-s20',x.id+'.json');
  if(fs.existsSync(js)){continue;}
  try{
   const r=await synthesize(x.tts||x.text,wav,{voice:'zh_male_liufei_uranus_bigtts'});
   fs.writeFileSync(js,JSON.stringify({...x,...r,speed:20},null,2));
   console.log(x.id,r.duration.toFixed(3));
  }catch(e){failed=true;console.error(x.id,e.message);}
 }
}
await Promise.all([worker(),worker()]);
if(failed)process.exitCode=1;
else{
 const audio=items.map(x=>JSON.parse(fs.readFileSync(path.join(base,'audio-s20',x.id+'.json'))));
 fs.writeFileSync(path.join(base,'audio-manifest-s20.json'),JSON.stringify(audio,null,2));
 console.log('TOTAL',audio.reduce((s,x)=>s+x.duration,0));
}

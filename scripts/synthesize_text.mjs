// Native Volc narration for investigation projects or standalone text.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const cfg=JSON.parse(fs.readFileSync(path.join(root,'config.json'),'utf8'));
if(cfg.tts.engine!=='volc')throw new Error('Select tts.engine=volc first; other engines use your own generated audio.');
if(process.argv.length<4)throw new Error('Usage: node scripts/synthesize_text.mjs narration.txt output.wav');
const envFile=path.join(root,'.env');if(fs.existsSync(envFile))process.loadEnvFile(envFile);
if(cfg.tts.resourceId)process.env.VOLC_TTS_RESOURCE_ID=cfg.tts.resourceId;
if(cfg.tts.voice)process.env.VOLC_TTS_VOICE=cfg.tts.voice;
process.env.VOLC_TTS_SPEED=String(Math.round((cfg.tts.speed-1)*100));
const {synthesize}=await import('../skills/whiteboard-video/lib/tts/tts.mjs');
const text=fs.readFileSync(path.resolve(process.argv[2]),'utf8');
const output=path.resolve(process.argv[3]);fs.mkdirSync(path.dirname(output),{recursive:true});
const result=await synthesize(text,output,{voice:process.env.VOLC_TTS_VOICE});
fs.writeFileSync(output+'.json',JSON.stringify(result,null,2)+'\n');
console.log('NARRATION_GENERATED: audio plus provider word timestamps; verify pronunciation and coverage.');

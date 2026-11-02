const {chromium}=require('playwright');const {spawn}=require('child_process');const fs=require('fs');
const [,,html,out,cuts]=process.argv;const C=cuts.split(',').map(Number);
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1920}});
await pg.goto((process.env.BASEURL||'file://'+process.cwd()+'/')+html);await pg.evaluate(()=>document.fonts.ready);await pg.waitForFunction(()=>[...document.images,window.IMG,...(window.IMGS||[])].filter(Boolean).every(img=>img.complete&&img.naturalWidth>0),{timeout:180000});await pg.waitForTimeout(300);
const list=[];
for(let s=0;s<C.length-1;s++){const f0=Math.round(C[s]*30),f1=Math.round(C[s+1]*30);const tmp=`${out}_s${s}.tmp.mp4`,fin=`${out}_s${s}.mp4`;
 const ff=spawn('ffmpeg',['-loglevel','error','-y','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-r','30','-f','mp4',tmp]);
 for(let f=f0;f<f1;f++){const d=await pg.evaluate(t=>{draw(t);return document.getElementById('c').toDataURL('image/jpeg',0.92)},f/30);
  const buf=Buffer.from(d.split(',')[1],'base64');if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));}
 ff.stdin.end();const code=await new Promise(r=>ff.on('close',r));if(code!==0)throw 'ffmpeg '+code;fs.renameSync(tmp,fin);list.push(`file '${fin}'`);console.log('scene',s);}
fs.writeFileSync(out+'_list.txt',list.join('\n'));await b.close();})();

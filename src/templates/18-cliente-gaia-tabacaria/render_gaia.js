// node render_gaia.js out/video [snap t1,t2,...]  — renderiza (ou tira prints) carregando quadros sob demanda.
const {chromium}=require('playwright');const {spawn}=require('child_process');const fs=require('fs');const http=require('http');const path=require('path');
const [,,out,snap]=process.argv;const ROOT=__dirname;
const srv=http.createServer((q,r)=>{const f=path.join(ROOT,decodeURIComponent(q.url.split('?')[0]));fs.readFile(f,(e,d)=>{if(e){r.writeHead(404);return r.end();}r.writeHead(200,{'Content-Type':f.endsWith('.html')?'text/html':f.endsWith('.js')?'text/javascript':f.endsWith('.woff2')?'font/woff2':f.endsWith('.png')?'image/png':'image/jpeg'});r.end(d);});}).listen(0);
(async()=>{const port=srv.address().port;const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1920}});pg.on('pageerror',e=>console.log('ERR',e.message));
await pg.goto(`http://localhost:${port}/index.html`);await pg.evaluate(async()=>{await document.fonts.load('400 50px Bebas');await document.fonts.load('700 50px Cinzel');await new Promise(r=>{const i=new Image();i.onload=r;i.src='logo_gaia.png';});});
const grab=async t=>pg.evaluate(async t=>{await prep(t);draw(t);return document.getElementById('c').toDataURL('image/jpeg',0.93)},t);
if(snap){const ts=snap.split(',').map(Number);for(const t of ts){const d=await grab(t);fs.writeFileSync(`${out}_${t}.jpg`,Buffer.from(d.split(',')[1],'base64'));}await b.close();srv.close();return;}
const DUR=await pg.evaluate(()=>window.DUR);const N=Math.round(DUR*30);
const ff=spawn('ffmpeg',['-loglevel','error','-y','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-r','30',out+'.mp4']);
for(let f=0;f<N;f++){const d=await grab(f/30);const buf=Buffer.from(d.split(',')[1],'base64');if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));if(f%150==0)console.log('frame',f,'/',N);}
ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();srv.close();console.log('ok');})();

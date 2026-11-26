// node render.js out/video            → renderiza (30fps)      node render.js out/s 1.2,3.4 → prints
const {chromium}=require('playwright');const {spawn}=require('child_process');const fs=require('fs');const http=require('http');const path=require('path');
const [,,out,snap]=process.argv;const ROOT=__dirname;
const TY={'.html':'text/html','.js':'text/javascript','.woff2':'font/woff2','.otf':'font/otf'};
const srv=http.createServer((q,r)=>{const f=path.join(ROOT,decodeURIComponent(q.url.split('?')[0]));fs.readFile(f,(e,d)=>{if(e){r.writeHead(404);return r.end();}r.writeHead(200,{'Content-Type':TY[path.extname(f)]||'application/octet-stream'});r.end(d);});}).listen(0);
(async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});const pg=await b.newPage({viewport:{width:1080,height:1920}});pg.on('pageerror',e=>console.log('ERR',e.message));
await pg.goto(`http://localhost:${srv.address().port}/index.html`);await pg.waitForFunction(()=>window.ready,{timeout:120000});
const grab=t=>pg.evaluate(t=>{draw(t);return document.getElementById('c').toDataURL('image/jpeg',0.94)},t);
if(snap){for(const t of snap.split(',').map(Number)){const d=await grab(t);fs.writeFileSync(`${out}_${t}.jpg`,Buffer.from(d.split(',')[1],'base64'));}}
else{const N=Math.round(await pg.evaluate(()=>window.DUR)*30);const ff=spawn('ffmpeg',['-loglevel','error','-y','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-r','30',out+'.mp4']);
 const t0=Date.now();for(let f=0;f<N;f++){const buf=Buffer.from((await grab(f/30)).split(',')[1],'base64');if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));if(f%120==0)console.log('frame',f,'/',N,((Date.now()-t0)/1000|0)+'s');}
 ff.stdin.end();await new Promise(r=>ff.on('close',r));console.log('ok');}
await b.close();srv.close();})();

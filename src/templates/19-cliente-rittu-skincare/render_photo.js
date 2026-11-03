// node render_photo.js <saida.png> <vista> <amostras> [w] [h]   → foto por path tracing
const {chromium}=require('playwright');const fs=require('fs');const http=require('http');const path=require('path');const ROOT=__dirname;
const [,,out,view='serum',spp='64',w='1080',h='1920']=process.argv;
const TY={'.html':'text/html','.js':'text/javascript','.woff2':'font/woff2'};
const srv=http.createServer((q,r)=>{const f=path.join(ROOT,decodeURIComponent(q.url.split('?')[0]));fs.readFile(f,(e,d)=>{if(e){r.writeHead(404);return r.end();}r.writeHead(200,{'Content-Type':TY[path.extname(f)]||'application/octet-stream'});r.end(d);});}).listen(0);
(async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});const pg=await b.newPage({viewport:{width:+w,height:+h}});
pg.on('pageerror',e=>console.log('ERR',e.message,(e.stack||'').split('\n').slice(0,4).join(' | ')));pg.on('console',m=>{if(m.type()==='error')console.log('CONSOLE',m.text().slice(0,200));});
await pg.goto(`http://localhost:${srv.address().port}/photo.html?v=${view}&w=${w}&h=${h}`);await pg.waitForFunction(()=>window.ready,{timeout:300000});
const t0=Date.now();let s=0;while(s<+spp){s=await pg.evaluate(()=>step(4));if(s%16<4)console.log('spp',s,((Date.now()-t0)/1000|0)+'s');}
const d=await pg.evaluate(()=>png());fs.writeFileSync(out,Buffer.from(d.split(',')[1],'base64'));console.log('ok',out);await b.close();srv.close();})();

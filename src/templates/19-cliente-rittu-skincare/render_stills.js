// node render_stills.js <pasta>  → PNG 2048x2048 de cada vista, com estúdio e com fundo transparente
const {chromium}=require('playwright');const fs=require('fs');const http=require('http');const path=require('path');const ROOT=__dirname;const out=process.argv[2];const ONLY=process.argv[3]?process.argv[3].split(','):null;const SZ=process.argv[4]||'w=2048&h=2048';fs.mkdirSync(out,{recursive:true});
const TY={'.html':'text/html','.js':'text/javascript','.woff2':'font/woff2'};
const srv=http.createServer((q,r)=>{const f=path.join(ROOT,decodeURIComponent(q.url.split('?')[0]));fs.readFile(f,(e,d)=>{if(e){r.writeHead(404);return r.end();}r.writeHead(200,{'Content-Type':TY[path.extname(f)]||'application/octet-stream'});r.end(d);});}).listen(0);
(async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});const pg=await b.newPage({viewport:{width:2048,height:2048}});pg.on('pageerror',e=>console.log('ERR',e.message));
await pg.goto(`http://localhost:${srv.address().port}/stills.html?${SZ}`);await pg.waitForFunction(()=>window.ready,{timeout:120000});
for(const n of (ONLY||await pg.evaluate(()=>names)))for(const clean of [false,true]){const d=await pg.evaluate(([n,c])=>shot(n,c),[n,clean]);fs.writeFileSync(path.join(out,`rittu_${n}${clean?'_transparente':'_estudio'}.png`),Buffer.from(d.split(',')[1],'base64'));console.log(n,clean);}
await b.close();srv.close();})();

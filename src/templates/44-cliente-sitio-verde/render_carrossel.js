// node render_carrossel.js <pasta de saída> → gera carrossel_1.png … carrossel_N.png (1080x1350)
const {chromium}=require('playwright');const fs=require('fs'),http=require('http'),path=require('path');const out=process.argv[2]||'out';const ROOT=__dirname;
const TY={'.html':'text/html','.js':'text/javascript','.woff2':'font/woff2','.ttf':'font/ttf','.png':'image/png','.jpg':'image/jpeg'};
const srv=http.createServer((q,r)=>{const f=path.join(ROOT,decodeURIComponent(q.url.split('?')[0]));fs.readFile(f,(e,d)=>{if(e){r.writeHead(404);return r.end();}r.writeHead(200,{'Content-Type':TY[path.extname(f)]||'application/octet-stream'});r.end(d);});}).listen(0);
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1350}});pg.on('pageerror',e=>console.log('ERR',e.message));
await pg.goto(`http://localhost:${srv.address().port}/carrossel.html`);await pg.waitForFunction(()=>window.ready,{timeout:60000});fs.mkdirSync(out,{recursive:true});
const n=await pg.evaluate(()=>window.N);for(let i=0;i<n;i++){const d=await pg.evaluate(i=>{draw(i);return document.getElementById('c').toDataURL('image/png')},i);fs.writeFileSync(path.join(out,`carrossel_${i+1}.png`),Buffer.from(d.split(',')[1],'base64'));}
console.log('ok',n);await b.close();srv.close();})();

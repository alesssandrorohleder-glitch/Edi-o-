// node still.js saida.png 1.3  → imagem estática 3840×1920 em PNG (sem perda)
const {chromium}=require('playwright');const fs=require('fs');const http=require('http');const path=require('path');
const [,,out,t='1.3']=process.argv;const TY={'.html':'text/html','.woff2':'font/woff2'};
const srv=http.createServer((q,r)=>{fs.readFile(path.join(__dirname,decodeURIComponent(q.url.split('?')[0])),(e,d)=>{if(e){r.writeHead(404);return r.end();}r.writeHead(200,{'Content-Type':TY[path.extname(q.url.split('?')[0])]||'application/octet-stream'});r.end(d);});}).listen(0);
(async()=>{const b=await chromium.launch();const pg=await b.newPage();await pg.goto(`http://localhost:${srv.address().port}/index.html`);await pg.waitForFunction(()=>window.ready);
const d=await pg.evaluate(t=>{draw(t);return document.getElementById('c').toDataURL('image/png')},+t);fs.writeFileSync(out,Buffer.from(d.split(',')[1],'base64'));await b.close();srv.close();})();

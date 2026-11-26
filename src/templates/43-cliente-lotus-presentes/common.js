// Lótus Presentes de Luxo — kit visual (Reels 1080x1920 e carrossel 1080x1350): bordô + dourado + creme, Playfair Display + Cormorant + Poppins
export const TAU=Math.PI*2,cl=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)),p=(t,a,b)=>cl((t-a)/(b-a)),lerp=(a,b,k)=>a+(b-a)*k;
export const eo=k=>1-(1-cl(k))**3,eio=k=>{k=cl(k);return k<.5?4*k*k*k:1-(-2*k+2)**3/2;},eob=k=>{k=cl(k);const s=1.4;return 1+(s+1)*(k-1)**3+s*(k-1)**2;};
export const BOR='#7E1D3B',BOR2='#3E0A1C',GOLD='#D8B56A',CREAM='#F7F0E6',INK='#3A0E1E';
export async function loadAll(){for(const f of['700 80px PF','italic 400 80px PFI','500 80px Corm','italic 300 80px Corm','400 60px Pop','500 60px Pop'])await document.fonts.load(f);
  const L=s=>new Promise(r=>{const i=new Image();i.onload=()=>r(i);i.src=s;});const I={};for(const n of['rosas','colorido','margaridas','logo','p_50rosas','p_12rosas','p_7girassois','p_vangogh'])I[n]=await L(`midia/${n}${n=='logo'||n.startsWith('p_')?'.png':'.jpg'}`);return I;}
export function goldFill(g,y0,y1){const gr=g.createLinearGradient(0,y0,0,y1);gr.addColorStop(0,'#F6E2A9');gr.addColorStop(.45,GOLD);gr.addColorStop(.6,'#A9792F');gr.addColorStop(1,'#EBCB80');return gr;}
const FONT={PF:'700 SZpx PF',PFI:'italic 400 SZpx PFI',Corm:'500 SZpx Corm',CormI:'italic 300 SZpx Corm',Pop:'400 SZpx Pop',PopM:'500 SZpx Pop'};
export function T(g,s,x,y,size,col,o={}){const{f='Pop',al='center',ls=0,a=1,sh=0}=o;if(a<=0)return;g.save();g.globalAlpha*=a;g.font=FONT[f].replace('SZ',size);g.textAlign=al;g.textBaseline='alphabetic';if(ls)g.letterSpacing=ls+'px';
  const mw=o.mw||960,w0=g.measureText(s).width;if(w0>mw){g.translate(x,y);g.scale(mw/w0,1);g.translate(-x,-y);}
  if(sh){g.shadowColor='rgba(0,0,0,.5)';g.shadowBlur=sh;g.shadowOffsetY=sh/4;}g.fillStyle=col=='gold'?goldFill(g,y-size,y+size*.2):col;g.fillText(s,x,y);g.restore();}
// texto que sobe de uma máscara (revelação de grife)
export function rise(g,s,x,y,size,col,k,o={}){if(k<=0)return;g.save();g.beginPath();g.rect(0,y-size*1.1,g.canvas.width,size*1.45);g.clip();T(g,s,x,y+(1-eo(k))*size*1.2,size,col,o);g.restore();}
export function caps(g,s,x,y,size,k,col=CREAM,o={}){if(k<=0)return;T(g,s,x,y,size,col,{f:o.f||'PopM',ls:lerp(size*.5,size*.25,eo(k)),a:eo(k),sh:o.sh??0,mw:o.mw});}
export function goldLine(g,x,y,w,k,th=2){if(k<=0)return;g.save();g.strokeStyle=goldFill(g,y-2,y+2);g.lineWidth=th;g.beginPath();g.moveTo(x-w/2*eio(k),y);g.lineTo(x+w/2*eio(k),y);g.stroke();g.restore();}
export function dust(g,W,H,t,n=40){g.save();g.globalCompositeOperation='lighter';for(let i=0;i<n;i++){const s=(i*0.618)%1,x=(s*W+Math.sin(t*.4+i)*40)%W,y=(H-((t*(18+i%7*6)+i*97)%(H+40))),r=1.5+(i%4);
  const a=.25+.25*Math.sin(t*2+i);g.fillStyle=`rgba(246,226,169,${a})`;g.beginPath();g.arc(x,y,r,0,TAU);g.fill();}g.restore();}
export function borBg(g,W,H,t){const gr=g.createRadialGradient(W/2,H*.4,40,W/2,H*.5,H*.85);gr.addColorStop(0,'#962646');gr.addColorStop(.55,BOR);gr.addColorStop(1,BOR2);g.fillStyle=gr;g.fillRect(0,0,W,H);dust(g,W,H,t);}
export function creamBg(g,W,H,t){const gr=g.createLinearGradient(0,0,W,H);gr.addColorStop(0,'#FBF6EF');gr.addColorStop(1,'#EFE3D3');g.fillStyle=gr;g.fillRect(0,0,W,H);
  g.save();g.globalAlpha=.022;g.fillStyle='#000';for(let i=0;i<5;i++){g.save();g.translate(W*.75,0);g.rotate(.5);g.fillRect(i*140-200+Math.sin(t*.3)*20,-200,50,H*2);g.restore();}g.restore();}
export function photo(g,img,W,H,k,z0=1.0,z1=1.08,px=0,py=0){const z=lerp(z0,z1,cl(k)),s=Math.max(W/img.width,H/img.height)*z,w=img.width*s,h=img.height*s;g.drawImage(img,(W-w)/2+px*k,(H-h)/2+py*k,w,h);}
export function sweep(g,W,H,k){if(k<=0||k>=1)return;g.save();g.globalCompositeOperation='lighter';const x=lerp(-400,W+400,eio(k));const gr=g.createLinearGradient(x-200,0,x+200,0);gr.addColorStop(0,'rgba(255,240,210,0)');gr.addColorStop(.5,'rgba(255,240,210,.22)');gr.addColorStop(1,'rgba(255,240,210,0)');g.fillStyle=gr;g.fillRect(0,0,W,H);g.restore();}
export function shade(g,W,H,y0,a=.9){const gr=g.createLinearGradient(0,y0,0,H);gr.addColorStop(0,'rgba(62,10,28,0)');gr.addColorStop(1,`rgba(62,10,28,${a})`);g.fillStyle=gr;g.fillRect(0,y0,W,H-y0);}
export function logo(g,I,x,y,r,k=1){if(k<=0)return;g.save();g.globalAlpha=cl(k*2);const e=lerp(.9,1,eo(k));g.translate(x,y);g.scale(e,e);g.shadowColor='rgba(0,0,0,.45)';g.shadowBlur=40;g.beginPath();g.arc(0,0,r+6,0,TAU);g.fillStyle=goldFill(g,-r,r);g.fill();g.shadowBlur=0;g.drawImage(I.logo,-r,-r,2*r,2*r);g.restore();}
export function pillBtn(g,s,x,y,k,size=42){if(k<=0)return;g.save();g.font=`500 ${size}px Pop`;const w=g.measureText(s).width+size*2.4,h=size*2.1;g.translate(x,y);g.globalAlpha=cl(k*2);g.scale(lerp(.92,1,eo(k)),lerp(.92,1,eo(k)));
  g.beginPath();g.roundRect(-w/2,-h/2,w,h,h/2);g.fillStyle=CREAM;g.fill();g.fillStyle=BOR;g.beginPath();g.arc(-w/2+h/2,0,h/2-8,0,TAU);g.fill();g.strokeStyle=CREAM;g.lineWidth=5;g.beginPath();g.moveTo(-w/2+h/2-14,0);g.lineTo(-w/2+h/2+14,0);g.moveTo(-w/2+h/2+2,-12);g.lineTo(-w/2+h/2+14,0);g.lineTo(-w/2+h/2+2,12);g.stroke();
  g.fillStyle=BOR;g.textAlign='center';g.textBaseline='middle';g.fillText(s,h/2-6,4);g.restore();}
// ícones de linha dourada
export function icon(g,kind,x,y,s,k){if(k<=0)return;g.save();g.translate(x,y);g.scale(s*lerp(.8,1,eo(k)),s*lerp(.8,1,eo(k)));g.globalAlpha=cl(k*2);g.strokeStyle=goldFill(g,-60,60);g.lineWidth=5;g.lineCap='round';g.lineJoin='round';g.beginPath();
  if(kind=='loja'){g.moveTo(-50,-10);g.lineTo(-50,50);g.lineTo(50,50);g.lineTo(50,-10);g.moveTo(-60,-10);g.lineTo(-45,-50);g.lineTo(45,-50);g.lineTo(60,-10);g.closePath();g.moveTo(-15,50);g.lineTo(-15,15);g.lineTo(15,15);g.lineTo(15,50);}
  if(kind=='seguro'){g.moveTo(0,-55);g.lineTo(45,-38);g.lineTo(45,5);g.quadraticCurveTo(40,40,0,58);g.quadraticCurveTo(-40,40,-45,5);g.lineTo(-45,-38);g.closePath();g.moveTo(-18,2);g.lineTo(-4,16);g.lineTo(22,-14);}
  if(kind=='pessoa'){g.arc(0,-25,22,0,TAU);g.moveTo(-42,55);g.quadraticCurveTo(-40,8,0,8);g.quadraticCurveTo(40,8,42,55);}
  if(kind=='relogio'){g.arc(0,0,50,0,TAU);g.moveTo(0,0);g.lineTo(0,-30);g.moveTo(0,0);g.lineTo(22,12);}
  if(kind=='pin'){g.moveTo(0,55);g.quadraticCurveTo(-48,0,-40,-25);g.arc(0,-25,40,Math.PI,0);g.quadraticCurveTo(48,0,0,55);g.moveTo(14,-25);g.arc(0,-25,14,0,TAU);}
  if(kind=='presente'){g.rect(-48,-10,96,62);g.rect(-55,-30,110,22);g.moveTo(0,-30);g.lineTo(0,52);g.moveTo(0,-30);g.quadraticCurveTo(-35,-70,-30,-35);g.moveTo(0,-30);g.quadraticCurveTo(35,-70,30,-35);}
  g.stroke();g.restore();}
// produto recortado (fundo transparente) com sombra suave no chão
export function product(g,img,x,y,hgt,k=1){if(k<=0)return;const s=hgt/img.height,w=img.width*s;g.save();g.globalAlpha=cl(k*2);const yy=y+(1-eo(k))*60;
  g.fillStyle='rgba(62,10,28,.18)';g.beginPath();g.ellipse(x,yy+hgt/2-70,w*.3,22,0,0,TAU);g.fill();g.drawImage(img,x-w/2,yy-hgt/2,w,hgt);g.restore();}
export function price(g,de,por,x,y,k=1,col='#7E1D3B'){if(k<=0)return;T(g,de,x,y,36,'rgba(58,14,30,.55)',{f:'Pop',a:k});g.save();g.globalAlpha=k*.55;g.font='400 36px Pop';const w=g.measureText(de).width;g.strokeStyle='#3A0E1E';g.lineWidth=3;g.beginPath();g.moveTo(x-w/2,y-12);g.lineTo(x+w/2,y-12);g.stroke();g.restore();
  T(g,por,x,y+78,72,col,{f:'PF',a:k});}

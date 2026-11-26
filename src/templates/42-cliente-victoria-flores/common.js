// Victoria Flores — kit visual compartilhado (Reels 1080x1920 e carrossel 1080x1350)
export const TAU=Math.PI*2,cl=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)),p=(t,a,b)=>cl((t-a)/(b-a)),lerp=(a,b,k)=>a+(b-a)*k;
export const eo=k=>1-(1-cl(k))**3,eio=k=>{k=cl(k);return k<.5?4*k*k*k:1-(-2*k+2)**3/2;},eob=k=>{k=cl(k);const s=1.6;return 1+(s+1)*(k-1)**3+s*(k-1)**2;};
export const WINE='#5A0B16',WINE2='#1A0306',GOLD='#E2C27A',GOLD2='#B8893A',CREAM='#FBF3E8',ROSE='#C8102E';
export async function loadAll(){for(const f of['80px GV','500 80px Corm','italic 300 80px Corm','400 60px Jost','400 60px Pop','500 60px Pop'])await document.fonts.load(f);
  const L=s=>new Promise(r=>{const i=new Image();i.onload=()=>r(i);i.src=s;});const I={};for(const n of['rosas','lirios','girassois','kit','logo'])I[n]=await L(`midia/${n}${n=='logo'?'.png':'.jpg'}`);return I;}
export function goldFill(g,y0,y1){const gr=g.createLinearGradient(0,y0,0,y1);gr.addColorStop(0,'#F7E3A8');gr.addColorStop(.45,GOLD);gr.addColorStop(.55,GOLD2);gr.addColorStop(1,'#F2D58C');return gr;}
export function T(g,s,x,y,size,col,o={}){const{f='Pop',w=400,al='center',ls=0,a=1,sh=0,st=0}=o;if(a<=0)return;g.save();g.globalAlpha*=a;g.font=`${f=='Corm'&&o.it?'italic 300':w} ${size}px ${f}`;g.textAlign=al;g.textBaseline='alphabetic';
  if(ls)g.letterSpacing=ls+'px';{const mw=o.mw||960,w0=g.measureText(s).width;if(w0>mw){g.translate(x,y);g.scale(mw/w0,1);g.translate(-x,-y);}}if(sh){g.shadowColor='rgba(0,0,0,.55)';g.shadowBlur=sh;g.shadowOffsetY=sh/4;}g.fillStyle=col=='gold'?goldFill(g,y-size,y+size*.2):col;g.fillText(s,x,y);g.restore();}
// texto escrito à mão (revela da esquerda p/ direita)
export function script(g,s,x,y,size,k,o={}){if(k<=0)return;g.save();g.font=`${size}px GV`;const w=g.measureText(s).width;g.beginPath();g.rect(x-w/2-40,y-size*1.2,(w+80)*eio(k),size*1.8);g.clip();T(g,s,x,y,size,o.col||'gold',{f:'GV',sh:o.sh??18});g.restore();}
export function caps(g,s,x,y,size,k,col=CREAM,o={}){if(k<=0)return;T(g,s,x,y+(1-eo(k))*30,size,col,{f:'Corm',w:500,ls:lerp(size*.4,size*.12,eo(k)),a:eo(k),sh:o.sh??12});}
export function wineBg(g,W,H,t){const gr=g.createRadialGradient(W/2,H*.42,50,W/2,H*.5,H*.8);gr.addColorStop(0,'#7A1020');gr.addColorStop(.55,WINE);gr.addColorStop(1,WINE2);g.fillStyle=gr;g.fillRect(0,0,W,H);
  g.save();g.globalAlpha=.06;for(let i=0;i<6;i++){g.strokeStyle=GOLD;g.lineWidth=2;g.beginPath();g.arc(W/2,H*.5,300+i*140+Math.sin(t+i)*10,0,TAU);g.stroke();}g.restore();}
// pétala de rosa
export function petal(g,x,y,s,a,col='#B3122B'){g.save();g.translate(x,y);g.rotate(a);g.scale(s,s);const gr=g.createRadialGradient(-6,-8,2,0,0,30);gr.addColorStop(0,'#E8354F');gr.addColorStop(.7,col);gr.addColorStop(1,'#6E0715');
  g.fillStyle=gr;g.beginPath();g.moveTo(0,-26);g.bezierCurveTo(24,-26,30,6,0,28);g.bezierCurveTo(-30,6,-24,-26,0,-26);g.fill();g.strokeStyle='rgba(255,255,255,.15)';g.lineWidth=2;g.beginPath();g.moveTo(0,-20);g.quadraticCurveTo(6,0,0,22);g.stroke();g.restore();}
export function petals(g,W,H,t,n=26,sp=1){for(let i=0;i<n;i++){const s=(i*0.618)%1,x=(s*W+Math.sin(t*.9+i)*60+W)%W,y=((t*(120+i%5*40)*sp+i*173)%(H+200))-100;petal(g,x,y,.8+(i%4)*.35,t*(.6+i%3*.3)+i);}}
// foto com "Ken Burns" (cobre o quadro)
export function photo(g,img,W,H,t,z0=1.0,z1=1.08,px=0,py=0){const k=cl(t),z=lerp(z0,z1,k),s=Math.max(W/img.width,H/img.height)*z,w=img.width*s,h=img.height*s;g.drawImage(img,(W-w)/2+px*k,(H-h)/2+py*k,w,h);}
export function shade(g,W,H,y0,a=.85){const gr=g.createLinearGradient(0,y0,0,H);gr.addColorStop(0,'rgba(26,3,6,0)');gr.addColorStop(1,`rgba(26,3,6,${a})`);g.fillStyle=gr;g.fillRect(0,y0,W,H-y0);}
export function frame(g,W,H,m=36,a=1){g.save();g.globalAlpha=a;g.strokeStyle=goldFill(g,0,H);g.lineWidth=3;g.strokeRect(m,m,W-2*m,H-2*m);g.lineWidth=1.5;g.strokeRect(m+12,m+12,W-2*m-24,H-2*m-24);g.restore();}
export function logo(g,I,x,y,r,k=1){if(k<=0)return;g.save();g.globalAlpha=cl(k*2);const e=eob(k);g.translate(x,y);g.scale(e,e);g.shadowColor='rgba(0,0,0,.5)';g.shadowBlur=40;g.beginPath();g.arc(0,0,r+10,0,TAU);g.fillStyle=goldFill(g,-r,r);g.fill();g.shadowBlur=0;g.drawImage(I.logo,-r,-r,2*r,2*r);g.restore();}
export function pillBtn(g,s,x,y,k,size=46){if(k<=0)return;g.save();g.font=`500 ${size}px Pop`;const w=g.measureText(s).width+size*2.2,h=size*2;g.translate(x,y);const e=eob(k);g.scale(e,e);
  g.beginPath();g.roundRect(-w/2,-h/2,w,h,h/2);g.fillStyle='#25D366';g.shadowColor='rgba(0,0,0,.4)';g.shadowBlur=24;g.fill();g.shadowBlur=0;g.fillStyle='#fff';g.textAlign='center';g.textBaseline='middle';g.fillText(s,0,4);g.restore();}
export function pin(g,x,y,s,col=ROSE){g.save();g.translate(x,y);g.scale(s,s);g.fillStyle=col;g.beginPath();g.arc(0,-60,40,Math.PI,0);g.quadraticCurveTo(40,-30,0,0);g.quadraticCurveTo(-40,-30,-40,-60);g.fill();g.fillStyle=CREAM;g.beginPath();g.arc(0,-60,15,0,TAU);g.fill();g.restore();}
export function moto(g,x,y,s,t){g.save();g.translate(x,y);g.scale(s,s);g.strokeStyle=CREAM;g.lineWidth=7;g.lineCap='round';g.lineJoin='round';const b=Math.sin(t*20)*2;
  for(const wx of[-70,70]){g.beginPath();g.arc(wx,0,32,0,TAU);g.stroke();}g.beginPath();g.moveTo(-70,0);g.lineTo(-20,-40+b);g.lineTo(40,-40+b);g.lineTo(70,0);g.moveTo(40,-40+b);g.lineTo(55,-80+b);g.lineTo(80,-80+b);g.stroke();
  g.fillStyle=ROSE;g.beginPath();g.roundRect(-100,-110+b,70,60,10);g.fill();g.fillStyle=CREAM;g.beginPath();g.arc(-10,-110+b,18,0,TAU);g.fill();g.restore();}

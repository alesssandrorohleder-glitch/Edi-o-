// Sítio Verde Hortifruti — kit visual (Reels 1080x1920): verde da marca + verde-limão + vermelho do pingo do logo, Poppins
export const TAU=Math.PI*2,cl=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)),p=(t,a,b)=>cl((t-a)/(b-a)),lerp=(a,b,k)=>a+(b-a)*k;
export const eo=k=>1-(1-cl(k))**3,eio=k=>{k=cl(k);return k<.5?4*k*k*k:1-(-2*k+2)**3/2;},eob=k=>{k=cl(k);const s=1.7;return 1+(s+1)*(k-1)**3+s*(k-1)**2;};
export const VERDE='#006636',VERDE2='#00431F',LIMAO='#8CC63F',VERM='#E3262C',BRANCO='#FFFFFF',CREME='#F6F8EE';
export const IMGS=['morangos','loja','copo','salada','cafe','adega','flores','delivery','brooklin','fachada','berinjela','pastel','logo'];
export async function loadAll(){for(const f of['700 80px Pop','500 60px Pop','400 60px Pop'])await document.fonts.load(f);
  const L=s=>new Promise(r=>{const i=new Image();i.onload=()=>r(i);i.src=s;});const I={};for(const n of IMGS)I[n]=await L(`midia/${n}.${n=='logo'?'png':'jpg'}`);return I;}
export function T(g,s,x,y,size,col,o={}){const{w=700,al='center',ls=0,a=1,sh=0}=o;if(a<=0)return;g.save();g.globalAlpha*=a;g.font=`${w} ${size}px Pop`;g.textAlign=al;g.textBaseline='alphabetic';if(ls)g.letterSpacing=ls+'px';
  const mw=o.mw||960,w0=g.measureText(s).width;if(w0>mw){g.translate(x,y);g.scale(mw/w0,1);g.translate(-x,-y);}if(sh){g.shadowColor='rgba(0,0,0,.45)';g.shadowBlur=sh;g.shadowOffsetY=sh/3;}g.fillStyle=col;g.fillText(s,x,y);g.restore();}
// palavra que entra com "pop" (escala com mola)
export function pop(g,s,x,y,size,col,k,o={}){if(k<=0)return;const e=eob(k);g.save();g.translate(x,y);g.scale(e,e);T(g,s,0,0,size,col,{...o,a:cl(k*3)});g.restore();}
export function rise(g,s,x,y,size,col,k,o={}){if(k<=0)return;g.save();g.beginPath();g.rect(0,y-size*1.05,g.canvas.width,size*1.35);g.clip();T(g,s,x,y+(1-eo(k))*size*1.15,size,col,o);g.restore();}
// etiqueta (faixa colorida atrás do texto)
export function tag(g,s,x,y,size,bg,fg,k,o={}){if(k<=0)return;g.save();g.font=`${o.w||700} ${size}px Pop`;const w=g.measureText(s).width+size*.9,h=size*1.35;const e=eo(k);g.translate(x,y);g.rotate(o.rot||0);
  g.beginPath();g.roundRect(-w/2,-h*.78,w*e,h,h*.22);g.fillStyle=bg;g.fill();g.beginPath();g.rect(-w/2,-h,w*e,h*1.4);g.clip();g.fillStyle=fg;g.textAlign='center';g.fillText(s,0,0);g.restore();}
export function photo(g,img,W,H,k,z0=1.0,z1=1.08,px=0,py=0){const z=lerp(z0,z1,cl(k)),s=Math.max(W/img.width,H/img.height)*z,w=img.width*s,h=img.height*s;g.drawImage(img,(W-w)/2+px*k,(H-h)/2+py*k,w,h);}
export function shadeB(g,W,H,y0,a=.85){const gr=g.createLinearGradient(0,y0,0,H);gr.addColorStop(0,'rgba(0,40,18,0)');gr.addColorStop(1,`rgba(0,40,18,${a})`);g.fillStyle=gr;g.fillRect(0,y0,W,H-y0);}
export function shadeT(g,W,y1,a=.55){const gr=g.createLinearGradient(0,0,0,y1);gr.addColorStop(0,`rgba(0,40,18,${a})`);gr.addColorStop(1,'rgba(0,40,18,0)');g.fillStyle=gr;g.fillRect(0,0,W,y1);}
// folhinhas caindo
export function leaf(g,x,y,s,a,col=LIMAO){g.save();g.translate(x,y);g.rotate(a);g.scale(s,s);g.fillStyle=col;g.beginPath();g.moveTo(0,-30);g.quadraticCurveTo(26,-6,0,30);g.quadraticCurveTo(-26,-6,0,-30);g.fill();g.strokeStyle='rgba(0,67,31,.5)';g.lineWidth=3;g.beginPath();g.moveTo(0,-24);g.lineTo(0,24);g.stroke();g.restore();}
export function leaves(g,W,H,t,n=16){for(let i=0;i<n;i++){const s=(i*0.618)%1,x=(s*W+Math.sin(t*1.1+i)*50+W)%W,y=((t*(140+i%5*40)+i*197)%(H+200))-100;leaf(g,x,y,.7+(i%3)*.3,t*(.8+i%3*.4)+i,i%4?LIMAO:'#B8DB6A');}}
export function greenBg(g,W,H,t){const gr=g.createLinearGradient(0,0,0,H);gr.addColorStop(0,'#007A40');gr.addColorStop(1,VERDE2);g.fillStyle=gr;g.fillRect(0,0,W,H);
  g.save();g.globalAlpha=.08;g.strokeStyle='#fff';g.lineWidth=10;for(let i=0;i<7;i++){g.beginPath();for(let x=-50;x<=W+50;x+=20)g.lineTo(x,200+i*260+Math.sin(x*.012+t*2+i)*24);g.stroke();}g.restore();}
export function dot(g,x,y,r,col=VERM){g.beginPath();g.arc(x,y,r,0,TAU);g.fillStyle=col;g.fill();}
export function logo(g,I,x,y,w,k=1){if(k<=0)return;const e=eob(k),h=w*I.logo.height/I.logo.width;g.save();g.translate(x,y);g.scale(e,e);g.globalAlpha=cl(k*3);g.shadowColor='rgba(0,0,0,.35)';g.shadowBlur=30;g.drawImage(I.logo,-w/2,-h/2,w,h);g.restore();}

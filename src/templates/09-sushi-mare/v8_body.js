
const W=1080,H=1920,c=document.getElementById('c');let x=c.getContext('2d');const X0=x;
const BK='#0A0A0B',RED='#C8342B',GOLD='#C9A45C',RICE='#F3EFE7',DIM='rgba(243,239,231,.62)';
const SANS='Inter,sans-serif',JP='"Noto Serif CJK JP","Noto Serif CJK SC",serif';
const cl=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)),p=(t,a,b)=>cl((t-a)/(b-a));
const eo=t=>1-Math.pow(1-t,3),eo5=t=>1-Math.pow(1-t,5),eio=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2,sine=t=>-(Math.cos(Math.PI*t)-1)/2;
const rnd=s=>{const r=Math.sin(s*127.1+311.7)*43758.5453;return r-Math.floor(r)};const lerp=(a,b,k)=>a+(b-a)*k;
function T(s,X,Y,size,col,{font=SANS,w=300,align='center',a=1,ls=0}={}){x.save();x.globalAlpha*=a;x.fillStyle=col;x.font=`${w} ${size}px ${font}`;x.textAlign=align;x.textBaseline='middle';x.letterSpacing=ls+'px';x.fillText(s,X,Y);x.restore();}
function reveal(s,X,Y,size,col,t,t0,o={}){const k=sine(p(t,t0,t0+1.0));if(k<=0)return;T(s,X,Y+(1-k)*14,size,col,{...o,a:k*(o.a??1),ls:(o.ls??0)+(1-k)*14});}
function vtext(s,X,Y,size,col,t,t0,a=1){[...s].forEach((ch,i)=>{const k=sine(p(t,t0+i*.18,t0+i*.18+.8));if(k<=0)return;T(ch,X,Y+i*size*1.15+(1-k)*16,size,col,{font:JP,w:500,a:k*a});});}
function line(X,Y,len,k,col=GOLD,a=1){if(k<=0)return;x.save();x.globalAlpha=a;x.fillStyle=col;x.fillRect(X-len/2*k,Y-1,len*k,2);x.restore();}
// atmospheric background
function bgDark(t,warm=.10){x.fillStyle=BK;x.fillRect(0,0,W,H);
  for(let i=0;i<3;i++){const cx=540+Math.sin(t*.15+i*2)*320,cy=900+Math.cos(t*.12+i*1.7)*500;const g=x.createRadialGradient(cx,cy,0,cx,cy,700);g.addColorStop(0,`rgba(${i==1?120:70},${i==1?40:55},${i==1?30:50},${warm})`);g.addColorStop(1,'rgba(0,0,0,0)');x.fillStyle=g;x.fillRect(0,0,W,H);}}
function grainVig(t){x.save();x.globalAlpha=.05;const f=Math.floor(t*24);for(let i=0;i<450;i++){x.fillStyle=i%2?'#fff':'#000';x.fillRect(rnd(i+f*1.3)*W,rnd(i*2.7+f)*H,2,2);}x.restore();
  const v=x.createRadialGradient(W/2,H/2,H*.28,W/2,H/2,H*.8);v.addColorStop(0,'rgba(0,0,0,0)');v.addColorStop(1,'rgba(0,0,0,.7)');x.fillStyle=v;x.fillRect(0,0,W,H);}
// textured vermilion sun
function sun(cx,cy,r,a=1){if(r<=0)return;x.save();x.globalAlpha=a;const g=x.createRadialGradient(cx-r*.3,cy-r*.3,r*.1,cx,cy,r);g.addColorStop(0,'#D8443A');g.addColorStop(1,'#A8261F');x.fillStyle=g;x.beginPath();x.arc(cx,cy,r,0,7);x.fill();
  x.globalAlpha=a*.12;for(let i=0;i<160;i++){const an=rnd(i)*7,rr=Math.sqrt(rnd(i*3))*r;x.fillStyle=i%2?'#000':'#fff';x.fillRect(cx+Math.cos(an)*rr,cy+Math.sin(an)*rr,2,2);}x.restore();}
// sumi-e brush stroke along a path
function brush(pts,k,wid,col,a=1){if(k<=0)return;const N=90;const sm=[];for(let i=0;i<=N;i++){const u=i/N*(pts.length-1);const j=Math.min(pts.length-2,Math.floor(u)),f=u-j;sm.push([lerp(pts[j][0],pts[j+1][0],f),lerp(pts[j][1],pts[j+1][1],f)]);}
  const n=Math.floor(N*cl(k));x.save();x.globalAlpha=a;x.strokeStyle=col;x.lineCap='round';
  for(let b=0;b<18;b++){const off=(b/17-.5)*wid;x.globalAlpha=a*(.35+.65*rnd(b*7));x.lineWidth=wid/14*(1+rnd(b)*1.5);x.beginPath();
    for(let i=0;i<=n;i++){const u=i/N;const taper=Math.sin(Math.PI*Math.min(1,u*1.15))**.6;const [px,py]=sm[i];const [qx,qy]=sm[Math.min(N,i+1)];const dx=qx-px,dy=qy-py,l=Math.hypot(dx,dy)||1;
      const gap=rnd(b*13+Math.floor(u*12))<.08&&u>.6;if(gap){x.moveTo(px-dy/l*off*taper,py+dx/l*off*taper);continue;}
      x.lineTo(px-dy/l*off*taper,py+dx/l*off*taper);}x.stroke();}x.restore();}
function product(im,cx,cy,w,t,t0,{drift=90,glow=true}={}){const k=eo5(p(t,t0,t0+1.4));if(k<=0)return;const h=w*im.height/im.width;const s=lerp(.94,1.0,eo(p(t,t0,t0+5)));
  const dx=(1-k)*drift;x.save();x.globalAlpha=k;
  if(glow){const g=x.createRadialGradient(cx,cy,0,cx,cy,w*.75);g.addColorStop(0,'rgba(201,164,92,.18)');g.addColorStop(1,'rgba(0,0,0,0)');x.fillStyle=g;x.fillRect(cx-w,cy-w,2*w,2*w);}
  x.fillStyle='rgba(0,0,0,.55)';x.filter='blur(18px)';x.beginPath();x.ellipse(cx+dx,cy+h*.45,w*.45,h*.08,0,0,7);x.fill();x.filter='none';
  x.translate(cx+dx,cy);x.scale(s,s);x.drawImage(im,-w/2,-h/2,w,h);
  // light sweep
  const sw=p(t,t0+1.2,t0+2.6);if(sw>0&&sw<1){x.globalCompositeOperation='source-atop';}
  x.restore();
  if(sw>0&&sw<1){ // sweep using offscreen
    const o=SW;const og=o.getContext('2d');o.width=Math.ceil(w);o.height=Math.ceil(h);og.clearRect(0,0,o.width,o.height);og.drawImage(im,0,0,w,h);og.globalCompositeOperation='source-atop';
    const sx=lerp(-w*.4,w*1.4,sine(sw));const gg=og.createLinearGradient(sx-90,0,sx+90,0);gg.addColorStop(0,'rgba(255,245,225,0)');gg.addColorStop(.5,'rgba(255,245,225,.35)');gg.addColorStop(1,'rgba(255,245,225,0)');og.fillStyle=gg;og.save();og.transform(1,0,-.3,1,0,0);og.fillRect(-w,0,3*w,h);og.restore();
    x.save();x.translate(cx+dx,cy);x.scale(s,s);x.drawImage(o,-w/2,-h/2);x.restore();}
}
const SW=document.createElement('canvas');
function titleBlock(en,pt,jp,t,t0,Y=1380){reveal(en,W/2,Y,64,RICE,t,t0,{w:300,ls:16});line(W/2,Y+60,160,eo(p(t,t0+.4,t0+1.2)));reveal(pt,W/2,Y+120,40,DIM,t,t0+.6,{w:300,ls:2});vtext(jp,110,520,58,GOLD,t,t0+.2,.95);}
function photo(im,t,{z0=1.12,z1=1.0,py0=0,py1=0,blur0=14,dur=5,dim=0}={}){const k=sine(p(t,0,dur));const z=lerp(z0,z1,k);const sc=Math.max(W/im.width,H/im.height)*z;const w=im.width*sc,h=im.height*sc;const bl=blur0*(1-eo(p(t,0,1.4)));
  x.save();if(bl>.3)x.filter=`blur(${bl}px)`;x.drawImage(im,(W-w)/2,(H-h)/2+lerp(py0,py1,k),w,h);x.restore();if(dim){x.fillStyle=`rgba(0,0,0,${dim})`;x.fillRect(0,0,W,H);}}

/* ---------------- SCENES ---------------- */
function s1(t){ // 0-5 opening
  bgDark(t,.06);
  sun(540,840,300*eo5(p(t,.6,2.2)),1);
  brush([[120,1120],[380,1090],[700,1110],[980,1060]],eio(p(t,.2,1.3)),70,'#E9E4DA',.9);
  const kk=sine(p(t,1.6,2.6));if(kk>0){T('海',540,840,300,RICE,{font:JP,w:900,a:kk});}
  reveal('UMI',W/2,1300,120,RICE,t,2.2,{w:200,ls:48});
  line(W/2,1385,260,eo(p(t,2.7,3.5)));
  reveal('SUSHI BAR  ·  OMAKASE',W/2,1450,40,GOLD,t,2.9,{w:400,ls:10});
}
function s2(t){ // 5-10 hero
  photo(IM.hero,t,{z0:1.14,z1:1.02,blur0:16});
  const g=x.createLinearGradient(0,H*.5,0,H*.74);g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(1,'rgba(0,0,0,.93)');x.fillStyle=g;x.fillRect(0,0,W,H);
  const g2=x.createLinearGradient(0,0,0,H*.25);g2.addColorStop(0,'rgba(0,0,0,.6)');g2.addColorStop(1,'rgba(0,0,0,0)');x.fillStyle=g2;x.fillRect(0,0,W,H);
  reveal('A arte',W/2,1380,96,RICE,t,1.6,{w:200,ls:6});
  reveal('do sushi.',W/2,1490,96,RICE,t,2.1,{w:200,ls:6});
  line(W/2,1560,200,eo(p(t,2.6,3.4)));
  vtext('職人の技',980,330,52,GOLD,t,2.4,.9);
}
function s3(t){ // 10-15 nigiri
  bgDark(t);sun(700,640,230*eo5(p(t,0,1.6)),.95);
  product(IM.nigiri,560,900,880,t,.2);
  titleBlock('SAKE NIGIRI','salmão fresco · corte do dia','握り',t,1.2);
}
function s4(t){ // 15-20 uramaki -> hot roll
  bgDark(t);sun(380,620,220*eo5(p(t,0,1.4)),.9);
  const out=eio(p(t,2.1,2.45));
  if(out<1){x.save();x.globalAlpha=1-out;product(IM.uramaki,560,920,700,t,.1);titleBlock('URAMAKI','arroz por fora · gergelim','裏巻き',t,.9);x.restore();}
  if(t>2.45){product(IM.hotroll,540,930,860,t,2.45,{drift:-90});titleBlock('HOT ROLL','crocante · molho tarê','揚げ巻',t,2.8);}
}
function s5(t){ // 20-25 temaki -> omakase
  bgDark(t,.12);sun(720,600,210*eo5(p(t,0,1.4)),.9);
  const out=eio(p(t,2.1,2.45));
  if(out<1){x.save();x.globalAlpha=1-out;product(IM.temaki,560,880,520,t,.1,{drift:0});titleBlock('TEMAKI','cone de alga · salmão','手巻き',t,.9);x.restore();}
  if(t>2.45){product(IM.chopnigiri,560,900,820,t,2.45);titleBlock('OMAKASE','a escolha do chef','お任せ',t,2.8);}
}
function s6(t){ // 25-30 platter / reservations
  photo(IM.hero,t,{z0:1.0,z1:1.16,py0:-60,py1:40,blur0:0,dim:.25});
  const g=x.createLinearGradient(0,H*.45,0,H*.68);g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(1,'rgba(0,0,0,.94)');x.fillStyle=g;x.fillRect(0,0,W,H);
  reveal('COMBINADOS',W/2,1260,72,RICE,t,.5,{w:300,ls:20});
  reveal('EXCLUSIVOS',W/2,1350,72,GOLD,t,.8,{w:300,ls:20});
  line(W/2,1420,200,eo(p(t,1.2,2.0)));
  reveal('Reserve sua mesa  ·  Delivery',W/2,1485,42,DIM,t,1.5,{w:300,ls:2});
}
function s7(t){ // 30-35 CTA
  bgDark(t,.06);sun(540,520,150*eo5(p(t,0,1.4)),.95);
  reveal('Esse restaurante não existe.',W/2,820,46,DIM,t,.4,{w:300,ls:2});
  reveal('Mas o vídeo do seu',W/2,940,70,RICE,t,1.0,{w:300,ls:2});
  reveal('pode ter esse nível.',W/2,1030,70,GOLD,t,1.3,{w:400,ls:2});
  line(W/2,1110,220,eo(p(t,1.8,2.6)));
  const bk=eo5(p(t,2.4,3.2));if(bk>0){x.save();x.globalAlpha=bk;x.strokeStyle=GOLD;x.lineWidth=2;x.beginPath();x.roundRect(W/2-330,1210,660,130,65);x.stroke();T('ME CHAMA NO DIRECT',W/2,1276,40,RICE,{w:500,ls:8});x.restore();}
  reveal('@alecreator_motion',W/2,1430,52,RICE,t,2.9,{w:300,ls:3});
  vtext('ありがとう',110,560,50,GOLD,t,1.6,.8);
}
const SC=[[s1,0,5],[s2,5,10],[s3,10,15],[s4,15,20],[s5,20,25],[s6,25,30],[s7,30,35]];
window.DUR=35;const XF=.7;
const buf=document.createElement('canvas');buf.width=W;buf.height=H;const bx=buf.getContext('2d');
window.draw=function(t){const i=SC.findIndex(([,a,b])=>t>=a&&t<b);const k=i<0?SC.length-1:i;const [f,a]=SC[k];
  x=X0;x.save();f(t-a);x.restore();
  if(k>0&&t-a<XF){const [pf,pa]=SC[k-1];x=bx;x.save();x.setTransform(1,0,0,1,0,0);x.globalAlpha=1;x.filter='none';pf(t-pa);x.restore();x=X0;
    const e=sine((t-a)/XF);x.save();x.globalAlpha=1-e;x.filter=`blur(${e*10}px)`;x.drawImage(buf,0,0);x.restore();}
  grainVig(t);
  const fi=1-p(t,0,.6),fo=p(t,34.3,35);const f2=Math.max(fi,fo);if(f2>0){x.fillStyle=`rgba(0,0,0,${f2})`;x.fillRect(0,0,W,H);}};
</script></body></html>

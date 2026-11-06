
const W=1080,H=1920,c=document.getElementById('c');let x=c.getContext('2d');const X0=x;
const BLK='#09090A',WH='#FFFFFF',LIME='#D4FF2A',GRY='#8A8F96';
const DISP='"Inter Display",Inter,sans-serif',SANS='Inter,sans-serif';
const BPM=128,BT=60/BPM,BAR=BT*4;
const cl=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)),p=(t,a,b)=>cl((t-a)/(b-a));
const eo=t=>1-Math.pow(1-t,3),eo5=t=>1-Math.pow(1-t,5),eio=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2,sine=t=>-(Math.cos(Math.PI*t)-1)/2,ei=t=>t*t*t;
const back=t=>{if(t<=0)return 0;const c1=1.7,c3=c1+1;return 1+c3*Math.pow(t-1,3)+c1*Math.pow(t-1,2)};
const lerp=(a,b,k)=>a+(b-a)*k;
const rnd=s=>{const r=Math.sin(s*127.1+311.7)*43758.5453;return r-Math.floor(r)};
const img=k=>(typeof IM!=='undefined'&&IM[k]&&IM[k].naturalWidth)?IM[k]:null;

/* ---------- text ---------- */
function TX(s,X,Y,size,col,{w=900,skew=-.16,ls=-2,align='center',a=1,font=DISP,stroke=0,fit=0}={}){
  x.save();x.globalAlpha*=a;x.font=`${w} ${size}px ${font}`;x.letterSpacing=ls+'px';x.textAlign=align;x.textBaseline='middle';
  let sc=1;if(fit){const mw=x.measureText(s).width;if(mw>fit)sc=fit/mw;}
  x.translate(X,Y);x.transform(1,0,skew,1,0,0);x.scale(sc,sc);
  if(stroke){x.lineWidth=stroke;x.strokeStyle=col;x.lineJoin='round';x.strokeText(s,0,0);}else{x.fillStyle=col;x.fillText(s,0,0);}
  x.restore();}
function rgb(s,X,Y,size,col,amt,o={}){ // chromatic split
  if(amt>.5){x.save();x.globalCompositeOperation='screen';TX(s,X-amt,Y,size,'#FF2050',{...o,a:(o.a??1)*.85});TX(s,X+amt,Y,size,'#20D0FF',{...o,a:(o.a??1)*.85});x.restore();}
  TX(s,X,Y,size,col,o);}
function slam(s,X,Y,size,col,t,t0,o={}){const k=p(t,t0,t0+.16);if(k<=0)return;const e=eo(k);const sc=lerp(2.1,1,e);
  x.save();x.translate(X,Y);x.scale(sc,sc);rgb(s,0,0,size,col,(1-e)*26+Math.max(0,1-(t-t0-.16)*8)*8,{...o,a:(o.a??1)*cl(k*2)});x.restore();}
function up(s,X,Y,size,col,t,t0,o={}){const k=eo5(p(t,t0,t0+.5));if(k<=0)return;x.save();x.beginPath();x.rect(0,Y-size*.75,W,size*1.5);x.clip();TX(s,X,Y+(1-k)*size*1.1,size,col,o);x.restore();}
function fade(s,X,Y,size,col,t,t0,o={}){const k=eo(p(t,t0,t0+.45));if(k<=0)return;TX(s,X,Y+(1-k)*18,size,col,{skew:0,w:500,ls:0,font:SANS,...o,a:k*(o.a??1)});}

/* ---------- fx ---------- */
const NZ=document.createElement('canvas');NZ.width=NZ.height=256;{const g=NZ.getContext('2d'),d=g.createImageData(256,256);for(let i=0;i<d.data.length;i+=4){const v=Math.random()*255;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=255;}g.putImageData(d,0,0);}
function grain(t,a=.07){x.save();x.globalAlpha=a;x.globalCompositeOperation='overlay';const f=Math.floor(t*30);const ox=-rnd(f)*256,oy=-rnd(f+7)*256;for(let X=ox;X<W;X+=256)for(let Y=oy;Y<H;Y+=256)x.drawImage(NZ,X,Y);x.restore();}
function vign(a=.55){const g=x.createRadialGradient(W/2,H/2,H*.25,W/2,H/2,H*.75);g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(1,`rgba(0,0,0,${a})`);x.fillStyle=g;x.fillRect(0,0,W,H);}
function speed(t,k,col='rgba(255,255,255,',n=34,dir=1,seed=1){if(k<=0)return;x.save();x.lineCap='round';for(let i=0;i<n;i++){const y=rnd(i*3.1+seed)*H,len=200+rnd(i+seed)*700,sp=2400+rnd(i*7+seed)*2600;const X=((rnd(i*5+seed)*W*2-t*sp*dir)%(W*2)+W*2)%(W*2)-W*.5;
  x.strokeStyle=col+(.12+rnd(i*9+seed)*.35)*k+')';x.lineWidth=1+rnd(i*11+seed)*4;x.beginPath();x.moveTo(X,y);x.lineTo(X+len*dir,y);x.stroke();}x.restore();}
const GB=document.createElement('canvas');GB.width=W;GB.height=H;const gb=GB.getContext('2d');
function glitch(t,amt){if(amt<=.02)return;gb.clearRect(0,0,W,H);gb.drawImage(c,0,0);const f=Math.floor(t*30);const n=Math.floor(4+amt*14);
  for(let i=0;i<n;i++){const y=rnd(f*13+i)*H,h=10+rnd(f*7+i*3)*120*amt,dx=(rnd(f*3+i*5)-.5)*260*amt;x.drawImage(GB,0,y,W,h,dx,y,W,h);}
  x.save();x.globalCompositeOperation='screen';x.globalAlpha=.35*amt;x.drawImage(GB,14*amt,0);x.restore();}
function shake(t,t0,amp=24,dec=10){const d=t-t0;if(d<0)return [0,0];const e=Math.exp(-d*dec);return [Math.sin(d*90)*amp*e,Math.cos(d*77)*amp*e*.7];}
function burst(cx,cy,t,t0,col=LIME,n=40,spd=900,seed=3){const d=t-t0;if(d<0||d>1.4)return;x.save();for(let i=0;i<n;i++){const a=rnd(i+seed)*Math.PI*2,v=spd*(.3+rnd(i*2+seed)*.9);const r=v*(1-Math.exp(-d*3.2))/1.4;
  const X=cx+Math.cos(a)*r,Y=cy+Math.sin(a)*r*.6+d*d*260;x.globalAlpha=cl(1-d/1.4);x.fillStyle=i%3?col:WH;const s=2+rnd(i*5+seed)*6;x.fillRect(X-s/2,Y-s/2,s,s);}x.restore();}
function ring(cx,cy,t,t0,col=LIME,max=700){const d=p(t,t0,t0+.55);if(d<=0||d>=1)return;x.save();x.strokeStyle=col;x.globalAlpha=1-d;x.lineWidth=30*(1-d)+2;x.beginPath();x.ellipse(cx,cy,eo(d)*max,eo(d)*max*.32,0,0,7);x.stroke();x.restore();}

/* ---------- product ---------- */
function shoe(k,cx,cy,w,{rot=0,hue=0,glow=LIME,shadow=1,blur=0,flip=false}={}){const im=img(k);
  x.save();x.translate(cx,cy);
  if(shadow>0){const g=x.createRadialGradient(0,w*.24,0,0,w*.24,w*.5);g.addColorStop(0,`rgba(0,0,0,${.55*shadow})`);g.addColorStop(1,'rgba(0,0,0,0)');x.save();x.scale(1,.18);x.fillStyle=g;x.fillRect(-w*.6,w*.24/.18-w*.5,w*1.2,w);x.restore();}
  x.rotate(rot);if(flip)x.scale(-1,1);
  if(!im){x.fillStyle='#DDD';x.beginPath();x.roundRect(-w/2,-w*.16,w,w*.32,w*.1);x.fill();x.fillStyle=glow;x.fillRect(-w/2,w*.1,w,w*.06);x.restore();return;}
  const h=w*im.height/im.width;
  if(blur>0){for(let i=1;i<=6;i++){x.globalAlpha=.12;x.drawImage(im,-w/2+blur*i,-h/2,w,h);}x.globalAlpha=1;}
  if(hue)x.filter=`hue-rotate(${hue}deg) saturate(1.15)`;
  x.drawImage(im,-w/2,-h/2,w,h);x.filter='none';x.restore();}
function cover(im,z=1,ox=0,oy=0,rot=0){if(!im){x.fillStyle='#222';x.fillRect(0,0,W,H);return;}x.save();x.translate(W/2+ox,H/2+oy);x.rotate(rot);const s=Math.max(W/im.width,H/im.height)*z;x.drawImage(im,-im.width*s/2,-im.height*s/2,im.width*s,im.height*s);x.restore();}
function bgDark(t,glowA=.35,gx=W/2,gy=900){x.fillStyle=BLK;x.fillRect(0,0,W,H);const g=x.createRadialGradient(gx,gy,0,gx,gy,900);g.addColorStop(0,`rgba(212,255,42,${glowA*.35})`);g.addColorStop(.5,`rgba(212,255,42,${glowA*.08})`);g.addColorStop(1,'rgba(0,0,0,0)');x.fillStyle=g;x.fillRect(0,0,W,H);}
function grid(t,a=.08,sp=90){x.save();x.strokeStyle=`rgba(255,255,255,${a})`;x.lineWidth=1;const o=(t*40)%sp;for(let X=-sp+o;X<W+sp;X+=sp){x.beginPath();x.moveTo(X,0);x.lineTo(X,H);x.stroke();}for(let Y=-sp+o;Y<H+sp;Y+=sp){x.beginPath();x.moveTo(0,Y);x.lineTo(W,Y);x.stroke();}x.restore();}
function marquee(s,Y,size,t,spd,col,{stroke=3,a=1,skew=-.16}={}){x.save();x.globalAlpha=a;x.font=`900 ${size}px ${DISP}`;x.letterSpacing='-2px';const unit=x.measureText(s+'  ').width;let X=-((t*spd)%unit+unit)%unit;
  while(X<W+unit){TX(s+'  ',X,Y,size,col,{align:'left',stroke,skew});X+=unit;}x.restore();}

/* ================= SCENES ================= */
// S1 0–3.75 build-up: one word per beat, strobe inversions
function s1(t){const words=['ISSO','NÃO','É','SÓ','UM','TÊNIS.'];const i=Math.min(5,Math.floor(t/BT));const lt=t-i*BT;
  const inv=i%2===1&&i<5;x.fillStyle=inv?WH:BLK;x.fillRect(0,0,W,H);
  const build=p(t,5*BT,3.75);
  if(i===5){ // riser: converging lines + zoom
    const g=x.createRadialGradient(W/2,960,0,W/2,960,700);g.addColorStop(0,`rgba(212,255,42,${.25*build})`);g.addColorStop(1,'rgba(0,0,0,0)');x.fillStyle=g;x.fillRect(0,0,W,H);
    x.save();x.strokeStyle=LIME;x.lineCap='round';for(let j=0;j<28;j++){const a=j/28*Math.PI*2+rnd(j)*.2;const r0=lerp(1300,260,eio(build))+rnd(j*3)*200,r1=r0+120+rnd(j*5)*260;
      x.globalAlpha=.25+.5*build;x.lineWidth=2+rnd(j*7)*3;x.beginPath();x.moveTo(W/2+Math.cos(a)*r0,960+Math.sin(a)*r0);x.lineTo(W/2+Math.cos(a)*r1,960+Math.sin(a)*r1);x.stroke();}x.restore();}
  const [sx,sy]=i===5?[Math.sin(t*95)*14*build*build,Math.cos(t*83)*14*build*build]:shake(t,i*BT,10,14);
  x.save();x.translate(sx,sy);const zs=i===5?1+.25*ei(build):1;x.translate(W/2,960);x.scale(zs,zs);x.translate(-W/2,-960);
  slam(words[i],W/2,960,300,inv?BLK:WH,t,i*BT,{fit:900});x.restore();
  if(i===0)fade('ZEFYR  ·  ZF-1',W/2,1180,40,GRY,t,.15,{ls:8,w:600});
}
// S2 3.75–7.5 DROP hero
function s2(t){const land=.32;
  bgDark(t,.6*eo(p(t,0,.4)),W/2,880);
  const [sx,sy]=shake(t,land,30,8);x.save();x.translate(sx,sy);
  // giant outlined word behind
  const k=eo5(p(t,0,.35));x.save();x.translate(W/2,820);x.scale(lerp(1.6,1,k),lerp(1.6,1,k));TX('ZEFYR',0,0,330,LIME,{stroke:4,a:k,ls:-6});x.restore();
  speed(t,1-p(t,land,land+.6),'rgba(212,255,42,',30,1,4);
  ring(W/2,1020,t,land,LIME,620);burst(W/2,1000,t,land,LIME,46,1100,9);
  // shoe flies in from right with blur
  const fk=eo5(p(t,0,land)),hover=Math.sin((t-land)*2.6)*12*p(t,land,land+.6);
  const kick=t>2.8?Math.sin(p(t,2.8,3.3)*Math.PI)*-.12:0;
  shoe('side',lerp(-520,W/2,fk),880+hover,900,{rot:lerp(.35,-.04,fk)+kick,blur:(1-fk)*-60,shadow:fk});
  x.restore();
  // fill word in front partially (text-behind feel: lower half of outline filled)
  slam('ZF-1 PHANTOM',W/2,1290,72,WH,t,2*BT+.02,{ls:2});
  up('O FUTURO',W/2,1410,96,WH,t,3*BT+.02,{});
  up('TÁ NOS SEUS PÉS.',W/2,1510,96,LIME,t,4*BT+.02,{fit:960});
}
// S3 7.5–11.25 tech callouts
function counter(v,t,t0,d=.8){return Math.round(v*eo(p(t,t0,t0+d)));}
function callout(px,py,lx,ly,t,t0,big,small,align){const k=p(t,t0,t0+.35);if(k<=0)return;x.save();x.strokeStyle=LIME;x.lineWidth=3;
  x.fillStyle=LIME;x.beginPath();x.arc(px,py,10*back(p(t,t0,t0+.25)),0,7);x.fill();
  x.globalAlpha=.35;x.beginPath();x.arc(px,py,10+((t-t0)*40%30),0,7);x.stroke();x.globalAlpha=1;
  const e=eo(k);x.beginPath();x.moveTo(px,py);x.lineTo(lerp(px,lx,e),lerp(py,ly,e));x.stroke();x.restore();
  const ax=align==='left'?lx+16:lx-16;up(big,ax,ly-34,84,WH,t,t0+.2,{align});fade(small,ax,ly+34,40,LIME,t,t0+.35,{align,w:600,ls:3});}
function s3(t){bgDark(t,.35,W/2,980);grid(t,.06);
  const z=lerp(1.08,1,eo(p(t,0,1.2))),r=Math.sin(t*1.4)*.035,hy=Math.sin(t*2.2)*14;
  x.save();x.translate(W/2,1000);x.scale(z,z);x.translate(-W/2,-1000);shoe('q34',W/2,1000+hy,820,{rot:r});x.restore();
  // scan line
  const sk=p(t,.1,1.0);if(sk>0&&sk<1){const Y=lerp(620,1380,sine(sk));const g=x.createLinearGradient(0,Y-60,0,Y+6);g.addColorStop(0,'rgba(212,255,42,0)');g.addColorStop(1,'rgba(212,255,42,.35)');x.fillStyle=g;x.fillRect(80,Y-60,W-160,66);x.fillStyle=LIME;x.fillRect(80,Y,W-160,3);}
  up('ENGENHARIA',W/2,330,110,WH,t,.02,{ls:-3});
  callout(420,880,180,640,t,BT*1,counter(212,t,BT*1+.2)+'g','ULTRALEVE','left');
  callout(700,1150,900,1430,t,BT*3,'+'+counter(38,t,BT*3+.2)+'%','RETORNO DE ENERGIA','right');
  callout(560,1180,180,1480,t,BT*5,'AERO-X','ESPUMA RESPONSIVA','left');
}
// S4 11.25–15 sole / GRIP knockout
function s4(t){const im=img('sole2')||img('sole');const ph2=t>=BAR;
  if(!ph2){cover(img('sole'),lerp(1.3,1.12,eo(p(t,0,BAR))),0,0,lerp(.05,0,eo(p(t,0,BAR))));x.fillStyle='rgba(0,0,0,.35)';x.fillRect(0,0,W,H);
    slam('TRAÇÃO',W/2,860,190,WH,t,.02,{fit:940});slam('TOTAL.',W/2,1060,190,LIME,t,BT*2,{fit:940});return;}
  const u=t-BAR;x.fillStyle=BLK;x.fillRect(0,0,W,H);
  const sc=lerp(1.9,1,eo5(p(u,0,.5)));
  // knockout: draw photo clipped by text
  const L=document.__kc||(document.__kc=document.createElement('canvas'));L.width=W;L.height=H;const l=L.getContext('2d');
  l.save();l.translate(W/2,950);l.scale(sc,sc);l.transform(1,0,-.16,1,0,0);l.font=`900 400px ${DISP}`;l.letterSpacing='-14px';l.textAlign='center';l.textBaseline='middle';l.fillStyle='#fff';l.fillText('GRIP',0,0);l.restore();
  l.globalCompositeOperation='source-in';const xx=x;x=l;cover(im,lerp(1.05,1.25,p(u,0,BAR)),Math.sin(u)*30,0);x=xx;l.globalCompositeOperation='source-over';
  x.drawImage(L,0,0);
  x.save();x.translate(W/2,950);x.scale(sc,sc);TX('GRIP',0,0,400,LIME,{stroke:3,ls:-14});x.restore();
  fade('EM QUALQUER CHÃO.',W/2,1260,52,WH,t,BAR+BT*2,{font:DISP,w:800,ls:2,skew:-.16});
}
// S5 15–18.75 street, cinematic
function s5(t){const im=img('street');{const z=lerp(1.32,1.15,sine(p(t,0,3.75)));cover(im,z,440*z+lerp(25,-25,p(t,0,3.75)),-100);}
  const g=x.createLinearGradient(0,0,0,H);g.addColorStop(0,'rgba(0,0,0,.6)');g.addColorStop(.42,'rgba(0,0,0,0)');g.addColorStop(.8,'rgba(0,0,0,0)');g.addColorStop(1,'rgba(0,0,0,.6)');x.fillStyle=g;x.fillRect(0,0,W,H);
  // rain
  x.save();x.strokeStyle='rgba(255,255,255,.18)';x.lineWidth=2;for(let i=0;i<70;i++){const X=rnd(i)*W*1.2,Y=((rnd(i*3)*H+t*2200)%(H+200))-100;x.beginPath();x.moveTo(X,Y);x.lineTo(X-14,Y+60);x.stroke();}x.restore();
  // light leak
  const lk=Math.sin(p(t,.2,2.6)*Math.PI);if(lk>0){x.save();x.globalCompositeOperation='screen';const lg=x.createRadialGradient(W*.9,400,0,W*.9,400,800);lg.addColorStop(0,`rgba(255,140,60,${.35*lk})`);lg.addColorStop(1,'rgba(0,0,0,0)');x.fillStyle=lg;x.fillRect(0,0,W,H);x.restore();}
  slam('FEITO',90,350,160,WH,t,BT*1,{align:'left'});slam('PRA',90,505,160,WH,t,BT*2,{align:'left'});slam('RUA.',90,660,160,LIME,t,BT*3,{align:'left'});
  // letterbox
  const lb=eo5(p(t,0,.4))*120;x.fillStyle='#000';x.fillRect(0,0,W,lb);x.fillRect(0,H-lb,W,lb);
}
// S6 18.75–22.5 colorways, change every 2 beats
const CW=[['PHANTOM',0,'#0B0B0C',LIME],['OCEAN',150,'#0A2A6B','#5FD0FF'],['INFRARED',-90,'#5A0A12','#FF3B4A'],['SOLAR',-50,'#6B3A00','#FFB020']];
function s6(t){const i=Math.min(3,Math.floor(t/(BT*2))),u=t-i*BT*2;const [name,hue,bg,ac]=CW[i];
  x.fillStyle=bg;x.fillRect(0,0,W,H);
  if(i>0){const pv=CW[i-1];const wk=eo5(p(u,0,.22));x.save();x.fillStyle=pv[2];x.beginPath();x.rect(0,0,W*(1-wk),H);x.fill();x.restore();}
  const rg=x.createRadialGradient(W/2,900,0,W/2,900,800);rg.addColorStop(0,'rgba(255,255,255,.12)');rg.addColorStop(1,'rgba(0,0,0,0)');x.fillStyle=rg;x.fillRect(0,0,W,H);
  marquee(name+' ',620,220,t,500,ac,{stroke:3,a:.55});marquee(name+' ',1180,220,t,-500,ac,{stroke:3,a:.55});
  const sk=eo5(p(u,0,.28));const [sx,sy]=shake(t,i*BT*2+.28,16,10);
  shoe('side',lerp(-700,W/2,sk)+sx,900+sy+Math.sin(t*3)*10,860,{rot:lerp(.25,-.05,sk),hue,blur:(1-sk)*50});
  speed(t,1-p(u,.2,.6),'rgba(255,255,255,',20,-1,i*9);
  slam(name,W/2,1370,150,WH,t,i*BT*2+.05,{fit:940});
  fade(`COLORWAY 0${i+1} / 04`,W/2,1490,40,ac,t,i*BT*2+.25,{w:700,ls:6});
}
// S7 22.5–26.25 drop date + tapes
function slot(s,X,Y,size,t,t0){x.save();x.font=`900 ${size}px ${DISP}`;x.letterSpacing='-4px';const ws=[...s].map(ch=>x.measureText(ch).width);const tw=ws.reduce((a,b)=>a+b,0);let cx=X-tw/2;
  [...s].forEach((ch,j)=>{const st=t0+j*.08,k=eo5(p(t,st,st+.6));if(k<=0){cx+=ws[j];return;}x.save();x.beginPath();x.rect(cx-10,Y-size*.62,ws[j]+20,size*1.24);x.clip();
    const digits='0123456789';const roll=(1-k)*6;for(let r=-1;r<=1;r++){const off=(roll%1)+r;const c2=r===0&&k>.98?ch:(/\d/.test(ch)?digits[Math.floor(rnd(Math.floor(roll)+r+j)*10)]:ch);
      TX(k>.98&&r!==0?'':c2,cx+ws[j]/2,Y-off*size*1.1,size,j%3===2?WH:LIME,{skew:0,ls:0});}x.restore();cx+=ws[j];});x.restore();}
function tape(Y,rot,t,spd,bg,fg,txt,k){if(k<=0)return;x.save();x.translate(W/2,Y);x.rotate(rot);x.beginPath();x.rect(-W*eo5(k),-46,W*2*eo5(k),92);x.clip();x.fillStyle=bg;x.fillRect(-W,-46,W*2,92);
  x.translate(-W/2,-Y);x.font=`900 50px ${DISP}`;x.letterSpacing='2px';const unit=x.measureText(txt).width;let X=-W*.5-((t*spd)%unit+unit)%unit;while(X<W*1.5){TX(txt,X,Y+2,50,fg,{align:'left',ls:2});X+=unit;}x.restore();}
function s7(t){bgDark(t,.25,W/2,700);grid(t,.04,120);
  fade('LANÇAMENTO OFICIAL',W/2,360,44,LIME,t,.05,{w:700,ls:8});
  slot('11.11',W/2,560,260,t,.15);
  shoe('side',W/2+Math.sin(t*1.6)*20,1000,760,{rot:-.08+Math.sin(t*2)*.03,blur:0,shadow:1});
  burst(W/2,1000,t,BT*2,LIME,30,800,21);
  tape(1290,-.12,t,260,LIME,BLK,'EDIÇÃO LIMITADA  ✦  500 PARES  ✦  ',p(t,BT*3,BT*3+.4));
  tape(1360,.09,t,-260,WH,BLK,'ZF-1 PHANTOM  ✦  R$ 899  ✦  ',p(t,BT*4,BT*4+.4));
  up('SÓ 500 PARES.',W/2,1530,80,WH,t,BT*6,{});
}
// S8 26.25–31.875 CTA
function s8(t){bgDark(t,.3,W/2,1300);
  TX('ZEFYR',W/2,330,70,LIME,{stroke:2,a:eo(p(t,0,.4)),ls:-2});
  fade('Essa marca não existe.',W/2,560,48,GRY,t,.25,{});
  up('MAS O SEU',W/2,700,110,WH,t,BT*1,{});
  up('LANÇAMENTO',W/2,815,110,WH,t,BT*1+.15,{fit:960});
  up('PODE TER',W/2,930,110,WH,t,BT*2,{});
  slam('ESSE IMPACTO.',W/2,1050,110,LIME,t,BT*3,{fit:960});
  ['Anúncios de produto','Lançamentos e drops','Reels de alto impacto'].forEach((s,i)=>{const k=eo(p(t,BT*4.4+i*.2,BT*4.4+i*.2+.4));if(k<=0)return;x.save();x.globalAlpha=k;x.translate((1-k)*-30,0);
    x.fillStyle=LIME;x.fillRect(282,1168+i*64,14,14);TX(s,316,1175+i*64,42,WH,{align:'left',w:500,skew:0,ls:0,font:SANS});x.restore();});
  const bk=back(p(t,BT*7,BT*7+.45)),pul=t>BT*8?1+.03*Math.exp(-((t-BT*8)%BT)*9):1;
  if(bk>0){x.save();x.translate(W/2,1440);x.scale(bk*pul,bk*pul);x.fillStyle=LIME;x.beginPath();x.roundRect(-340,-70,680,140,70);x.fill();TX('Me chama no direct',0,3,50,BLK,{w:700,skew:0,ls:0,font:SANS});x.restore();}
  fade('@alecreator_motion',W/2,1560,52,WH,t,BT*8,{w:600});
}

const SC=[[s1,0,3.75],[s2,3.75,7.5],[s3,7.5,11.25],[s4,11.25,15],[s5,15,18.75],[s6,18.75,22.5],[s7,22.5,26.25],[s8,26.25,31.875]];
window.DUR=31.875;
window.draw=function(t){x=X0;const i=SC.findIndex(([,a,b])=>t>=a&&t<b);const k=i<0?SC.length-1:i;const [f,a]=SC[k];const lt=t-a;
  x.save();
  // zoom punch on cut
  if(k>0){const zp=1+.09*Math.exp(-lt*9);x.translate(W/2,H/2);x.scale(zp,zp);x.translate(-W/2,-H/2);}
  // beat pulse (from drop on)
  if(t>=3.75&&t<26.25){const bp=(t-3.75)%BT;const s=1+.012*Math.exp(-bp*12);x.translate(W/2,H/2);x.scale(s,s);x.translate(-W/2,-H/2);}
  f(lt);x.restore();
  // cut glitch + flash
  if(k>0&&lt<.2){glitch(t,(1-lt/.2)*.9);}
  if(k>0&&lt<.14){x.fillStyle=k===1?`rgba(255,255,255,${1-lt/.14})`:`rgba(212,255,42,${(1-lt/.14)*.55})`;x.fillRect(0,0,W,H);}
  // pre-drop whiteout
  if(t>3.55&&t<3.75){x.fillStyle=`rgba(255,255,255,${p(t,3.55,3.75)})`;x.fillRect(0,0,W,H);}
  vign(.45);grain(t,.08);
  const fo=p(t,31.3,31.875);if(fo>0){x.fillStyle=`rgba(0,0,0,${fo})`;x.fillRect(0,0,W,H);}
};

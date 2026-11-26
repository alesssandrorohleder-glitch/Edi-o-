
const W=1080,H=1920,c=document.getElementById('c');let x=c.getContext('2d');const X0=x;
const INK='#1F2326',SAL='#F07A55',SALD='#E0603C',CREAM='#FFF6EE',WH='#FFFFFF',GRY='#6F757B';
const DISP='"Inter Display",Inter,sans-serif',SANS='Inter,sans-serif';
const cl=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)),p=(t,a,b)=>cl((t-a)/(b-a));
const eo=t=>1-Math.pow(1-t,3),eo5=t=>1-Math.pow(1-t,5),eio=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2,sine=t=>-(Math.cos(Math.PI*t)-1)/2;
const back=t=>{if(t<=0)return 0;const c1=1.7,c3=c1+1;return 1+c3*Math.pow(t-1,3)+c1*Math.pow(t-1,2)};
const rnd=s=>{const r=Math.sin(s*127.1+311.7)*43758.5453;return r-Math.floor(r)};const lerp=(a,b,k)=>a+(b-a)*k;
const F=1300/1438; // scale of _s images vs original
function T(s,X,Y,size,col,{font=DISP,w=700,align='center',a=1,ls=0,stroke=0}={}){x.save();x.globalAlpha*=a;x.font=`${w} ${size}px ${font}`;x.textAlign=align;x.textBaseline='middle';x.letterSpacing=ls+'px';
  if(stroke){x.lineWidth=stroke;x.strokeStyle=col;x.strokeText(s,X,Y);}else{x.fillStyle=col;x.fillText(s,X,Y);}x.restore();}
function maskUp(s,X,Y,size,col,t,t0,o={}){const k=eo5(p(t,t0,t0+.45));if(k<=0)return;x.save();x.beginPath();x.rect(0,Y-size*.75,W,size*1.5);x.clip();T(s,X,Y+(1-k)*size*1.1,size,col,o);x.restore();}
function fade(s,X,Y,size,col,t,t0,o={}){const k=eo(p(t,t0,t0+.5));if(k<=0)return;T(s,X,Y+(1-k)*14,size,col,{...o,a:k*(o.a??1)});}
function pill(s,X,Y,size,bg,fg,k){if(k<=0)return;x.save();x.translate(X,Y);x.scale(k,k);x.font=`600 ${size}px ${SANS}`;x.letterSpacing='0px';const w=x.measureText(s).width+size*1.5,h=size*1.9;x.shadowColor='rgba(0,0,0,.18)';x.shadowBlur=24;x.shadowOffsetY=8;x.fillStyle=bg;x.beginPath();x.roundRect(-w/2,-h/2,w,h,h/2);x.fill();x.shadowColor='transparent';T(s,0,2,size,fg,{font:SANS,w:600});x.restore();}
// full-bleed photo: cover canvas, then zoom/rotate around (fx,fy) in canvas coords
function photo(im,{z=1,rot=0,dx=0,dy=0,blur=0}={}){const sc=Math.max(W/im.width,H/im.height)*z;x.save();x.translate(W/2+dx,H/2+dy);x.rotate(rot);if(blur>.3)x.filter=`blur(${blur}px)`;x.drawImage(im,-im.width*sc/2,-im.height*sc/2,im.width*sc,im.height*sc);x.restore();}
// same transform but drawing the cutout (for text-behind effect); off = crop offset in original px
function photoCut(cut,src,off,{z=1,rot=0,dx=0,dy=0}={}){const sc=Math.max(W/src.width,H/src.height)*z;x.save();x.translate(W/2+dx,H/2+dy);x.rotate(rot);x.drawImage(cut,-src.width*sc/2+off[0]*F*sc,-src.height*sc/2+off[1]*F*sc,cut.width*sc,cut.height*sc);x.restore();}
function particles(t,t0,n,cx,cy,spread,seed=1,col=null){const tt=t-t0;if(tt<0)return;for(let i=0;i<n;i++){const a=rnd(i+seed)*Math.PI*2,v=spread*(.4+rnd(i*3+seed)*.8);const px=cx+Math.cos(a)*v*eo(cl(tt/1.2)),py=cy+Math.sin(a)*v*eo(cl(tt/1.2))+tt*tt*90;
  const al=cl(1-tt/2.2);if(al<=0)continue;x.save();x.globalAlpha=al;x.translate(px,py);x.rotate(tt*3+i);const kind=col||(i%5===0?'roe':i%3===0?'black':'sesame');
  if(kind==='roe'){x.fillStyle='#F2671F';x.beginPath();x.arc(0,0,7,0,7);x.fill();x.fillStyle='rgba(255,255,255,.6)';x.beginPath();x.arc(-2,-2,2,0,7);x.fill();}
  else if(kind==='crumb'){x.fillStyle='#D99A3D';x.beginPath();x.moveTo(-8,-5);x.lineTo(7,-7);x.lineTo(9,5);x.lineTo(-6,8);x.closePath();x.fill();}
  else {x.fillStyle=kind==='black'?'#222':'#F1E3C2';x.beginPath();x.ellipse(0,0,8,4,0,0,7);x.fill();}x.restore();}}
function floatSeeds(t,n,seed,a=.6){for(let i=0;i<n;i++){const px=(rnd(i+seed)*W+Math.sin(t*.7+i)*40),py=((rnd(i*5+seed)*H)-t*(30+rnd(i)*40)+H*3)%H;x.save();x.globalAlpha=a;x.translate(px,py);x.rotate(t+i);x.fillStyle=i%4===0?'#222':'#F1E3C2';x.beginPath();x.ellipse(0,0,7,3.5,0,0,7);x.fill();x.restore();}}
function shake(t,t0,amp=16){const d=t-t0;if(d>=0&&d<.3){const k=1-d/.3;x.translate(Math.sin(d*95)*amp*k,Math.cos(d*80)*amp*k);}}
function gradDark(y0,y1,a=.85){const g=x.createLinearGradient(0,y0,0,y1);g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(1,`rgba(0,0,0,${a})`);x.fillStyle=g;x.fillRect(0,0,W,H);}

/* ---------------- SCENES ---------------- */
function s1(t){ // 0-4 explode intro
  const snap=eo5(p(t,0,.5));photo(IM.explode,{z:lerp(1.45,1.12,snap)-t*.015,blur:lerp(18,0,snap),dy:-t*10});
  gradDark(H*.35,H*.75,.55);{const g=x.createLinearGradient(0,0,W*.8,0);g.addColorStop(0,'rgba(0,0,0,.55)');g.addColorStop(1,'rgba(0,0,0,0)');x.fillStyle=g;x.fillRect(0,0,W,H);}floatSeeds(t,26,3,.55);
  const out=eio(p(t,2.2,2.6));
  x.save();x.globalAlpha=1-out;x.translate(-out*200,0);
  maskUp('FRESCO.',110,620,150,WH,t,.5,{align:'left',w:800});
  maskUp('LEVE.',110,780,150,WH,t,1.0,{align:'left',w:800});
  maskUp('BRASILEIRO.',110,940,150,SAL,t,1.5,{align:'left',w:800});
  x.restore();
  const lk=eo5(p(t,2.5,3.0));if(lk>0){x.save();x.translate(W/2,900);x.scale(lerp(1.4,1,lk),lerp(1.4,1,lk));x.globalAlpha=lk;
    x.font=`700 230px ${DISP}`;x.letterSpacing='-6px';x.textAlign='left';x.textBaseline='middle';const wa=x.measureText('mar').width,wb=x.measureText('é').width;
    x.shadowColor='rgba(0,0,0,.4)';x.shadowBlur=40;x.fillStyle=WH;x.fillText('mar',-(wa+wb)/2,0);x.fillStyle=SAL;x.fillText('é',-(wa+wb)/2+wa,0);x.restore();
    const wk=eio(p(t,2.7,3.4));x.save();x.strokeStyle=SAL;x.lineWidth=12;x.lineCap='round';x.beginPath();for(let i=0;i<=60*wk;i++){const u=i/60;x.lineTo(W/2-260+u*520,1080+Math.sin(u*Math.PI*3+t*4)*20);}x.stroke();x.restore();
    fade('SUSHI  ·  DELIVERY  ·  RODÍZIO',W/2,1180,40,WH,t,3.0,{font:SANS,w:500,ls:8});}
}
function s2(t){ // 4-8 nigiri cutout floating
  x.fillStyle=WH;x.fillRect(0,0,W,H);
  const gg=x.createRadialGradient(W/2,1000,50,W/2,1000,900);gg.addColorStop(0,'rgba(240,122,85,.14)');gg.addColorStop(1,'rgba(255,255,255,0)');x.fillStyle=gg;x.fillRect(0,0,W,H);
  // giant outlined word scrolling behind
  x.save();x.globalAlpha=.9;T('NIGIRI',W/2+260-t*140,980,360,'rgba(240,122,85,.35)',{w:800,stroke:3});T('NIGIRI',W/2-300+t*120,640,200,'rgba(31,35,38,.08)',{w:800});x.restore();
  x.save();shake(t,.5,14);
  const im=IM.ncut;const w=900,h=w*im.height/im.width;const drop=eo5(p(t,.05,.5));const land=t>.5?back(p(t,.5,.9)):0;
  const y=lerp(-500,1000,drop)+Math.sin(t*2.2)*14*(t>1?1:0);const rot=lerp(-.6,0,drop)+Math.sin(t*1.6)*.03;const sq=t>.5&&t<.8?1+Math.sin((t-.5)/.3*Math.PI)*.06:1;
  // shadow
  x.fillStyle='rgba(31,35,38,.18)';x.filter='blur(22px)';x.beginPath();x.ellipse(W/2,1000+h*.45,w*.4*drop,30,0,0,7);x.fill();x.filter='none';
  x.translate(W/2,y);x.rotate(rot);x.scale(sq,2-sq);x.drawImage(im,-w/2,-h/2,w,h);x.restore();
  particles(t,.5,34,W/2,1000,520,7);
  fade('01',150,330,48,SAL,t,.9,{w:700,align:'left'});
  maskUp('Nigiri',150,420,110,INK,t,1.0,{align:'left',w:700});
  maskUp('de salmão',150,530,110,INK,t,1.15,{align:'left',w:300});
  pill('salmão fresco · corte do dia',W/2,1450,40,INK,WH,back(p(t,1.6,2.0)));
  pill('R$ 18,90',W/2,1560,44,SAL,WH,back(p(t,2.0,2.4)));
}
function s3(t){ // 8-12 uramaki photo with text-behind
  const z=lerp(1.25,1.05,eo5(p(t,0,.8)))+ (t>2?.05*eo5(p(t,2,2.4)):0)+t*.01;const dx=lerp(120,0,eo5(p(t,0,.8)));
  photo(IM.uramaki,{z,dx});
  T('URAMAKI',W/2-t*40+60,420,210,'rgba(240,122,85,.95)',{w:800});
  photoCut(IM.ucut,IM.uramaki,[67,557],{z,dx});
  const tags=[['salmão',300,1290],['abacate',780,1150],['pepino',820,1340],['gergelim',260,1050]];
  tags.forEach(([s,X,Y],i)=>pill(s,X,Y,40,i%2?SAL:INK,WH,back(p(t,1.0+i*.5,1.4+i*.5))));
  maskUp('Uramaki filadélfia',W/2,1450,64,INK,t,1.2,{w:700});
  pill('R$ 24,90',W/2,1555,44,SAL,WH,back(p(t,2.2,2.6)));
}
function s4(t){ // 12-16 hot roll drop
  x.fillStyle='#FEFEFE';x.fillRect(0,0,W,H);x.save();shake(t,.6,22);
  const drop=eo5(p(t,.1,.6));const z=1.06+t*.01;const dy=lerp(-1130,-410,drop);
  photo(IM.hotroll,{z,dy});
  photoCut(IM.hcut,IM.hotroll,[53,471],{z,dy});
  x.restore();
  particles(t,.6,40,W/2,850,560,11,'crumb');
  maskUp('HOT ROLL',W/2,1265,150,INK,t,.7,{w:800});
  maskUp('Crocante por fora,',W/2,1385,56,INK,t,1.3,{w:700});
  maskUp('cremoso por dentro.',W/2,1455,56,SAL,t,1.5,{w:700});
  pill('R$ 26,90',W/2,1555,44,SAL,WH,back(p(t,2.0,2.4)));
}
function s5(t){ // 16-20 temaki reveal
  x.fillStyle=SAL;x.fillRect(0,0,W,H);
  const r=eio(p(t,0,.7))*1300;x.save();x.beginPath();x.arc(W/2,900,r,0,7);x.clip();photo(IM.temaki,{z:1.18-t*.025,dy:20-t*8});gradDark(H*.55,H*.85,.75);x.restore();
  x.save();x.translate(150,1100);x.rotate(-Math.PI/2);T('TEMAKI',0,0,220,'rgba(255,255,255,.95)',{w:800,stroke:4,a:eo(p(t,.6,1.0))});x.restore();
  fade('04',120,330,48,WH,t,.8,{w:700,align:'left'});
  maskUp('Temaki',W/2+120,1350,110,WH,t,1.0,{w:700});
  maskUp('montado na hora',W/2+120,1450,52,'rgba(255,255,255,.85)',t,1.25,{w:400});
  pill('R$ 29,90',W/2+120,1555,44,SAL,WH,back(p(t,1.8,2.2)));
}
function s6(t){ // 20-24 montage
  const shots=[[IM.nigiri3,0,1],[IM.chop,1,2],[IM.nigiri1,2,2.5],[IM.uramaki,2.5,3],[IM.hotroll,3,3.5],[IM.temaki,3.5,4]];
  const s=shots.find(([,a,b])=>t>=a&&t<b)||shots[5];const lt=t-s[1];photo(s[0],{z:1.22-lt*.12});
  x.fillStyle='rgba(0,0,0,.38)';x.fillRect(0,0,W,H);
  const fl=Math.min(...shots.map(([,a])=>Math.abs(t-a)));if(fl<.08){x.fillStyle=`rgba(255,255,255,${.7*(1-fl/.08)})`;x.fillRect(0,0,W,H);}
  maskUp('DO JEITO',W/2,820,150,WH,t,.1,{w:800});
  maskUp('QUE VOCÊ',W/2,980,150,WH,t,.35,{w:800});
  maskUp('GOSTA.',W/2,1140,150,SAL,t,.6,{w:800});
}
function s7(t){ // 24-28 platter
  const k=eo5(p(t,0,1.2));photo(IM.platter,{z:lerp(1.6,1.05,k),rot:lerp(.25,0,k)});
  gradDark(H*.5,H*.8,.85);
  maskUp('COMBINADOS',W/2,1380,110,WH,t,.6,{w:800,ls:4});
  fade('30 peças · R$ 89,90',W/2,1480,52,'rgba(255,255,255,.92)',t,.9,{font:SANS,w:600});
  pill('Delivery em 40 min',W/2,1580-30,44,SAL,WH,back(p(t,1.3,1.7)));
}
function s8(t){ // 28-34 CTA
  const g=x.createLinearGradient(0,0,0,H);g.addColorStop(0,'#F48A66');g.addColorStop(1,'#E0603C');x.fillStyle=g;x.fillRect(0,0,W,H);
  floatSeeds(t,22,9,.5);
  const im=IM.ncut;const w=520,h=w*im.height/im.width;const k=eo5(p(t,0,.7));x.save();x.translate(W/2+Math.sin(t*1.5)*10,420+Math.sin(t*2)*16-(1-k)*400);x.rotate(Math.sin(t*1.2)*.08-.08);x.shadowColor='rgba(0,0,0,.25)';x.shadowBlur=40;x.shadowOffsetY=20;x.drawImage(im,-w/2,-h/2,w,h);x.restore();
  fade('Esse restaurante não existe.',W/2,740,46,'rgba(255,255,255,.85)',t,.5,{font:SANS,w:400});
  maskUp('Mas o vídeo do seu',W/2,870,84,WH,t,.9,{w:700});
  maskUp('pode ter esse',W/2,970,84,WH,t,1.1,{w:700});
  maskUp('movimento.',W/2,1075,100,INK,t,1.3,{w:800});
  const bk=back(p(t,2.6,3.1));const pul=1+.03*Math.exp(-((t%.5))*8)*(t>3.1?1:0);if(bk>0){x.save();x.translate(W/2,1300);x.scale(bk*pul,bk*pul);x.shadowColor='rgba(0,0,0,.2)';x.shadowBlur=30;x.fillStyle=WH;x.beginPath();x.roundRect(-340,-75,680,150,75);x.fill();x.shadowColor='transparent';T('Me chama no direct',0,3,50,SALD,{font:SANS,w:700});x.restore();}
  fade('@alecreator_motion',W/2,1450,58,WH,t,3.1,{font:SANS,w:700});
}
const SC=[[s1,0,4],[s2,4,8],[s3,8,12],[s4,12,16],[s5,16,20],[s6,20,24],[s7,24,28],[s8,28,34]];
window.DUR=34;const XF=.28;
const buf=document.createElement('canvas');buf.width=W;buf.height=H;const bx=buf.getContext('2d');
const nb=document.createElement('canvas');nb.width=W;nb.height=H;const nx=nb.getContext('2d');
window.draw=function(t){const i=SC.findIndex(([,a,b])=>t>=a&&t<b);const k=i<0?SC.length-1:i;const [f,a]=SC[k];
  const bp=t%0.5;const punch=1+.008*Math.exp(-bp*12);
  if(k>0&&t-a<XF && k!==5){ // whip pan transition with motion blur
    x=bx;x.save();x.setTransform(1,0,0,1,0,0);x.globalAlpha=1;x.filter='none';SC[k-1][0](t-SC[k-1][1]);x.restore();
    x=nx;x.save();x.setTransform(1,0,0,1,0,0);x.globalAlpha=1;x.filter='none';f(t-a);x.restore();x=X0;
    const e=eio((t-a)/XF);const off=e*W;x.save();x.fillStyle='#000';x.fillRect(0,0,W,H);
    for(let j=0;j<6;j++){const o=j*28*Math.sin(Math.PI*e);x.globalAlpha=j?.18:1;x.drawImage(buf,-off-o,0);x.drawImage(nb,W-off-o,0);}x.restore();
  } else {x=X0;x.save();x.translate(W/2,H/2);x.scale(punch,punch);x.translate(-W/2,-H/2);f(t-a);x.restore();}
  const fo=p(t,33.4,34);if(fo>0){x.fillStyle=`rgba(0,0,0,${fo})`;x.fillRect(0,0,W,H);}};
</script></body></html>

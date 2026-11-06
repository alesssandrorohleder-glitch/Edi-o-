
/* ---------- wood background (pre-rendered once) ---------- */
const WOOD=document.createElement('canvas');WOOD.width=W;WOOD.height=H;
(function(){const g=WOOD.getContext('2d');const tones=['#3A2416','#42291A','#35200F','#4A2F1D','#3E2717','#46301F'];
  for(let i=0;i*190<H;i++){const y=i*190;g.fillStyle=tones[i%tones.length];g.fillRect(0,y,W,190);
    for(let k=0;k<26;k++){g.strokeStyle=`rgba(${k%3?20:90},${k%3?10:55},${k%3?5:30},${.10+rnd(i*31+k)*.18})`;g.lineWidth=1+rnd(k+i)*2.5;g.beginPath();
      const yy=y+8+rnd(i*7+k*3)*174;for(let X=0;X<=W;X+=30){g.lineTo(X,yy+Math.sin(X*.006+k+i)*6+Math.sin(X*.02+k)*2);}g.stroke();}
    g.fillStyle='rgba(0,0,0,.55)';g.fillRect(0,y,W,4);g.fillStyle='rgba(255,220,180,.06)';g.fillRect(0,y+4,W,2);}
  // flour dust
  for(let i=0;i<500;i++){const fx=rnd(i*3.1)*W,fy=rnd(i*7.7)*H;const cluster=(fx<260&&fy>1300)||(fx>860&&fy<420);if(!cluster&&rnd(i)>.25)continue;g.fillStyle=`rgba(255,250,240,${.2+rnd(i*5)*.5})`;g.beginPath();g.arc(fx,fy,1+rnd(i*9)*2.4,0,7);g.fill();}
  const v=g.createRadialGradient(W/2,H/2,H*.3,W/2,H/2,H*.75);v.addColorStop(0,'rgba(0,0,0,0)');v.addColorStop(1,'rgba(0,0,0,.55)');g.fillStyle=v;g.fillRect(0,0,W,H);})();
function wood(){x.drawImage(WOOD,0,0);}
function deco(t,list){list.forEach(([nm,X,Y,s,r],i)=>{const im=IM[nm];const k=eo5(p(t,.0+i*.06,.5+i*.06));if(k<=0)return;x.save();x.translate(X,Y);x.rotate(r+(1-k)*.6);x.scale(s*k,s*k);
  x.shadowColor='rgba(0,0,0,.45)';x.shadowBlur=24;x.shadowOffsetY=10;x.drawImage(im,-im.width/2,-im.height/2);x.restore();});}
/* ---------- pizza & slices ---------- */
const PC={x:540,y:536,r:540};
function slice(i,cx,cy,s,rot=0){const im=IM.pizza;const a0=-Math.PI/2+i*Math.PI/4,a1=a0+Math.PI/4;
  x.save();x.translate(cx,cy);x.rotate(rot);x.scale(s,s);x.beginPath();x.moveTo(0,0);x.arc(0,0,PC.r+20,a0,a1);x.closePath();x.clip();
  x.shadowColor='rgba(0,0,0,.4)';x.drawImage(im,-PC.x,-PC.y);x.restore();}
function sliceShadow(i,cx,cy,s,rot=0){const a0=-Math.PI/2+i*Math.PI/4,a1=a0+Math.PI/4;x.save();x.translate(cx+6,cy+16);x.rotate(rot);x.scale(s,s);x.fillStyle='rgba(0,0,0,.35)';x.filter='blur(10px)';
  x.beginPath();x.moveTo(0,0);x.arc(0,0,PC.r-10,a0,a1);x.closePath();x.fill();x.restore();}
function pizzaAssemble(cx,cy,s,t,t0,step=.5){ // slices fly in, then close gaps
  const close=eio(p(t,t0+8*step+.1,t0+8*step+.5));
  for(let i=0;i<8;i++){const ti=t0+i*step;const k=p(t,ti,ti+.3);if(k<=0)continue;const mid=-Math.PI/2+i*Math.PI/4+Math.PI/8;
    const e=eo5(k);const far=1300*(1-e);const gap=26*(1-close);const ox=Math.cos(mid)*(far+gap),oy=Math.sin(mid)*(far+gap);
    const rot=(1-e)*(i%2?.8:-.8);const after=t-ti-.3;const sq=after>0&&after<.2?1+Math.sin(after/.2*Math.PI)*.04:1;
    sliceShadow(i,cx+ox,cy+oy,s*sq,rot);slice(i,cx+ox,cy+oy,s*sq,rot);}
}
function wholePizza(cx,cy,s,rot=0,shadow=true){const im=IM.pizza;x.save();x.translate(cx,cy);x.rotate(rot);x.scale(s,s);
  if(shadow){x.shadowColor='rgba(0,0,0,.5)';x.shadowBlur=50;x.shadowOffsetY=24;}x.drawImage(im,-PC.x,-PC.y);x.restore();}
function steam(cx,topY,t,a=1){x.save();x.strokeStyle=`rgba(255,255,255,${.7*a})`;x.lineWidth=14;x.lineCap='round';for(let j=-1;j<=1;j++){x.beginPath();for(let i=0;i<=16;i++){const u=i/16;x.lineTo(cx+j*120+Math.sin(u*6+t*5+j)*20,topY-u*220);}x.stroke();}x.restore();}
function box(cx,cy,s){x.save();x.translate(cx,cy);x.scale(s,s);x.fillStyle='#C9A06A';x.beginPath();x.roundRect(-260,-60,520,200,16);x.fill();
  x.fillStyle='#D8B27C';x.beginPath();x.moveTo(-260,-60);x.lineTo(260,-60);x.lineTo(220,-190);x.lineTo(-220,-190);x.closePath();x.fill();
  x.strokeStyle='rgba(0,0,0,.2)';x.lineWidth=4;x.strokeRect(-260,-60,520,200);
  circ(0,40,74,RD);T('900°',0,44,52,WH);T('FORNO',0,-125,56,RD);x.restore();}

/* ---------------- SCENES ---------------- */
function s1(t){ // 0-4 hook
  const beat=Math.floor(t/.5);const bgs=[RD,BK,YE,RD];
  if(t<2){x.fillStyle=bgs[beat%4];x.fillRect(0,0,W,H);halftone(beat%4===2?RD:BK,.18);}
  else {wood();}
  x.save();shakeAt(t,[0,.5,1.0,2.0]);
  if(t<2){
    slam('SEXTA',W/2,720,210,beat%4===2?RD:WH,t,0);
    slam('É DIA DE',W/2,920,130,beat%4===2?BK:YE,t,.5);
    slam('PIZZA!',W/2,1130,250,beat%4===2?RD:YE,t,1.0,{rot:-.05,stroke:beat%4===2?0:14,sc:BK});
  } else {
    deco(t-2,[['basil',170,330,1.0,-.4],['tomato',900,300,1.3,.3],['tomato',960,1500,1.1,-.6],['basil',120,1480,.8,1.9]]);
    const k=pop(t,2.0,.45);x.save();x.translate(W/2,900);x.scale(k,k);burst(0,0,360,YE,t,16);burst(0,0,300,RD,-t,16,.2);
    T('FORNO',0,-60,130,WH,{stroke:14,sc:BK});T('900°',0,70,130,YE,{stroke:14,sc:BK});x.restore();
    sticker('PIZZA NAPOLITANA',W/2,1210,50,BK,YE,t,2.5,-.04);
  }
  x.restore();
}
function s2(t){ // 4-10 slice by slice
  wood();
  T('FATIA POR FATIA',W/2,330,72,WH,{a:eo(p(t,0,.3)),stroke:10,sc:BK});
  pizzaAssemble(W/2,1000,.86,t,.5,.5);
  if(t>4.6)steam(W/2,560,t,cl((t-4.6)*3));
  sticker('MASSA DE LONGA FERMENTAÇÃO',W/2,1545,40,YE,BK,t,1.0,-.03);
  sticker('MOLHO ITALIANO',220,690,42,RD,WH,t,2.0,-.1);
  sticker('MUÇARELA',880,700,42,BK,YE,t,3.0,.1);
  sticker('FORNO A LENHA',840,1410,44,RD,WH,t,4.0,.08);
}
function s3(t){ // 10-16 price
  x.fillStyle=RD;x.fillRect(0,0,W,H);rays(W/2,1060,t,'#C21F18',RD,22);halftone(BK,.12);
  wholePizza(W/2,1080,.8*eo5(p(t,0,.5)),t*.25);
  x.save();shakeAt(t,[.5,1.5],14);
  slam('DE R$ 89,90',W/2,400,90,WH,t,.5);
  const sk=eo5(p(t,1.0,1.25));if(sk>0){x.strokeStyle=YE;x.lineWidth=14;x.lineCap='round';x.beginPath();x.moveTo(W/2-300,410);x.lineTo(W/2-300+600*sk,390);x.stroke();}
  slam('POR APENAS',W/2,560,70,YE,t,1.5);
  const bk=pop(t,1.5,.45);x.save();x.translate(W/2,1060);x.scale(bk,bk);burst(0,0,340,YE,t,18);burst(0,0,290,WH,-t*.5,18,.15);x.restore();
  const v=lerp(89.9,59.9,eo(p(t,1.7,2.6)));if(t>1.7){T('R$',W/2,945,64,RD);priceSlots(money(v),W/2,1070,170,RD,0);}
  x.restore();
  sticker('PIZZA GRANDE · 8 FATIAS',W/2,1450,46,BK,YE,t,3.0,-.04);
  sticker('+ REFRI',W/2,1560,46,WH,RD,t,3.5,.05);
}
function s4(t){ // 16-20 urgency
  wood();x.fillStyle='rgba(0,0,0,.35)';x.fillRect(0,0,W,H);
  band(360,-.07,'SÓ HOJE',t*300,YE,BK);band(1480,.06,'PEDE JÁ',-t*260,RD,WH);
  T('PROMO ACABA EM',W/2,640,64,WH,{a:eo(p(t,.2,.5))});
  const total=2*3600+59*60+59-Math.floor(t);const hh=String(Math.floor(total/3600)).padStart(2,'0'),mm=String(Math.floor(total%3600/60)).padStart(2,'0'),ss=String(total%60).padStart(2,'0');
  const k=pop(t,.4,.4);x.save();x.translate(W/2,860);x.scale(k,k);
  [hh,mm,ss].forEach((g,i)=>{const bx=(i-1)*300;x.fillStyle='rgba(20,12,8,.85)';x.beginPath();x.roundRect(bx-130,-120,260,240,40);x.fill();const fl=i===2?Math.exp(-((t%1))*6):0;
    x.save();if(i===2){x.translate(bx,0);x.scale(1+fl*.08,1+fl*.08);x.translate(-bx,0);}priceSlots(g,bx,8,170,i===2?YE:WH,0);x.restore();
    T(['HORAS','MIN','SEG'][i],bx,175,40,'#C9B8A6',{font:P,w:600});});
  T(':',-150,0,150,WH);T(':',150,0,150,WH);x.restore();
  const bt=pop(t,1.5,.4);const pul=1+.05*Math.exp(-((t%.5))*8);x.save();x.translate(W/2,1210);x.scale(bt*pul,bt*pul);x.fillStyle=YE;x.beginPath();x.roundRect(-330,-80,660,160,80);x.fill();T('PEDIR AGORA',0,6,74,BK);x.restore();
}
function s5(t){ // 20-24 montage
  const i=Math.min(3,Math.floor(t));const lt=t-i;
  if(i===1||i===3){x.fillStyle=i===1?YE:RD;x.fillRect(0,0,W,H);halftone(BK,.14);}else wood();
  x.save();shakeAt(t,[0,1,2,3],12);
  slam(['PEPPERONI','FATIA','COMBO','DELIVERY'][i],W/2,420,i===0?150:180,i===1?RD:YE,t,i,{stroke:14,sc:BK});
  const k=pop(t,i+.05,.4);x.save();x.translate(W/2,1060);x.scale(k,k);
  if(i===0){wholePizza(0,0,.8,lt*.8);deco(lt,[['basil',-380,-420,.7,-.5],['tomato',390,440,1.0,.4]]);}
  else if(i===1){const mid=-Math.PI/2+4*Math.PI/4+Math.PI/8,sc=1.3;x.rotate(Math.sin(lt*3)*.04);const ox=-Math.cos(mid)*PC.r*.55*sc,oy=-Math.sin(mid)*PC.r*.55*sc;sliceShadow(4,ox,oy,sc,0);slice(4,ox,oy,sc,0);}
  else if(i===2){wholePizza(-110,40,.62,0);const im=IM.soda,w=230,h=w*im.height/im.width;x.save();x.shadowColor='rgba(0,0,0,.5)';x.shadowBlur=30;x.drawImage(im,250-w/2,260-h,w,h);x.restore();}
  else {box(0,0,1.2);T('30 MIN',0,280,80,WH,{stroke:10,sc:BK});}
  x.restore();x.restore();
  if(i===3)sticker('ENTREGA RÁPIDA',W/2,1500,48,WH,RD,t,3.2,-.05);
}
function s6(t){ // 24-32 CTA
  wood();x.fillStyle='rgba(15,9,5,.55)';x.fillRect(0,0,W,H);
  deco(t,[['basil',150,1650,.9,-.3],['tomato',930,1640,1.2,.5],['basil',960,220,.7,2.4]]);
  slam('ESSA PIZZARIA',W/2,380,90,WH,t,.0);
  slam('NÃO EXISTE.',W/2,490,110,RD,t,.5,{rot:-.03,stroke:10,sc:BK});
  const kk=eo(p(t,1.5,1.8));T('MAS SEU ANÚNCIO',W/2,700,80,WH,{a:kk});
  slam('PODE BOMBAR',W/2,830,120,YE,t,2.0,{rot:.02,stroke:12,sc:BK});
  slam('ASSIM.',W/2,970,140,YE,t,2.5,{rot:-.03,stroke:12,sc:BK});
  sticker('MOTION PARA PIZZARIAS E DELIVERY',W/2,1120,40,RD,WH,t,3.2,-.02);
  const bt=pop(t,4.0,.4);const pul=1+.04*Math.exp(-((t%.5))*8)*(t>4.5?1:0);x.save();x.translate(W/2,1310);x.scale(bt*pul,bt*pul);x.fillStyle=YE;x.beginPath();x.roundRect(-350,-75,700,150,75);x.fill();T('ME CHAMA NO DIRECT',0,6,58,BK);x.restore();
  const ak=eo5(p(t,4.5,4.9));if(ak>0){x.save();x.beginPath();x.rect(0,1400,W,120);x.clip();T('@alecreator_motion',W/2,1460+(1-ak)*100,60,WH,{font:P,w:700});x.restore();}
}
const SC=[[s1,0,4],[s2,4,10],[s3,10,16],[s4,16,20],[s5,20,24],[s6,24,32]];
window.DUR=32;
function flash(t){for(const [,a] of SC){if(a===0)continue;const d=t-a;if(d>=0&&d<.12){x.fillStyle=`rgba(255,255,255,${.6*(1-d/.12)})`;x.fillRect(0,0,W,H);}}}
window.draw=function(t){const s=SC.find(([,a,b])=>t>=a&&t<b)||SC[SC.length-1];
  const bp=t%0.5;const punch=1+.01*Math.exp(-bp*12);x.save();x.translate(W/2,H/2);x.scale(punch,punch);x.translate(-W/2,-H/2);s[0](t-s[1]);x.restore();flash(t);
  const fo=p(t,31.4,32);if(fo>0){x.fillStyle=`rgba(0,0,0,${fo})`;x.fillRect(0,0,W,H);}};
draw(1);
</script></body></html>

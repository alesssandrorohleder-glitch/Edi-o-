
const W=1080,H=1920,c=document.getElementById('c');let x=c.getContext('2d');const X0=x;
const BG='#F6F1EA',INK='#1F2326',GRY='#7B8086',SAL='#F07A55',SALD='#D9603D',GRN='#5E9E5A',WH='#FFFFFF';
const DISP='"Inter Display",Inter,sans-serif',SANS='Inter,sans-serif';
const cl=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)),p=(t,a,b)=>cl((t-a)/(b-a));
const eo=t=>1-Math.pow(1-t,3),eo5=t=>1-Math.pow(1-t,5),eio=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2,sine=t=>-(Math.cos(Math.PI*t)-1)/2;
const back=t=>{if(t<=0)return 0;const c1=1.3,c3=c1+1;return 1+c3*Math.pow(t-1,3)+c1*Math.pow(t-1,2)};
const lerp=(a,b,k)=>a+(b-a)*k;
function T(s,X,Y,size,col,{font=SANS,w=400,align='center',a=1,ls=0}={}){x.save();x.globalAlpha*=a;x.fillStyle=col;x.font=`${w} ${size}px ${font}`;x.textAlign=align;x.textBaseline='middle';x.letterSpacing=ls+'px';x.fillText(s,X,Y);x.restore();}
function up(s,X,Y,size,col,t,t0,o={}){const k=eo5(p(t,t0,t0+.7));if(k<=0)return;x.save();x.beginPath();x.rect(0,Y-size*.8,W,size*1.6);x.clip();T(s,X,Y+(1-k)*size*.9,size,col,o);x.restore();}
function fade(s,X,Y,size,col,t,t0,o={}){const k=eo(p(t,t0,t0+.6));if(k<=0)return;T(s,X,Y+(1-k)*16,size,col,{...o,a:k});}
function bg(t){x.fillStyle=BG;x.fillRect(0,0,W,H);
  [[160,240,420,'rgba(240,122,85,.10)'],[960,1700,520,'rgba(94,158,90,.07)'],[980,300,300,'rgba(240,122,85,.06)']].forEach(([cx,cy,r,col],i)=>{const X=cx+Math.sin(t*.3+i)*30,Y=cy+Math.cos(t*.25+i)*30;const g=x.createRadialGradient(X,Y,0,X,Y,r);g.addColorStop(0,col);g.addColorStop(1,'rgba(0,0,0,0)');x.fillStyle=g;x.fillRect(0,0,W,H);});}
function wave(cx,cy,w,k,col=SAL,lw=10,ph=0){if(k<=0)return;x.save();x.strokeStyle=col;x.lineWidth=lw;x.lineCap='round';x.beginPath();const n=80;for(let i=0;i<=n*k;i++){const u=i/n;const X=cx-w/2+u*w,Y=cy+Math.sin(u*Math.PI*3+ph)*w*.045;i?x.lineTo(X,Y):x.moveTo(X,Y);}x.stroke();x.restore();}
// photo card with rounded corners, soft shadow and slow inner zoom
function card(im,cx,cy,w,h,t,t0,{from='up',z0=1.12,z1=1.0,dur=4,r=40}={}){const k=eo5(p(t,t0,t0+.9));if(k<=0)return;
  const oy=from==='up'?(1-k)*260:0,ox=from==='right'?(1-k)*700:from==='left'?-(1-k)*700:0,rot=(1-k)*(from==='up'?.05:0);
  const z=lerp(z0,z1,sine(p(t,t0,t0+dur)));
  x.save();x.translate(cx+ox,cy+oy);x.rotate(rot);x.globalAlpha=cl(k*1.5);
  x.shadowColor='rgba(31,35,38,.22)';x.shadowBlur=60;x.shadowOffsetY=30;x.fillStyle=WH;x.beginPath();x.roundRect(-w/2,-h/2,w,h,r);x.fill();x.shadowColor='transparent';
  x.beginPath();x.roundRect(-w/2,-h/2,w,h,r);x.clip();
  const sc=Math.max(w/im.width,h/im.height)*z;const iw=im.width*sc,ih=im.height*sc;x.drawImage(im,-iw/2,-ih/2,iw,ih);
  // gentle light sweep
  const sw=p(t,t0+.9,t0+2.2);if(sw>0&&sw<1){const sx=lerp(-w,w,sine(sw));const g=x.createLinearGradient(sx-120,0,sx+120,0);g.addColorStop(0,'rgba(255,255,255,0)');g.addColorStop(.5,'rgba(255,255,255,.16)');g.addColorStop(1,'rgba(255,255,255,0)');x.fillStyle=g;x.save();x.transform(1,0,-.3,1,0,0);x.fillRect(-w*1.5,-h/2,w*3,h);x.restore();}
  x.restore();}
function pill(s,X,Y,size,bg,fg,k){if(k<=0)return;x.save();x.translate(X,Y);x.scale(k,k);x.font=`600 ${size}px ${SANS}`;const w=x.measureText(s).width+size*1.5,h=size*1.9;x.fillStyle=bg;x.beginPath();x.roundRect(-w/2,-h/2,w,h,h/2);x.fill();T(s,0,2,size,fg,{w:600});x.restore();}
function productScene(t,{img,num,name,title,desc,price}){bg(t);
  card(img,W/2,790,560,1000,t,.05);
  fade(`${num}  ·  ${name}`,W/2,1400,40,SAL,t,.45,{w:600,ls:6});
  up(title,W/2,1478,72,INK,t,.6,{font:DISP,w:600});
  fade(desc,W/2,1545,40,GRY,t,.9,{w:400});
  pill(price,840,350,42,INK,WH,back(p(t,1.3,1.75)));
}

/* ---------------- SCENES ---------------- */
function s1(t){ // 0-4 logo
  bg(t);
  wave(W/2,760,520,eio(p(t,.2,1.2)),SAL,12);
  wave(W/2,800,380,eio(p(t,.45,1.4)),'rgba(240,122,85,.45)',8,1.2);
  const k=eo5(p(t,.9,1.6));if(k>0){x.save();x.beginPath();x.rect(0,820,W,280);x.clip();x.translate(0,(1-k)*200);
    x.font=`600 200px ${DISP}`;x.letterSpacing='-4px';x.textBaseline='middle';x.textAlign='left';const a='mar',b='é';const wa=x.measureText(a).width,wb=x.measureText(b).width;const X0p=W/2-(wa+wb)/2;
    x.fillStyle=INK;x.fillText(a,X0p,960);x.fillStyle=SAL;x.fillText(b,X0p+wa,960);x.restore();}
  fade('SUSHI  ·  DELIVERY  ·  RODÍZIO',W/2,1130,40,GRY,t,1.6,{w:500,ls:8});
}
function s2(t){ // 4-8 hero
  bg(t);
  card(IM.hero,W/2,800,620,1110,t,.0,{z0:1.1,z1:1.0});
  up('Sushi fresquinho,',W/2,1440,64,INK,t,.9,{font:DISP,w:600});
  up('do jeito brasileiro.',W/2,1525,64,SAL,t,1.15,{font:DISP,w:600});
}
function s3(t){productScene(t,{img:IM.t1,num:'01',name:'NIGIRI',title:'Nigiri de salmão',desc:'peixe fresco, corte do dia',price:'R$ 18,90'});}
function s4(t){productScene(t,{img:IM.t2,num:'02',name:'URAMAKI',title:'Uramaki filadélfia',desc:'salmão, cream cheese e gergelim',price:'R$ 24,90'});}
function s5(t){productScene(t,{img:IM.t6,num:'03',name:'HOT ROLL',title:'Hot roll crocante',desc:'o queridinho do Brasil',price:'R$ 26,90'});}
function s6(t){productScene(t,{img:IM.t4,num:'04',name:'TEMAKI',title:'Temaki de salmão',desc:'com cebolinha e muito sabor',price:'R$ 29,90'});}
function s7(t){ // 24-28 combos
  bg(t);
  card(IM.t8,W/2-120,820,520,930,t,.05,{from:'left'});
  card(IM.t9,W/2+230,1000,380,680,t,.45,{from:'right',r:32});
  fade('COMBINADOS',W/2,1450,40,SAL,t,.8,{w:600,ls:8});
  up('Peça pelo app.',W/2,1525,64,INK,t,1.0,{font:DISP,w:600});
  pill('Entrega em 40 min',W/2,330,42,SAL,WH,back(p(t,1.4,1.85)));
}
function s8(t){ // 28-34 CTA
  bg(t);
  wave(W/2,430,300,eio(p(t,.1,1.0)),SAL,10);
  fade('Esse restaurante não existe.',W/2,620,46,GRY,t,.4,{w:400});
  up('Mas o vídeo do seu',W/2,760,80,INK,t,.9,{font:DISP,w:600});
  up('pode ficar assim.',W/2,860,80,SAL,t,1.15,{font:DISP,w:600});
  ['Restaurantes e delivery','Reels e anúncios','Cardápio animado'].forEach((s,i)=>{const k=eo(p(t,1.8+i*.25,2.4+i*.25));if(k<=0)return;x.save();x.globalAlpha=k;x.translate((1-k)*-30,0);
    x.fillStyle=SAL;x.beginPath();x.arc(290,1010+i*84,9,0,7);x.fill();T(s,320,1010+i*84,44,INK,{align:'left',w:500});x.restore();});
  const bk=back(p(t,2.9,3.4));const pul=1+.025*Math.exp(-((t%.5))*8)*(t>3.4?1:0);if(bk>0){x.save();x.translate(W/2,1330);x.scale(bk*pul,bk*pul);x.fillStyle=INK;x.beginPath();x.roundRect(-330,-72,660,144,72);x.fill();T('Me chama no direct',0,3,48,WH,{w:600});x.restore();}
  fade('@alecreator_motion',W/2,1470,54,SAL,t,3.4,{w:600});
}
const SC=[[s1,0,4],[s2,4,8],[s3,8,12],[s4,12,16],[s5,16,20],[s6,20,24],[s7,24,28],[s8,28,34]];
window.DUR=34;const XF=.32;
const buf=document.createElement('canvas');buf.width=W;buf.height=H;const bx=buf.getContext('2d');
window.draw=function(t){const i=SC.findIndex(([,a,b])=>t>=a&&t<b);const k=i<0?SC.length-1:i;const [f,a]=SC[k];
  x=X0;x.save();f(t-a);x.restore();
  if(k>0&&t-a<XF){const [pf,pa]=SC[k-1];x=bx;x.save();x.setTransform(1,0,0,1,0,0);x.globalAlpha=1;pf(t-pa);x.restore();x=X0;
    const e=eio((t-a)/XF);x.save();x.globalAlpha=1-e;x.drawImage(buf,-e*260,0);x.restore();}
  const fi=1-p(t,0,.4),fo=p(t,33.4,34);const f2=Math.max(fi,fo);if(f2>0){x.fillStyle=`rgba(246,241,234,${f2})`;x.fillRect(0,0,W,H);}};
</script></body></html>


const W=1080,H=1920,c=document.getElementById('c');let x=c.getContext('2d');const X0=x;
const INK='#0E0E0E',PAPER='#ECECE8',WH='#FFFFFF',LIME='#D4FF2A',GRY='#8C8C88',GRYD='#6A6A66';
const DISP='"Inter Display",Inter,sans-serif',SANS='Inter,sans-serif';
const BPM=128,BT=60/BPM,BAR=BT*4,M=90;
const cl=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)),p=(t,a,b)=>cl((t-a)/(b-a));
const eo=t=>1-Math.pow(1-t,3),eo5=t=>1-Math.pow(1-t,5),eio=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2,sine=t=>-(Math.cos(Math.PI*t)-1)/2;
const eqi=t=>t<.5?16*t**5:1-Math.pow(-2*t+2,5)/2;
const lerp=(a,b,k)=>a+(b-a)*k;
const rnd=s=>{const r=Math.sin(s*127.1+311.7)*43758.5453;return r-Math.floor(r)};
const img=k=>(typeof IM!=='undefined'&&IM[k]&&IM[k].naturalWidth)?IM[k]:null;

function TX(s,X,Y,size,col,{w=900,ls=null,align='left',a=1,font=DISP,fit=0}={}){
  x.save();x.globalAlpha*=a;x.font=`${w} ${size}px ${font}`;x.letterSpacing=(ls??(w>=800?-size*.035:0))+'px';x.textAlign=align;x.textBaseline='middle';
  let sc=1;if(fit){const mw=x.measureText(s).width;if(mw>fit)sc=fit/mw;}
  x.translate(X,Y);x.scale(sc,sc);x.fillStyle=col;x.fillText(s,0,0);x.restore();}
function LB(s,X,Y,col,{align='left',a=1,size=40,w=600}={}){TX(s,X,Y,size,col,{w,ls:4,align,a,font:SANS});}
function up(s,X,Y,size,col,t,t0,o={}){const k=eqi(p(t,t0,t0+.55));if(k<=0)return;x.save();x.beginPath();x.rect(0,Y-size*.62,W,size*1.24);x.clip();TX(s,X,Y+(1-k)*size*1.15,size,col,o);x.restore();}
function lab(s,X,Y,col,t,t0,o={}){const k=eo(p(t,t0,t0+.45));if(k<=0)return;x.save();x.beginPath();x.rect(0,Y-30,W,60);x.clip();LB(s,X,Y+(1-k)*44,col,o);x.restore();}
function hair(X0,X1,Y,col,t,t0,d=.5){const k=eqi(p(t,t0,t0+d));if(k<=0)return;x.fillStyle=col;x.fillRect(X0,Y-1,(X1-X0)*k,2);}
const NZ=document.createElement('canvas');NZ.width=NZ.height=256;{const g=NZ.getContext('2d'),d=g.createImageData(256,256);for(let i=0;i<d.data.length;i+=4){const v=Math.random()*255;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=255;}g.putImageData(d,0,0);}
function grain(t,a=.035){x.save();x.globalAlpha=a;x.globalCompositeOperation='overlay';const f=Math.floor(t*30);const ox=-rnd(f)*256,oy=-rnd(f+7)*256;for(let X=ox;X<W;X+=256)for(let Y=oy;Y<H;Y+=256)x.drawImage(NZ,X,Y);x.restore();}
function shoe(k,cx,cy,w,{rot=0,hue=0,shadow=1,trail=0,a=1,dark=true}={}){const im=img(k);if(!im)return;const h=w*im.height/im.width;
  x.save();x.globalAlpha*=a;x.translate(cx,cy);
  if(shadow>0){x.save();x.scale(1,.12);const g=x.createRadialGradient(0,h*.46/.12,0,0,h*.46/.12,w*.48);g.addColorStop(0,`rgba(0,0,0,${(dark?.7:.28)*shadow})`);g.addColorStop(1,'rgba(0,0,0,0)');x.fillStyle=g;x.fillRect(-w*.6,h*.46/.12-w*.5,w*1.2,w);x.restore();}
  x.rotate(rot);if(hue)x.filter=`hue-rotate(${hue}deg)`;
  if(trail>1){for(let i=3;i>=1;i--){x.globalAlpha=a*.10;x.drawImage(im,-w/2-trail*i,-h/2,w,h);}x.globalAlpha=a;}
  x.drawImage(im,-w/2,-h/2,w,h);x.filter='none';x.restore();}
function cover(im,z=1,ox=0,oy=0){if(!im)return;x.save();x.translate(W/2+ox,H/2+oy);const s=Math.max(W/im.width,H/im.height)*z;x.drawImage(im,-im.width*s/2,-im.height*s/2,im.width*s,im.height*s);x.restore();}
function chrome(col,right,t,a=1){const k=eo(p(t,.05,.5))*a;if(k<=0)return;LB('ZEFYR',M,300,col,{a:k,w:800});LB(right,W-M,300,col,{a:k,align:'right',w:500});}

/* S1 0–3.75  statement on paper, ink panel rises into drop */
function s1(t){x.fillStyle=PAPER;x.fillRect(0,0,W,H);chrome(INK,'ZF-1 PHANTOM',t);
  up('ISSO NÃO',M,780,180,INK,t,.02);up('É SÓ UM',M,960,180,INK,t,BT*2);up('TÊNIS.',M,1140,180,INK,t,BT*4);
  const ul=eqi(p(t,BT*4+.25,BT*4+.75));if(ul>0){x.fillStyle=LIME;x.fillRect(M,1250,560*ul,18);}
  lab('LANÇAMENTO SS26',M,1380,GRYD,t,BT*6);
  const pk=eqi(p(t,3.25,3.75));if(pk>0){x.fillStyle=INK;x.fillRect(0,H*(1-pk),W,H*pk);}
}
/* S2 3.75–7.5 hero: word behind, shoe slides in */
function s2(t){x.fillStyle=INK;x.fillRect(0,0,W,H);
  const z=lerp(1,1.035,sine(p(t,0,3.75)));x.save();x.translate(W/2,900);x.scale(z,z);x.translate(-W/2,-900);
  up('ZEFYR',W/2,560,330,WH,t,.05,{align:'center',fit:940});
  const k=eo5(p(t,.05,.8));const hv=Math.sin(Math.max(0,t-.8)*2.2)*8*p(t,.8,1.4);
  shoe('side',lerp(-620,W/2,k),905+hv,960,{rot:lerp(.06,0,k),trail:(1-k)*40,shadow:k});
  x.restore();
  chrome(WH,'01',t,p(t,.6,1));
  lab('ZF-1 PHANTOM',M,1255,LIME,t,BT*2);
  up('O FUTURO TÁ',M,1360,108,WH,t,BT*3,{fit:900});up('NOS SEUS PÉS.',M,1470,108,WH,t,BT*3+.12,{fit:900});
}
/* S3 7.5–11.25 specs table */
function counter(v,t,t0,d=.7){return Math.round(v*eo(p(t,t0,t0+d)));}
function s3(t){x.fillStyle=PAPER;x.fillRect(0,0,W,H);chrome(INK,'02  ENGENHARIA',t);
  const k=eo5(p(t,0,.7));const fl=Math.sin(t*1.8)*8;
  shoe('q34',W/2,770+(1-k)*60+fl,800,{a:k,rot:Math.sin(t*1.2)*.015,dark:false,shadow:k});
  const rows=[['PESO',t2=>counter(212,t2,BT*2+.1)+' g'],['RETORNO DE ENERGIA',t2=>'+'+counter(38,t2,BT*4+.1)+'%'],['ESPUMA',()=>'AERO-X']];
  rows.forEach(([l,v],i)=>{const t0=BT*2*(i+1),Y=1195+i*120;hair(M,W-M,Y-60,INK,t,t0-.1);
    lab(l,M,Y,GRYD,t,t0);up(v(t),W-M,Y,76,INK,t,t0,{align:'right'});});
  hair(M,W-M,1195+2*120+60,INK,t,BT*6+.2);
}
/* S4 11.25–15 sole: full bleed, then GRIP knockout on paper */
function s4(t){if(t<BAR){const g0=img('sole');cover(g0,lerp(1.14,1.04,sine(p(t,0,BAR))),-40,0);
    const g=x.createLinearGradient(0,900,0,H);g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(1,'rgba(0,0,0,.8)');x.fillStyle=g;x.fillRect(0,0,W,H);
    chrome(WH,'03  SOLADO',t);up('TRAÇÃO',M,1360,190,WH,t,BT,{fit:900});lab('SOLADO MULTIDIRECIONAL',M,1480,LIME,t,BT*2);return;}
  const u=t-BAR;x.fillStyle=PAPER;x.fillRect(0,0,W,H);chrome(INK,'03  SOLADO',u+1);
  const sc=lerp(1.12,1,eo5(p(u,0,.7)));
  const L=document.__kc||(document.__kc=document.createElement('canvas'));L.width=W;L.height=H;const l=L.getContext('2d');
  l.save();l.translate(W/2,880);l.scale(sc,sc);l.font=`900 420px ${DISP}`;l.letterSpacing='-16px';l.textAlign='center';l.textBaseline='middle';
  const mw=l.measureText('GRIP').width;const f=Math.min(1,960/mw);l.scale(f,f);l.fillStyle='#fff';l.fillText('GRIP',0,0);l.restore();
  l.globalCompositeOperation='source-in';const xx=x;x=l;cover(img('sole2'),lerp(1.05,1.18,p(u,0,BAR)),0,-60);x=xx;l.globalCompositeOperation='source-over';
  x.drawImage(L,0,0);
  up('EM QUALQUER CHÃO.',W/2,1180,64,INK,t,BAR+BT*2,{align:'center'});
}
/* S5 15–18.75 street, cinematic */
function s5(t){const im=img('street');const z=lerp(1.32,1.15,sine(p(t,0,3.75)));cover(im,z,440*z+lerp(25,-25,p(t,0,3.75)),-100);
  const g=x.createLinearGradient(0,0,0,H);g.addColorStop(0,'rgba(0,0,0,.65)');g.addColorStop(.42,'rgba(0,0,0,0)');g.addColorStop(.85,'rgba(0,0,0,0)');g.addColorStop(1,'rgba(0,0,0,.5)');x.fillStyle=g;x.fillRect(0,0,W,H);
  up('FEITO',M,400,170,WH,t,BT);up('PRA RUA.',M,570,170,WH,t,BT*2,{fit:900});
  lab('04  CIDADE',M,700,LIME,t,BT*3);
  const lb=eqi(p(t,0,.6))*130;x.fillStyle='#000';x.fillRect(0,0,W,lb);x.fillRect(0,H-lb,W,lb);
}
/* S6 18.75–22.5 colorways with panel push */
const CW=[['PHANTOM',0,'#121212',LIME],['OCEAN',150,'#14305A','#7FC8FF'],['INFRARED',-90,'#561417','#FF5A5F'],['SOLAR',-50,'#6E360B','#FFB347']];
function panel(i,ox,t){const [name,hue,bg,ac]=CW[i];x.save();x.translate(ox,0);x.fillStyle=bg;x.fillRect(0,0,W,H);
  LB('COLORWAY',M,300,WH,{a:.7});LB(`0${i+1} / 04`,W-M,300,WH,{align:'right',a:.7,w:500});
  x.restore();
  shoe('side',W/2+ox*1.25,880+Math.sin(t*2)*6,920,{hue,shadow:1});
  x.save();x.translate(ox,0);TX(name,M,1330,170,WH,{fit:900});
  CW.forEach((cw,j)=>{x.beginPath();x.arc(M+22+j*70,1470,18,0,7);x.fillStyle=cw[3];x.globalAlpha=j===i?1:.35;x.fill();if(j===i){x.globalAlpha=1;x.strokeStyle=WH;x.lineWidth=3;x.beginPath();x.arc(M+22+j*70,1470,28,0,7);x.stroke();}});
  x.restore();}
function s6(t){const i=Math.min(3,Math.floor(t/(BT*2))),u=t-i*BT*2;
  if(i>0&&u<.4){const e=eqi(u/.4);panel(i-1,-W*e,t);panel(i,W*(1-e),t);}else panel(i,0,t);}
/* S7 22.5–26.25 drop info */
function slot(s,X,Y,size,t,t0,col){x.save();x.font=`900 ${size}px ${DISP}`;x.letterSpacing='0px';const ws=[...s].map(ch=>x.measureText(ch).width*.94);let cx=X;
  [...s].forEach((ch,j)=>{const st=t0+j*.07,k=eo5(p(t,st,st+.65));if(k<=0){cx+=ws[j];return;}x.save();x.beginPath();x.rect(cx-6,Y-size*.6,ws[j]+12,size*1.2);x.clip();
    const n=/\d/.test(ch)?5:0,off=(1-k)*n;for(let r=0;r<=n;r++){const d=r-off;if(Math.abs(d)>1.2)continue;const c2=r===0?ch:String(Math.floor(rnd(r*7+j)*10));
      TX(c2,cx+ws[j]/2,Y+d*size*1.1,size,col,{align:'center',ls:0});}x.restore();cx+=ws[j];});x.restore();}
function s7(t){x.fillStyle=INK;x.fillRect(0,0,W,H);chrome(WH,'05  DROP',t);
  lab('LANÇAMENTO OFICIAL',M,400,LIME,t,.05);slot('11.11',M,600,250,t,.15,WH);
  const k=eo5(p(t,BT*2,BT*2+.7));shoe('side',W/2,935+(1-k)*50+Math.sin(t*1.8)*6,820,{a:k,shadow:k});
  hair(M,W-M,1250,'rgba(255,255,255,.35)',t,BT*4-.1);
  lab('EDIÇÃO LIMITADA',M,1305,GRY,t,BT*4);up('500 PARES',M,1385,76,WH,t,BT*4+.05);
  lab('PREÇO',580,1305,GRY,t,BT*5);up('R$ 899',580,1385,76,WH,t,BT*5+.05);
  hair(M,W-M,1450,'rgba(255,255,255,.35)',t,BT*5+.2);
}
/* S8 26.25–31.875 CTA */
function s8(t){x.fillStyle=INK;x.fillRect(0,0,W,H);chrome(WH,'@alecreator_motion',t);
  lab('Essa marca não existe.',M,430,GRY,t,.15,{w:500});
  up('MAS O SEU',M,560,112,WH,t,BT);up('LANÇAMENTO',M,680,112,WH,t,BT+.1,{fit:900});up('PODE TER ESSE',M,800,112,WH,t,BT*2,{fit:900});up('IMPACTO.',M,920,112,LIME,t,BT*3);
  ['Anúncios de produto','Lançamentos e drops','Reels de alto impacto'].forEach((s,i)=>{const t0=BT*4.4+i*.18;hair(M,W-M,1035+i*80,'rgba(255,255,255,.18)',t,t0-.1);lab(s,M,1075+i*80,WH,t,t0,{w:500,size:42});});
  hair(M,W-M,1035+3*80,'rgba(255,255,255,.18)',t,BT*4.4+.5);
  const bk=eqi(p(t,BT*7,BT*7+.5));if(bk>0){x.save();x.beginPath();x.rect(M,1330,620*bk,130);x.clip();x.fillStyle=LIME;x.beginPath();x.roundRect(M,1330,620,130,65);x.fill();
    TX('Me chama no direct',M+310,1397,48,INK,{w:700,align:'center',font:SANS,ls:0});x.restore();}
  lab('@alecreator_motion',M,1530,WH,t,BT*8,{size:48,w:600});
}

const SC=[[s1,0,3.75],[s2,3.75,7.5],[s3,7.5,11.25],[s4,11.25,15],[s5,15,18.75],[s6,18.75,22.5],[s7,22.5,26.25],[s8,26.25,31.875]];
window.DUR=31.875;
window.draw=function(t){x=X0;const i=SC.findIndex(([,a,b])=>t>=a&&t<b);const k=i<0?SC.length-1:i;const [f,a]=SC[k];const lt=t-a;
  x.save();if(k>1){const zp=1+.03*(1-eo(p(lt,0,.5)));x.translate(W/2,H/2);x.scale(zp,zp);x.translate(-W/2,-H/2);}
  f(lt);x.restore();grain(t);
  const fo=p(t,31.3,31.875);if(fo>0){x.fillStyle=`rgba(0,0,0,${fo})`;x.fillRect(0,0,W,H);}
  const fi=1-p(t,0,.25);if(fi>0){x.fillStyle=`rgba(236,236,232,${fi})`;x.fillRect(0,0,W,H);}
};

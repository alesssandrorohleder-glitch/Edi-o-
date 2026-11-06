
const W=1080,H=1920,c=document.getElementById('c');let x=c.getContext('2d');const X0=x;
const NAVY='#0E1A27',CREAM='#F3EEE6',GOLD='#C9A46A',GOLDL='#E4C892',WH='#FFFFFF',INK='#1C2430',GRY='#8D8A84';
const SERIF='Lora,serif',SANS='Inter,sans-serif';
const BPM=120,BT=.5,BAR=2,M=90;
const cl=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)),p=(t,a,b)=>cl((t-a)/(b-a));
const eo=t=>1-Math.pow(1-t,3),eo5=t=>1-Math.pow(1-t,5),eio=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2,sine=t=>-(Math.cos(Math.PI*t)-1)/2;
const lerp=(a,b,k)=>a+(b-a)*k;const rnd=s=>{const r=Math.sin(s*127.1+311.7)*43758.5453;return r-Math.floor(r)};
function TX(s,X,Y,size,col,{w=400,ls=0,align='left',a=1,font=SERIF,italic=false,fit=0}={}){x.save();x.globalAlpha*=a;x.font=`${italic?'italic ':''}${w} ${size}px ${font}`;x.letterSpacing=ls+'px';x.textAlign=align;x.textBaseline='middle';
  let sc=1;if(fit){const mw=x.measureText(s).width;if(mw>fit)sc=fit/mw;}x.translate(X,Y);x.scale(sc,sc);x.fillStyle=col;x.fillText(s,0,0);x.restore();}
function LB(s,X,Y,col,o={}){TX(s,X,Y,o.size||40,col,{w:o.w||600,ls:o.ls??8,align:o.align||'left',a:o.a??1,font:SANS});}
function up(s,X,Y,size,col,t,t0,o={}){const k=eo5(p(t,t0,t0+.9));if(k<=0)return;x.save();x.beginPath();x.rect(0,Y-size*.75,W,size*1.5);x.clip();TX(s,X,Y+(1-k)*size*1.1,size,col,{...o,a:(o.a??1)*cl(k*1.6)});x.restore();}
function lab(s,X,Y,col,t,t0,o={}){const k=eo5(p(t,t0,t0+.8));if(k<=0)return;LB(s,X+(1-k)*(o.align==='right'?-30:30)*(o.align==='center'?0:1),Y,col,{...o,a:k*(o.a??1)});}
function hair(X0,X1,Y,col,t,t0,d=.7){const k=eio(p(t,t0,t0+d));if(k<=0)return;x.fillStyle=col;x.fillRect(X0,Y-1,(X1-X0)*k,2);}
function vfull(arr,ct,{z=1}={}){const n=arr.length;const fi=Math.max(0,Math.min(n-1.001,ct*24));const i0=Math.floor(fi),fr=arr[i0],fr2=arr[Math.min(n-1,i0+1)],bl=fi-i0;
  x.fillStyle='#000';x.fillRect(0,0,W,H);if(!fr||!fr.naturalWidth)return;x.save();x.translate(W/2,H/2);x.scale(z,z);x.translate(-W/2,-H/2);x.drawImage(fr,0,0,W,H);if(bl>.01&&fr2&&fr2.naturalWidth){x.globalAlpha=bl;x.drawImage(fr2,0,0,W,H);}x.restore();}
function still(im,z,ox=0,oy=0){x.fillStyle='#000';x.fillRect(0,0,W,H);if(!im||!im.naturalWidth)return;const s=Math.max(W/im.width,H/im.height)*z;x.drawImage(im,W/2+ox-im.width*s/2,H/2+oy-im.height*s/2,im.width*s,im.height*s);}
function grad(top=.5,bot=.6,y0=760,y1=1100){let g=x.createLinearGradient(0,0,0,y0);g.addColorStop(0,`rgba(8,14,22,${top})`);g.addColorStop(1,'rgba(8,14,22,0)');x.fillStyle=g;x.fillRect(0,0,W,y0);
  g=x.createLinearGradient(0,y1,0,H);g.addColorStop(0,'rgba(8,14,22,0)');g.addColorStop(1,`rgba(8,14,22,${bot})`);x.fillStyle=g;x.fillRect(0,y1,W,H-y1);}
function counter(v,t,t0,d=1.2){return Math.round(v*eo(p(t,t0,t0+d)));}

/* S1 hook: drone rising + brand */
function s1(t){vfull(CL.c2,1.375+t*1.0,{z:1.0});grad(.55,.55,800,1200);
  const k=eo5(p(t,.6,1.8));x.save();x.globalAlpha=k;TX('VERANO',W/2,440,170,WH,{align:'center',ls:lerp(60,26,k),w:500});x.restore();
  hair(W/2-120,W/2+120,560,GOLD,t,1.2);
  lab('RESIDENCE',W/2,620,GOLDL,t,1.5,{align:'center',ls:18});
  lab('LANÇAMENTO  ·  FRENTE MAR',W/2,1500,WH,t,2.4,{align:'center',ls:8,w:500});
}
/* S2 living room */
function s2(t){vfull(CL.c6,t*1.05,{z:1.0});grad(.25,.75,500,1000);
  lab('SALA DE ESTAR',M,1250,GOLDL,t,.4);
  up('Pé-direito duplo',M,1350,92,WH,t,.6,{w:500});
  up('e vista para o mar.',M,1455,92,WH,t,.85,{w:500,italic:true});
}
/* S3 floor plan */
function s3(t){x.fillStyle=CREAM;x.fillRect(0,0,W,H);
  lab('PLANTA TIPO',M,330,GOLD,t,.1);up('Espaço pensado',M,425,84,INK,t,.25,{w:500});up('para viver bem.',M,520,84,INK,t,.45,{w:500,italic:true});
  // plan geometry (x 140..940, y 640..1160)
  const ox=140,oy=640,Wp=800,Hp=520;const L=[[0,0,800,0],[800,0,800,520],[800,520,0,520],[0,520,0,0],[300,0,300,300],[0,300,180,300],[240,300,300,300],[300,230,520,230],[520,0,520,150],[520,200,520,230],[620,230,800,230],[520,230,560,230],[300,300,300,520],[560,300,800,300],[560,300,560,420]];
  const dk=p(t,.3,2.0);x.save();x.translate(ox,oy);x.strokeStyle=INK;x.lineCap='square';
  // room fills
  const fk=eo(p(t,1.6,2.4));const rooms=[[0,0,300,300,'MASTER'],[300,0,220,230,'SUÍTE'],[520,0,280,230,'SUÍTE'],[300,230,500,290,'LIVING'],[0,300,300,220,'COZINHA']];
  rooms.forEach(([rx,ry,rw,rh,nm],i)=>{x.fillStyle=`rgba(201,164,106,${.10*fk})`;x.fillRect(rx,ry,rw,rh);});
  L.forEach(([a,b,c2,d],i)=>{const k=eio(cl(dk*L.length-i*.55,0,1));if(k<=0)return;x.lineWidth=i<4?10:5;x.beginPath();x.moveTo(a,b);x.lineTo(lerp(a,c2,k),lerp(b,d,k));x.stroke();});
  // door arcs
  [[180,300,60,Math.PI,1.5*Math.PI],[520,150,50,.5*Math.PI,Math.PI],[560,230,60,Math.PI*1.5,2*Math.PI]].forEach(([cx,cy,r,a0,a1],i)=>{const k=eo(p(t,1.4+i*.1,1.9+i*.1));if(k<=0)return;x.lineWidth=2;x.strokeStyle='rgba(28,36,48,.6)';x.beginPath();x.arc(cx,cy,r,a0,lerp(a0,a1,k));x.stroke();});
  x.restore();
  // varanda strip
  const vk=eio(p(t,1.2,1.9));x.fillStyle=`rgba(201,164,106,${.25*vk})`;x.fillRect(ox,oy+520+18,Wp*vk,70);
  rooms.forEach(([rx,ry,rw,rh,nm],i)=>lab(nm,ox+rx+rw/2,oy+ry+rh/2,INK,t,1.9+i*.12,{align:'center',size:36,ls:1,w:600}));
  lab('VARANDA GOURMET',ox+Wp/2,oy+520+53,INK,t,2.4,{align:'center',size:36,ls:3});
  // stats
  hair(M,W-M,1330,'rgba(28,36,48,.25)',t,2.2);
  [[counter(142,t,2.4)+' m²','ÁREA PRIVATIVA'],[counter(3,t,2.6,.6)+'','SUÍTES'],[counter(2,t,2.8,.6)+'','VAGAS']].forEach(([v,l],i)=>{const X=[M,M+420,M+680][i];up(v,X,1410,84,INK,t,2.4+i*.2,{w:500});lab(l,X,1490,GRY,t,2.55+i*.2,{size:40,ls:2});});
}
/* S4 balcony clip */
function s4(t){vfull(CL.c7,t*1.2,{z:1.0});grad(.25,.75,500,1000);
  lab('VARANDA GOURMET',M,1250,GOLDL,t,.4);up('Churrasqueira e',M,1350,92,WH,t,.6,{w:500});up('pôr do sol diário.',M,1455,92,WH,t,.85,{w:500,italic:true});
}
/* S5 rooftop pool clip */
function s5(t){vfull(CL.c8,2.15+t*.93,{z:1.0});grad(.6,.3,800,1300);
  lab('ROOFTOP',M,330,GOLDL,t,.4);up('Piscina de',M,430,96,WH,t,.6,{w:500});up('borda infinita.',M,540,96,WH,t,.85,{w:500,italic:true});
}
/* S6 map */
function s6(t){x.fillStyle=NAVY;x.fillRect(0,0,W,H);
  lab('LOCALIZAÇÃO',M,330,GOLD,t,.1);up('No coração',M,425,84,WH,t,.25,{w:500});up('da orla.',M,520,84,WH,t,.45,{w:500,italic:true});
  // ocean (right side) with coastline
  const mk=eo(p(t,0,.8));x.save();x.globalAlpha=mk;
  x.fillStyle='#132538';x.beginPath();x.moveTo(760,600);for(let y=600;y<=1450;y+=10)x.lineTo(760+Math.sin(y*.012)*40+ (y-600)*.08,y);x.lineTo(W,1450);x.lineTo(W,600);x.closePath();x.fill();
  // street grid
  x.strokeStyle='rgba(255,255,255,.10)';x.lineWidth=2;for(let i=0;i<12;i++){const y=620+i*72;x.beginPath();x.moveTo(60,y+rnd(i)*20);x.lineTo(760,y+rnd(i+3)*20);x.stroke();}
  for(let i=0;i<9;i++){const X=80+i*85;x.beginPath();x.moveTo(X,600);x.lineTo(X+rnd(i+9)*40,1450);x.stroke();}
  x.strokeStyle='rgba(255,255,255,.22)';x.lineWidth=6;x.beginPath();x.moveTo(60,1100);x.bezierCurveTo(300,1050,500,1150,760,1000);x.stroke();
  x.restore();
  // pin
  const P=[520,1000];const pk=eo5(p(t,.6,1.1));
  for(let r=0;r<3;r++){const ph=((t-1.1)*0.8+r/3)%1;if(t>1.1){x.strokeStyle=`rgba(201,164,106,${(1-ph)*.6})`;x.lineWidth=3;x.beginPath();x.arc(P[0],P[1],20+ph*110,0,7);x.stroke();}}
  x.fillStyle=GOLD;x.beginPath();x.arc(P[0],P[1],22*pk,0,7);x.fill();x.fillStyle=NAVY;x.beginPath();x.arc(P[0],P[1],8*pk,0,7);x.fill();
  lab('VERANO',P[0],P[1]-64,WH,t,1.0,{align:'center',size:40,ls:6,w:700});
  const POI=[[820,860,'Praia','2 min'],[230,760,'Shopping','6 min'],[180,1330,'Aeroporto','15 min']];
  POI.forEach(([px,py,nm,tm],i)=>{const t0=1.3+i*.45;const k=eio(p(t,t0,t0+.6));if(k<=0)return;
    x.save();x.strokeStyle=GOLDL;x.lineWidth=4;x.setLineDash([12,10]);const mx=(P[0]+px)/2,my=(P[1]+py)/2-80;x.beginPath();
    const N=30;for(let j=0;j<=N*k;j++){const u=j/N;const X=(1-u)*(1-u)*P[0]+2*(1-u)*u*mx+u*u*px,Y=(1-u)*(1-u)*P[1]+2*(1-u)*u*my+u*u*py;j?x.lineTo(X,Y):x.moveTo(X,Y);}x.stroke();x.restore();
    const dk=eo5(p(t,t0+.5,t0+.8));if(dk>0){x.fillStyle=WH;x.beginPath();x.arc(px,py,10*dk,0,7);x.fill();}
  });
  // legend list
  hair(M,W-M,1520-20-150,'rgba(255,255,255,.2)',t,1.2);
  POI.forEach(([,,nm,tm],i)=>{const Y=1400+i*0;});
  [['Praia','2 min'],['Shopping','6 min'],['Aeroporto','15 min']].forEach(([nm,tm],i)=>{const X=M+i*310;up(tm,X,1430,64,WH,t,1.6+i*.45,{w:500});lab(nm.toUpperCase(),X,1500,GOLDL,t,1.75+i*.45,{size:40,ls:2});});
}
/* S7 amenities over glass facade clip */
function icon(k,cx,cy,s,a){x.save();x.globalAlpha=a;x.translate(cx,cy);x.strokeStyle=GOLDL;x.lineWidth=4;x.lineCap='round';x.lineJoin='round';x.beginPath();
  if(k===0){x.moveTo(-s*.5,0);x.lineTo(s*.5,0);x.moveTo(-s*.35,-s*.25);x.lineTo(-s*.35,s*.25);x.moveTo(s*.35,-s*.25);x.lineTo(s*.35,s*.25);x.moveTo(-s*.5,-s*.15);x.lineTo(-s*.5,s*.15);x.moveTo(s*.5,-s*.15);x.lineTo(s*.5,s*.15);}
  if(k===1){x.moveTo(0,s*.45);x.bezierCurveTo(-s*.6,s*.1,-s*.3,-s*.5,0,-s*.5);x.bezierCurveTo(s*.3,-s*.5,s*.6,s*.1,0,s*.45);x.moveTo(0,s*.45);x.lineTo(0,-s*.2);}
  if(k===2){x.rect(-s*.4,-s*.3,s*.8,s*.45);x.moveTo(-s*.55,s*.3);x.lineTo(s*.55,s*.3);}
  if(k===3){x.arc(0,s*.15,s*.22,0,7);[[-.32,-.15],[-.12,-.38],[.12,-.38],[.32,-.15]].forEach(([a,b])=>{x.moveTo(a*s+s*.09,b*s);x.arc(a*s,b*s,s*.09,0,7);});}
  x.stroke();x.restore();}
function s7(t){vfull(CL.c5,t*1.2,{z:1.0});grad(.35,.85,600,950);
  lab('LAZER COMPLETO',M,1130,GOLDL,t,.3);up('Tudo dentro de casa.',M,1230,84,WH,t,.5,{w:500,fit:900});
  [['ACADEMIA',0],['SPA',1],['COWORKING',2],['PET PLACE',3]].forEach(([nm,k],i)=>{const X=M+110+i*210-110+60,t0=1.0+i*.25;const kk=eo5(p(t,t0,t0+.6));if(kk<=0)return;
    const cx=M+(i%2)*450,cy=1370+Math.floor(i/2)*110;icon(k,cx+32,cy-(1-kk)*20,56,kk);LB(nm,cx+90,cy,WH,{size:40,ls:3,a:kk});});
}
/* S8 facade still + price */
function s8(t){still(IM.fachada,lerp(1.14,1.02,eo(p(t,0,4))),0,lerp(80,0,eo(p(t,0,4))));grad(.75,.6,900,1200);
  lab('LANÇAMENTO',M,330,GOLDL,t,.3);TX('A partir de',M,420,48,WH,{a:eo(p(t,.5,1.0)),font:SERIF,italic:true});
  up('R$ 1,2 mi',M,540,150,WH,t,.7,{w:500});
  hair(M,W-M,1400,'rgba(255,255,255,.35)',t,1.4);
  lab('ENTREGA 2028',M,1460,WH,t,1.6,{size:40,ls:5});lab('FINANCIAMENTO DIRETO',M,1530,GOLDL,t,1.8,{size:40,ls:5});
}
/* S9 CTA */
function s9(t){x.fillStyle=CREAM;x.fillRect(0,0,W,H);
  TX('VERANO',W/2,360,64,INK,{align:'center',ls:20,w:500,a:eo(p(t,0,.6))});
  lab('Esse empreendimento não existe.',W/2,560,GRY,t,.3,{align:'center',ls:0,w:500,size:44});
  up('Mas o vídeo do seu',W/2,700,92,INK,t,.6,{align:'center',w:500});
  up('lançamento pode',W/2,810,92,INK,t,.8,{align:'center',w:500});
  up('vender assim.',W/2,925,100,GOLD,t,1.0,{align:'center',w:500,italic:true});
  ['Lançamentos imobiliários','Tours e drone animados','Reels para corretores'].forEach((s,i)=>{const t0=1.6+i*.2;hair(M+120,W-M-120,1040+i*76,'rgba(28,36,48,.15)',t,t0-.1);lab(s,W/2,1078+i*76,INK,t,t0,{align:'center',ls:0,w:500,size:40});});
  const bk=eo5(p(t,2.6,3.2));if(bk>0){x.save();x.globalAlpha=bk;x.translate(W/2,1390+(1-bk)*30);x.fillStyle=NAVY;x.beginPath();x.roundRect(-330,-68,660,136,68);x.fill();TX('Me chama no direct',0,2,48,WH,{align:'center',w:600,font:SANS});x.restore();}
  lab('@alecreator_motion',W/2,1530,GOLD,t,3.2,{align:'center',ls:0,w:600,size:50});
}
const NZ=document.createElement('canvas');NZ.width=NZ.height=256;{const g=NZ.getContext('2d'),d=g.createImageData(256,256);for(let i=0;i<d.data.length;i+=4){const v=128+(Math.random()-.5)*255;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=255;}g.putImageData(d,0,0);}
function grain(t,a=.06){x.save();x.globalAlpha=a;x.globalCompositeOperation='overlay';const f=Math.floor(t*24);const ox=-rnd(f)*256,oy=-rnd(f+7)*256;for(let X=ox;X<W;X+=256)for(let Y=oy;Y<H;Y+=256)x.drawImage(NZ,X,Y);x.restore();}
const SC=[[s1,0,4],[s2,4,8],[s3,8,12],[s4,12,16],[s5,16,20],[s6,20,24],[s7,24,28],[s8,28,32],[s9,32,38]];
window.DUR=38;
const TB1=document.createElement('canvas');TB1.width=W;TB1.height=H;const TB2=document.createElement('canvas');TB2.width=W;TB2.height=H;const TR=.7;
function renderTo(cv,f,lt){const g=cv.getContext('2d');g.setTransform(1,0,0,1,0,0);g.globalAlpha=1;g.clearRect(0,0,W,H);const xx=x;x=g;x.save();f(lt);x.restore();x=xx;}
window.draw=function(t){x=X0;const i=SC.findIndex(([,a,b])=>t>=a&&t<b);const k=i<0?SC.length-1:i;const [f,a]=SC[k];const lt=t-a;
  if(k>0&&lt<TR){const [pf,pa]=SC[k-1];renderTo(TB1,pf,t-pa);renderTo(TB2,f,lt);const e=eio(lt/TR);
    x.drawImage(TB1,0,0);x.save();x.globalAlpha=e;const z=1.05-.05*e;x.translate(W/2,H/2);x.scale(z,z);x.translate(-W/2,-H/2);x.drawImage(TB2,0,0);x.restore();
  }else{x.save();f(lt);x.restore();}
  grain(t);
  const fi=1-p(t,0,.35);if(fi>0){x.fillStyle=`rgba(0,0,0,${fi})`;x.fillRect(0,0,W,H);}
  const fo=p(t,37.4,38);if(fo>0){x.fillStyle=`rgba(243,238,230,${fo})`;x.fillRect(0,0,W,H);}
};

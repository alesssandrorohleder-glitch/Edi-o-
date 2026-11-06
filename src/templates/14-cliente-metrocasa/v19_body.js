
const W=1080,H=1920,c=document.getElementById('c');let x=c.getContext('2d');const X0=x;
const RED='#E31E24',DRED='#A9121A',GRAPH='#19191B',GRAPH2='#26262A',WH='#FFFFFF',CREAM='#F6F3EE',GOLD='#FFC21A',GRY='#8A8A90',INK='#141416';
const P='Poppins',D='"Inter Display"',SCRIPT='"TeX Gyre Chorus"';
const BT=.5,BAR=2,M=90;
const cl=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)),p=(t,a,b)=>cl((t-a)/(b-a));
const eo=t=>1-Math.pow(1-t,3),eo5=t=>1-Math.pow(1-t,5),eio=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2,sine=t=>-(Math.cos(Math.PI*t)-1)/2;
const back=(t,s=1.7)=>{if(t<=0)return 0;if(t>=1)return 1;const c3=s+1;return 1+c3*Math.pow(t-1,3)+s*Math.pow(t-1,2)};
const lerp=(a,b,k)=>a+(b-a)*k;const rnd=s=>{const r=Math.sin(s*127.1+311.7)*43758.5453;return r-Math.floor(r)};
function TX(s,X,Y,size,col,{w=700,f=P,ls=0,align='center',a=1,fit=0,italic=false}={}){x.save();x.globalAlpha*=a;x.font=`${italic?'italic ':''}${w} ${size}px ${f}`;x.letterSpacing=ls+'px';x.textAlign=align;x.textBaseline='middle';
  let sc=1;if(fit){const mw=x.measureText(s).width;if(mw>fit)sc=fit/mw;}x.translate(X,Y);x.scale(sc,sc);x.fillStyle=col;x.fillText(s,0,0);x.restore();}
function up(s,X,Y,size,col,t,t0,o={}){const k=eo5(p(t,t0,t0+.55));if(k<=0)return;x.save();x.beginPath();x.rect(0,Y-size*.75,W,size*1.5);x.clip();TX(s,X,Y+(1-k)*size*1.2,size,col,o);x.restore();}
function slam(s,X,Y,size,col,t,t0,o={}){const k=p(t,t0,t0+.22);if(k<=0)return;const e=back(k,2.2);x.save();x.translate(X,Y);x.scale(lerp(1.8,1,eo(k)),lerp(1.8,1,eo(k)));TX(s,0,0,size,col,{...o,a:cl(k*3)});x.restore();}
function tag(s,X,Y,size,bg,fg,t,t0,{align='center',rot=0}={}){const k=back(p(t,t0,t0+.4));if(k<=0)return;x.save();x.font=`700 ${size}px ${P}`;const w=x.measureText(s).width+size*1.2,h=size*1.7;
  x.translate(X+(align==='left'?w/2:0),Y);x.rotate(rot);x.scale(k,k);x.fillStyle=bg;x.beginPath();x.roundRect(-w/2,-h/2,w,h,h*.22);x.fill();TX(s,0,2,size,fg);x.restore();}
function shake(t,t0,amp=18,dec=12){const d=t-t0;if(d<0)return [0,0];const e=Math.exp(-d*dec);return [Math.sin(d*85)*amp*e,Math.cos(d*71)*amp*e*.6];}

/* ---------- logo (original artwork, animated in parts) ---------- */
const LS=[2274,1361];
function logo(cx,cy,w,{pk=1,wk=1,ck=1,col='white'}={}){const s=w/LS[0];const X=cx-w/2,Y=cy-LS[1]*s/2;
  const tint=(im,cc)=>{if(cc==='white')return im;const key='t'+cc+im.src;if(!window[key]){const cv=document.createElement('canvas');cv.width=im.naturalWidth;cv.height=im.naturalHeight;const g=cv.getContext('2d');g.drawImage(im,0,0);g.globalCompositeOperation='source-in';g.fillStyle=cc;g.fillRect(0,0,cv.width,cv.height);window[key]=cv;}return window[key];};
  const iconCol=col==='white'?'white':col, wordCol=col==='white'?'white':col, conCol='white';
  POLYS.forEach((poly,i)=>{const k=Array.isArray(pk)?pk[i]:pk;if(k<=0)return;let cx0=0,cy0=0;poly.forEach(([a,b2])=>{cx0+=a;cy0+=b2;});cx0/=poly.length;cy0/=poly.length;
    const dirs=[[-500,-700,-.8],[500,-700,.8],[-600,500,-.6],[600,500,.6]];const e=eo5(k);const [dx,dy,dr]=dirs[i];
    x.save();x.translate(X+cx0*s+dx*(1-e),Y+cy0*s+dy*(1-e));x.rotate(dr*(1-e));x.globalAlpha=cl(k*2);x.fillStyle=iconCol==='white'?WH:iconCol;x.beginPath();poly.forEach(([a,b2],q)=>{const px=(a-cx0)*s,py=(b2-cy0)*s;q?x.lineTo(px,py):x.moveTo(px,py);});x.closePath();x.fill();x.restore();});
  if(wk>0){x.save();x.beginPath();x.rect(X-20,Y+860*s,(w+40)*eo5(wk),360*s);x.clip();x.drawImage(tint(IM.word2x,wordCol),X,Y,w,LS[1]*s);x.restore();}
  if(ck>0){x.save();x.globalAlpha=eo(ck);x.translate(0,(1-eo(ck))*20);x.drawImage(tint(IM.constr2x,conCol),X,Y,w,LS[1]*s);x.restore();}}
const NZ=document.createElement('canvas');NZ.width=NZ.height=256;{const g=NZ.getContext('2d'),d=g.createImageData(256,256);for(let i=0;i<d.data.length;i+=4){const v=128+(Math.random()-.5)*255;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=255;}g.putImageData(d,0,0);}
function grain(t,a=.035){x.save();x.globalAlpha=a;x.globalCompositeOperation='overlay';const f=Math.floor(t*24);const ox=-rnd(f)*256,oy=-rnd(f+7)*256;for(let X=ox;X<W;X+=256)for(let Y=oy;Y<H;Y+=256)x.drawImage(NZ,X,Y);x.restore();}
function roofBg(t,col,a=.07){x.save();x.globalAlpha=a;x.fillStyle=col;const o=(t*40)%360;for(let i=-2;i<8;i++){const X=-200+i*360+o;x.beginPath();x.moveTo(X,H);x.lineTo(X+520,H-900);x.lineTo(X+640,H-900);x.lineTo(X+120,H);x.closePath();x.fill();}x.restore();}
function cover(im,X,Y,w,h,z=1,ox=0,oy=0){if(!im||!im.naturalWidth)return;const s=Math.max(w/im.naturalWidth,h/im.naturalHeight)*z;x.drawImage(im,X+w/2+ox-im.naturalWidth*s/2,Y+h/2+oy-im.naturalHeight*s/2,im.naturalWidth*s,im.naturalHeight*s);}
function card(im,cx,cy,w,h,t,t0,{rot=0,from=1,r=34,z0=1.15}={}){const k=eo5(p(t,t0,t0+.7));if(k<=0)return;x.save();x.translate(cx+(1-k)*900*from,cy);x.rotate(rot*k+(1-k)*.3*from);
  x.fillStyle='rgba(0,0,0,.28)';x.beginPath();x.roundRect(-w/2+14,-h/2+22,w,h,r);x.fill();x.fillStyle=WH;x.beginPath();x.roundRect(-w/2-10,-h/2-10,w+20,h+20,r+8);x.fill();
  x.beginPath();x.roundRect(-w/2,-h/2,w,h,r);x.clip();cover(im,-w/2,-h/2,w,h,lerp(z0,1.02,eo(p(t,t0,t0+2.5))));x.restore();}

/* ================= SCENES ================= */
// S1 hook: rent bill
function s1(t){x.fillStyle=GRAPH;x.fillRect(0,0,W,H);roofBg(t,WH,.035);
  const [sx,sy]=shake(t,BT*2,14);x.save();x.translate(sx,sy);
  up('Você ainda',W/2,520,96,WH,t,.05,{w:500});
  slam('PAGA',W/2,650,170,WH,t,BT*1);slam('ALUGUEL?',W/2,810,170,RED,t,BT*2,{fit:960});x.restore();
  // bill card
  const bk=eo5(p(t,BT*2.6,BT*3.6));const crush=eio(p(t,BT*5.2,BT*6.2));const fly=eo(p(t,BT*6.2,BT*7.4));
  if(bk>0){x.save();x.translate(W/2+fly*700,1300+(1-bk)*500-fly*300);x.rotate(lerp(-.06,0,bk)+crush*.6+fly*1.4);x.scale(lerp(1,.25,crush),lerp(1,.35,crush));
    x.fillStyle=CREAM;x.beginPath();x.roundRect(-300,-200,600,400,18);x.fill();
    TX('BOLETO',-250,-140,30,GRY,{align:'left',ls:6});TX('ALUGUEL',-250,-80,52,INK,{align:'left'});
    x.fillStyle='#DDD8D0';for(let i=0;i<3;i++)x.fillRect(-250,-20+i*40,380-i*90,14);
    TX('R$ 1.500',250,120,64,RED,{align:'right'});TX('todo mês',250,168,28,GRY,{align:'right',w:500});
    // barcode
    for(let i=0;i<34;i++){x.fillStyle=INK;x.fillRect(-250+i*9,120,rnd(i)*5+2,50);}
    if(crush>0){x.strokeStyle=`rgba(0,0,0,${.25*crush})`;x.lineWidth=4;for(let i=0;i<6;i++){x.beginPath();x.moveTo(-300+rnd(i)*600,-200);x.lineTo(-300+rnd(i+9)*600,200);x.stroke();}}
    x.restore();}
  up('Chega de pagar o sonho dos outros.',W/2,1600,44,GRY,t,BT*6,{w:500,fit:900});
}
// S2 logo assemble + Nunca pare de sonhar
function s2(t){x.fillStyle=RED;x.fillRect(0,0,W,H);roofBg(t,'#000',.06);
  const pk=[0,1,2,3].map(i=>p(t,.05+i*.12,.65+i*.12));const mv=eio(p(t,BT*4,BT*5));
  logo(W/2,lerp(860,520,mv),lerp(820,560,mv),{pk,wk:p(t,.75,1.3),ck:p(t,1.2,1.6)});
  tag('NUNCA PARE DE',W/2,960,40,WH,RED,t,BT*5);
  // handwritten "Sonhar" reveal
  const k=p(t,BT*5.6,BT*7.6);if(k>0){x.save();x.font=`400 230px ${SCRIPT}`;const sw=x.measureText('Sonhar').width;const X=W/2-sw/2;x.beginPath();x.rect(X-40,1000,(sw+80)*eio(k),300);x.clip();TX('Sonhar',W/2,1140,230,WH,{f:SCRIPT,w:400});x.restore();
    const px=X-40+(sw+80)*eio(k);if(k<1){x.fillStyle=WH;x.beginPath();x.arc(px,1150+Math.sin(k*30)*40,8,0,7);x.fill();}}
}
// S3 metro line
function s3(t){x.fillStyle=CREAM;x.fillRect(0,0,W,H);
  up('Seu apê em SP,',M,340,84,INK,t,.05,{align:'left'});up('pertinho do',M,440,84,INK,t,BT*1,{align:'left'});slam('METRÔ.',M+230,560,130,RED,t,BT*2,{align:'left'});
  const PTS=[[150,820],[420,820],[600,1000],[600,1180],[860,1180],[930,1400],[930,1560]];const NM=['ZONA NORTE','CENTRO','ZONA LESTE','ZONA SUL','ZONA OESTE','',''];
  const seg=[];let tot=0;for(let i=1;i<PTS.length;i++){const d=Math.hypot(PTS[i][0]-PTS[i-1][0],PTS[i][1]-PTS[i-1][1]);seg.push(d);tot+=d;}
  const k=eio(p(t,BT*1.5,BT*6.5));const L=tot*k;
  x.save();x.lineCap='round';x.lineJoin='round';x.strokeStyle='#DDD6CC';x.lineWidth=26;x.beginPath();PTS.forEach(([a,b],i)=>i?x.lineTo(a,b):x.moveTo(a,b));x.stroke();
  x.strokeStyle=RED;x.beginPath();x.moveTo(...PTS[0]);let acc=0,head=PTS[0];for(let i=1;i<PTS.length;i++){const d=seg[i-1];if(acc+d<=L){x.lineTo(...PTS[i]);acc+=d;head=PTS[i];}else{const u=(L-acc)/d;head=[lerp(PTS[i-1][0],PTS[i][0],u),lerp(PTS[i-1][1],PTS[i][1],u)];x.lineTo(...head);break;}}x.stroke();x.restore();
  // stations
  let a2=0;PTS.slice(0,5).forEach(([a,b],i)=>{const reach=i===0?0:seg.slice(0,i).reduce((q,r)=>q+r,0);const on=L>=reach;const e=on?back(cl((L-reach)/120),2.2):0;
    x.fillStyle=WH;x.beginPath();x.arc(a,b,22,0,7);x.fill();x.strokeStyle=on?RED:'#CFC7BC';x.lineWidth=8;x.beginPath();x.arc(a,b,22,0,7);x.stroke();
    if(e>0){const OF=[[0,64,'center'],[0,-64,'center'],[-48,0,'right'],[-48,0,'right'],[0,-64,'center']][i];TX(NM[i],a+OF[0],b+OF[1],32,INK,{ls:2,a:cl(e),align:OF[2]});}});
  // train head
  if(k>0&&k<1){x.fillStyle=RED;x.beginPath();x.arc(head[0],head[1],30,0,7);x.fill();x.fillStyle=WH;x.beginPath();x.arc(head[0],head[1],12,0,7);x.fill();}
  // destination pin with logo icon
  const pk=back(p(t,BT*6.4,BT*7.2),2);if(pk>0){x.save();x.translate(930,1560);x.scale(pk,pk);x.fillStyle=RED;x.beginPath();x.moveTo(0,0);x.bezierCurveTo(-80,-90,-90,-200,0,-210);x.bezierCurveTo(90,-200,80,-90,0,0);x.fill();
    const s=.055;x.fillStyle=WH;POLYS.forEach(poly=>{x.beginPath();poly.forEach(([a,b2],q)=>{const px=(a-1170)*s,py=(b2-410)*s-160;q?x.lineTo(px,py):x.moveTo(px,py);});x.closePath();x.fill();});x.restore();}
  up('Apartamentos em todas as regiões de São Paulo.',M,1720,40,GRY,t,BT*5,{align:'left',w:500,fit:820});
}
// S4 building rises (na planta)
function s4(t){const g=x.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1E2A44');g.addColorStop(.6,'#C8574A');g.addColorStop(1,'#F2A35E');x.fillStyle=g;x.fillRect(0,0,W,H);
  const bx=W/2-230,bw=460,fh=58,floors=17,base=1650;const rise=p(t,.1,BT*5);const nf=Math.floor(rise*floors+.999);
  // drawn building
  const ph=eio(p(t,BT*5.2,BT*6.6));
  x.save();x.globalAlpha=1-ph;
  for(let f=0;f<nf;f++){const fk=cl(rise*floors-f);const y=base-(f+1)*fh;x.fillStyle=f%2?'#E9E3DA':'#F3EEE6';x.fillRect(bx,y+(1-eo(fk))*-60,bw,fh-2);
    x.fillStyle=RED;x.fillRect(bx+bw*.62,y,bw*.12,fh-2);
    for(let w2=0;w2<6;w2++){const lit=rnd(f*7+w2)>.45&&t>BT*2;x.fillStyle=lit?'#FFD27A':'#5A6170';x.fillRect(bx+22+w2*72,y+14,40,26);}}
  // crane
  const ck=eo5(p(t,0,.8));x.strokeStyle=GOLD;x.lineWidth=10;x.beginPath();x.moveTo(bx+bw+80,base);x.lineTo(bx+bw+80,base-1060*ck);x.lineTo(bx-60,base-1060*ck);x.stroke();
  x.beginPath();x.moveTo(bx+bw+80,base-1060*ck);x.lineTo(bx+bw+300,base-1060*ck);x.stroke();x.fillStyle=GOLD;x.fillRect(bx+bw+230,base-1060*ck,70,60);x.beginPath();x.moveTo(bx+bw+80,base-1060*ck);x.lineTo(bx+bw+80,base-1060*ck-120);x.lineTo(bx-60,base-1060*ck);x.moveTo(bx+bw+80,base-1060*ck-120);x.lineTo(bx+bw+300,base-1060*ck);x.lineWidth=4;x.stroke();
  x.lineWidth=3;x.beginPath();const hx=bx+bw/2+Math.sin(t*2)*40;x.moveTo(hx,base-1060*ck);x.lineTo(hx,base-(nf+1)*fh-40);x.stroke();
  x.restore();
  // real render reveals with wipe from bottom
  if(ph>0){const cw=820,chh=1080,cx0=W/2-cw/2,cy0=650;x.save();x.beginPath();x.roundRect(cx0,cy0+chh*(1-ph),cw,chh*ph,40);x.clip();cover(IM.b_ipiranga,cx0,cy0,cw,chh,lerp(1.15,1.03,eo(p(t,BT*5.2,4))));x.restore();
    const tk=p(t,BT*6.4,BT*7.2);if(tk>0)tag('EM CONSTRUÇÃO',cx0+cw-190,cy0+60,32,RED,WH,t,BT*6.4);}
  x.fillStyle=GRAPH;x.globalAlpha=1-ph;x.fillRect(0,base,W,H-base);x.globalAlpha=1;
  tag('NA PLANTA',M,330,40,RED,WH,t,BT*.5,{align:'left'});
  up('Veja seu apê',M,440,92,WH,t,BT*1,{align:'left'});up('nascer.',M,545,92,WH,t,BT*1.5,{align:'left'});
  const cnt=Math.floor(nf);TX(`${String(cnt).padStart(2,'0')} ANDARES`,W/2,1770,44,GOLD,{a:1-ph,ls:4});
}
const EMP=[['b_santana','Prime Santana','ZONA NORTE'],['b_analia','Clube Anália Franco','ZONA LESTE'],['b_ipiranga','Prime Alto do Ipiranga','ZONA SUL'],['b_guilhermina','Clube Guilhermina','ZONA LESTE'],['b_boavista','Alto da Boa Vista','ZONA SUL'],['b_sapopemba','Prime Sapopemba','ZONA LESTE'],['b_gronchi','Bosque Giovanni Gronchi','ZONA SUL']];
function sEmp(t){x.fillStyle=GRAPH;x.fillRect(0,0,W,H);roofBg(t,WH,.03);
  tag('+ DE 120 PROJETOS',M,330,40,RED,WH,t,.05,{align:'left'});up('Tem Metrocasa',M,440,88,WH,t,BT*.6,{align:'left'});up('perto de você.',M,540,88,RED,t,BT*1.1,{align:'left'});
  const cw=520,ch=760,gap=40,Y=1150;const u=Math.max(0,(t-.6)/.62);const st=Math.min(5,Math.floor(u));const scroll=(cw+gap)*(st+(st<5?eo5(cl((u-st)*1.6)):0))+(1-eo5(p(t,0,.8)))*-900;
  EMP.forEach(([im,nm,zn],i)=>{const cx=W/2+i*(cw+gap)-scroll;const d=Math.abs(cx-W/2)/(cw+gap);if(cx<-cw||cx>W+cw)return;const s=lerp(1,.84,cl(d));
    x.save();x.translate(cx,Y);x.scale(s,s);x.globalAlpha=lerp(1,.55,cl(d));x.beginPath();x.roundRect(-cw/2,-ch/2,cw,ch,34);x.clip();cover(IM[im],-cw/2,-ch/2,cw,ch,1.04);
    const g=x.createLinearGradient(0,ch*.1,0,ch/2);g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(1,'rgba(0,0,0,.85)');x.fillStyle=g;x.fillRect(-cw/2,0,cw,ch/2);
    TX(zn,-cw/2+34,ch/2-130,28,GOLD,{align:'left',ls:3});TX(nm,-cw/2+34,ch/2-80,40,WH,{align:'left',fit:cw-60});x.restore();});
  up('Studios, 1 e 2 dorms em todas as regiões.',W/2,1650,40,GRY,t,BT*5,{w:500,fit:900});
}
// S5 lazer cards
function s5(t){x.fillStyle=RED;x.fillRect(0,0,W,H);x.save();x.fillStyle=DRED;x.beginPath();x.moveTo(0,H*.55);x.lineTo(W,H*.35);x.lineTo(W,H);x.lineTo(0,H);x.fill();x.restore();roofBg(t,'#000',.05);
  tag('LAZER COMPLETO',M,330,40,WH,RED,t,.05,{align:'left'});up('Tudo pra viver',M,440,88,WH,t,BT*.6,{align:'left'});up('bem, no prédio.',M,540,88,WH,t,BT*1.1,{align:'left'});
  card(IM.churras,W/2-110,880,620,420,t,BT*1.4,{rot:-.04,from:-1});card(IM.piscina,W/2+120,1340,620,420,t,BT*3,{rot:.035,from:1});
  tag('CHURRASQUEIRA',W/2-110,1105,34,GRAPH,WH,t,BT*2.4);tag('PISCINA',W/2+120,1565,34,GRAPH,WH,t,BT*4);
  ['PLAYGROUND','PET PLACE','BICICLETÁRIO'].forEach((s,i)=>{const k=eo5(p(t,BT*5+i*.18,BT*5+i*.18+.5));if(k<=0)return;TX('+ '+s,M,1700+i*0,1,WH);});
  up('+ playground  •  pet place  •  bicicletário',W/2,1700,38,WH,t,BT*5.2,{w:500,fit:900});
}
// S6 plantas
function plan(type,X,Y,w,h,k){x.save();x.translate(X,Y);x.strokeStyle=INK;x.lineCap='square';const L=[[0,0,w,0],[w,0,w,h],[w,h,0,h],[0,h,0,0]];
  if(type>=1){L.push([w*.55,0,w*.55,h*.55],[w*.55,h*.55,w,h*.55]);} if(type>=2){L.push([0,h*.5,w*.35,h*.5],[w*.35,h*.5,w*.35,h]);} else L.push([0,h*.62,w*.3,h*.62]);
  L.forEach(([a,b,c2,d],i)=>{const e=eio(cl(k*L.length*.9-i*.6));if(e<=0)return;x.lineWidth=i<4?10:5;x.beginPath();x.moveTo(a,b);x.lineTo(lerp(a,c2,e),lerp(b,d,e));x.stroke();});
  const fk=eo(cl(k*1.6-.6));x.fillStyle=`rgba(227,30,36,${.08*fk})`;x.fillRect(0,0,w,h);
  const lab=[['SALA',w*.28,h*.3],['QUARTO',w*.78,h*.27],['COZINHA',w*.15,h*.78]];if(type>=2)lab.push(['QUARTO',w*.68,h*.78]);if(type===0){lab.length=0;lab.push(['LIVING + QUARTO',w*.5,h*.35],['COZINHA',w*.15,h*.82]);}
  lab.forEach(([s,a,b])=>TX(s,a,b,30,INK,{a:fk,ls:2}));x.restore();}
function s6(t){x.fillStyle=WH;x.fillRect(0,0,W,H);
  tag('PLANTAS',M,330,40,RED,WH,t,.05,{align:'left'});up('O tamanho certo',M,440,88,INK,t,BT*.6,{align:'left'});up('pra sua vida.',M,540,88,RED,t,BT*1.1,{align:'left'});
  const types=[['STUDIO','23 a 25 m²','pl_studio'],['2 DORMS','34 m²','pl_2d']];const i=t<2.35?0:1;const it=t-(i?2.35:BT*1.6);
  types.forEach(([s,m2],j)=>{const X=M+j*450,act=j===i;const k=eo5(p(t,BT*1.2+j*.12,BT*1.2+j*.12+.5));if(k<=0)return;x.save();x.globalAlpha=k;x.fillStyle=act?RED:'#F1EEEA';x.beginPath();x.roundRect(X,650,420,110,55);x.fill();TX(s,X+40,690,36,act?WH:INK,{align:'left'});TX(m2,X+40,730,28,act?WH:GRY,{align:'left',w:500});x.restore();});
  const k=eo5(p(it,0,.6));if(k>0&&t>BT*1.6){const im=IM[types[i][2]];const w=900,h=w*im.naturalHeight/im.naturalWidth,X=W/2-w/2,Y=1180-h/2;
    x.save();x.globalAlpha=k;x.translate(0,(1-k)*80);x.fillStyle='rgba(0,0,0,.12)';x.beginPath();x.roundRect(X+10,Y+18,w,h,26);x.fill();x.beginPath();x.roundRect(X,Y,w,h,26);x.clip();
    const z=lerp(1.12,1.0,eo(p(it,0,1.6)));x.translate(W/2,Y+h/2);x.scale(z,z);x.drawImage(im,-w/2,-h/2,w,h);x.restore();
    x.save();x.globalAlpha=eio(p(it,.3,.9));x.strokeStyle=RED;x.lineWidth=6;x.beginPath();x.roundRect(X-14,Y-14+(1-k)*80,w+28,h+28,34);x.stroke();x.restore();}
  up('Studio, 1 e 2 dormitórios.',M,1600,48,INK,t,BT*5.5,{align:'left',w:500});
}
// S7 offer
function s7(t){x.fillStyle=RED;x.fillRect(0,0,W,H);const rg=x.createRadialGradient(W/2,900,50,W/2,900,1000);rg.addColorStop(0,'rgba(255,120,60,.45)');rg.addColorStop(1,'rgba(0,0,0,0)');x.fillStyle=rg;x.fillRect(0,0,W,H);
  // rays
  x.save();x.translate(W/2,880);x.rotate(t*.15);x.globalAlpha=.08;x.fillStyle=WH;for(let i=0;i<16;i++){x.rotate(Math.PI/8);x.beginPath();x.moveTo(0,0);x.lineTo(1400,-90);x.lineTo(1400,90);x.fill();}x.restore();
  tag('APARTAMENTOS A PARTIR DE',W/2,520,38,WH,RED,t,.1);
  const n=Math.round(149*eo(p(t,BT*1,BT*3)));const pk=back(p(t,BT*1,BT*1.6),2);const [sx,sy]=shake(t,BT*3,14);
  if(pk>0){x.save();x.translate(W/2+sx,800+sy);x.scale(pk,pk);TX('R$',-330,-10,70,WH,{align:'right'});TX(String(n),-20,0,300,GOLD,{f:D,w:900,ls:-12});TX('MIL*',300,-60,80,WH,{align:'left',f:D,w:900});TX('À VISTA',300,40,40,WH,{align:'left'});x.restore();}
  [['ITBI + REGISTRO GRÁTIS',1100,BT*4],['UBER PRA VOCÊ VISITAR',1230,BT*5],['MINHA CASA MINHA VIDA',1360,BT*6]].forEach(([s,Y,t0],i)=>tag(s,W/2,Y,44,i===2?GOLD:WH,i===2?INK:RED,t,t0,{rot:(i-1)*.015}));
  TX('*Consulte condições no plantão de vendas.',W/2,1560,28,WH,{w:400,a:.75*eo(p(t,BT*4,BT*5))});
}
// S8 CTA
function s8(t){x.fillStyle=GRAPH;x.fillRect(0,0,W,H);roofBg(t,WH,.03);
  const pk=[0,1,2,3].map(i=>p(t,.05+i*.1,.6+i*.1));logo(W/2,600,760,{pk,wk:p(t,.7,1.2),ck:p(t,1.1,1.5),col:RED});
  up('Mais de 120 projetos',W/2,980,64,WH,t,BT*3,{});up('pertinho do que importa.',W/2,1065,56,GRY,t,BT*3.6,{w:500});
  const bk=back(p(t,BT*5,BT*5.8),1.6);const pul=t>BT*6?1+.03*Math.exp(-((t-BT*6)%BT)*8):1;
  if(bk>0){x.save();x.translate(W/2,1260);x.scale(bk*pul,bk*pul);x.fillStyle=RED;x.beginPath();x.roundRect(-360,-72,720,144,72);x.fill();TX('Vamos conversar?',0,3,52,WH);x.restore();}
  up('(11) 5061-0022',W/2,1420,54,WH,t,BT*6.5,{});up('@construtorametrocasa',W/2,1500,42,RED,t,BT*7,{w:600});
}
const SC=[[s1,0,4],[s2,4,8],[s3,8,12],[s4,12,16],[sEmp,16,20],[s5,20,24],[s6,24,28],[s7,28,34],[s8,34,40]];
window.DUR=40;const TR=.45;
const TB1=document.createElement('canvas');TB1.width=W;TB1.height=H;const TB2=document.createElement('canvas');TB2.width=W;TB2.height=H;
function renderTo(cv,f,lt){const g=cv.getContext('2d');g.setTransform(1,0,0,1,0,0);g.globalAlpha=1;g.clearRect(0,0,W,H);const xx=x;x=g;x.save();f(lt);x.restore();x=xx;}
window.draw=function(t){x=X0;const i=SC.findIndex(([,a,b])=>t>=a&&t<b);const k=i<0?SC.length-1:i;const [f,a]=SC[k];const lt=t-a;
  if(k>0&&lt<TR){const [pf,pa]=SC[k-1];renderTo(TB1,pf,t-pa);renderTo(TB2,f,lt);const e=eio(lt/TR);x.drawImage(TB1,0,0);
    // roof-angle slash wipe: red band + reveal
    const ex=lerp(-900,W+900,e);x.save();x.beginPath();x.moveTo(-600,H+100);x.lineTo(ex-500,H+100);x.lineTo(ex+300,-100);x.lineTo(-600,-100);x.closePath();x.clip();x.drawImage(TB2,0,0);x.restore();
    x.fillStyle=k%2?WH:RED;x.beginPath();x.moveTo(ex-500,H+100);x.lineTo(ex-360,H+100);x.lineTo(ex+440,-100);x.lineTo(ex+300,-100);x.closePath();x.fill();
  }else{x.save();f(lt);x.restore();}
  grain(t);
  const fo=p(t,39.5,40);if(fo>0){x.fillStyle=`rgba(0,0,0,${fo})`;x.fillRect(0,0,W,H);}
};

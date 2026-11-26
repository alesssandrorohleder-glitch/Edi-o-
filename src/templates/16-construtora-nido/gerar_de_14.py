import re,sys
src=open('../14-cliente-metrocasa/index.html').read()
lines=src.split('\n')
# remove image loading + logo polys lines (3,4)
lines[2]='window.IMGS=[];'
lines[3]=''
s='\n'.join(lines)
def R(a,b,cnt=1):
    global s
    n=s.count(a)
    assert n==cnt,(n,a[:80]); s=s.replace(a,b)
R("const RED='#E31E24',DRED='#A9121A'","const RED='#12866F',DRED='#0B5E4E'")
R("function cover(im","function coverX(im")
# ---- new logo (fictional) ----
i0=s.index('/* ---------- logo');i1=s.index('const NZ=')
s=s[:i0]+r'''/* ---------- logo fictício NIDO (vetorial) ---------- */
const ICON=[[[-170,10],[0,-160],[0,-92],[-104,10]],[[0,-160],[170,10],[104,10],[0,-92]],[[-104,40],[104,40],[104,190],[34,190],[34,112],[-34,112],[-34,190],[-104,190]]];
function icon(k,col,s){const dirs=[[-500,-700,-.8],[500,-700,.8],[0,700,0]];ICON.forEach((poly,i)=>{const kk=Array.isArray(k)?k[i]:k;if(kk<=0)return;const e=eo5(kk);const [dx,dy,dr]=dirs[i];
  x.save();x.translate(dx*(1-e),dy*(1-e));x.rotate(dr*(1-e));x.globalAlpha*=cl(kk*2);x.fillStyle=col;x.beginPath();poly.forEach(([a,b],q)=>q?x.lineTo(a*s,b*s):x.moveTo(a*s,b*s));x.closePath();x.fill();x.restore();});}
function logo(cx,cy,w,{pk=1,wk=1,ck=1,col='white'}={}){const s=w/700,c2=col==='white'?WH:col;
  x.save();x.translate(cx,cy-170*s);icon(pk,c2,s*1.05);x.restore();
  if(wk>0){x.save();x.beginPath();x.rect(cx-w/2-20,cy+40*s,(w+40)*eo5(wk),240*s);x.clip();TX('NIDO',cx,cy+165*s,210*s,c2,{w:800,ls:30*s});x.restore();}
  if(ck>0)TX('CONSTRUTORA',cx,cy+300*s+(1-eo(ck))*20,Math.max(40,48*s),c2,{w:600,ls:14*s,a:eo(ck)});}
/* ilustrações vetoriais (substituem fotos/renders) */
function building(seed,X,Y,w,h){const sky=x.createLinearGradient(X,Y,X,Y+h);sky.addColorStop(0,['#9FD3E6','#F7C59F','#BFD7EA','#FAD4C0','#A8DADC','#F6BD60','#CDE7F0'][seed%7]);sky.addColorStop(1,'#FFF6EC');x.fillStyle=sky;x.fillRect(X,Y,w,h);
  x.fillStyle='rgba(255,255,255,.8)';x.beginPath();x.arc(X+w*.78,Y+h*.16,40,0,7);x.fill();
  const bw=w*(.42+rnd(seed)*.14),bh=h*(.6+rnd(seed+3)*.2),bx=X+w/2-bw/2-20,by=Y+h*.92-bh;const tone=['#F3EEE6','#E9E3DA','#FFFFFF','#EDE7DF'][seed%4];
  x.fillStyle='#C9C2B8';x.fillRect(bx+bw,by+30,w*.16,bh-30);x.fillStyle=tone;x.fillRect(bx,by,bw,bh);x.fillStyle=RED;x.fillRect(bx+bw*.68,by,bw*.1,bh);
  const fl=Math.floor(bh/44);for(let f=0;f<fl;f++)for(let c3=0;c3<4;c3++){x.fillStyle=rnd(seed*31+f*7+c3)>.55?'#FFD27A':'#5A6170';x.fillRect(bx+16+c3*(bw*.62-16)/4+4,by+12+f*44,(bw*.62-16)/4-10,24);}
  x.fillStyle='#7BAE7F';for(let i=0;i<5;i++){x.beginPath();x.arc(X+30+i*w/4.5,Y+h*.93,34+rnd(seed+i)*14,0,7);x.fill();}x.fillStyle='#CFC6BA';x.fillRect(X,Y+h*.94,w,h*.06);}
function poolArt(X,Y,w,h){x.fillStyle='#F6E7D2';x.fillRect(X,Y,w,h);x.fillStyle='#3BB3C9';x.beginPath();x.roundRect(X+50,Y+70,w-100,h-150,30);x.fill();x.strokeStyle='rgba(255,255,255,.7)';x.lineWidth=6;
  for(let r=0;r<4;r++){x.beginPath();for(let i=0;i<=20;i++){const px=X+70+i*(w-140)/20,py=Y+120+r*55+Math.sin(i*.9+r+performanceT*3)*8;i?x.lineTo(px,py):x.moveTo(px,py);}x.stroke();}
  x.strokeStyle='#9AA3AD';x.lineWidth=8;[0,40].forEach(d=>{x.beginPath();x.moveTo(X+w-150+d,Y+40);x.lineTo(X+w-150+d,Y+150);x.stroke();});
  x.fillStyle=GOLD;x.beginPath();x.moveTo(X+120,Y+h-40);x.arc(X+120,Y+h-40,90,Math.PI,0);x.fill();x.fillStyle='#8B6B4A';x.fillRect(X+116,Y+h-40,8,40);}
function grillArt(X,Y,w,h){x.fillStyle='#E9DCC9';x.fillRect(X,Y,w,h);x.fillStyle='#B98B5E';for(let i=0;i<8;i++)x.fillRect(X,Y+h*.62+i*22,w,16);
  x.strokeStyle='#5A4636';x.lineWidth=3;x.beginPath();x.moveTo(X,Y+50);x.quadraticCurveTo(X+w/2,Y+120,X+w,Y+50);x.stroke();for(let i=1;i<9;i++){const px=X+i*w/9,py=Y+50+70*Math.sin(Math.PI*i/9)*.9;x.fillStyle=Math.sin(performanceT*4+i)>0?'#FFD27A':'#F2B84B';x.beginPath();x.arc(px,py+12,11,0,7);x.fill();}
  x.fillStyle='#3B3B40';x.beginPath();x.roundRect(X+w/2-170,Y+h*.3,340,150,20);x.fill();x.fillStyle='#55555C';x.fillRect(X+w/2-190,Y+h*.3-20,380,30);
  x.fillStyle='#E06A3A';for(let i=0;i<4;i++){x.beginPath();x.ellipse(X+w/2-110+i*72,Y+h*.3-26,26,12,0,0,7);x.fill();}
  x.strokeStyle='rgba(255,255,255,.5)';x.lineWidth=5;for(let i=0;i<3;i++){x.beginPath();const sx=X+w/2-60+i*60;for(let j=0;j<=10;j++){const py=Y+h*.3-50-j*12,px=sx+Math.sin(j*.8+performanceT*3+i)*10;j?x.lineTo(px,py):x.moveTo(px,py);}x.stroke();}
  x.fillStyle='#5A6170';x.fillRect(X+w/2-150,Y+h*.3+150,16,70);x.fillRect(X+w/2+134,Y+h*.3+150,16,70);}
let performanceT=0;
function cover(art,X,Y,w,h){if(typeof art==='function')art(X,Y,w,h);}
'''+s[i1:]
# s2 slogan
R("tag('NUNCA PARE DE',W/2,960,40,WH,RED,t,BT*5);","tag('SEU LUGAR COMEÇA',W/2,960,40,WH,RED,t,BT*5);")
R("const sw=x.measureText('Sonhar').width","const sw=x.measureText('aqui.').width")
R("TX('Sonhar',W/2,1140,230,WH,{f:SCRIPT,w:400})","TX('aqui.',W/2,1140,230,WH,{f:SCRIPT,w:400})")
# s3 pin icon
R("const s=.055;x.fillStyle=WH;POLYS.forEach(poly=>{x.beginPath();poly.forEach(([a,b2],q)=>{const px=(a-1170)*s,py=(b2-410)*s-160;q?x.lineTo(px,py):x.moveTo(px,py);});x.closePath();x.fill();});x.restore();}",
  "x.translate(0,-140);icon(1,WH,.28);x.restore();}")
# s4: drawn building only, no real render
R("const ph=eio(p(t,BT*5.2,BT*6.6));","const ph=0;")
R("x.fillStyle=GRAPH;x.globalAlpha=1-ph;x.fillRect(0,base,W,H-base);x.globalAlpha=1;",
  "x.fillStyle=GRAPH;x.fillRect(0,base,W,H-base);tag('EM CONSTRUÇÃO',M+330,650,32,RED,WH,t,BT*6.4,{align:'left'});")
R("TX(`${String(cnt).padStart(2,'0')} ANDARES`,W/2,1770,44,GOLD,{a:1-ph,ls:4});","TX(`${String(cnt).padStart(2,'0')} ANDARES`,M,650,44,GOLD,{a:p(t,.3,.8),ls:4,align:'left'});")
# empreendimentos fictícios desenhados
i0=s.index('const EMP=');i1=s.index('function sEmp')
s=s[:i0]+"const EMP=[[0,'Residencial Jardins','ZONA NORTE'],[1,'Parque das Flores','ZONA LESTE'],[2,'Vista Alegre','ZONA SUL'],[3,'Bosque Real','ZONA OESTE'],[4,'Alto do Sol','ZONA SUL'],[5,'Recanto Verde','ZONA LESTE'],[6,'Portal do Parque','ZONA NORTE']];\n"+s[i1:]
R("tag('+ DE 120 PROJETOS',M,330,40,RED,WH,t,.05,{align:'left'});up('Tem Metrocasa',","tag('+ DE 30 PROJETOS',M,330,40,RED,WH,t,.05,{align:'left'});up('Tem NIDO',")
R("cover(IM[im],-cw/2,-ch/2,cw,ch,1.04);","building(im,-cw/2,-ch/2,cw,ch);")
R("TX(zn,-cw/2+34,ch/2-130,28,GOLD","TX(zn,-cw/2+34,ch/2-130,32,GOLD")
# lazer
R("card(IM.churras,","card(grillArt,");R("card(IM.piscina,","card(poolArt,")
R("cover(im,-w/2,-h/2,w,h,lerp(z0,1.02,eo(p(t,t0,t0+2.5))));","cover(im,-w/2,-h/2,w,h);")
# plantas vetoriais
R("const types=[['STUDIO','23 a 25 m²','pl_studio'],['2 DORMS','34 m²','pl_2d']];","const types=[['STUDIO','26 m²',0],['2 DORMS','38 m²',2]];")
i0=s.index("const k=eo5(p(it,0,.6));if(k>0&&t>BT*1.6){const im=");i1=s.index("  up('Studio, 1 e 2 dormitórios.'")
s=s[:i0]+"const k=eo5(p(it,0,.6));if(k>0&&t>BT*1.6){const w=860,h=600,X=W/2-w/2,Y=880;x.save();x.globalAlpha=k;x.translate(0,(1-k)*80);x.fillStyle='#F7F5F1';x.beginPath();x.roundRect(X-40,Y-40,w+80,h+80,30);x.fill();plan(types[i][2],X,Y,w,h,p(it,.1,1.8));x.restore();}\n"+s[i1:]
R("x.fillStyle=`rgba(227,30,36,${.08*fk})`","x.fillStyle=`rgba(18,134,111,${.08*fk})`")
R("lab.forEach(([s,a,b])=>TX(s,a,b,30,INK,{a:fk,ls:2}));","lab.forEach(([s,a,b])=>TX(s,a,b,40,INK,{a:fk,ls:2}));")
R("TX(m2,X+40,730,28,","TX(m2,X+40,730,32,")
# oferta
R("Math.round(149*","Math.round(199*")
R("[['ITBI + REGISTRO GRÁTIS',1100,BT*4],['UBER PRA VOCÊ VISITAR',1230,BT*5],['MINHA CASA MINHA VIDA',1360,BT*6]]","[['DOCUMENTAÇÃO GRÁTIS',1100,BT*4],['ENTRADA FACILITADA',1230,BT*5],['MINHA CASA MINHA VIDA',1360,BT*6]]")
R("TX('*Consulte condições no plantão de vendas.',W/2,1560,28,","TX('*Condições ilustrativas.',W/2,1500,40,")
# CTA portfólio
i0=s.index("  up('Mais de 120 projetos'");i1=s.index("const SC=")
s=s[:i0]+r"""  up('Essa construtora não existe.',W/2,960,52,GRY,t,BT*2.5,{w:500});
  up('Mas o vídeo da sua',W/2,1060,72,WH,t,BT*3.2,{});up('pode ficar assim.',W/2,1150,72,RED,t,BT*3.6,{});
  ['Construtoras e imobiliárias','Lançamentos e corretores'].forEach((sv,i)=>up('• '+sv,W/2,1250+i*64,42,WH,t,BT*4.3+i*.25,{w:500}));
  const bk=back(p(t,BT*5.6,BT*6.4),1.6);const pul=t>BT*6.4?1+.03*Math.exp(-((t-BT*6.4)%BT)*8):1;
  if(bk>0){x.save();x.translate(W/2,1440);x.scale(bk*pul,bk*pul);x.fillStyle=RED;x.beginPath();x.roundRect(-360,-66,720,132,66);x.fill();TX('Me chama no direct',0,3,50,WH);x.restore();}
  up('@alecreator_motion',W/2,1560,50,GOLD,t,BT*7,{});
}
"""+s[i1:]
R("logo(W/2,600,760,{pk,","logo(W/2,560,620,{pk,")
R("const pk=[0,1,2,3].map(i=>p(t,.05+i*.1,.6+i*.1));logo","const pk=[0,1,2].map(i=>p(t,.05+i*.1,.6+i*.1));logo")
R("const pk=[0,1,2,3].map(i=>p(t,.05+i*.12,.65+i*.12));","const pk=[0,1,2].map(i=>p(t,.05+i*.12,.65+i*.12));")
R("window.draw=function(t){x=X0;","window.draw=function(t){performanceT=t;x=X0;")
s=s.replace("Nunca pare de sonhar","slogan").replace('"Sonhar" reveal',"\"aqui.\" reveal")
for bad in ['Metrocasa','metro/','5061','construtorametrocasa','Ipiranga','Prime ','Sonhar','Uber','UBER','ITBI']:
    assert bad not in s,bad
open('index.html','w').write(s);print('ok',len(s))

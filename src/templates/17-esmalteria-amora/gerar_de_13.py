# Gera index.html (marca fictícia AMORA) a partir do corpo do vídeo 13, removendo marca/filmagens/contatos do cliente.
import re,os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
s=open('../13-cliente-esmalteria-cereja/v18_body.js').read()
def R(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(n,a[:90]); s=s.replace(a,b)
# paleta ameixa/amora no lugar do vermelho-cereja
R("const VINHO='#5A0E1B',VINHO2='#3E0912',CER='#B3132B',CER2='#D7263D'","const VINHO='#3A1233',VINHO2='#260B22',CER='#6E2A6B',CER2='#9B3D8F'")
R("INK='#2A0A10'","INK='#24091F'")
for a,b in [("'#2A050C'","'#1E0819'"),("'#5A0812'","'#3E1238'"),("rgba(179,19,43,","rgba(110,42,107,"),("'#9E1024','#C8283A'","'#5A1F57','#8A3A80'"),
            ("'#6B1A20'","'#4E1A49'"),("'#3A0A10'","'#2A0C27'"),("'#140306'","'#100410'"),("rgba(30,8,12,","rgba(24,8,22,")]:
    s=s.replace(a,b)
# fruta: amora (drupas) no lugar da cereja
i0=s.index('function cherryBall');i1=s.index('function cherries')
s=s[:i0]+r'''function cherryBall(cx,cy,r,col=CER){ // amora: cacho de drupas
  const pts=[];for(let j=0;j<5;j++){const n=[3,4,4,3,2][j];for(let i=0;i<n;i++)pts.push([(i-(n-1)/2)*r*.46,(j-1.6)*r*.4]);}
  pts.forEach(([dx,dy],i)=>{const rr=r*.3;const g=x.createRadialGradient(cx+dx-rr*.35,cy+dy-rr*.4,rr*.05,cx+dx,cy+dy,rr*1.05);g.addColorStop(0,'#C57BC0');g.addColorStop(.4,col);g.addColorStop(1,'#1E0819');
    x.fillStyle=g;x.beginPath();x.arc(cx+dx,cy+dy,rr,0,7);x.fill();x.fillStyle='rgba(255,255,255,.55)';x.beginPath();x.arc(cx+dx-rr*.35,cy+dy-rr*.38,rr*.16,0,7);x.fill();});
  x.fillStyle=FOLHA;for(let i=-1;i<=1;i++){x.beginPath();x.ellipse(cx+i*r*.22,cy-r*.85,r*.12,r*.3,i*.7,0,7);x.fill();}}
'''+s[i1:]
# logo fictício: wordmark AMORA (texto) + amorinha em cima
i0=s.index('// tinted logo canvases');i1=s.index('const NZ=')
s=s[:i0]+r'''// logo fictício AMORA (tipográfico)
function logo(col,cx,cy,w,reveal=1,cherryK=1,shine=-1){x.save();x.font=`900 100px ${THICK}`;x.letterSpacing='6px';const mw=x.measureText('AMORA').width;x.restore();const size=100*w/mw,h=size*1.1;const X=cx-w/2,Y=cy-h/2;
  x.save();x.beginPath();const rx=X-60+(w+260)*reveal;x.moveTo(X-60,Y-60);x.lineTo(rx,Y-60);x.lineTo(rx-120,Y+h*1.6+60);x.lineTo(X-60,Y+h*1.6+60);x.closePath();x.clip();
  TX('AMORA',cx,cy,size,col,{kind:'thick',ls:6});TX('esmalteria',cx,cy+h*.78,size*.34,col,{kind:'ital'});
  if(shine>=0&&shine<=1){x.globalCompositeOperation='source-atop';const sx=X-200+(w+400)*shine;const g=x.createLinearGradient(sx-120,0,sx+120,0);g.addColorStop(0,'rgba(255,230,180,0)');g.addColorStop(.5,'rgba(255,230,180,.75)');g.addColorStop(1,'rgba(255,230,180,0)');x.fillStyle=g;x.fillRect(X,Y-40,w,h*1.6);}
  x.restore();
  if(cherryK>0){const r=Math.max(14,w*.035);const dy=(1-cherryK)*-300;cherryBall(X+w-size*.36,Y-r*.9+dy,r);}}
// ilustrações vetoriais (substituem as filmagens)
function coffeeArt(X,Y,w,h,t){const g=x.createLinearGradient(0,Y,0,Y+h);g.addColorStop(0,'#F6D49A');g.addColorStop(1,'#C98A3E');x.fillStyle=g;x.fillRect(X,Y,w,h);
  x.fillStyle='#8A5A2E';x.fillRect(X,Y+h*.72,w,h*.28);const cx=X+w/2,cy=Y+h*.66;
  x.fillStyle=CREAM;x.beginPath();x.ellipse(cx,cy+60,170,34,0,0,7);x.fill();x.beginPath();x.moveTo(cx-110,cy-70);x.lineTo(cx+110,cy-70);x.quadraticCurveTo(cx+100,cy+50,cx,cy+56);x.quadraticCurveTo(cx-100,cy+50,cx-110,cy-70);x.fill();
  x.strokeStyle=CREAM;x.lineWidth=18;x.beginPath();x.arc(cx+118,cy-20,34,-1.2,1.2);x.stroke();x.fillStyle='#4A2A14';x.beginPath();x.ellipse(cx,cy-70,104,20,0,0,7);x.fill();
  x.strokeStyle='rgba(255,255,255,.7)';x.lineWidth=6;x.lineCap='round';for(let i=0;i<3;i++){x.beginPath();for(let y=0;y<200;y+=10){const px=cx-50+i*50+Math.sin(y*.05+t*3+i)*14;y?x.lineTo(px,cy-100-y):x.moveTo(px,cy-100);}x.stroke();}}
function maniArt(X,Y,w,h,t){const g=x.createLinearGradient(0,Y,0,Y+h);g.addColorStop(0,'#F3D3C7');g.addColorStop(1,'#D9A3B5');x.fillStyle=g;x.fillRect(X,Y,w,h);
  [['#9B3D8F',-90,0],['#E59AA0',95,40]].forEach(([c2,dx,dy],i)=>{const bx=X+w/2+dx,by=Y+h*.62+dy;x.save();x.translate(bx,by);x.rotate((i?.12:-.1)+Math.sin(t*1.2+i)*.03);
    x.fillStyle=c2;x.beginPath();x.roundRect(-70,-90,140,170,30);x.fill();x.fillStyle='rgba(255,255,255,.35)';x.fillRect(-48,-70,16,120);x.fillStyle='#2A1A22';x.beginPath();x.roundRect(-30,-230,60,145,10);x.fill();x.fillStyle='rgba(255,255,255,.2)';x.fillRect(-20,-220,10,120);x.restore();});
  for(let i=0;i<5;i++){x.fillStyle=SW[i*2+3];x.beginPath();x.ellipse(X+70+i*70,Y+h*.9,22,30,0,0,7);x.fill();}}
function beachArt(t){const g=x.createLinearGradient(0,0,0,H);g.addColorStop(0,'#3E1F4A');g.addColorStop(.45,'#C9677A');g.addColorStop(.62,'#F6B26B');x.fillStyle=g;x.fillRect(0,0,W,H);
  x.fillStyle='#FFE1A8';x.beginPath();x.arc(W*.42,1080,150,0,7);x.fill();x.fillStyle='#4A2B57';x.fillRect(0,1150,W,330);
  x.strokeStyle='rgba(255,225,168,.6)';x.lineWidth=5;for(let i=0;i<12;i++){const y=1170+i*24,wd=260-i*12+Math.sin(t*2+i)*20;x.beginPath();x.moveTo(W*.42-wd/2,y);x.lineTo(W*.42+wd/2,y);x.stroke();}
  x.fillStyle='#E8B98A';x.beginPath();x.moveTo(0,1480);x.quadraticCurveTo(W/2,1420,W,1490);x.lineTo(W,H);x.lineTo(0,H);x.fill();}
'''+s[i1:]
R("function clipFrame(arr,ct,X,Y,w,h,{crop=[0,0.18,1,.82],z=1}={}){","function clipFrame(arr,ct,X,Y,w,h,{crop=[0,0.18,1,.82],z=1}={}){if(typeof arr==='function'){arr(X,Y,w,h,ct);return;}")
# textos
R("soft('Quando a beleza pede',W/2,560,76,","soft('Feito com calma,',W/2,560,76,")
R("letters('CEREJA',W/2,1010,","letters('AMORA',W/2,1010,")
R("soft('no topo.',W/2,1240,","soft('e muito cuidado.',W/2,1240,")
R("label('A EXPERIÊNCIA CEREJA'","label('A EXPERIÊNCIA AMORA'")
R("'Café Cereja'","'Café da casa'")
R("label('CAFÉ CEREJA',","label('CAFÉ DA CASA',")
R("archWin(CL.coffee,","archWin(coffeeArt,");R("archWin(CL.mani,","archWin(maniArt,")
R("const sk=p(t,BT*2.5,3.84);","const sk=0;")
R("clipFrame(CL.wide,t*.8,0,0,W,H,{crop:[0,0,1,1],z:lerp(1.12,1.04,sine(p(t,0,3.84)))});","beachArt(t);")
R("letters('REFÚGIO',W/2,1290,","letters('REFÚGIO',W/2,1290,")
R("soft('em Caraíva, Bahia.',","soft('pra sua rotina.',")
# s8: nova unidade genérica
R("x.measureText('Cereja').width","x.measureText('Amora').width")
R("x.fillText('Cereja',","x.fillText('Amora',")
R("x.fillText('Pinheiros',0,0)","x.fillText('seu bairro',0,0)")
R("TX('Rua Arthur de Azevedo, 972',","TX('Nova unidade',")
R("label('SÃO PAULO · PINHEIROS',","label('AGENDA ABERTA',")
# s9: CTA de portfólio
i0=s.index("  label('DUAS UNIDADES.");i1=s.index("const HANDLE=")
s=s[:i0]+r"""  soft('Essa marca não existe.',W/2,1000,52,CREAM,t,BT*4.2,{kind:'ital'});
  letters('MAS O VÍDEO DA SUA',W/2,1100,64,CREAM,t,BT*4.8,{stag:.02,fit:940});letters('ESMALTERIA',W/2,1185,64,AMB2,t,BT*5.2,{stag:.03});soft('pode ficar assim.',W/2,1270,60,CREAM,t,BT*5.6,{kind:'ital'});
  label('ESMALTERIAS • SALÕES • CLÍNICAS',W/2,1350,AMB2,t,BT*6,{size:34,ls:4});
  const bk=eo5(p(t,BT*6.6,BT*6.6+.6));if(bk>0){x.save();x.globalAlpha=bk;x.translate(W/2,1440+(1-bk)*30);x.fillStyle=CREAM;x.beginPath();x.roundRect(-360,-56,720,112,56);x.fill();TX('Me chama no direct',0,2,46,VINHO,{kind:'sans'});x.restore();}
  label('@alecreator_motion',W/2,1545,AMB2,t,BT*7.4,{size:44,ls:2});
}
"""+s[i1:]
R("const HANDLE='@esmalteriacereja';","")
R("const rv=eio(p(t,BT*.8,BT*3));logo(CREAM,W/2,640,740,rv,t<BT*3.1?0:back(p(t,BT*3.1,BT*4.1),2.2),p(t,BT*4.5,BT*6.5));",
  "const rv=eio(p(t,BT*.8,BT*3));logo(CREAM,W/2,700,640,rv,0,p(t,BT*4.5,BT*6.5));"
  "const land=BT*4.1;if(t>BT*3.1){const fy=lerp(-400,425,eo(p(t,BT*3.1,land)));const sw=t>land?Math.sin((t-land)*6)*.22*Math.exp(-(t-land)*2):0;cherries(W/2,fy,70,sw,1);}")
s=s.replace("// S8 Pinheiros coming soon (their dark-wine grain style)","// S8 nova unidade")
low=s.lower()
for bad in ['cereja','caraíva','pinheiros','arthur','99824','@cereja','whatsapp','cl.','logo_letters','im.letters']:
    assert bad not in low,bad
h='<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:#000}canvas{display:block}</style></head><body><canvas id="c" width="1080" height="1920"></canvas><script>\nconst IM={};window.IMGS=[];\n'+s+'</script></body></html>'
open('index.html','w').write(h);print('ok',len(h))

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
W,H=1080,1920;rng=np.random.default_rng(3)
# ---- fundo (vai ser muito desfocado) ----
bg=Image.new('RGB',(W,H));d=ImageDraw.Draw(bg)
y=np.linspace(0,1,H)[:,None];x=np.linspace(0,1,W)[None,:]
wall=np.dstack([214-30*x+0*y,190-34*x+0*y,160-40*x+0*y]);bg=Image.fromarray(np.clip(wall,0,255).astype(np.uint8));d=ImageDraw.Draw(bg)
# janela à esquerda com luz de fim de tarde + cortina de linho
d.rectangle((-40,180,430,1250),fill=(255,226,170));d.rectangle((-40,180,430,1250),outline=(150,120,90),width=26);d.line((195,180,195,1250),fill=(150,120,90),width=18)
for i in range(9):
    xx=330+i*28;c=(236-(i%2)*18,222-(i%2)*18,196-(i%2)*16);d.rectangle((xx,120,xx+30,1350),fill=c)
d.rectangle((-60,120,90,1350),fill=(230,214,186))
# sofá bege + manta de tricô
d.rounded_rectangle((300,1060,1180,1500),60,fill=(196,170,138));d.rounded_rectangle((260,1180,1180,1500),50,fill=(206,182,150))
d.rounded_rectangle((420,1000,640,1250),70,fill=(214,192,160));d.rounded_rectangle((760,1010,980,1250),70,fill=(188,160,128))
d.polygon([(820,1060),(1100,1040),(1120,1420),(870,1440)],fill=(232,222,204))
# luzes de natal quentes (cordão no topo da janela e na parede)
lights=[]
for i in range(26):
    t=i/25;lights.append((int(-20+t*1120),int(150+70*np.sin(t*9)+t*40)))
for i in range(10):lights.append((int(470+i*65),int(760+30*np.sin(i))))
bg=bg.filter(ImageFilter.GaussianBlur(16))
a=np.asarray(bg).astype(float)
# bokeh: discos com borda levemente mais clara
bk=np.zeros((H,W,3))
for (lx,ly) in lights+[(rng.integers(0,W),rng.integers(120,1300)) for _ in range(14)]:
    r=rng.integers(14,34);yy,xx=np.ogrid[-ly:H-ly,-lx:W-lx];dd=np.sqrt(xx*xx+yy*yy)
    disk=np.clip(r-dd,0,1.5)/1.5;disk*=0.75+0.25*np.clip((dd/r)**3,0,1)
    col=np.array([255,196,110]) if rng.random()<.8 else np.array([255,226,170]);bk+=disk[...,None]*col*rng.uniform(.25,.5)
a=a+bk*(1-a/320)
# luz quente entrando pela janela (vazamento suave)
gl=np.exp(-(((x-0.1)/0.45)**2+((y-0.35)/0.3)**2));a+=gl[...,None]*np.array([60,38,10])
# brilho da árvore na parede
gt=np.exp(-(((x-0.5)/0.28)**2+((y-0.5)/0.22)**2));a+=gt[...,None]*np.array([55,38,8])
# ---- aparador de madeira clara ----
TOP0,TOP1,FR=1440,1540,1590
def grain(h,w,base,s=1.):
    n=rng.standard_normal((h//3+2,w//200+2));n=np.asarray(Image.fromarray(((n-n.min())/(np.ptp(n))*255).astype(np.uint8)).resize((w,h),Image.BICUBIC)).astype(float)/255
    line=np.sin((np.arange(h)[:,None]*0.9+n*4+np.arange(w)[None,:]*0.0))*0.5+0.5
    return np.dstack([base[i]*(0.9+0.12*line*s+0.06*n) for i in range(3)])
# tampo em perspectiva (trapézio)
top=grain(TOP1-TOP0,W,(222,190,150))
for r in range(TOP1-TOP0):
    k=r/(TOP1-TOP0);a[TOP0+r,:]=top[r]*(0.95+0.08*k)
# luz da janela e das luzes no tampo
yy=np.arange(TOP0,TOP1)[:,None];xx=np.arange(W)[None,:]
a[TOP0:TOP1]+=(np.exp(-(((xx-540)/300)**2))*np.exp(-((yy-1500)/60)**2))[...,None]*np.array([70,50,15])
a[TOP1:FR]=grain(FR-TOP1,W,(236,206,166),.6)*1.02  # borda frontal iluminada
front=grain(H-FR,W,(196,160,120),1.2)
fr=np.linspace(1,.72,H-FR)[:,None,None];a[FR:]=front*fr
# frestas das gavetas
for xg in (360,720):a[FR+30:,xg-3:xg+3]*=0.55
a[FR+40:FR+52,140:240]=a[FR+40:FR+52,140:240]*.6+np.array([170,140,90])*.4
img=Image.fromarray(np.clip(a,0,255).astype(np.uint8))
# a frente do móvel fica levemente desfocada (mais perto da câmera)
low=img.crop((0,FR,W,H)).filter(ImageFilter.GaussianBlur(2.2));img.paste(low,(0,FR))
# ---- árvore (produto sem alteração) ----
t=Image.open('tree.png');al=np.asarray(t.split()[3]).astype(float)/255
al=np.clip((al-.12)/.6,0,1);m=Image.fromarray((al*255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.8));t.putalpha(m)
t=t.crop(t.getbbox());th=int(H*.60);tw=int(t.width*th/t.height);t=t.resize((tw,th),Image.LANCZOS)
bx=(W-tw)//2;by=1505-th
# sombra de contato + poça de luz no tampo
sh=Image.new('L',(W,H),0);ds=ImageDraw.Draw(sh);ds.ellipse((W//2-150,1478,W//2+150,1530),fill=170);sh=sh.filter(ImageFilter.GaussianBlur(16))
img=Image.composite(Image.new('RGB',(W,H),(70,45,25)),img,sh)
img.paste(t,(bx,by),t)
# ---- acabamento de foto de celular: luz quente, grão fino, vinheta ----
a=np.asarray(img).astype(float)
g=rng.normal(0,3.2,(H,W,1));a+=g
v=1-0.28*((x-0.5)**2*1.6+(y-0.48)**2*1.1)*2.2;a*=np.clip(v,0.6,1)[...,None]
a=a*np.array([1.03,1.0,0.94])
Image.fromarray(np.clip(a,0,255).astype(np.uint8)).save('arvore_sala.jpg',quality=95)

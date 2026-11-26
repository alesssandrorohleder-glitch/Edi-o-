# Recorta produtos dos prints do site (1170x2532; coords medidas na tela 924x2000) → midia/*.png (recorte) e *.jpg (fotos)
import numpy as np, os, sys
from PIL import Image, ImageFilter
from scipy import ndimage
U=sys.argv[1];S=1170/924
CUT={ # nome: (arquivo, y0, y1)  — lanches/porções em fundo branco → recorte
 'ultra':('37e7cf39',570,830),'bacon':('41e2adaa',1147,1403),'australiano':('8a17439b',807,1065),'doritos':('41e2adaa',548,795),
 'big':('97f6290a',520,780),'plusburguer':('37e7cf39',1177,1435),'salada':('8a17439b',502,763),'cheddar':('37e7cf39',874,1128),
 'batata':('97f6290a',1014,1270),'batatacb':('f25c8611',872,1130),'acai1':('67bc1cae',493,750),'acai2':('67bc1cae',796,1053),'acai3':('67bc1cae',1100,1356),'acai4':('67bc1cae',1403,1660),
 'suco':('77a3b222',690,955)}
PH={'picanha':('036d328d',800,1058),'parmegiana':('036d328d',497,755),'churrasco':('92f203b0',589,848),'cafe':('3ffa96e1',697,955),'cappuccino':('3ffa96e1',1304,1562),
 'shake':('b9a5272b',945,1203),'supreme':('25f243cf',519,777),'shake2':('b9a5272b',642,900),'nuggets':('92f203b0',893,1151)}
def load(f,y0,y1,x0=585,x1=885): return Image.open(f'{U}/{f}-image.png').convert('RGB').crop((int(x0*S),int(y0*S),int(x1*S),int(y1*S)))
os.makedirs('midia',exist_ok=True)
for n,(f,y0,y1) in CUT.items():
    a=np.asarray(load(f,y0,y1,590,880)).astype(float);mx=a.max(2);mn=a.min(2);sat=(mx-mn)/(mx+1);lum=a.mean(2)
    # fundo/sombra = claro e sem cor
    bg=(sat<.12)&(lum>175)
    if not n.startswith('batata'):
        h=bg.shape[0];yy=np.arange(h)[:,None]>h*.82;bg|=yy&(sat<.2)&(lum>110)
    m=~bg;m=ndimage.binary_opening(m,iterations=2);lab,nl=ndimage.label(m)
    if nl: sz=ndimage.sum(m,lab,range(1,nl+1));m=np.isin(lab,1+np.where(sz>sz.max()*.04)[0])
    m=ndimage.binary_fill_holes(m);m=ndimage.binary_erosion(m,iterations=1)
    al=np.asarray(Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)))
    im=Image.fromarray(np.dstack([a.astype(np.uint8),al]),'RGBA');im=im.crop(im.getbbox());im.save(f'midia/{n}.png');print(n,im.size)
for n,(f,y0,y1) in PH.items():
    im=load(f,y0+6,y1-6,592,878);im.save(f'midia/{n}.jpg',quality=95);print(n,im.size)

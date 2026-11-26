import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as nd
src='/root/.claude/uploads/68a3c0dc-e655-5ab0-9ff5-d5143994bef0/0c31a95f-image.jpg'
im=np.asarray(Image.open(src).convert('RGB')).astype(float)
mn=im.min(2);mx=im.max(2);sat=mx-mn
fg=(mn<230)|(sat>22)
fg=nd.binary_opening(fg,iterations=1)
lab,nl=nd.label(fg);objs=nd.find_objects(lab);sizes=nd.sum(fg,lab,range(1,nl+1))
big=[i+1 for i in range(nl) if sizes[i]>400]
# map by bbox like before
info={}
for k in big:
    sl=objs[k-1];info[k]=(sl[1].start,sl[0].start)
def pick(xmin,ymin,ymax):
    for k,(x0,y0) in info.items():
        if x0>=xmin-15 and x0<=xmin+40 and ymin-30<=y0<=ymax: return k
order={'bun_top':(402,300,330),'cheese':(400,450,480),'full':(27,480,510),'patty':(410,530,560),'lettuce':(392,640,670),'tomato':(410,770,800),'bun_bottom':(405,865,895)}
for nm,(xx,y0,y1) in order.items():
    k=pick(xx,y0,y1);m=lab==k
    m=nd.binary_fill_holes(nd.binary_closing(m,iterations=2))
    # shadow removal: neutral bright pixels at bottom are not object
    shadow=(sat<40)&(mn>170)
    if nm in('bun_bottom','full'):
        ys=np.where(m.any(1))[0];yb=ys.max();cut=yb-int((yb-ys.min())*0.14)
        low=np.zeros_like(m);low[cut:]=True;shadow=shadow|(low&(sat<55)&(mn>110))
    core=nd.binary_erosion(m&~shadow,iterations=2)
    core=nd.binary_fill_holes(core)
    if nm in('patty','bun_bottom','bun_top','tomato'):
        core=nd.binary_opening(core,structure=np.ones((5,5)),iterations=1);core=nd.binary_erosion(core,iterations=1)
    lab2,n2=nd.label(core);sz=nd.sum(core,lab2,range(1,n2+1));core=lab2==(1+np.argmax(sz))
    band=nd.binary_dilation(core,iterations=(1 if nm in('patty','bun_bottom','bun_top','tomato') else 2))&~core
    # alpha in band from distance to white
    a_col=np.clip((250-mn)/70,0,1)*np.clip(1-(shadow*1.0),0,1);a_col=np.where(a_col<.35,0,a_col)
    a=np.where(core,1.0,np.where(band,a_col,0.0))
    a=nd.gaussian_filter(a,.6)*np.where(core,1,1)
    a=np.maximum(a,core*1.0)
    # decontaminate white halo
    A=np.clip(a,1e-3,1)[...,None]
    C=np.clip((im-(1-A)*255)/A,0,255)
    C=np.where((a<1)[...,None],C,im)
    sl=nd.find_objects(core.astype(int))[0];y0_,y1_,x0_,x1_=sl[0].start-6,sl[0].stop+6,sl[1].start-6,sl[1].stop+6
    out=np.dstack([C,a*255])[y0_:y1_,x0_:x1_].astype(np.uint8)
    I=Image.fromarray(out,'RGBA');I=I.resize((I.width*5//2,I.height*5//2),Image.LANCZOS)
    # sharpen rgb only
    r,g,b,al=I.split();rgb=Image.merge('RGB',(r,g,b)).filter(ImageFilter.UnsharpMask(radius=2,percent=55,threshold=2));I=Image.merge('RGBA',(*rgb.split(),al))
    I.save(f'burger/{nm}.png');print(nm,I.size)

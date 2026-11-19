import cv2,numpy as np,sys
from scipy import ndimage as nd
from PIL import Image
def cut(name,scale=.5,thr=14,core_thr=40,it=6):
    im=cv2.imread(f'sushi2/{name}.jpg');H,W=im.shape[:2]
    sm=cv2.resize(im,None,fx=scale,fy=scale,interpolation=cv2.INTER_AREA)
    lab=cv2.cvtColor(sm,cv2.COLOR_BGR2LAB).astype(float)
    # background estimate from border median
    b=np.concatenate([lab[:20].reshape(-1,3),lab[-20:].reshape(-1,3),lab[:,:20].reshape(-1,3),lab[:,-20:].reshape(-1,3)])
    bgc=np.median(b,0);d=np.linalg.norm(lab-bgc,axis=2)
    # texture (local std) helps white rice
    g=cv2.cvtColor(sm,cv2.COLOR_BGR2GRAY).astype(float);mu=cv2.blur(g,(7,7));sd=np.sqrt(np.maximum(cv2.blur(g*g,(7,7))-mu*mu,0))
    score=d+sd*2.2
    mask=np.full(g.shape,cv2.GC_BGD,np.uint8)
    pr=score>thr;pr=nd.binary_dilation(pr,iterations=8)
    mask[pr]=cv2.GC_PR_BGD
    mask[score>thr]=cv2.GC_PR_FGD
    core=nd.binary_erosion(score>core_thr,iterations=4);core=nd.binary_fill_holes(nd.binary_closing(core,iterations=6));core=nd.binary_erosion(core,iterations=6)
    mask[core]=cv2.GC_FGD
    bg=np.zeros((1,65));fg=np.zeros((1,65));cv2.grabCut(sm,mask,None,bg,fg,it,cv2.GC_INIT_WITH_MASK)
    m=(mask==1)|(mask==3);m=nd.binary_fill_holes(nd.binary_opening(m,iterations=2))
    hsv=cv2.cvtColor(sm,cv2.COLOR_BGR2HSV).astype(float);S=hsv[...,1];V=hsv[...,2]
    sd2=cv2.GaussianBlur(sd,(0,0),2)
    shadow=(S<26)&(sd2<5.5)&(V>120)
    border=m&~nd.binary_erosion(m,iterations=3)
    lb,nb=nd.label(shadow&m);touch=np.unique(lb[border&shadow]);touch=touch[touch>0]
    m=m&~np.isin(lb,touch)
    m=nd.binary_opening(m,structure=np.ones((7,7)));m=nd.binary_fill_holes(m)
    labm,n=nd.label(m);sz=nd.sum(m,labm,range(1,n+1));keep=[i+1 for i in range(n) if sz[i]>sz.max()*0.002];m=np.isin(labm,keep)
    mf=cv2.resize(m.astype(np.float32),(W,H),interpolation=cv2.INTER_LINEAR)
    mf=cv2.GaussianBlur(mf,(0,0),2.5);a=np.clip((mf-.5)*2.5+.5,0,1)
    ys,xs=np.where(a>.02);y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
    rgb=cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
    # decontaminate white halo
    A=np.clip(a,1e-3,1)[...,None];C=np.clip((rgb-(1-A)*bgc_rgb(im))/A,0,255);C=np.where((a<1)[...,None],C,rgb)
    I=Image.fromarray(np.dstack([C,a*255])[y0:y1,x0:x1].astype(np.uint8),'RGBA');I.save(f'sushi2/{name}_cut.png');print(name,I.size);open(f'sushi2/{name}_off.txt','w').write(f'{x0} {y0}')
def bgc_rgb(im):
    b=np.concatenate([im[:30].reshape(-1,3),im[-30:].reshape(-1,3)]);return np.median(b,0)[::-1]
for nm in sys.argv[1:]: cut(nm)

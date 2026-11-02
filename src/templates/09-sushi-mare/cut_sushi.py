import cv2,numpy as np
from scipy import ndimage as nd
from PIL import Image, ImageFilter
def gc(tile,rect,name,extra_bg=None,extra_fg=None,scale=3,it=8):
    im=cv2.imread(f'sushi/{tile}.png');H,W=im.shape[:2]
    mask=np.zeros((H,W),np.uint8);x,y,w,h=rect
    mask[:]=cv2.GC_BGD;mask[y:y+h,x:x+w]=cv2.GC_PR_FGD
    if extra_fg:
        for (a,b,c,d) in extra_fg: mask[b:d,a:c]=cv2.GC_FGD
    if extra_bg:
        for (a,b,c,d) in extra_bg: mask[b:d,a:c]=cv2.GC_BGD
    bg=np.zeros((1,65));fg=np.zeros((1,65));cv2.grabCut(im,mask,None,bg,fg,it,cv2.GC_INIT_WITH_MASK)
    m=(mask==1)|(mask==3);m=nd.binary_opening(m,iterations=1);m=nd.binary_fill_holes(m)
    lab,n=nd.label(m);sz=nd.sum(m,lab,range(1,n+1));m=lab==(1+np.argmax(sz))
    big=cv2.resize(im,None,fx=scale,fy=scale,interpolation=cv2.INTER_LANCZOS4)
    mb=cv2.resize(m.astype(np.float32),None,fx=scale,fy=scale,interpolation=cv2.INTER_LINEAR)
    mb=cv2.GaussianBlur(mb,(0,0),scale*.9);a=np.clip((mb-.5)*2.4+.5,0,1)
    ys,xs=np.where(a>.05);y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
    rgb=cv2.cvtColor(big,cv2.COLOR_BGR2RGB)[y0:y1,x0:x1]
    I=Image.fromarray(np.dstack([rgb,(a[y0:y1,x0:x1]*255).astype(np.uint8)]),'RGBA')
    r,g,b,al=I.split();rgb2=Image.merge('RGB',(r,g,b)).filter(ImageFilter.UnsharpMask(radius=3,percent=80,threshold=2));I=Image.merge('RGBA',(*rgb2.split(),al))
    I.save(f'sushi/{name}.png');print(name,I.size)
gc('tile1',(2,140,232,185),'nigiri')
gc('tile2',(6,165,170,195),'uramaki',extra_bg=[(170,0,234,420),(0,0,234,150)])
gc('tile6',(2,150,200,200),'hotroll',extra_bg=[(0,0,234,140)])
gc('tile4',(18,22,195,285),'temaki',extra_bg=[(0,300,234,420)])
gc('tile9',(25,140,200,140),'chopnigiri')
c=Image.new('RGBA',(2000,800),(12,12,13,255));xo=10
for nm in ['nigiri','uramaki','hotroll','temaki','chopnigiri']:
    I=Image.open(f'sushi/{nm}.png');I=I.resize((I.width*2//3,I.height*2//3));c.alpha_composite(I,(xo,20));xo+=I.width+15
c.convert('RGB').save('pv_sushi.jpg')

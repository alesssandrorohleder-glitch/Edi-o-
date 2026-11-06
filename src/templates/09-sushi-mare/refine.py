import numpy as np,cv2
from scipy import ndimage as nd
from PIL import Image
def refine(nm,vthr=70,open_r=4,out=None):
    I=np.asarray(Image.open(f'sushi/{nm}.png')).astype(np.float32);rgb=I[...,:3];a=I[...,3]/255
    hsv=cv2.cvtColor(rgb.astype(np.uint8),cv2.COLOR_RGB2HSV).astype(int);V=hsv[...,2];S=hsv[...,1]
    m=a>.5
    dark=(V<vthr)&m
    # dark components touching the outside boundary
    border=m&~nd.binary_erosion(m,iterations=3)
    lab,n=nd.label(dark);touch=np.unique(lab[border&dark]);touch=touch[touch>0]
    kill=np.isin(lab,touch)
    m2=m&~kill
    m2=nd.binary_opening(m2,structure=np.ones((open_r*2+1,open_r*2+1)))
    m2=nd.binary_fill_holes(m2);lab,n=nd.label(m2);sz=nd.sum(m2,lab,range(1,n+1));m2=lab==(1+np.argmax(sz))
    # smooth outline
    sm=cv2.GaussianBlur(m2.astype(np.float32),(0,0),3)>.5
    al=cv2.GaussianBlur(sm.astype(np.float32),(0,0),1.1);al=np.clip((al-.5)*2.2+.5,0,1)
    ys,xs=np.where(al>.02);y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
    o=np.dstack([rgb,al*255])[y0:y1,x0:x1].astype(np.uint8);Image.fromarray(o,'RGBA').save(f'sushi/{out or nm}_r.png')
for nm,v in [('nigiri',60),('uramaki',55),('hotroll',45)]: refine(nm,v)
c=Image.new('RGBA',(2000,700),(245,240,232,255));xo=10
for nm in ['nigiri','uramaki','hotroll']:
    I=Image.open(f'sushi/{nm}_r.png');I=I.resize((I.width*2//3*1,I.height*2//3));c.alpha_composite(I,(xo,20));xo+=I.width+20
c.convert('RGB').save('chk.jpg')

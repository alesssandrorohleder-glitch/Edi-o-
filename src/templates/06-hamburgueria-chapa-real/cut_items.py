import cv2,numpy as np
from scipy import ndimage as nd
from PIL import Image, ImageFilter
U='/root/.claude/uploads/68a3c0dc-e655-5ab0-9ff5-d5143994bef0/'
def finish(im,m,name,scale=2.0,feather=1.2):
    m=nd.binary_fill_holes(m);lab,n=nd.label(m);sz=nd.sum(m,lab,range(1,n+1));m=lab==(1+np.argmax(sz))
    a=cv2.GaussianBlur(m.astype(np.float32),(0,0),feather)
    a=np.clip((a-.5)*2.2+.5,0,1)
    ys,xs=np.where(m);y0,y1,x0,x1=max(0,ys.min()-4),min(m.shape[0],ys.max()+5),max(0,xs.min()-4),min(m.shape[1],xs.max()+5)
    rgb=cv2.cvtColor(im,cv2.COLOR_BGR2RGB)[y0:y1,x0:x1]
    I=Image.fromarray(np.dstack([rgb,(a[y0:y1,x0:x1]*255).astype(np.uint8)]),'RGBA')
    I=I.resize((int(I.width*scale),int(I.height*scale)),Image.LANCZOS)
    r,g,b,al=I.split();rgb2=Image.merge('RGB',(r,g,b)).filter(ImageFilter.UnsharpMask(radius=2,percent=50,threshold=2));I=Image.merge('RGBA',(*rgb2.split(),al))
    I.save(f'burger/{name}.png');print(name,I.size)
# ---- soda
im=cv2.imread(U+'3242c4dd-image.jpg');H,W=im.shape[:2]
poly=np.array([(70,445),(78,410),(110,375),(200,350),(350,337),(500,342),(590,365),(625,395),(634,440),(628,470),(600,492),(586,520),(578,560),(571,620),(562,680),(553,700),(540,800),(527,900),(513,1000),(493,1073),(473,1133),(455,1155),(427,1168),(380,1176),(320,1175),(267,1161),(237,1128),(217,1080),(200,1000),(183,900),(167,800),(150,700),(138,640),(128,590),(122,540),(105,515),(80,490),(70,470)],np.int32)
pm=np.zeros((H,W),np.uint8);cv2.fillPoly(pm,[poly],1)
straw=[(337,585),(374,400),(402,215),(416,165),(442,130),(585,-5)]
cv2.polylines(pm,[np.array(straw,np.int32)],False,1,24)
mask=np.full((H,W),cv2.GC_BGD,np.uint8)
dil=cv2.dilate(pm,np.ones((5,5)));ero=cv2.erode(pm,np.ones((7,7)))
mask[dil>0]=cv2.GC_PR_BGD;mask[pm>0]=cv2.GC_PR_FGD;mask[ero>0]=cv2.GC_FGD
bg=np.zeros((1,65),np.float64);fg=np.zeros((1,65),np.float64)
cv2.grabCut(im,mask,None,bg,fg,6,cv2.GC_INIT_WITH_MASK)
m=((mask==cv2.GC_FGD)|(mask==cv2.GC_PR_FGD))
gc=m.copy()
m=(m&(dil>0))|(ero>0)
m=nd.binary_opening(m,iterations=2)
sw=np.zeros((H,W),np.uint8);cv2.polylines(sw,[np.array(straw,np.int32)],False,1,30)
pl=np.zeros((H,W),np.uint8);cv2.fillPoly(pl,[poly],1);pl=cv2.dilate(pl,np.ones((5,5)))
m[:380]=gc[:380]&((sw[:380]>0)|(pl[:380]>0))
body=pm>0
m[540:]=body[540:]
finish(im,m,'soda',2.0)
# ---- fries
im=cv2.imread(U+'e65d7557-image.jpg');H,W=im.shape[:2]
poly=np.array([(150,236),(430,388),(690,316),(690,450),(668,560),(642,568),(620,600),(615,700),(612,800),(560,792),(545,822),(362,958),(140,850),(32,605),(24,560),(30,470),(70,380),(114,290)],np.int32)
pm=np.zeros((H,W),np.uint8);cv2.fillPoly(pm,[poly],1)
dil=cv2.dilate(pm,np.ones((11,11)));ero=cv2.erode(pm,np.ones((13,13)))
mask=np.full((H,W),cv2.GC_BGD,np.uint8);mask[dil>0]=cv2.GC_PR_BGD;mask[pm>0]=cv2.GC_PR_FGD;mask[ero>0]=cv2.GC_FGD
bg=np.zeros((1,65),np.float64);fg=np.zeros((1,65),np.float64)
cv2.grabCut(im,mask,None,bg,fg,6,cv2.GC_INIT_WITH_MASK)
m=((mask==cv2.GC_FGD)|(mask==cv2.GC_PR_FGD));m=(m&(dil>0))|(ero>0)
m=nd.binary_opening(m,iterations=1)
finish(im,m,'fries_photo',2.0)

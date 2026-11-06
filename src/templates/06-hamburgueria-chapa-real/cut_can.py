import cv2,numpy as np,math
from scipy import ndimage as nd
from PIL import Image
im=cv2.imread('/root/.claude/uploads/68a3c0dc-e655-5ab0-9ff5-d5143994bef0/1a02e225-image.jpg');H,W=im.shape[:2]
pts=[]
for k in range(0,181,6):
    a=math.radians(180+k);pts.append((446+170*math.cos(a),480+44*math.sin(a)))
pts+=[(622,498),(638,525),(648,560),(650,620),(650,1000),(648,1100),(645,1120),(638,1140),(625,1158),(605,1172),(590,1185),(570,1200),(550,1214),(540,1218),(500,1225),(450,1226),(400,1222),(360,1216),(340,1209),(320,1201),(300,1190),(280,1173),(265,1157),(255,1145),(247,1125),(244,1100),(244,1000),(243,620),(248,560),(262,522),(276,498)]
poly=np.array(pts,np.int32)
pm=np.zeros((H,W),np.uint8);cv2.fillPoly(pm,[poly],1)
dil=cv2.dilate(pm,np.ones((9,9)));ero=cv2.erode(pm,np.ones((11,11)))
mask=np.full((H,W),cv2.GC_BGD,np.uint8);mask[dil>0]=cv2.GC_PR_BGD;mask[pm>0]=cv2.GC_PR_FGD;mask[ero>0]=cv2.GC_FGD
bg=np.zeros((1,65));fg=np.zeros((1,65))
cv2.grabCut(im,mask,None,bg,fg,6,cv2.GC_INIT_WITH_MASK)
m=((mask==1)|(mask==3))&(dil>0)|(ero>0)
m=nd.binary_fill_holes(nd.binary_opening(m,iterations=1))
m[1150:]=pm[1150:]>0
lab,n=nd.label(m);sz=nd.sum(m,lab,range(1,n+1));m=lab==(1+np.argmax(sz))
a=cv2.GaussianBlur(m.astype(np.float32),(0,0),1.0);a=np.clip((a-.5)*2+.5,0,1)
ys,xs=np.where(m);y0,y1,x0,x1=ys.min()-4,ys.max()+5,xs.min()-4,xs.max()+5
rgb=cv2.cvtColor(im,cv2.COLOR_BGR2RGB)[y0:y1,x0:x1]
Image.fromarray(np.dstack([rgb,(a[y0:y1,x0:x1]*255).astype(np.uint8)]),'RGBA').save('burger/soda.png')
print(x0,y0,x1,y1)
c=Image.new('RGBA',(1000,900),(230,57,70,255));s=Image.open('burger/soda.png');c.alpha_composite(s,(20,20))
b2=Image.new('RGBA',(500,900),(20,20,20,255));b2.alpha_composite(s.crop((0,0,500,900)) if s.width>500 else s,(0,0))
c.convert('RGB').save('pv_can.jpg')

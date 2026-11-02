import cv2,numpy as np,sys
f=sys.argv[1];BANDY=int(sys.argv[2]) if len(sys.argv)>2 else 0
im=cv2.imread(f'zefyr/{f}_raw.jpg');h,w=im.shape[:2];g=im.astype(np.float32)
yy,xx=np.mgrid[0:h,0:w];yy=yy/h;xx=xx/w
m=np.zeros((h,w),bool);b=60;m[:b]=1;m[-b:]=1;m[:,:b]=1;m[:,-b:]=1
A=np.stack([np.ones_like(xx),xx,yy,xx*xx,yy*yy,xx*yy],-1);bg=np.zeros_like(g)
for c in range(3):
    coef,*_=np.linalg.lstsq(A[m],g[...,c][m],rcond=None);bg[...,c]=A@coef
lum=g.mean(-1);bl=bg.mean(-1)
sat=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)[...,1].astype(np.float32)
gy=cv2.Sobel(cv2.GaussianBlur(lum,(0,0),1),cv2.CV_32F,0,1);gx=cv2.Sobel(cv2.GaussianBlur(lum,(0,0),1),cv2.CV_32F,1,0)
tex=cv2.GaussianBlur(np.hypot(gx,gy),(0,0),2)
seed=((lum>bl+7)|(sat>45)|(lum<120)|(tex>30)).astype(np.uint8)*255
np.save('/tmp/claude-0/x.npy',0) if False else None
seed=cv2.morphologyEx(seed,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
seed=cv2.morphologyEx(seed,cv2.MORPH_CLOSE,np.ones((21,21),np.uint8))
n,l,st,_=cv2.connectedComponentsWithStats(seed);big=1+np.argmax(st[1:,4]);a=np.where(l==big,255,0).astype(np.uint8)
# fill holes
ff=a.copy();msk=np.zeros((h+2,w+2),np.uint8);cv2.floodFill(ff,msk,(0,0),255);holes=(ff==0)
filled=a.copy();filled[holes]=255
# reopen bg-like holes in top 35% of bbox (pull loops)
x0,y0,bw,bh=cv2.boundingRect(a)
bglike=(np.abs(lum-bl)<6)&(sat<15)&(tex<8)
n,l,st,_=cv2.connectedComponentsWithStats(holes.astype(np.uint8))
for i in range(1,n):
    comp=l==i
    if st[i,1]<y0+bh*.35 and bglike[comp].mean()>.7: filled[comp]=0
a=filled
cv2.imwrite(f'zefyr/{f}_seed.png',a)
# grabcut refine boundary band
gc=np.full((h,w),cv2.GC_PR_BGD,np.uint8);gc[a>0]=cv2.GC_PR_FGD
k=np.ones((31,31),np.uint8);gc[cv2.erode(a,k)>0]=cv2.GC_FGD;gc[cv2.dilate(a,k)==0]=cv2.GC_BGD
bgm=np.zeros((1,65));fgm=np.zeros((1,65))
cv2.grabCut(im,gc,None,bgm,fgm,4,cv2.GC_INIT_WITH_MASK)
a2=np.where((gc==1)|(gc==3),255,0).astype(np.uint8)
n,l,st,_=cv2.connectedComponentsWithStats(a2);big=1+np.argmax(st[1:,4]);a2=np.where(l==big,255,0).astype(np.uint8)
# fill holes where seed said FG
ff=a2.copy();msk=np.zeros((h+2,w+2),np.uint8);cv2.floodFill(ff,msk,(0,0),255);hl=(ff==0)&(a>0);a2[hl]=255
# remove ground shadow below absolute row
if BANDY>0:
    band=np.zeros((h,w),bool);band[BANDY:]=True
    hue=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)[...,0]
    keep=~((sat<40)&(lum>90))
    a2[1200:]=0
    if f=='side':
        r=np.zeros((h,w),bool);r[1050:1130,1080:1262]=True;a2[r&(sat<40)&(lum>90)&(lum<228)]=0
    keep=cv2.morphologyEx(keep.astype(np.uint8),cv2.MORPH_OPEN,np.ones((5,5),np.uint8))>0
    a2[band&~keep]=0
# fill small holes not bg-like-in-top
ff=a2.copy();msk=np.zeros((h+2,w+2),np.uint8);cv2.floodFill(ff,msk,(0,0),255);hl=(ff==0)
n,l,st,_=cv2.connectedComponentsWithStats(hl.astype(np.uint8))
x0,y0,bw,bh=cv2.boundingRect(a2)
for i in range(1,n):
    comp=l==i
    if st[i,4]<8000 and not (st[i,1]<y0+bh*.35 and bglike[comp].mean()>.7): a2[comp]=255
a2=cv2.morphologyEx(a2,cv2.MORPH_OPEN,np.ones((7,7),np.uint8))
n,l,st,_=cv2.connectedComponentsWithStats(a2);big=1+np.argmax(st[1:,4]);a2=np.where(l==big,255,0).astype(np.uint8)
if f=='side':
    P=[(300,1030),(330,1040),(400,1110),(455,1124),(520,1158),(595,1172),(610,1191),(980,1191),(1037,1140),(1090,1112),(1100,1102),(1258,1102),(1270,1120),(1295,1146),(1310,1197),(1700,1199),(1745,1186),(1845,1151),(1929,1151),(2008,1125),(2092,1088),(2145,1057),(2215,1003),(2576,1000),(2576,1438),(0,1438),(0,1030)]
    cv2.fillPoly(a2,[np.array(P,np.int32)],0)
    for (bx0,by0,bx1,by1) in [(505,240,610,420),(990,200,1160,335)]:
        r=np.zeros((h,w),bool);r[by0:by1,bx0:bx1]=True
        a2[r&(sat<28)&(lum>bl-18)&(lum<bl+22)]=0
x0,y0,bw,bh=cv2.boundingRect(a2);tb=np.zeros((h,w),bool);tb[y0:int(y0+bh*.14)]=True;a2[tb&bglike]=0
af=cv2.GaussianBlur(a2,(0,0),1.0)
# decontaminate edge: pull edge colors away from bg
al=af[...,None]/255.;col=g.copy()
edge=(al>0.05)&(al<0.95)
col=np.where(edge,np.clip((g-bg*(1-al))/np.maximum(al,.3),0,255),g)
x,y,ww,hh=cv2.boundingRect(a2);pad=8;print('bbox',x,y,ww,hh)
out=np.dstack([col.astype(np.uint8),af])[max(0,y-pad):y+hh+pad,max(0,x-pad):x+ww+pad]
sc=1400/out.shape[1];o2=cv2.resize(out,None,fx=sc,fy=sc,interpolation=cv2.INTER_AREA)
cv2.imwrite(f'zefyr/{f}_cut.png',o2)
for nm,c in (('dk',(12,12,12)),('lm',(40,255,212))):
    al=o2[...,3:4]/255.;bc=np.zeros_like(o2[...,:3]);bc[:]=c
    cv2.imwrite(f'zefyr/prev_{f}_{nm}.jpg',(o2[...,:3]*al+bc*(1-al)).astype(np.uint8))
print(f,o2.shape)

import sys,os,numpy as np,cv2
U='/root/.claude/uploads/2257bdf4-1523-5b9a-994b-213b0d64e6c2/';OUT='/home/user/Edi-o-/fotos-editadas/'
F=['2a4ddf20','6f198d56','6fd27572','5241c8b8','747a3d98','133b1d5a','6136bc15','34b8f03c','0799194c']
rng=np.random.default_rng(1)
def grade(bgr):
    im=bgr.astype(np.float32)/255.
    # 1) igualar exposição (luminância média alvo, preservando céu)
    L=im@np.array([.114,.587,.299],np.float32);m=np.median(L);g=np.log(.42)/np.log(max(m,1e-3));g=np.clip(g,.8,1.25);im=im**g
    # 2) balanço levemente quente
    im[...,2]*=1.035;im[...,0]*=.965
    # 3) curva suave: preto levantado, realces com rolloff
    im=np.clip(im,0,1);im=.035+.93*(im*im*(3-2*im)*.35+im*.65);im=np.where(im>.85,.85+(im-.85)*.7,im)
    # 4) cor por matiz (HSV): verdes -> oliva, pele protegida
    hsv=cv2.cvtColor(np.clip(im,0,1).astype(np.float32),cv2.COLOR_BGR2HSV);H,S,V=hsv[...,0],hsv[...,1],hsv[...,2]   # H em graus 0-360
    gw=np.clip(1-np.abs(H-105)/55,0,1)            # verdes/amarelados
    H-=8*gw;S*=1-.22*gw;V*=1-.04*gw
    sw=np.clip(1-np.abs(H-25)/18,0,1)*(S>.15)      # pele
    S*=1+.04*sw
    S*=.94;hsv=np.stack([H%360,np.clip(S,0,1),V],-1);im=cv2.cvtColor(hsv.astype(np.float32),cv2.COLOR_HSV2BGR)
    # 5) split tone: sombras levemente frias, luzes quentes
    L=im@np.array([.114,.587,.299],np.float32);sh=np.clip(1-L/.45,0,1)[...,None];hi=np.clip((L-.6)/.4,0,1)[...,None]
    im+=sh*np.array([.018,.006,-.006],np.float32)+hi*np.array([-.02,.0,.018],np.float32)
    # 6) nitidez leve + grão fino + vinheta
    im=im.astype(np.float32);bl=cv2.GaussianBlur(im,(0,0),1.4);im=im+(im-bl)*.35
    h,w=im.shape[:2];yy,xx=np.mgrid[0:h,0:w].astype(np.float32);r=np.sqrt(((xx-w/2)/(w/2))**2+((yy-h/2)/(h/2))**2);im*=(1-.16*np.clip(r-.55,0,1)**1.5)[...,None]
    gr=cv2.GaussianBlur(rng.standard_normal((h,w)).astype(np.float32),(0,0),.7)*.022;im+=gr[...,None]
    return (np.clip(im,0,1)*255+.5).astype(np.uint8)
thumbs=[]
for i,f in enumerate(F,1):
    src=cv2.imread(U+f+'-image.jpg');o=grade(src);cv2.imwrite(OUT+f'foto_{i:02d}.jpg',o,[cv2.IMWRITE_JPEG_QUALITY,95])
    a=cv2.resize(src,(300,int(300*src.shape[0]/src.shape[1])));b=cv2.resize(o,a.shape[1::-1]);thumbs.append(np.vstack([a,b]))
hh=max(t.shape[0] for t in thumbs);thumbs=[cv2.copyMakeBorder(t,0,hh-t.shape[0],0,4,cv2.BORDER_CONSTANT) for t in thumbs]
cv2.imwrite(sys.argv[1],np.hstack(thumbs));print('ok')

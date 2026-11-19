import sys,numpy as np,cv2
U='/root/.claude/uploads/2257bdf4-1523-5b9a-994b-213b0d64e6c2/';OUT='/home/user/Edi-o-/fotos-editadas-v3/'
F=['2a4ddf20','6f198d56','6fd27572','5241c8b8','747a3d98','133b1d5a','6136bc15','34b8f03c','0799194c']
def grade(bgr):
    im=bgr.astype(np.float32)/255.
    L=im@np.array([.114,.587,.299],np.float32);m=np.median(L);g=np.clip(np.log(.45)/np.log(max(m,1e-3)),.85,1.15);im=im**g   # exposição levemente igualada
    pass                                                                                             # um pouco mais quente
    # contraste em S (sem levantar o preto)
    im=np.clip(im,0,1);s=im*im*(3-2*im);im=im*.55+s*.45
    # definição (contraste local) + nitidez fina
    big=cv2.GaussianBlur(im,(0,0),18);im=im+(im-big)*.12;fine=cv2.GaussianBlur(im,(0,0),.8);im=im+(im-fine)*.15
    # vibrância: mais nos tons pouco saturados, pele protegida; verdes frescos
    hsv=cv2.cvtColor(np.clip(im,0,1).astype(np.float32),cv2.COLOR_BGR2HSV);H,S_,V=hsv[...,0],hsv[...,1],hsv[...,2]
    skin=np.clip(1-np.abs(H-25)/20,0,1)*(S_>.12);green=np.clip(1-np.abs(H-100)/50,0,1)
    orange=np.clip(1-np.abs(H-30)/22,0,1);S_=S_+(1-S_)*S_*.35*(1-skin);S_*=1-.14*orange;S_*=1+.06*green;H=H-3*green                     # vibrância + verde fresco (levemente para o amarelo)
    hsv=np.stack([H%360,np.clip(S_,0,1),V],-1);im=cv2.cvtColor(hsv.astype(np.float32),cv2.COLOR_HSV2BGR)
    # céu: segura realces
    im=np.where(im>.9,.9+(im-.9)*.6,im)
    h,w=im.shape[:2];yy,xx=np.mgrid[0:h,0:w].astype(np.float32);r=np.sqrt(((xx-w/2)/(w/2))**2+((yy-h/2)/(h/2))**2);im*=(1-.07*np.clip(r-.6,0,1)**1.5)[...,None]
    return (np.clip(im,0,1)*255+.5).astype(np.uint8)
import os;os.makedirs(OUT,exist_ok=True);th=[]
for i,f in enumerate(F,1):
    src=cv2.imread(U+f+'-image.jpg');o=grade(src);cv2.imwrite(OUT+f'foto_{i:02d}.png',o,[cv2.IMWRITE_PNG_COMPRESSION,6])
    a=cv2.resize(src,(300,int(300*src.shape[0]/src.shape[1])));b=cv2.resize(o,a.shape[1::-1]);th.append(cv2.copyMakeBorder(np.vstack([a,b]),0,0,0,4,cv2.BORDER_CONSTANT))
cv2.imwrite(sys.argv[1],np.hstack(th));print('ok')

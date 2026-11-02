# Trilha + efeitos do vídeo 15 (Focinho). Gera trilha_final.mp3 e so_efeitos.mp3 (requer numpy, scipy, ffmpeg).
import numpy as np, wave, subprocess, os
from scipy.signal import fftconvolve, butter, sosfilt
SR=44100; D=34.0; n=int(SR*D); rng=np.random.default_rng(15)
M=np.zeros((n,2)); S=np.zeros((n,2)); HERE=os.path.dirname(os.path.abspath(__file__))
def tt(d): return np.arange(int(d*SR))/SR
def add(B,sig,at,g=1.0,pan=0.0):
    i=int(round(at*SR)); j=min(n,i+len(sig))
    if j<=i or i<0: return
    B[i:j,0]+=sig[:j-i]*g*(1-pan*.6); B[i:j,1]+=sig[:j-i]*g*(1+pan*.6)
def lpf(x,fc): return sosfilt(butter(2,fc,'low',fs=SR,output='sos'),x)
def hpf(x,fc): return sosfilt(butter(2,fc,'high',fs=SR,output='sos'),x)
def bpf(x,a,b): return sosfilt(butter(2,[a,b],'band',fs=SR,output='sos'),x)
mid=lambda m: 440*2**((m-69)/12)
def env(d,a=.005,r=.15): t=tt(d); return np.minimum(1,t/a)*np.clip((d-t)/r,0,1)
# instrumentos (uma frequência por nota — sem detune)
def uke(f,d=.4): t=tt(d); s=np.sin(2*np.pi*f*t)+.45*np.sin(4*np.pi*f*t)*np.exp(-t*9)+.2*np.sin(6*np.pi*f*t)*np.exp(-t*14); return s*np.exp(-t*7)*np.minimum(1,t/.002)*.06
def bell(f,d=.5): t=tt(d); return (np.sin(2*np.pi*f*t)+.25*np.sin(2*np.pi*4*f*t)*np.exp(-t*12))*np.exp(-t*6)*np.minimum(1,t/.002)*.05
def bass(f,d): t=tt(d); s=np.sin(2*np.pi*f*t)+.25*np.sin(4*np.pi*f*t); return lpf(s,700)*env(d,.01,.06)*.2
def pad(ms,d): t=tt(d); s=sum(np.sin(2*np.pi*mid(m)*t) for m in ms)/len(ms); return lpf(s,1500)*env(d,.3,.3)*.05
def kick(): t=tt(.3); return np.sin(2*np.pi*np.cumsum(50+110*np.exp(-t*40))/SR)*np.exp(-t*10)*.55
def clap():
    t=tt(.2); nz=bpf(rng.standard_normal(len(t)),1200,6000); e=sum(np.exp(-np.clip(t-d,0,None)*80)*(t>=d) for d in (0,.012,.024)); return nz*e*.14
def hat(o=False): d=.18 if o else .05; t=tt(d); return hpf(rng.standard_normal(len(t)),8000)*np.exp(-t*(15 if o else 60))*.05
def snapF(): t=tt(.08); return bpf(rng.standard_normal(len(t)),2000,7000)*np.exp(-t*60)*.08
# F | Dm | Bb | C   (I-vi-IV-V)
CH=[(41,[60,65,69]),(38,[62,65,69]),(46,[62,65,70]),(48,[60,64,67])]
MEL=[72,74,77,74, 76,74,72,69, 70,72,74,77, 76,72,74,72]  # gancho em colcheias por compasso (4 notas)
BEAT=.5; BAR=2.0
for b in range(int(D/BAR)):
    tb=b*BAR; root,ch=CH[b%4]; intro=tb<4; outro=tb>=32; brk=20<=tb<24
    add(M,pad([m+12 for m in ch],BAR),tb)
    if outro: add(M,uke(mid(ch[2]+12),1.8),tb,1.4); continue
    # ukulele: batida "ilha" (1, e-de-2, 3, e-de-3, 4)
    for st in (0,.75,1.0,1.25,1.5):
        for i,m in enumerate(ch): add(M,uke(mid(m)),tb+st+i*.008,1.0 if st in (0,1.0) else .7,pan=-.3+i*.3)
    if intro:
        for q in range(4): add(M,snapF(),tb+q*BEAT+BEAT if q%2 else tb+q*BEAT+BEAT,.6)
        continue
    add(M,bass(mid(root),.45),tb); add(M,bass(mid(root),.2),tb+.75,.8); add(M,bass(mid(root+12),.2),tb+1.0,.7); add(M,bass(mid(root+7),.4),tb+1.5,.8)
    for q in range(4):
        tq=tb+q*BEAT
        if not brk or q==0: add(M,kick(),tq)
        if q in (1,3): add(M,clap(),tq)
        add(M,hat(),tq+BEAT/2,1,pan=.3); add(M,hat(),tq,.5,pan=-.3)
    if not brk:
        k=(b%4)*4
        for i in range(4): add(M,bell(mid(MEL[k+i])),tb+i*BEAT,1.0,pan=.15)
# ---------- efeitos (níveis: soft < med < big; mínimo 0,45s entre eles) ----------
def whoosh(d=.5): t=tt(d); return bpf(rng.standard_normal(len(t)),500,4000)*np.sin(np.pi*t/d)**2*.05
def popS(g=1): t=tt(.12); f=480*(1+1.4*np.exp(-t*45)); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*28)*.07*g
def tick(): t=tt(.08); return np.sin(2*np.pi*1500*t)*np.exp(-t*60)*.035
def bubbles():
    o=np.zeros(int(.6*SR))
    for k,(d,f) in enumerate([(0,700),(.12,950),(.22,820),(.36,1100)]):
        t=tt(.1); s=np.sin(2*np.pi*np.cumsum(f*(1+1.5*t/.1))/SR)*np.exp(-t*40)*.045; i=int(d*SR); o[i:i+len(s)]+=s
    return o
def boing(): t=tt(.45); f=180+140*np.sin(2*np.pi*7*t)*np.exp(-t*5); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*6)*.08
def chime(): return bell(mid(84),.9)*1.2+np.pad(bell(mid(89),.9)*1.0,(int(.08*SR),0))[:int(.9*SR)]
def BIG(): t=tt(1.0); return (np.sin(2*np.pi*mid(77)*t)+.6*np.sin(2*np.pi*mid(84)*t))*np.exp(-t*3.5)*np.minimum(1,t/.003)*.07
def cash():
    t=tt(.7); return (np.sin(2*np.pi*mid(88)*t)*np.exp(-t*7)+.6*np.sin(2*np.pi*mid(93)*t)*np.exp(-np.clip(t-.07,0,None)*7)*(t>.07))*.06
def scratch(): t=tt(.3); return bpf(rng.standard_normal(len(t)),900,3000)*np.sin(np.pi*t/.3)*.05
def horn():
    t=tt(.5); s=np.sin(2*np.pi*mid(69)*t)+np.sin(2*np.pi*mid(73)*t)*.0; s=np.sign(s)*np.abs(s)**.6; return lpf(s,2200)*env(.5,.01,.08)*.045
ev=[(0.4,popS(.7)),(0.9,popS(.8)),(1.4,whoosh(.4)),(2.3,boing()),
    (4.0,whoosh()),(4.5,popS()),(5.05,tick()),(5.6,chime()),
    (8.0,whoosh()),(8.5,popS()),(9.3,bubbles()),(11.0,tick()),(11.5,tick()),(12.3,bubbles()),
    (14.0,whoosh()),(14.5,popS(.8)),(15.0,popS(.8)),(15.5,popS(.8)),(16.0,popS(.8)),(17.0,tick()),
    (20.0,whoosh()),(20.5,BIG()),(21.0,BIG()),(22.0,scratch()),(22.45,cash()),(23.0,tick()),
    (24.0,whoosh()),(24.5,popS()),(25.4,horn()),(27.1,whoosh(.7)),
    (28.0,whoosh()),(28.6,tick()),(29.6,popS(.6)),(30.2,popS(.6)),(30.8,BIG()),(31.3,chime()),(31.8,boing())]
last=-9
for t,sig in ev:
    if t-last<0.45: continue
    add(S,sig,t); last=t
it=tt(1.0); ir=rng.standard_normal(len(it))*np.exp(-it*6); ir=lpf(ir,6000); ir/=np.sqrt((ir**2).sum())
wet=np.stack([fftconvolve(M[:,0],ir)[:n],fftconvolve(M[:,1],ir)[:n]],1)
fade=np.ones(n); fo=int(.8*SR); fade[-fo:]=np.linspace(1,0,fo)
def save(B,name):
    B=B*fade[:,None]; B=B/np.max(np.abs(B))*.89; w=os.path.join(HERE,name+'.wav')
    with wave.open(w,'wb') as f: f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((B*32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',w,'-b:a','192k',os.path.join(HERE,name+'.mp3')],check=True); os.remove(w)
save(M*.9+wet*.12+S*1.1,'trilha_final'); save(S,'so_efeitos')
print('ok')

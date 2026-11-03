# Trilha deep house elegante (120bpm) + efeitos do vídeo 19 (NOCTÉA). Gera trilha_final.mp3 e so_efeitos.mp3.
import numpy as np, wave, subprocess, os
from scipy.signal import fftconvolve, butter, sosfilt
SR=44100; BT=.5; ST=BT/4; D=38.0; n=int(SR*D); rng=np.random.default_rng(19); HERE=os.path.dirname(os.path.abspath(__file__))
def tt(d): return np.arange(int(d*SR))/SR
def buf(): return np.zeros(n)
def add(B,s,at,g=1.0):
    i=int(round(at*SR)); j=min(n,i+len(s))
    if j>i>=0: B[i:j]+=s[:j-i]*g
def lpf(x,fc): return sosfilt(butter(2,fc,'low',fs=SR,output='sos'),x)
def hpf(x,fc): return sosfilt(butter(2,fc,'high',fs=SR,output='sos'),x)
def bpf(x,a,c): return sosfilt(butter(2,[a,c],'band',fs=SR,output='sos'),x)
mid=lambda m:440*2**((m-69)/12)
def env(d,a=.005,r=.2): t=tt(d); return np.minimum(1,t/a)*np.clip((d-t)/r,0,1)
def sec(t):
    if t<8: return 'intro'
    if 20<=t<24: return 'break'
    if t>=33: return 'outro'
    return 'groove'
# Dm9 – Bbmaj7 – Fmaj7 – C(add9)   (melancólico e sofisticado)
CH=[(38,[62,65,69,72,76]),(34,[58,62,65,69]),(41,[60,65,69,72]),(36,[60,64,67,74])]
def rhodes(f,d,v=1): t=tt(d); s=np.sin(2*np.pi*f*t+.6*np.sin(2*np.pi*f*t)*np.exp(-t*3))*np.exp(-t*1.4)+.15*np.sin(2*np.pi*4*f*t)*np.exp(-t*6); return s*env(d,.004,.3)*.045*v
def bell(f,d=1.6,v=1): t=tt(d); return (np.sin(2*np.pi*f*t)+.3*np.sin(2*np.pi*2.76*f*t)*np.exp(-t*4))*np.exp(-t*2.2)*np.minimum(1,t/.002)*.03*v
def pad(ms,d): t=tt(d); s=sum(np.sin(2*np.pi*mid(m)*t) for m in ms)/len(ms); return lpf(s,1100)*env(d,1.0,1.0)*.06
def sub(f,d): t=tt(d); return np.sin(2*np.pi*f*t)*env(d,.01,.08)*.2
def kick(): t=tt(.35); return np.sin(2*np.pi*np.cumsum(48+90*np.exp(-t*32))/SR)*np.exp(-t*8)*.5
def rim(): t=tt(.06); return (np.sin(2*np.pi*780*t)+.4*np.sin(2*np.pi*1600*t))*np.exp(-t*80)*.03
def shaker(v=1): t=tt(.07); return hpf(rng.standard_normal(len(t)),7000)*np.sin(np.pi*t/.07)**2*.03*v
def hat(): t=tt(.2); return hpf(rng.standard_normal(len(t)),8000)*np.exp(-t*16)*.03
def clap(): t=tt(.25); nz=bpf(rng.standard_normal(len(t)),1200,6000); e=sum(np.exp(-np.clip(t-d,0,None)*70)*(t>=d) for d in (0,.012,.024)); return nz*e*.07
M=buf(); K=buf(); kicks=[]
for bar in range(int(D/2)):
    tb=bar*2.0; root,ch=CH[bar%4]; s=sec(tb)
    add(M,pad([m+12 for m in ch[:3]],2.2),tb,1.4 if s in('intro','break','outro') else .8)
    if s=='outro' and tb>=36: continue
    # rhodes: comp sincopado
    for st,v in ([(0,1),(1.25,.6)] if s!='intro' else [(0,.8)]):
        for i,m in enumerate(ch): add(M,rhodes(mid(m),1.2,v),tb+st+i*.012)
    if s in('intro','break','outro'):
        arp=[ch[0]+12,ch[2]+12,ch[1]+12,ch[3]+12]
        for k in range(4): add(M,bell(mid(arp[k%len(arp)]+12),v=.8),tb+k*.5)
        add(M,sub(mid(root),2.0),tb,.6); continue
    add(M,sub(mid(root),.9),tb); add(M,sub(mid(root),.4),tb+1.25,.8); add(M,sub(mid(root+12),.2),tb+1.75,.5)
    for q in range(4):
        tq=tb+q*BT; add(K,kick(),tq); kicks.append(tq)
        if q in(1,3): add(M,clap(),tq)
        add(M,hat(),tq+BT/2)
        for h in range(4): add(M,shaker(.9 if h==2 else .5),tq+h*ST)
        if q==2: add(M,rim(),tq+3*ST)
    if bar%2==1: add(M,bell(mid(ch[-1]+12),v=.7),tb+1.75)
# sidechain
SC=np.ones(n); tn=np.arange(n)/SR
for k in kicks:
    i=int(k*SR); j=min(n,i+int(.28*SR)); SC[i:j]=np.minimum(SC[i:j],1-.45*np.exp(-(tn[i:j]-k)/.1))
# ---------------- efeitos ----------------
S=buf()
def shimmer(g=1): t=tt(2.0); return sum(np.sin(2*np.pi*mid(m)*t)*np.exp(-t*(2+i*.4))*np.minimum(1,np.clip(t-i*.07,0,None)/.004) for i,m in enumerate([86,93,98,105]))*.012*g
def twinkle(): t=tt(.5); return np.sin(2*np.pi*mid(100)*t)*np.exp(-t*9)*.012
def air(d=1.2,g=1): t=tt(d); return bpf(rng.standard_normal(len(t)),400,3500)*np.sin(np.pi*t/d)**2*.035*g
def glass(): t=tt(1.2); return (np.sin(2*np.pi*2350*t)*np.exp(-t*5)+.5*np.sin(2*np.pi*3710*t)*np.exp(-t*7)+.3*np.sin(2*np.pi*5600*t)*np.exp(-t*11))*.03
def boom(): t=tt(2.5); return (np.sin(2*np.pi*np.cumsum(40+50*np.exp(-t*4))/SR)*np.exp(-t*1.6)+lpf(rng.standard_normal(len(t)),900)*np.exp(-t*3)*.2)*.2
def swell(d): t=tt(d); return lpf(rng.standard_normal(len(t)),2500)*(t/d)**2.5*.05
ev=[(.3,air(1.6,.8)),(1.2,twinkle()),(2.1,twinkle()),(3.0,shimmer(.8)),(3.9,air()),(5.2,twinkle()),(7.9,air(1.2,1.2)),(8.6,shimmer(.7)),
    (9.7,twinkle()),(12.0,glass()),(13.9,air()),(15.0,twinkle()),(15.6,twinkle()),(16.2,twinkle()),(16.8,twinkle()),(17.5,shimmer(.6)),
    (19.9,air(1.4,1.1)),(20.6,bell(mid(88),2,1.2)),(21.8,bell(mid(91),2,1.2)),(23.9,air()),(24.9,shimmer(.8)),(27.9,air()),
    (28.4,twinkle()),(29.6,boom()),(30.1,shimmer(1.2)),(32.9,air()),(35.4,twinkle()),(36.1,shimmer(.7))]
last=-9
for t,s in sorted(ev,key=lambda e:e[0]):
    if t-last<.45: continue
    add(S,s,t); last=t
add(S,swell(1.9),6.1); add(S,swell(1.5),27.9)
# ---------------- mix ----------------
def rev(x,dec=2.0,l=2.6,fc=5000):
    it=tt(l); ir=rng.standard_normal(len(it))*np.exp(-it*dec); ir=lpf(ir,fc); ir/=np.sqrt((ir**2).sum()); return fftconvolve(x,ir)[:n]
music=K+M*SC+rev(M,1.8,3,4500)*.35
fx=S+rev(S,1.5,3,6000)*.45
fade=np.ones(n); fo=int(1.2*SR); fade[-fo:]=np.linspace(1,0,fo)
def save(B,name):
    B=hpf(B,30); B=np.tanh(B*1.2)/1.2*fade; B=B/np.max(np.abs(B))*.89; L=B.copy(); R=B.copy()
    hi=hpf(B,2500)*.15; L+=np.roll(hi,int(.013*SR)); R-=np.roll(hi,int(.013*SR)); St=np.stack([L,R],1); St/=np.max(np.abs(St))/.89
    w=os.path.join(HERE,name+'.wav')
    with wave.open(w,'wb') as f: f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((St*32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',w,'-b:a','256k',os.path.join(HERE,name+'.mp3')],check=True); os.remove(w)
save(music*.9+fx*1.2,'trilha_final'); save(fx,'so_efeitos'); print('ok')

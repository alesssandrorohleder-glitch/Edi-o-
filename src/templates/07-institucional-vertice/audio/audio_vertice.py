import numpy as np, wave
from scipy.signal import fftconvolve, butter, sosfilt
SR=44100; D=34.0; n=int(SR*D); rng=np.random.default_rng(12)
M=np.zeros((n,2)); S=np.zeros((n,2))
def tt(d): return np.arange(int(d*SR))/SR
def add(B,sig,at,g=1.0,pan=0.0):
    i=int(round(at*SR)); j=min(n,i+len(sig))
    if j<=i or i<0: return
    B[i:j,0]+=sig[:j-i]*g*(1-pan*.6); B[i:j,1]+=sig[:j-i]*g*(1+pan*.6)
def lpf(x,fc): return sosfilt(butter(2,fc,'low',fs=SR,output='sos'),x)
def hpf(x,fc): return sosfilt(butter(2,fc,'high',fs=SR,output='sos'),x)
def bpf(x,a,b): return sosfilt(butter(2,[a,b],'band',fs=SR,output='sos'),x)
mid=lambda m: 440*2**((m-69)/12)
def env(d,a=.005,r=.2): t=tt(d); return np.minimum(1,t/a)*np.clip((d-t)/r,0,1)
def piano(f,d,v=1.0): t=tt(d); s=np.sin(2*np.pi*f*t)*np.exp(-t*2.2)+.3*np.sin(2*np.pi*2*f*t)*np.exp(-t*3.5)+.1*np.sin(2*np.pi*3*f*t)*np.exp(-t*5); return s*env(d)*.15*v
def pluck(f,d=.3): t=tt(d); s=np.sin(2*np.pi*f*t)+.3*np.sin(2*np.pi*2*f*t); return s*np.exp(-t*12)*np.minimum(1,t/.002)*.07
def pad(ms,d): t=tt(d); s=sum(np.sin(2*np.pi*mid(m)*t) for m in ms)/len(ms); return lpf(s,1800)*env(d,.4,.4)*.07
def sub(f,d): t=tt(d); return np.sin(2*np.pi*f*t)*env(d,.05,.2)*.2
def kick(): t=tt(.35); return np.sin(2*np.pi*np.cumsum(48+90*np.exp(-t*35))/SR)*np.exp(-t*9)*.6
def clap():
    t=tt(.22); nz=bpf(rng.standard_normal(len(t)),1200,5000); e=sum(np.exp(-np.clip(t-d,0,None)*70)*(t>=d) for d in (0,.01,.02))+np.exp(-t*18)*.4; return nz*e*.16
def shaker(): t=tt(.06); return hpf(rng.standard_normal(len(t)),7000)*np.sin(np.pi*t/.06)**2*.045
# F | C | Dm | Bb
CH=[(41,[57,60,65]),(48,[55,60,64]),(38,[57,62,65]),(46,[58,62,65])]
BEAT=.5;BAR=2.0
for b in range(int(D/BAR)):
    tb=b*BAR; root,ch=CH[b%4]; intro=tb<4; end=tb>=32
    add(M,pad([m+12 for m in ch],BAR),tb)
    add(M,sub(mid(root),BAR),tb,.6 if intro else 1)
    for i,m in enumerate(ch): add(M,piano(mid(m),BAR),tb+i*.02,1,pan=-.2+i*.2)
    if end: continue
    arp=[ch[0]+12,ch[1]+12,ch[2]+12,ch[1]+12]
    for k in range(8): add(M,pluck(mid(arp[k%4]+(12 if k>=4 else 0))),tb+k*BEAT/2,1 if not intro else .7,pan=(-.35 if k%2 else .35))
    if not intro:
        for q in range(4):
            tq=tb+q*BEAT
            if q in (0,2): add(M,kick(),tq)
            if q in (1,3): add(M,clap(),tq)
            for h in range(2): add(M,shaker(),tq+h*BEAT/2,1 if h else .5,pan=.3)
add(M,piano(mid(65),1.8),33.0); add(M,piano(mid(69),1.8),33.0)
def S_(): t=tt(.12); f=mid(CH[0][1][2]+24); return np.sin(2*np.pi*1760*t)*np.exp(-t*40)*.035
def MED(f=1046.5): t=tt(.5); return (np.sin(2*np.pi*f*t)+.2*np.sin(4*np.pi*f*t))*np.exp(-t*8)*np.minimum(1,t/.003)*.05
def BIG(f1=1046.5,f2=1568): t=tt(1.0); return (np.sin(2*np.pi*f1*t)+.6*np.sin(2*np.pi*f2*t))*np.exp(-t*3.5)*np.minimum(1,t/.003)*.065
def whoosh(d=.6): t=tt(d); return bpf(rng.standard_normal(len(t)),400,3000)*np.sin(np.pi*t/d)**2*.045
def popS(): t=tt(.12); f=520*(1+1.2*np.exp(-t*50)); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*30)*.07
def plink(): t=tt(.6); return (np.sin(2*np.pi*1318.5*t)*np.exp(-t*7)+.4*np.sin(2*np.pi*1975.5*t)*np.exp(-t*10))*.06
ev=[(0.3,whoosh(.8)),(1.5,MED(880)),(2.0,MED(1046.5)),(2.5,S_()),
    (4.1,whoosh()),(5.2,BIG(1046.5,1568)),(6.2,S_()),
    (8.1,MED(880)),(8.6,whoosh(.8)),(10.6,popS()),(11.6,MED(1318.5)),
    (14.1,MED(880)),(14.5,popS()),(15.0,popS()),(15.5,popS()),(16.0,popS()),
    (20.1,MED(880)),(21.0,plink()),(21.5,popS()),(22.2,MED(1046.5)),
    (24.1,S_()),(24.6,MED(1046.5)),(25.6,BIG(1046.5,1568)),
    (28.2,S_()),(28.9,MED(1046.5)),(29.8,popS()),(31.0,BIG(1046.5,1568)),(31.5,MED(1318.5))]
last=-9
for t,sig in ev:
    if t-last<0.45: continue
    add(S,sig,t); last=t
it=tt(1.2); ir=rng.standard_normal(len(it))*np.exp(-it*5); ir=lpf(ir,6000); ir/=np.sqrt((ir**2).sum())
wet=np.stack([fftconvolve(M[:,0],ir)[:n],fftconvolve(M[:,1],ir)[:n]],1)
out=M*.9+wet*.12+S*1.1
t=np.arange(n)/SR; out*=np.clip((D-t)/1.2,0,1)[:,None]
out=np.tanh(out/np.abs(out).max()*1.4)/np.tanh(1.4)*.92
w=wave.open('audio_vertice.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out.reshape(-1)*32767).astype(np.int16).tobytes()); w.close(); print('ok')

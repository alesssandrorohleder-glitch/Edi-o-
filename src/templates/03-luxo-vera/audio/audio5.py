import numpy as np, wave
from scipy.signal import fftconvolve, butter, sosfilt
SR=44100; D=36.0; n=int(SR*D); rng=np.random.default_rng(3)
M=np.zeros((n,2)); S=np.zeros((n,2))
def tt(d): return np.arange(int(d*SR))/SR
def add(B,sig,at,g=1.0,pan=0.0):
    i=int(round(at*SR)); j=min(n,i+len(sig))
    if j<=i or i<0: return
    B[i:j,0]+=sig[:j-i]*g*(1-pan*.6); B[i:j,1]+=sig[:j-i]*g*(1+pan*.6)
def lpf(x,fc): return sosfilt(butter(2,fc,'low',fs=SR,output='sos'),x)
def hpf(x,fc): return sosfilt(butter(2,fc,'high',fs=SR,output='sos'),x)
mid=lambda m: 440*2**((m-69)/12)
def env(d,a=.01,r=.3): t=tt(d); return np.minimum(1,t/a)*np.clip((d-t)/r,0,1)
def piano(f,d,v=1.0):  # clean harmonic tone, no detune
    t=tt(d); s=np.sin(2*np.pi*f*t)*np.exp(-t*1.8)+.35*np.sin(2*np.pi*2*f*t)*np.exp(-t*3)+.12*np.sin(2*np.pi*3*f*t)*np.exp(-t*5)
    return s*env(d,.005,.25)*.16*v
def pad(fs,d): t=tt(d); s=sum(np.sin(2*np.pi*f*t) for f in fs)/len(fs); return lpf(s,1500)*env(d,.6,.6)*.09
def sub(f,d): t=tt(d); return np.sin(2*np.pi*f*t)*env(d,.08,.4)*.20
def kick(): t=tt(.5); return np.sin(2*np.pi*np.cumsum(45+55*np.exp(-t*25))/SR)*np.exp(-t*7)*.45
def shaker(): t=tt(.07); return hpf(rng.standard_normal(len(t)),7000)*np.sin(np.pi*t/.07)**2*.05
# C  Am  F  G  (triads, one chord per 3s bar)
CH=[[48,52,55],[45,48,52],[41,45,48],[43,47,50]]
bar=3.0; beat=.75
for b in range(12):
    tb=b*bar; c=CH[b%4]; brk=8<=b<10
    add(M,pad([mid(m+12) for m in c],bar),tb)
    add(M,sub(mid(c[0]-12 if c[0]>44 else c[0]),bar),tb,.8 if brk else 1)
    for i,m in enumerate(c): add(M,piano(mid(m+12),bar),tb,.8,pan=-.2+i*.2)
    arp=[c[0]+24,c[1]+24,c[2]+24,c[1]+24]
    for k in range(4):
        if brk and k%2: continue
        add(M,piano(mid(arp[k]),beat*1.0,.7),tb+k*beat,1,pan=(.3 if k%2 else -.3))
    if 2<=b<11 and not brk:
        for q in (0,2): add(M,kick(),tb+q*beat,.9)
        for q in range(8): add(M,shaker(),tb+q*beat/2,1 if q%2 else .5)
# ---- sfx: ONE sound per event, in key, never overlapping ----
def chord_at(t): return CH[int(t//bar)%4]
def SMALLs(t): f=mid(chord_at(t)[2]+36); x=tt(.12); return np.sin(2*np.pi*f*x)*np.exp(-x*40)*.035
def MEDs(t): f=mid(chord_at(t)[0]+36); x=tt(.9); return (np.sin(2*np.pi*f*x)+.2*np.sin(2*np.pi*2*f*x))*np.exp(-x*5)*np.minimum(1,x/.004)*.06
def BIGs(t):
    c=chord_at(t); x=tt(1.4); f1=mid(c[0]+24); f2=mid(c[2]+24)
    s=(np.sin(2*np.pi*f1*x)+.6*np.sin(2*np.pi*f2*x)+.15*np.sin(2*np.pi*2*f1*x))*np.exp(-x*2.8)*np.minimum(1,x/.004)
    return s*.08+np.sin(2*np.pi*mid(c[0])*x)*np.exp(-x*4)*.06
ev=[(0.8,'M'),(1.3,'S'),(2.6,'M'),(3.4,'B'),(7.6,'B'),(8.5,'M'),(9.5,'S'),(13.7,'B'),(14.3,'S'),(15.5,'S'),
    (18.6,'S'),(19.1,'B'),(19.7,'M'),(21.0,'M'),(21.6,'S'),(24.5,'M'),(26.95,'M'),(28.0,'B'),
    (30.35,'M'),(30.9,'B'),(31.8,'S'),(32.3,'S'),(32.8,'M'),(33.4,'M')]
last=-9; used=[]
for t,k in ev:
    if t-last<0.45: continue
    add(S,{'S':SMALLs,'M':MEDs,'B':BIGs}[k](t),t); last=t; used.append((t,k))
print(len(used),'sfx')
# gentle reverb on music only (same IR both sides)
it=tt(1.8); ir=rng.standard_normal(len(it))*np.exp(-it*3.5); ir=lpf(ir,5000); ir/=np.sqrt((ir**2).sum())
wet=np.stack([fftconvolve(M[:,0],ir)[:n],fftconvolve(M[:,1],ir)[:n]],1)
out=M*.85+wet*.18+S
t=np.arange(n)/SR; out*=np.clip((D-t)/1.8,0,1)[:,None]*np.clip(t/.3,0,1)[:,None]
out=out/np.abs(out).max()*.9
w=wave.open('audio_vera2.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out.reshape(-1)*32767).astype(np.int16).tobytes()); w.close(); print('ok')

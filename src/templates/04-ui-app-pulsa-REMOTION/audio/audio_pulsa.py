import numpy as np, wave
from scipy.signal import fftconvolve, butter, sosfilt
SR=44100; D=32.0; n=int(SR*D); rng=np.random.default_rng(21)
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
BEAT=.5; BAR=2.0
def kick(): t=tt(.4); f=50+160*np.exp(-t*40); return np.tanh(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*8)*1.7)*.8
def clap():
    t=tt(.3); nz=bpf(rng.standard_normal(len(t)),1000,5000); e=sum(np.exp(-np.clip(t-d,0,None)*60)*(t>=d) for d in (0,.01,.02))+np.exp(-t*15)*.5
    return nz*e*.26
def hat(o=False): t=tt(.18 if o else .04); return hpf(rng.standard_normal(len(t)),8000)*np.exp(-t*(13 if o else 80))*(.12 if o else .07)
def organ(f,d): t=tt(d); s=np.sin(2*np.pi*f*t)+.45*np.sin(2*np.pi*2*f*t)+.2*np.sin(2*np.pi*3*f*t); return s*np.exp(-t*6)*np.minimum(1,t/.003)*np.clip((d-t)/.02,0,1)
def stab(ms,d=.3): return sum(organ(mid(m),d) for m in ms)/len(ms)*.17
def bass(f,d): t=tt(d); s=np.tanh((np.sin(2*np.pi*f*t)+.25*np.sin(2*np.pi*2*f*t))*1.3); return s*np.minimum(1,t/.004)*np.clip((d-t)/.015,0,1)*.28
def pluck(f,d=.3): t=tt(d); s=np.sin(2*np.pi*f*t)+.35*np.sin(2*np.pi*2*f*t); return s*np.exp(-t*11)*np.minimum(1,t/.002)*.08
# C | G | Am | F
CH=[(48,[60,64,67,72]),(43,[59,62,67,71]),(45,[60,64,69,72]),(41,[60,65,69,72])]
HOOK=[84,79,76,79, 81,79,76,74]
side=np.ones(n)
for b in range(int(D/BAR)):
    tb=b*BAR; root,ch=CH[b%4]; intro=tb<2; end=tb>=30
    for pos in (0,1.5,2.5,3.0):
        if end and pos>0: continue
        add(M,stab(ch,.9 if end else .3),tb+pos*BEAT,.75 if intro else 1,pan=.15)
    if intro or end:
        if end: add(M,bass(mid(root),.9),tb,1); add(M,kick(),tb,.9)
        continue
    for q in range(4):
        tq=tb+q*BEAT; add(M,kick(),tq,.85)
        i=int(tq*SR); seg=1-.5*np.exp(-np.arange(int(.28*SR))/SR*12); k=min(len(seg),n-i); side[i:i+k]=np.minimum(side[i:i+k],seg[:k])
        if q%2: add(M,clap(),tq)
        add(M,hat(True),tq+BEAT/2,1,pan=.25); add(M,hat(),tq+BEAT/4,.8,pan=-.3); add(M,hat(),tq+3*BEAT/4,.8,pan=-.3)
        add(M,bass(mid(root)*(2 if q==3 else 1),BEAT/2*.85),tq+BEAT/2)
    if 8<=tb<26:
        for k in range(8):
            if k in (0,1,2,4,6): add(M,pluck(mid(HOOK[k]+(0 if b%2 else -2))),tb+k*BEAT/2,1,pan=(-.3 if k%2 else .3))
M*=side[:,None]
# --- sfx: tiered, one per event, >=0.45s apart
def tap(): x=tt(.06); return (np.sin(2*np.pi*1800*x)*np.exp(-x*90)+hpf(rng.standard_normal(len(x)),3000)*np.exp(-x*300)*.3)*.10
def soft(f=1568): x=tt(.5); return (np.sin(2*np.pi*f*x)+.2*np.sin(4*np.pi*f*x))*np.exp(-x*8)*np.minimum(1,x/.003)*.05
def whoosh(d=.45): x=tt(d); return bpf(rng.standard_normal(len(x)),400,3000)*np.sin(np.pi*x/d)**2*.06
def big(f1=1046.5,f2=1568): x=tt(1.0); return (np.sin(2*np.pi*f1*x)+.6*np.sin(2*np.pi*f2*x))*np.exp(-x*3.5)*np.minimum(1,x/.003)*.07
def notif(): o=np.zeros(int(.8*SR)); a=soft(1568); b=soft(2093); o[:len(a)]+=a*1.3; j=int(.11*SR); o[j:j+len(b)]+=b[:len(o)-j]*1.3; return o
ev=[(0.15,whoosh(.5)),(0.5,big(1046.5,1568)),(3.1,soft(1318.5)),(4.8,soft(1568)),
    (9.93,tap()),(11.5,soft(1318.5)),(15.6,tap()),(17.07,tap()),(17.87,tap()),(18.87,tap()),(19.93,tap()),
    (20.9,big(1046.5,1318.5)),(23.27,notif()),(25.0,whoosh(.6)),
    (27.07,soft(1046.5)),(27.8,soft(1318.5)),(28.73,soft(1568)),(30.2,big(1046.5,1568))]
last=-9
for t,sig in ev:
    if t-last<0.45: continue
    add(S,sig,t); last=t
it=tt(1.0); ir=rng.standard_normal(len(it))*np.exp(-it*6); ir=lpf(ir,6000); ir/=np.sqrt((ir**2).sum())
wet=np.stack([fftconvolve(M[:,0],ir)[:n],fftconvolve(M[:,1],ir)[:n]],1)
out=M*.9+wet*.1+S*1.1
t=np.arange(n)/SR; out*=np.clip((D-t)/1.0,0,1)[:,None]
out=np.tanh(out/np.abs(out).max()*1.5)/np.tanh(1.5)*.92
w=wave.open('pulsa-audio.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out.reshape(-1)*32767).astype(np.int16).tobytes()); w.close(); print('ok')

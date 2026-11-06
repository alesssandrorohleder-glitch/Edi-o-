import numpy as np, wave
from scipy.signal import fftconvolve, butter, sosfilt
SR=44100; D=34.0; n=int(SR*D); rng=np.random.default_rng(31)
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
BEAT=.5;BAR=2.0;ST=BEAT/4
def kick(): t=tt(.4); return np.tanh(np.sin(2*np.pi*np.cumsum(48+150*np.exp(-t*40))/SR)*np.exp(-t*8)*1.7)*.75
def clap():
    t=tt(.25); nz=bpf(rng.standard_normal(len(t)),1100,5000); e=sum(np.exp(-np.clip(t-d,0,None)*70)*(t>=d) for d in (0,.01,.02))+np.exp(-t*16)*.4; return nz*e*.2
def ohat(): t=tt(.18); return hpf(rng.standard_normal(len(t)),8000)*np.exp(-t*14)*.10
def pandeiro(acc=False): t=tt(.09); j=hpf(rng.standard_normal(len(t)),6000)*np.exp(-t*40); s=np.sin(2*np.pi*np.cumsum(220+80*np.exp(-t*60))/SR)*np.exp(-t*45)*(.5 if acc else 0); return (j*.12+s*.25)
def agogo(hi=True): t=tt(.2); f=1320 if hi else 990; return (np.sin(2*np.pi*f*t)+.4*np.sin(2*np.pi*f*2.7*t))*np.exp(-t*18)*.06
def surdo(): t=tt(.6); return np.sin(2*np.pi*np.cumsum(55+30*np.exp(-t*20))/SR)*np.exp(-t*5)*.4
def nylon(f,d=.8):
    t=tt(d);s=sum(g*np.sin(2*np.pi*f*k*t)*np.exp(-t*dc) for k,(g,dc) in enumerate([(1,3.5),(.5,5),(.28,7),(.14,10)],1))
    return (s+lpf(rng.standard_normal(len(t)),f*4)*np.exp(-t*120)*.25)*np.minimum(1,t/.002)*np.clip((d-t)/.05,0,1)*.07
def strum(ms,d=.35): o=np.zeros(int((d+.1)*SR))
def chord(ms,d=.35):
    o=np.zeros(int((d+.1)*SR))
    for i,m in enumerate(ms): s=nylon(mid(m),d);j=int(i*.01*SR);o[j:j+len(s)]+=s[:len(o)-j]
    return o
def bass(f,d): t=tt(d); s=np.tanh((np.sin(2*np.pi*f*t)+.3*np.sin(2*np.pi*2*f*t))*1.3); return lpf(s,900)*np.minimum(1,t/.004)*np.clip((d-t)/.02,0,1)*.30
def pluck(f,d=.25): t=tt(d); s=np.sin(2*np.pi*f*t)+.3*np.sin(2*np.pi*2*f*t); return s*np.exp(-t*12)*np.minimum(1,t/.002)*.07
CH=[(38,[53,57,60,64]),(43,[53,59,62,64]),(36,[52,55,59,62]),(33,[55,61,64,69])]
RIFF=[76,74,72,69,72,74,76,79]
side=np.ones(n)
for b in range(int(D/BAR)):
    tb=b*BAR; root,ch=CH[b%4]; intro=tb<4; brk=24<=tb<28; end=tb>=32
    if end: add(M,chord([52,55,59,62,67],1.6),tb,1.4);add(M,bass(mid(36),1.4),tb);add(M,kick(),tb);continue
    for q in range(4):
        tq=tb+q*BEAT
        if not intro and not brk:
            add(M,kick(),tq);i0=int(tq*SR);seg=1-.5*np.exp(-np.arange(int(.25*SR))/SR*14);k=min(len(seg),n-i0);side[i0:i0+k]=np.minimum(side[i0:i0+k],seg[:k])
            add(M,ohat(),tq+BEAT/2,1,pan=.2)
            add(M,bass(mid(root)*(2 if q==3 else 1),BEAT/2*.85),tq+BEAT/2)
        if q in (1,3) and not intro: add(M,clap(),tq)
        if q==1: add(M,surdo(),tq,1 if not intro else .6)
        for s16 in range(4): add(M,pandeiro(s16==2),tq+s16*ST,.9,pan=-.3)
    # agogo pattern (2 bars)
    for pos,hi in ([(0,1),(1.5,0),(2,1),(3,0)] if b%2==0 else [(0.5,1),(1.5,1),(2.5,0),(3.5,1)]): add(M,agogo(hi),tb+pos*BEAT,1,pan=.35)
    # nylon guitar syncopated comp
    for e in ([0,3,6] if b%2==0 else [2,5]): add(M,chord(ch,.35),tb+e*BEAT/2,1,pan=-.1)
    if (8<=tb<24) or (28<=tb<32):
        for k in range(8):
            if k in (0,2,3,5,6): add(M,pluck(mid(RIFF[k]+(0 if b%2 else -3))),tb+k*BEAT/2,1,pan=.3)
M*=side[:,None]
# ---- SFX (tiered, spaced)
def whoosh(d=.35): t=tt(d); u=t/d; nz=rng.standard_normal(len(t)); return (nz-lpf(nz,2500))*np.sin(np.pi*u)**2*.08
def thud(g=1): t=tt(.4); return np.tanh(np.sin(2*np.pi*np.cumsum(55+90*np.exp(-t*30))/SR)*np.exp(-t*9)*1.4)*.2*g
def click(): t=tt(.03); return hpf(rng.standard_normal(len(t)),3000)*np.exp(-t*200)*.08
def pop(): t=tt(.14); f=700*(1+1.2*np.exp(-t*45)); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*28)*.065
def chime(): t=tt(1.2); return sum(a*np.sin(2*np.pi*f*t)*np.exp(-t*k) for f,a,k in [(1568,1,3),(2093,.6,4),(2637,.35,5)])*np.minimum(1,t/.003)*.045
def crunch(): t=tt(.3); return bpf(rng.standard_normal(len(t)),1500,7000)*(np.abs(np.sin(t*90))**3)*np.exp(-t*10)*.12
def shutter(): t=tt(.06); return hpf(rng.standard_normal(len(t)),2500)*np.exp(-t*90)*.07
def swell(d=.7): t=tt(d); return bpf(rng.standard_normal(len(t)),300,3000)*(t/d)**2*np.exp(-np.maximum(t-d*.85,0)*30)*.06
ev=[(0.0,whoosh(.5)),(0.5,thud()),(1.0,thud()),(1.5,thud()),(2.5,chime())]
for c in [4,8,12,16,24,28]: ev.append((c-.12,whoosh()))
ev+=[(4.5,thud(1.3)),(5.0,click()),(5.6,pop()),(6.0,pop()),
     (9.0,pop()),(9.5,pop()),(10.0,pop()),(10.5,pop()),
     (12.6,thud(1.4)),(13.05,crunch()),(13.55,click()),
     (16.05,swell()),(17.0,click()),
     (20.0,shutter()),(21.0,shutter()),(22.0,shutter()),(22.5,shutter()),(23.0,shutter()),(23.5,shutter()),
     (24.5,thud(.8)),(25.3,pop()),
     (28.5,whoosh(.4)),(29.0,click()),(30.6,pop()),(31.1,chime())]
last=-9
for t,sig in sorted(ev,key=lambda e:e[0]):
    if t-last<0.42: continue
    add(S,sig,t); last=t
it=tt(.9); ir=rng.standard_normal(len(it))*np.exp(-it*7); ir=lpf(ir,6000); ir/=np.sqrt((ir**2).sum())
wet=np.stack([fftconvolve(M[:,0],ir)[:n],fftconvolve(M[:,1],ir)[:n]],1)
out=M*.92+wet*.08+S*1.15
t=np.arange(n)/SR; out*=np.clip((D-t)/1.0,0,1)[:,None]
out=np.tanh(out/np.abs(out).max()*1.5)/np.tanh(1.5)*.92
w=wave.open('audio_mare2.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out.reshape(-1)*32767).astype(np.int16).tobytes()); w.close(); print('ok')

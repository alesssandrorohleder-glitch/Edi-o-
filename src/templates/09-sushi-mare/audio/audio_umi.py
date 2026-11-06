import numpy as np, wave
from scipy.signal import fftconvolve, butter, sosfilt
SR=44100; D=35.0; n=int(SR*D); rng=np.random.default_rng(4)
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
BEAT=60/96;BAR=4*BEAT
def koto(f,d=1.4):
    t=tt(d);fr=f*(1+.012*np.exp(-t*18));ph=2*np.pi*np.cumsum(fr)/SR
    s=np.sin(ph)*np.exp(-t*3)+.45*np.sin(2*ph)*np.exp(-t*5)+.2*np.sin(3*ph)*np.exp(-t*8)+.08*np.sin(5*ph)*np.exp(-t*12)
    return s*np.minimum(1,t/.002)*.11
def flute(f,d):
    t=tt(d);vib=1+.006*np.sin(2*np.pi*5.2*t)*np.minimum(1,t/.6);ph=2*np.pi*np.cumsum(f*vib)/SR
    s=np.sin(ph)+.15*np.sin(2*ph);br=bpf(rng.standard_normal(len(t)),f*.8,f*3)*.25
    e=np.minimum(1,t/.25)*np.clip((d-t)/.5,0,1)
    return (s+br)*e*.055
def drone(d): t=tt(d); s=np.sin(2*np.pi*mid(45)*t)+.6*np.sin(2*np.pi*mid(52)*t)+.3*np.sin(2*np.pi*mid(57)*t); return lpf(s,900)*np.minimum(1,t/2)*np.clip((d-t)/2,0,1)*.06
def taiko(g=1): t=tt(1.2); s=np.sin(2*np.pi*np.cumsum(70+60*np.exp(-t*20))/SR)*np.exp(-t*4)+lpf(rng.standard_normal(len(t)),400)*np.exp(-t*12)*.4; return np.tanh(s*1.4)*.4*g
def pulse(): t=tt(.4); return np.sin(2*np.pi*np.cumsum(50+60*np.exp(-t*30))/SR)*np.exp(-t*8)*.38
def wood(): t=tt(.08); return (np.sin(2*np.pi*900*t)+.5*np.sin(2*np.pi*1500*t))*np.exp(-t*60)*.07
def shaker(): t=tt(.06); return hpf(rng.standard_normal(len(t)),7000)*np.sin(np.pi*t/.06)**2*.03
add(M,drone(D),0)
# hirajoshi on A: A B C E F
SC=[57,59,60,64,65,69,71,72,76]
PH=[[5,4,3,4,2,3,1,0],[3,4,5,7,6,5,4,3],[2,3,4,3,1,2,0,-9],[4,5,6,5,4,3,2,4]]
nb=int(D/BAR)
for b in range(nb):
    tb=b*BAR; sec='intro' if tb<5 else ('end' if tb>=32.5 else 'main')
    ph=PH[b%4]
    for k,idx in enumerate(ph):
        if idx<0: continue
        if sec=='intro' and k%2: continue
        add(M,koto(mid(SC[idx])),tb+k*BEAT/2,1,pan=(-.3 if k%2 else .3))
    if b%2==0: add(M,koto(mid(45)),tb,1.2)  # low anchor
    if sec=='main':
        for q in range(4):
            tq=tb+q*BEAT
            if q in (0,2): add(M,pulse(),tq)
            if q in (1,3): add(M,wood(),tq,1,pan=.2)
            for h in range(2): add(M,shaker(),tq+h*BEAT/2,1 if h else .5,pan=-.3)
# flute phrases
for t0,notes in [(0.4,[(69,1.6),(72,1.2),(76,2.0)]),(5.2,[(76,1.4),(72,1.0),(71,2.2)]),(25.3,[(72,1.5),(76,1.5),(81,2.0)]),(30.2,[(76,1.6),(72,1.6),(69,2.4)])]:
    tc=t0
    for m,d in notes: add(M,flute(mid(m),d+.3),tc,1,pan=.1); tc+=d
for tb in [0,5,10,15,20,25,30]: add(M,taiko(.8 if tb else .5),tb)
add(M,koto(mid(57),3),34.0,1.4);add(M,koto(mid(64),3),34.0,1.0)
# sfx minimal & tiered
def whoosh(d=1.0): t=tt(d); return bpf(rng.standard_normal(len(t)),300,2500)*np.sin(np.pi*t/d)**2*.05
def bell(f=1318.5,d=1.6,g=.06): t=tt(d); s=sum(a*np.sin(2*np.pi*f*r*t)*np.exp(-t*k) for r,a,k in [(1,1,2.5),(2.0,.4,4),(2.76,.25,6)]); return s*np.minimum(1,t/.002)*g
def tick(): t=tt(.1); return np.sin(2*np.pi*1760*t)*np.exp(-t*40)*.03
ev=[(0.2,whoosh()),(2.2,taiko(1.0)),(2.9,tick()),(10.3,bell(1318.5)),(15.2,bell(1174.7)),(17.5,bell(1318.5)),(20.2,bell(1174.7)),(22.5,bell(1318.5)),(25.6,bell(1760,2.0,.05)),(32.5,bell(1318.5,2.0,.07)),(33.0,tick())]
last=-9
for t,sig in ev:
    if t-last<0.45: continue
    add(S,sig,t); last=t
it=tt(2.2); ir=rng.standard_normal(len(it))*np.exp(-it*3); ir=lpf(ir,5500); ir/=np.sqrt((ir**2).sum())
mixdry=M+S
wet=np.stack([fftconvolve(mixdry[:,0],ir)[:n],fftconvolve(mixdry[:,1],ir)[:n]],1)
out=mixdry*.85+wet*.22
t=np.arange(n)/SR; out*=np.clip((D-t)/1.5,0,1)[:,None]*np.clip(t/.4,0,1)[:,None]
out=np.tanh(out/np.abs(out).max()*1.3)/np.tanh(1.3)*.92
w=wave.open('audio_umi.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out.reshape(-1)*32767).astype(np.int16).tobytes()); w.close(); print('ok')

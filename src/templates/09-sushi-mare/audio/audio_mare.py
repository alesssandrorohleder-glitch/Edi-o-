import numpy as np, wave
from scipy.signal import fftconvolve, butter, sosfilt
SR=44100; D=34.0; n=int(SR*D); rng=np.random.default_rng(21)
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
BEAT=.5;BAR=2.0
def nylon(f,d=.9):
    t=tt(d);s=np.zeros_like(t)
    for k,(g,dec) in enumerate([(1,3.5),(.55,5),(.3,7),(.15,10),(.08,14)],1): s+=g*np.sin(2*np.pi*f*k*t)*np.exp(-t*dec)
    att=lpf(rng.standard_normal(len(t)),f*4)*np.exp(-t*120)*.3
    return (s+att)*np.minimum(1,t/.002)*np.clip((d-t)/.05,0,1)*.07
def strum(ms,d=.6,g=1.0):
    o=np.zeros(int((d+.1)*SR))
    for i,m in enumerate(ms):
        s=nylon(mid(m),d);j=int(i*.012*SR);o[j:j+len(s)]+=s[:len(o)-j]
    return o*g
def bass(f,d): t=tt(d); s=np.sin(2*np.pi*f*t)+.3*np.sin(2*np.pi*2*f*t); return lpf(s,700)*np.minimum(1,t/.006)*np.exp(-t*3.2)*np.clip((d-t)/.03,0,1)*.34
def rim(): t=tt(.05); return (np.sin(2*np.pi*1700*t)+bpf(rng.standard_normal(len(t)),1500,5000)*.6)*np.exp(-t*90)*.10
def shaker(): t=tt(.06); return hpf(rng.standard_normal(len(t)),6500)*np.sin(np.pi*t/.06)**2*.035
def surdo(): t=tt(.45); return np.sin(2*np.pi*np.cumsum(60+40*np.exp(-t*25))/SR)*np.exp(-t*7)*.32
def epiano(f,d=1.2): t=tt(d); s=(np.sin(2*np.pi*f*t)+.25*np.sin(2*np.pi*2*f*t)*np.exp(-t*4))*np.exp(-t*2.2)*(1+.12*np.sin(2*np.pi*5*t)); return s*np.minimum(1,t/.004)*.07
# Dm9 | G13 | Cmaj9 | A7
CH=[(38,45,[53,57,60,64]),(43,50,[53,59,62,64]),(36,43,[52,55,59,62]),(33,40,[55,61,64,69])]
PAT=[[0,3,6],[2,5]]
MEL=[(0,74),(1.5,72),(2.5,69),(4,71),(5.5,67),(8,72),(9,76),(10.5,74),(12,73),(13.5,69)]
nb=int(D/BAR)
for b in range(nb):
    tb=b*BAR; root,fifth,ch=CH[b%4]; intro=tb<2; end=tb>=32
    if end:
        add(M,strum([52,55,59,62,67],1.9,1.3),tb);add(M,bass(mid(36),1.8),tb);continue
    for e in PAT[b%2]: add(M,strum(ch,.42 if e!=6 else .7),tb+e*BEAT/2,1,pan=-.15)
    if not intro:
        for pos,note in [(0,root),(1.5,fifth),(2,root),(3.5,fifth)]: add(M,bass(mid(note),BEAT*1.2),tb+pos*BEAT)
        for e in PAT[(b+1)%2]: add(M,rim(),tb+e*BEAT/2,1,pan=.3)
        for q in range(16): add(M,shaker(),tb+q*BEAT/4,1 if q%2 else .55,pan=.25)
        for q in (1,3): add(M,surdo(),tb+q*BEAT,1)
# melody in sections (light electric piano)
for start in [2.0,10.0,26.0]:
    for off,m in MEL: add(M,epiano(mid(m)),start+off*BEAT,1,pan=.2)
# ---- sfx: tiered, single, spaced
def whoosh(d=.45): t=tt(d); return bpf(rng.standard_normal(len(t)),500,4000)*np.sin(np.pi*t/d)**2*.04
def tick(): t=tt(.08); return np.sin(2*np.pi*2200*t)*np.exp(-t*60)*.025
def pop(): t=tt(.14); f=700*(1+1.2*np.exp(-t*45)); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*28)*.06
def MED(f=1046.5): t=tt(.6); return (np.sin(2*np.pi*f*t)+.2*np.sin(4*np.pi*f*t))*np.exp(-t*7)*np.minimum(1,t/.003)*.045
def BIG(f1=1046.5,f2=1568): t=tt(1.0); return (np.sin(2*np.pi*f1*t)+.6*np.sin(2*np.pi*f2*t))*np.exp(-t*3.5)*np.minimum(1,t/.003)*.06
ev=[(0.2,whoosh(.8)),(0.95,MED(1046.5)),(1.6,tick()),(4.05,whoosh()),(4.9,tick())]
for s0 in [8,12,16,20]: ev+=[(s0+.05,whoosh()),(s0+.5,tick()),(s0+1.3,pop())]
ev+=[(24.05,whoosh()),(24.8,tick()),(25.4,pop()),(28.1,whoosh()),(28.9,MED(1046.5)),(29.8,tick()),(30.9,BIG()),(31.45,MED(1318.5))]
last=-9
for t,sig in sorted(ev,key=lambda e:e[0]):
    if t-last<0.45: continue
    add(S,sig,t); last=t
it=tt(1.4); ir=rng.standard_normal(len(it))*np.exp(-it*4.5); ir=lpf(ir,6000); ir/=np.sqrt((ir**2).sum())
wet=np.stack([fftconvolve(M[:,0],ir)[:n],fftconvolve(M[:,1],ir)[:n]],1)
out=M*.9+wet*.14+S*1.1
t=np.arange(n)/SR; out*=np.clip((D-t)/1.4,0,1)[:,None]
out=np.tanh(out/np.abs(out).max()*1.3)/np.tanh(1.3)*.92
w=wave.open('audio_mare.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out.reshape(-1)*32767).astype(np.int16).tobytes()); w.close(); print('ok')

import numpy as np, wave
from scipy.signal import fftconvolve, butter, sosfilt
SR=44100; D=36.0; n=int(SR*D); rng=np.random.default_rng(33)
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
def kick(): t=tt(.35); f=55+140*np.exp(-t*40); return np.tanh(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)*1.6)*.7
def clap():
    t=tt(.25); nz=bpf(rng.standard_normal(len(t)),1200,5000); e=sum(np.exp(-np.clip(t-d,0,None)*70)*(t>=d) for d in (0,.01,.02))+np.exp(-t*18)*.4
    return nz*e*.22
def shaker(): t=tt(.07); return hpf(rng.standard_normal(len(t)),7000)*np.sin(np.pi*t/.07)**2*.06
def marimba(f,d=.45): t=tt(d); s=np.sin(2*np.pi*f*t)*np.exp(-t*9)+.25*np.sin(2*np.pi*4*f*t)*np.exp(-t*30); return s*np.minimum(1,t/.002)*.13
def uke(ms,d=.4):
    o=np.zeros(int(d*SR)+int(.05*SR))
    for i,m in enumerate(ms):
        t=tt(d); f=mid(m); s=(np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*2*f*t)+.2*np.sin(2*np.pi*3*f*t))*np.exp(-t*7)*np.minimum(1,t/.002)
        j=int(i*.012*SR); o[j:j+len(s)]+=s
    return o/len(ms)*.17
def bass(f,d): t=tt(d); s=np.sin(2*np.pi*f*t)+.2*np.sin(2*np.pi*2*f*t); return s*np.minimum(1,t/.004)*np.clip((d-t)/.02,0,1)*np.exp(-t*2)*.30
CH=[(48,[60,64,67]),(43,[59,62,67]),(45,[60,64,69]),(41,[60,65,69])]
MEL=[72,76,79,76, 74,79,83,79, 76,72,69,72, 77,72,69,72]
for b in range(int(D/BAR)):
    tb=b*BAR; root,ch=CH[b%4]; intro=tb<2; outro=tb>=34; brk=30<=tb<32
    if outro:
        add(M,uke(ch,1.5),tb); add(M,bass(mid(root),1.2),tb); add(M,kick(),tb); continue
    for q in range(4):
        tq=tb+q*BEAT
        # ukulele strum pattern: down on beats, up on & of 2 and 4
        add(M,uke(ch),tq,1,pan=-.2)
        if q in (1,3): add(M,uke([m+12 for m in ch],.25),tq+BEAT/2,.6,pan=.2)
        if not intro and not brk:
            if q in (0,2): add(M,kick(),tq)
            if q in (1,3): add(M,clap(),tq)
            add(M,bass(mid(root)*(1 if q!=3 else 1.5),BEAT*.8),tq)
        for h in range(2): add(M,shaker(),tq+h*BEAT/2,1 if h else .6,pan=.3)
    if not intro:
        for k in range(4):
            note=MEL[(b%4)*4+k]
            add(M,marimba(mid(note)),tb+k*BEAT,1 if not brk else .7,pan=(.35 if k%2 else -.35))
# ---- sfx (tiered, single, spaced)
def SMALL(): x=tt(.12); return np.sin(2*np.pi*1400*x)*np.exp(-x*45)*.05
def popS(): x=tt(.15); f=500*(1+1.5*np.exp(-x*50)); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*30)*.12
def MED(f=1046.5): x=tt(.5); return (np.sin(2*np.pi*f*x)+.2*np.sin(4*np.pi*f*x))*np.exp(-x*8)*np.minimum(1,x/.003)*.06
def BIG(f1=1046.5,f2=1568): x=tt(1.0); return (np.sin(2*np.pi*f1*x)+.6*np.sin(2*np.pi*f2*x))*np.exp(-x*3.5)*np.minimum(1,x/.003)*.08
def whoosh(d=.45): x=tt(d); return bpf(rng.standard_normal(len(x)),500,3500)*np.sin(np.pi*x/d)**2*.07
def tap(): x=tt(.05); return (np.sin(2*np.pi*2000*x)*np.exp(-x*100))*.09
def ding(): o=np.zeros(int(.9*SR)); a=MED(1568); b=MED(2093); o[:len(a)]+=a*1.4; j=int(.1*SR); o[j:j+len(b)]+=b[:len(o)-j]*1.4; return o
def tick(): x=tt(.04); return hpf(rng.standard_normal(len(x)),4000)*np.exp(-x*150)*.08
ev=[(0.4,MED(784)),(0.9,MED(1046.5)),(1.45,popS()),(1.95,tick()),(2.45,tick()),
    (3.75,whoosh()),(4.2,BIG(1046.5,1568)),(4.75,SMALL()),(5.5,MED(1318.5)),
    (7.75,whoosh()),(8.25,MED(1046.5)),(8.75,whoosh(.5)),(10.6,tap()),(11.08,tap()),(11.7,tap()),(12.1,ding()),
    (13.75,whoosh()),(14.25,MED(1046.5)),(14.75,SMALL()),(17.0,popS()),
    (19.75,whoosh()),(20.25,MED(1046.5)),(20.75,popS()),(23.0,popS()),(23.5,BIG(1318.5,1568)),
    (25.75,whoosh()),(26.15,MED(1046.5)),(26.6,popS()),(27.1,popS()),(27.6,popS()),
    (29.75,whoosh()),(30.25,SMALL()),(30.75,MED(1046.5)),(31.85,SMALL()),(32.85,BIG(1046.5,1568)),(33.35,MED(1318.5))]
last=-9
for t,sig in ev:
    if t-last<0.4: continue
    add(S,sig,t); last=t
it=tt(.9); ir=rng.standard_normal(len(it))*np.exp(-it*7); ir=lpf(ir,6000); ir/=np.sqrt((ir**2).sum())
wet=np.stack([fftconvolve(M[:,0],ir)[:n],fftconvolve(M[:,1],ir)[:n]],1)
out=M*.9+wet*.1+S*1.1
t=np.arange(n)/SR; out*=np.clip((D-t)/1.0,0,1)[:,None]
out=np.tanh(out/np.abs(out).max()*1.5)/np.tanh(1.5)*.92
w=wave.open('audio_lavo.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out.reshape(-1)*32767).astype(np.int16).tobytes()); w.close(); print('ok')

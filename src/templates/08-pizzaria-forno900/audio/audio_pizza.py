import numpy as np, wave
from scipy.signal import fftconvolve, butter, sosfilt
SR=44100; D=32.0; n=int(SR*D); rng=np.random.default_rng(9)
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
def kick(): t=tt(.35); return np.tanh(np.sin(2*np.pi*np.cumsum(52+120*np.exp(-t*40))/SR)*np.exp(-t*9)*1.5)*.65
def clap():
    t=tt(.22); nz=bpf(rng.standard_normal(len(t)),1200,5000); e=sum(np.exp(-np.clip(t-d,0,None)*70)*(t>=d) for d in (0,.01,.02))+np.exp(-t*18)*.4; return nz*e*.2
def tamb(): t=tt(.1); nz=hpf(rng.standard_normal(len(t)),6000); return (nz*np.exp(-t*35)+np.sin(2*np.pi*7200*t)*np.exp(-t*50)*.3)*.07
def mando(f,d=.11): t=tt(d); s=np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*2*f*t)+.25*np.sin(2*np.pi*3*f*t); return s*np.exp(-t*22)*np.minimum(1,t/.001)*.06
def accord(ms,d=.3): t=tt(d); s=sum(np.sin(2*np.pi*mid(m)*k*t)/k for m in ms for k in (1,3,5,7))/len(ms); return lpf(s,3000)*np.minimum(1,t/.01)*np.clip((d-t)/.04,0,1)*.10
def bass(f,d): t=tt(d); s=np.sin(2*np.pi*f*t)+.25*np.sin(2*np.pi*2*f*t); return s*np.minimum(1,t/.004)*np.clip((d-t)/.02,0,1)*np.exp(-t*2.5)*.32
CH=[(45,[57,60,64]),(38,[57,62,65]),(43,[55,59,62]),(48,[55,60,64])]
for b in range(int(D/BAR)):
    tb=b*BAR; root,ch=CH[b%4]; intro=tb<2; end=tb>=30
    if end:
        add(M,accord(ch,1.4),tb); add(M,bass(mid(root-12),1.2),tb); add(M,kick(),tb); continue
    for q in range(4):
        tq=tb+q*BEAT
        if q in (0,2): add(M,bass(mid(root-12)*(1 if q==0 else 1.5),BEAT*.9),tq,1 if not intro else .6)
        if q in (1,3): add(M,accord([m+12 for m in ch]),tq,1,pan=.15)
        if not intro:
            if q in (0,2): add(M,kick(),tq)
            if q in (1,3): add(M,clap(),tq)
        for h in range(2): add(M,tamb(),tq+h*BEAT/2,1 if h else .6,pan=-.3)
        # mandolin tremolo: 16ths on chord tones (melodic contour)
        if not intro:
            line=[ch[2]+12,ch[1]+12,ch[0]+12,ch[1]+12]
            for s16 in range(4): add(M,mando(mid(line[q]+ (12 if b%2 and q==3 else 0))),tq+s16*BEAT/4,1,pan=.35)
def thud(): t=tt(.35); return np.tanh(np.sin(2*np.pi*np.cumsum(60+80*np.exp(-t*30))/SR)*np.exp(-t*10)*1.5)*.17
def popS(): t=tt(.12); f=600*(1+1.4*np.exp(-t*50)); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*30)*.085
def MED(f=1046.5): t=tt(.4); return (np.sin(2*np.pi*f*t)+.2*np.sin(4*np.pi*f*t))*np.exp(-t*9)*np.minimum(1,t/.003)*.05
def BIG(f1=1046.5,f2=1568):
    t=tt(.9); a=(np.sin(2*np.pi*f1*t)+.6*np.sin(2*np.pi*f2*t))*np.exp(-t*4)*np.minimum(1,t/.003)*.07; h=thud()*.6; a[:len(h)]+=h; return a
def cash(): t=tt(.8); return (np.sin(2*np.pi*2093*t)+.5*np.sin(2*np.pi*3136*t))*np.exp(-t*5)*.08
def swish(): t=tt(.18); return hpf(rng.standard_normal(len(t)),2500)*np.sin(np.pi*t/.18)**2*.05
def tick(): t=tt(.04); return np.sin(2*np.pi*2400*t)*np.exp(-t*120)*.05
ev=[(0.0,thud()),(0.5,thud()),(1.0,thud()),(2.0,BIG(880,1318.5)),(2.5,popS()),(4.0,MED(880))]+[(4.5+i*.5,popS()) for i in range(8)]+[
    (10.5,thud()),(11.0,swish()),(11.5,thud()),(12.6,cash()),(13.0,popS()),(13.5,popS()),
    (16.2,MED()),(17.0,tick()),(17.5,popS()),(18.0,tick()),(19.0,tick()),
    (20.0,thud()),(21.0,thud()),(22.0,thud()),(23.0,thud()),
    (24.0,thud()),(24.5,BIG(880,1318.5)),(25.5,MED()),(26.0,thud()),(26.5,BIG()),(27.2,popS()),(28.0,BIG(1046.5,1568)),(28.5,MED(1318.5))]
last=-9
for t,sig in ev:
    if t-last<0.45: continue
    add(S,sig,t); last=t
it=tt(.8); ir=rng.standard_normal(len(it))*np.exp(-it*8); ir=lpf(ir,6000); ir/=np.sqrt((ir**2).sum())
wet=np.stack([fftconvolve(M[:,0],ir)[:n],fftconvolve(M[:,1],ir)[:n]],1)
out=M*.92+wet*.08+S*1.1
t=np.arange(n)/SR; out*=np.clip((D-t)/.8,0,1)[:,None]
out=np.tanh(out/np.abs(out).max()*1.5)/np.tanh(1.5)*.92
w=wave.open('audio_pizza.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out.reshape(-1)*32767).astype(np.int16).tobytes()); w.close(); print('ok')

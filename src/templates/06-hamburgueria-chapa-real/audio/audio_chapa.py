import numpy as np, wave
from scipy.signal import fftconvolve, butter, sosfilt
SR=44100; D=32.0; n=int(SR*D); rng=np.random.default_rng(5)
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
STEP=.125; BAR=2.0
def kick(): t=tt(.3); f=55+150*np.exp(-t*45); return np.tanh(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*10)*1.8)*.75
def snare():
    t=tt(.22); nz=bpf(rng.standard_normal(len(t)),1500,6000); return (nz*np.exp(-t*22)*.5+np.sin(2*np.pi*230*t)*np.exp(-t*30)*.35)*.6
def hat(): t=tt(.04); return hpf(rng.standard_normal(len(t)),8000)*np.exp(-t*90)*.07
def tom(f=160): t=tt(.2); return np.sin(2*np.pi*np.cumsum(f*(1+.6*np.exp(-t*30)))/SR)*np.exp(-t*14)*.3
def b808(f,d): t=tt(d); s=np.tanh(np.sin(2*np.pi*f*t)*1.6); return s*np.minimum(1,t/.004)*np.clip((d-t)/.03,0,1)*np.exp(-t*1.5)*.32
def brass(ms,d=.22): t=tt(d); s=sum(np.sin(2*np.pi*mid(m)*k*t)/k for m in ms for k in (1,2,3,4))/len(ms); return lpf(s,3500)*np.exp(-t*6)*np.minimum(1,t/.006)*np.clip((d-t)/.02,0,1)*.11
CH=[(45,[57,60,64]),(45,[57,60,64]),(41,[57,60,65]),(43,[59,62,67])]
KICK=[0,3,6,8,11,14]; SN=[4,12]; TOM=[7,15]; BR=[0,3,6,10,13]
for b in range(int(D/BAR)):
    tb=b*BAR; root,ch=CH[b%4]; intro=tb<2; brk=24<=tb<26; end=tb>=30
    if end:
        add(M,brass(ch,.8),tb); add(M,b808(mid(root-12),1.0),tb); add(M,kick(),tb); continue
    for st in range(16):
        ts=tb+st*STEP
        if not intro and not brk:
            if st in KICK: add(M,kick(),ts); add(M,b808(mid(root-12),STEP*2.4),ts,.9)
            if st in SN: add(M,snare(),ts)
            if st in TOM: add(M,tom(180 if st==7 else 140),ts,.8,pan=.3)
        if st%2==0: add(M,hat(),ts,1 if st%4==2 else .6,pan=-.3)
        if st in BR: add(M,brass(ch if st!=10 else [m+2 for m in ch]),ts,1 if not intro else .7,pan=.15)
# sfx: tiered, single, spaced
def thud(): t=tt(.35); return np.tanh(np.sin(2*np.pi*np.cumsum(60+80*np.exp(-t*30))/SR)*np.exp(-t*10)*1.5)*.18
def popS(): t=tt(.12); f=600*(1+1.4*np.exp(-t*50)); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*30)*.09
def MED(f=1046.5): t=tt(.4); return (np.sin(2*np.pi*f*t)+.2*np.sin(4*np.pi*f*t))*np.exp(-t*9)*np.minimum(1,t/.003)*.05
def BIG(f1=1046.5,f2=1568):
    t=tt(.9); a=(np.sin(2*np.pi*f1*t)+.6*np.sin(2*np.pi*f2*t))*np.exp(-t*4)*np.minimum(1,t/.003)*.07; h=thud()*.6; a[:len(h)]+=h; return a
def cash(): t=tt(.8); a=(np.sin(2*np.pi*2093*t)+.5*np.sin(2*np.pi*3136*t))*np.exp(-t*5)*.08; return a
def swish(): t=tt(.18); return hpf(rng.standard_normal(len(t)),2500)*np.sin(np.pi*t/.18)**2*.05
def tick(): t=tt(.04); return np.sin(2*np.pi*2400*t)*np.exp(-t*120)*.05
ev=[(0.0,thud()),(0.5,thud()),(1.0,thud()),(2.0,BIG()),(2.5,popS()),
    (4.0,MED()),(4.5,popS()),(5.0,popS()),(5.5,popS()),(6.0,popS()),(6.5,popS()),(7.0,popS()),
    (10.5,thud()),(11.0,swish()),(11.5,thud()),(12.6,cash()),(13.0,popS()),(13.5,popS()),
    (16.2,MED()),(17.0,tick()),(17.5,popS()),(18.0,tick()),(19.0,tick()),
    (20.0,thud()),(21.0,thud()),(22.0,thud()),(23.0,thud()),
    (24.0,thud()),(24.5,BIG(880,1318.5)),(25.5,MED()),(26.0,thud()),(26.5,BIG()),(27.2,popS()),(28.0,BIG(1046.5,1568)),(28.5,MED(1318.5))]
last=-9
for t,sig in ev:
    if t-last<0.45: continue
    add(S,sig,t); last=t
out=M*.95+S*1.1
t=np.arange(n)/SR; out*=np.clip((D-t)/.8,0,1)[:,None]
out=np.tanh(out/np.abs(out).max()*1.6)/np.tanh(1.6)*.92
w=wave.open('audio_chapa.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out.reshape(-1)*32767).astype(np.int16).tobytes()); w.close(); print('ok')

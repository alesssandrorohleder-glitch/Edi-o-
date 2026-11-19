import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve, butter, lfilter
SR=44100;DUR=39.375;N=int(SR*DUR);BPM=128;B=60/BPM;BAR=4*B;DROP=3.75
rng=np.random.default_rng(11)
mus=np.zeros(N);sfx=np.zeros(N)
def tt(d):return np.arange(int(d*SR))/SR
def add(buf,s,t,g=1.0):
    i=int(round(t*SR));j=min(N,i+len(s))
    if 0<=i<N:buf[i:j]+=s[:j-i]*g
def lp(s,f):b,a=butter(2,min(f,SR/2-100)/(SR/2));return lfilter(b,a,s)
def hp(s,f):b,a=butter(2,f/(SR/2),'high');return lfilter(b,a,s)
nt=lambda m:440*2**((m-69)/12)
def nrm(s):return s/(np.max(np.abs(s))+1e-9)
def impact(f=55,g=1,d=1.0):t=tt(d);fr=f+160*np.exp(-t*30);s=np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-t*4);return np.tanh(1.5*s)+hp(rng.standard_normal(len(t)),2000)*np.exp(-t*40)*.35
def snap():t=tt(.25);return hp(rng.standard_normal(len(t)),1500)*np.exp(-t*40)*.8+np.sin(2*np.pi*180*t)*np.exp(-t*30)*.6
def boom():t=tt(2.6);fr=34+90*np.exp(-t*10);s=np.tanh(2*np.sin(2*np.pi*np.cumsum(fr)/SR))*np.exp(-t*1.5);return s+lp(rng.standard_normal(len(t)),400)*np.exp(-t*2.5)*.6+hp(rng.standard_normal(len(t)),3000)*np.exp(-t*12)*.3
def whoosh(d=.45,up=True):
    t=tt(d);n=rng.standard_normal(len(t));e=np.sin(np.pi*t/d)**2
    out=np.zeros_like(n);seg=int(.02*SR)
    for i in range(0,len(n),seg):
        k=i/len(n);f=(600+5000*k) if up else (5600-5000*k);out[i:i+seg]=lp(n[i:i+seg+64],f)[:len(out[i:i+seg])]
    return hp(out,200)*e
def glitchs():t=tt(.22);s=np.sign(np.sin(2*np.pi*(300+2000*rng.random())*t))*(rng.random(len(t))>.4);return lp(s,7000)*np.exp(-t*12)*.6+whoosh(.22)*.8
def blip(f=1600):t=tt(.15);return np.sin(2*np.pi*f*t)*np.exp(-t*30)+np.sin(2*np.pi*f*2*t)*np.exp(-t*50)*.3
def riser(d,f0=150,f1=2400):
    t=tt(d);fr=f0*(f1/f0)**(t/d);s=np.sin(2*np.pi*np.cumsum(fr)/SR)*.35
    n=rng.standard_normal(len(t));nf=np.zeros_like(n);seg=int(.02*SR)
    for i in range(0,len(n),seg):nf[i:i+seg]=hp(n[i:i+seg+64],300+6000*(i/len(n))**2)[:len(nf[i:i+seg])]
    return (s+nf*.5)*(t/d)**2
def ratchet(d=.7):
    out=np.zeros(int(d*SR))
    for k in range(14):
        tk=d*(1-(1-k/14)**1.6);c=blip(2400+k*60)[:int(.04*SR)]*.5;i=int(tk*SR);j=min(len(out),i+len(c));out[i:j]+=c[:j-i]
    return out
def pop():t=tt(.2);fr=500*(1+1.2*np.exp(-t*50));return np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-t*18)
SOFT,MED,STR=.25,.45,.8

SOFT,MED,STR=.25,.45,.8
def tick():t=tt(.08);return hp(rng.standard_normal(len(t)),3000)*np.exp(-t*80)*.6+np.sin(2*np.pi*2200*t)*np.exp(-t*60)*.4
def splash(d=.6):
    t=tt(d);n=rng.standard_normal(len(t));return (hp(lp(n,6000),800)*np.exp(-t*9)*(1+.5*np.sin(2*np.pi*23*t)))*np.minimum(1,t/.005)
def shimmer(d=2.0):
    t=tt(d);s=sum(np.sin(2*np.pi*f*t+rng.random()*6)*np.exp(-t*(1.2+i*.4)) for i,f in enumerate([1760,2217,2637,3520]))
    return s*np.minimum(1,t/.15)*.4+riser(d,300,1500)*.3
EV=[(0.02,impact(75,d=.45),MED),(2*B,impact(68,d=.45),MED),(4*B,impact(55,d=.8),STR),(6*B,tick(),SOFT),(3.28,whoosh(.45),SOFT),
 (DROP,boom(),1.0),(DROP+2*B,tick(),SOFT),(DROP+3*B,snap(),MED),
 (7.5,whoosh(.4),SOFT),(7.5+B,snap(),MED),(7.5+6*B,boom(),STR),(7.5+6*B+.5,tick(),SOFT),
 (11.25,whoosh(.4),SOFT),(11.25+2*B,blip(1500),SOFT),(11.25+4*B,blip(1800),SOFT),(11.25+6*B,blip(2100),SOFT),
 (15.0,whoosh(.4),SOFT),(15+2*B,tick(),SOFT),(15+3*B,snap(),MED),
 (18.75,whoosh(.4),SOFT),(18.75+B,snap(),MED),(18.75+2*B,tick(),SOFT),(18.75+BAR,boom(),STR),(18.75+BAR+2*B,snap(),SOFT),
 (22.5,splash(),MED),(22.5+B,impact(78,d=.45),MED),(22.5+2*B,impact(60,d=.7),MED),(22.5+4*B,splash(),SOFT),
 (26.25,whoosh(.35),MED),(26.25+2*B,whoosh(.35),MED),(26.25+4*B,whoosh(.35),MED),(26.25+6*B,whoosh(.35),MED),
 (30.0,whoosh(.4,False),SOFT),(30+4*B,boom(),STR),(30+5*B,snap(),MED),(30+6*B,tick(),SOFT),
 (33.75,whoosh(.4,False),SOFT),(33.75+B,tick(),SOFT),(33.75+2*B,tick(),SOFT),(33.75+3*B,impact(62,d=.6),MED),(33.75+4.4*B,tick(),SOFT),(33.75+7*B,impact(70,d=.6),STR),(33.75+8*B,blip(1900),SOFT),
]
EV.sort(key=lambda e:e[0]);last=-9;kept=[]
for t,s_,g in EV:
    if t-last<0.45:continue
    add(sfx,nrm(s_),t,g);last=t;kept.append((t,g))
add(sfx,nrm(riser(1.2)),DROP-1.2,.3)
add(sfx,nrm(riser(1.0,200,1800)),7.5+6*B-1.0,.18)
add(sfx,nrm(shimmer(2.2)),15.1,.14)
add(sfx,nrm(riser(.9,200,1800)),30+4*B-.9,.18)
add(sfx,nrm(ratchet()),30+4*B+.15,.10)
ir=rng.standard_normal(int(SR*1.2))*np.exp(-np.arange(int(SR*1.2))/SR*5);ir=lp(ir,6000);ir/=np.sum(np.abs(ir))/10
out=sfx+fftconvolve(sfx,ir)[:N]*.18
fo=np.ones(N);i=int(38.8*SR);fo[i:]=np.linspace(1,0,N-i);out*=fo
out=np.tanh(out*1.3)/np.tanh(1.3);out/=np.max(np.abs(out))*1.12
wavfile.write('audio_zefyr_sfx.wav',SR,(np.stack([out,out],1)*32767).astype(np.int16))
print('ok',len(kept))

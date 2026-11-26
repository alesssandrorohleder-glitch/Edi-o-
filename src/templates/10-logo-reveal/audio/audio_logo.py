import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve, butter, lfilter
SR=44100;DUR=34.0;N=int(SR*DUR);BPM=120;B=60/BPM
rng=np.random.default_rng(7)
mus=np.zeros(N);sfx=np.zeros(N)
def tt(d):return np.arange(int(d*SR))/SR
def add(buf,s,t,g=1.0):
    i=int(t*SR);j=min(N,i+len(s))
    if i<N:buf[i:j]+=s[:j-i]*g
def lp(s,f):b,a=butter(2,f/(SR/2));return lfilter(b,a,s)
def hp(s,f):b,a=butter(2,f/(SR/2),'high');return lfilter(b,a,s)
def env(d,a=.005,r=.2):t=tt(d);return np.minimum(1,t/a)*np.exp(-t/r)
# ---------- music bed ----------
def kick():t=tt(.35);f=45+90*np.exp(-t*30);return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)
def hat(o=False):t=tt(.25 if o else .06);return hp(rng.standard_normal(len(t)),7000)*np.exp(-t*(14 if o else 70))
def clap():t=tt(.2);n=hp(rng.standard_normal(len(t)),1200);e=sum(np.exp(-np.maximum(t-d,0)*60)*(t>=d) for d in (0,.012,.024));return n*e*.6
def bass(f,d):t=tt(d);s=np.sin(2*np.pi*f*t)+.3*np.sin(4*np.pi*f*t);return s*np.minimum(1,t/.01)*np.exp(-t*3)
def pluck(f,d=.35):t=tt(d);s=sum(np.sin(2*np.pi*f*h*t)/h**1.3*np.exp(-t*(6+h*3)) for h in range(1,6));return s*np.minimum(1,t/.003)
nt=lambda m:440*2**((m-69)/12)
prog=[(45,[69,72,76]),(41,[69,72,77]),(43,[67,71,74]),(40,[68,71,76])]  # Am F G E
nbars=int(DUR/(4*B))+1
for bar in range(nbars):
    t0=bar*4*B;root,ch=prog[bar%4]
    if t0>=33.4:break
    for b in range(4):
        tb=t0+b*B
        if tb<2.0:continue
        add(mus,kick(),tb,.9)
        add(mus,hat(),tb+B/2,.18)
        if b%2==1:add(mus,clap(),tb,.35)
        add(mus,bass(nt(root),B*.45),tb+B/2,.5)
    for k,st in enumerate([0,.75,1.5,2.5,3.25]):
        add(mus,pluck(nt(ch[k%3])),t0+st*B,.13)
for k in range(8):add(mus,pluck(nt([69,72,76,81][k%4]),.3),k*B/2,.10)  # intro arp
# sidechain from kicks
sc=np.ones(N)
for bar in range(nbars):
    for b in range(4):
        tb=(bar*4+b)*B
        if 2.0<=tb<33.4:
            i=int(tb*SR);d=int(.25*SR);j=min(N,i+d)
            sc[i:j]=np.minimum(sc[i:j],1-.45*np.exp(-np.arange(j-i)/SR*14))
mus*=sc
# ---------- SFX ----------
def pop(f=900,g=1):t=tt(.18);fr=f*(1+.6*np.exp(-t*60));return np.sin(2*np.pi*np.cumsum(fr)/SR)*env(.18,.002,.04)*g
def marimba(f):t=tt(.6);return (np.sin(2*np.pi*f*t)+.25*np.sin(2*np.pi*f*4*t)*np.exp(-t*20))*env(.6,.002,.18)
def chime(f):t=tt(1.4);return sum(np.sin(2*np.pi*f*m*t)*a for m,a in((1,1),(2.76,.35),(5.4,.15)))*env(1.4,.002,.45)
def whoosh(d=.6):
    t=tt(d);n=rng.standard_normal(len(t));e=np.sin(np.pi*t/d)**2
    a=lp(n,2500)*e;return hp(a,250)*.9
def boing(f=300):t=tt(.45);fr=f*(1+.5*np.sin(2*np.pi*14*t)*np.exp(-t*8));return np.sin(2*np.pi*np.cumsum(fr)/SR)*env(.45,.003,.14)
def hit(f=55,g=1):t=tt(1.2);fr=f+120*np.exp(-t*25);s=np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-t*3.5);return s+lp(rng.standard_normal(len(t)),900)*np.exp(-t*25)*.4
def boom():t=tt(2.2);fr=38+70*np.exp(-t*12);return np.tanh(1.6*np.sin(2*np.pi*np.cumsum(fr)/SR))*np.exp(-t*1.6)+lp(rng.standard_normal(len(t)),300)*np.exp(-t*3)*.5
def shimmer(d=1.2):
    t=tt(d);s=sum(np.sin(2*np.pi*f*t+rng.random()*6)*np.exp(-t*(2+i)) for i,f in enumerate([2093,2637,3136,4186,5274]));return s*np.minimum(1,t/.02)*.35
def riser(d,f0=200,f1=1200):
    t=tt(d);fr=f0*(f1/f0)**(t/d);s=np.sin(2*np.pi*np.cumsum(fr)/SR)*.4+hp(rng.standard_normal(len(t)),3000)*.25*(t/d)
    return s*(t/d)**1.5*np.minimum(1,(d-t)/.05)
def crackle(d=.6):
    t=tt(d);s=hp(rng.standard_normal(len(t)),2000)*(rng.random(len(t))<.03)*3+np.sign(np.sin(2*np.pi*60*t))*.15*(rng.random(len(t))>.5)
    return s*np.minimum(1,t/.02)*np.minimum(1,(d-t)/.05)
def zap():
    t=tt(.6);fr=2400*np.exp(-t*9)+80;s=np.sign(np.sin(2*np.pi*np.cumsum(fr)/SR))*.4*np.exp(-t*6)
    return lp(s,6000)+hit(50)[:len(t)]*.9
def bell(f):t=tt(2.0);return sum(np.sin(2*np.pi*f*m*t)*a*np.exp(-t*dk) for m,a,dk in((1,1,1.2),(2,.5,2),(3.01,.3,3),(4.2,.2,4)))*np.minimum(1,t/.003)
def tick():return pop(1800,.6)
SOFT,MED,STR=.22,.42,.75
EV=[ # (time, sound, gain)
 (0.1,pop(700),SOFT),(0.6,pop(820),SOFT),(1.1,marimba(nt(76)),MED),(1.6,marimba(nt(81)),MED),(2.3,pop(1100),SOFT),
 (3.75,whoosh(),MED),
 (4.45,marimba(nt(72)),SOFT),(5.3,chime(nt(84)),MED),(6.1,pop(600),SOFT),(6.7,boing(),MED),(7.6,hit(70),MED),(8.2,tick(),SOFT),
 (9.75,whoosh(),MED),
 (11.5,shimmer(),MED),(12.0,boom(),STR),(13.0,chime(nt(79)),MED),(14.0,tick(),SOFT),
 (15.75,whoosh(),MED),
 (16.3,crackle(),SOFT),(17.0,zap(),STR),(17.6,hit(45,1),STR),(19.2,tick(),SOFT),
 (21.75,whoosh(),MED),
 (24.6,bell(nt(76)),STR),(25.8,tick(),SOFT),
 (27.75,whoosh(),MED),
 (28.15,pop(900),SOFT),(28.6,pop(760),SOFT),(29.2,marimba(nt(76)),MED),(29.8,tick(),SOFT),(30.3,tick(),SOFT),(30.8,hit(65),STR),(31.3,chime(nt(88)),MED),
]
last=-9;EV.sort(key=lambda e:e[0])
for t,s,g in EV:
    if t-last<0.45:continue
    add(sfx,s/np.max(np.abs(s)),t,g);last=t
# continuous beds (not discrete hits)
add(sfx,riser(1.0,300,900),10.45,.12)      # ATLAS line draw
add(sfx,riser(2.1,150,1400),22.3,.18)      # órbita swirl
# reverb
ir=rng.standard_normal(int(SR*1.4))*np.exp(-np.arange(int(SR*1.4))/SR*4);ir=lp(ir,5000);ir/=np.sum(np.abs(ir))/12
sfxw=sfx+fftconvolve(sfx,ir)[:N]*.18
musw=mus+fftconvolve(mus,ir)[:N]*.08
# duck music under strong hits
duck=np.ones(N)
for t,_,g in EV:
    if g>=STR:
        i=int(t*SR);j=min(N,i+int(1.2*SR));duck[i:j]=np.minimum(duck[i:j],1-.5*np.exp(-np.arange(j-i)/SR*2.5))
out=musw*.55*duck+sfxw*.9
fo=np.ones(N);i=int(33.2*SR);fo[i:]=np.linspace(1,0,N-i);out*=fo
out=np.tanh(out*1.3)/np.tanh(1.3);out/=np.max(np.abs(out))*1.12
st=np.stack([out,out],1)
wavfile.write('audio_logo.wav',SR,(st*32767).astype(np.int16))
print('ok')

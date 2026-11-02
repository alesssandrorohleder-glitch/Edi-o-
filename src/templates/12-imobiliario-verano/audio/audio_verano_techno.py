import numpy as np
from scipy.io import wavfile
from scipy.signal import butter,lfilter,fftconvolve
SR=44100;DUR=38.0;N=int(SR*DUR);B=0.5;BAR=2.0;rng=np.random.default_rng(21)
def tt(d):return np.arange(int(d*SR))/SR
def lp(s,f):b,a=butter(2,min(f,SR/2-100)/(SR/2));return lfilter(b,a,s)
def hp(s,f):b,a=butter(2,f/(SR/2),'high');return lfilter(b,a,s)
nt=lambda m:440*2**((m-69)/12)
L=np.zeros(N);R=np.zeros(N)
def st(s,t,g=1.,pan=0.):
    i=int(round(t*SR));j=min(N,i+len(s))
    if i<0 or i>=N:return
    gl=g*np.cos((pan+1)*np.pi/4)*1.414;gr=g*np.sin((pan+1)*np.pi/4)*1.414;L[i:j]+=s[:j-i]*gl;R[i:j]+=s[:j-i]*gr

def kick():
    t=tt(.4);f=44+120*np.exp(-t*38)+50*np.exp(-t*300);s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7.5)
    return np.tanh(s*1.7)+hp(rng.standard_normal(len(t)),4000)*np.exp(-t*500)*.2
def clap():t=tt(.35);n=hp(lp(rng.standard_normal(len(t)),7000),1000);e=sum(np.exp(-np.maximum(t-d,0)*55)*(t>=d) for d in (0,.009,.019));return n*(e+np.exp(-t*10)*.15)*.6
def hat(o=False):d=.18 if o else .04;t=tt(d);return hp(rng.standard_normal(len(t)),9500 if not o else 7500)*np.exp(-t*(20 if o else 110))
def ride():t=tt(.5);return hp(rng.standard_normal(len(t)),6000)*np.exp(-t*7)*.5+np.sin(2*np.pi*5200*t)*np.exp(-t*9)*.08
def perc(f=600):t=tt(.08);return np.sin(2*np.pi*f*t)*np.exp(-t*60)
def bass(f,d,cut=600):
    t=tt(d);s=sum(np.sin(2*np.pi*f*h*t)/h for h in range(1,8))
    env=np.minimum(1,t/.002)*np.exp(-t*14);return lp(s,cut)*env
def pluck(f,cut=2500,d=.35):
    t=tt(d);s=sum(np.sin(2*np.pi*f*h*t)/h**1.1 for h in range(1,10))
    return lp(s,cut)*np.minimum(1,t/.002)*np.exp(-t*10)
# A minor hypnotic: bass root per 2 bars, arp 16ths
ROOTS=[33,33,29,31]          # A A F G (per bar)
ARP=[69,72,76,72,69,74,72,76]
def bars(a,b,kick_on=True,hats=True,clap_on=True,bass_on=True,arp=True,arpcut=(1500,4000),ride_on=False):
    t0=a;bi=int(round(a/BAR))
    while t0<b-1e-6:
        r=ROOTS[bi%4]
        for k in range(4):
            tb=t0+k*B
            if kick_on:st(kick(),tb,.95)
            if hats:st(hat(True),tb+B/2,.12,.25)
            if hats:
                for s16 in (1,3):st(hat(),tb+s16*B/4,.05,-.3)
            if clap_on and k%2==1:st(clap(),tb,.32)
            if ride_on:st(ride(),tb+B/2,.06,.4)
            if bass_on:
                for s16 in (1,2,3):st(bass(nt(r+(12 if (s16==3 and k%2) else 0)),B/4*.9),tb+s16*B/4,.42)
        if arp:
            for k in range(16):
                tt0=t0+k*B/4*2/2
                u=((t0-a)+k*B/4)/max(.001,(b-a));cut=arpcut[0]+(arpcut[1]-arpcut[0])*u
                if k%2==0 or bi%2: st(pluck(nt(ARP[k%8]),cut),t0+k*B/2 if False else t0+k*B/4,.10 if k%2 else .13,.3 if k%4==1 else -.2)
        if bi%4==3:
            for k,f in enumerate([520,660,780]):st(perc(f),t0+3*B+k*B/4,.12,.5-k*.4)
        t0+=BAR;bi+=1
bars(0,4,kick_on=False,hats=False,clap_on=False,bass_on=False,arp=True,arpcut=(500,1800))
bars(4,12,ride_on=False,arpcut=(1200,2200))
bars(12,20,ride_on=True,arpcut=(2000,3500))
bars(20,24,kick_on=False,clap_on=False,bass_on=False,hats=True,arpcut=(900,2600))
bars(24,32,ride_on=True,arpcut=(2500,4000))
bars(32,36,ride_on=False,clap_on=True,arpcut=(2000,1000))
st(kick(),36,1.0);st(bass(nt(33),1.2,400),36,.5);st(pluck(nt(69),1500,1.5),36,.2)
def riser(d):
    t=tt(d);n=rng.standard_normal(len(t));o=np.zeros_like(n);seg=int(.02*SR)
    for i in range(0,len(n),seg):o[i:i+seg]=lp(n[i:i+seg+64],300+6000*(i/len(n))**2)[:len(o[i:i+seg])]
    return hp(o,200)*(t/d)**2
st(riser(2.0),2.0,.18);st(riser(2.0),22.0,.18)
for k in range(8):st(clap()*(.3+.7*k/8),23.0+k*B/4,.2)
def bell(f,d=1.2):t=tt(d);return (np.sin(2*np.pi*f*t)+.3*np.sin(2*np.pi*f*3*t)*np.exp(-t*6))*np.exp(-t*3)*np.minimum(1,t/.003)
# sidechain
sc=np.ones(N)
for tb in np.arange(4,37.6,B):
    if 20<=tb<24:continue
    i=int(tb*SR);j=min(N,i+int(.3*SR));sc[i:j]=np.minimum(sc[i:j],1-.55*np.exp(-np.arange(j-i)/SR*10))
L*=sc;R*=sc
# SFX: soft whoosh on each transition, gentle chime on price
SF=np.zeros(N)
def whoosh(d=.7):
    t=tt(d);n=rng.standard_normal(len(t));e=np.sin(np.pi*t/d)**2;o=np.zeros_like(n);seg=int(.02*SR)
    for i in range(0,len(n),seg):o[i:i+seg]=lp(n[i:i+seg+64],500+3500*np.sin(np.pi*i/len(n)))[:len(o[i:i+seg])]
    return hp(o,200)*e
EV=[(c-.35,whoosh(),.22) for c in [4,8,12,16,20,24,28,32]]+[(28.7,bell(nt(93),1.5),.18),(34.6,bell(nt(90),1.2),.12)]
last=-9
for t,s,g in sorted(EV,key=lambda e:e[0]):
    if t-last<.45:continue
    i=int(t*SR);j=min(N,i+len(s));SF[i:j]+=s[:j-i]/np.max(np.abs(s))*g;last=t
irm=rng.standard_normal(int(SR*1.8))*np.exp(-np.arange(int(SR*1.8))/SR*3.2);irm=lp(irm,6000);irm/=np.sum(np.abs(irm))/9
Lw=L+fftconvolve(L,irm)[:N]*.16+SF;Rw=R+fftconvolve(R,np.roll(irm,377))[:N]*.16+SF
fi=np.minimum(1,np.arange(N)/(SR*.6));fo=np.ones(N);i=int(37.0*SR);fo[i:]=np.linspace(1,0,N-i)
o=np.stack([Lw*fi*fo,Rw*fi*fo],1);o=np.tanh(o*1.4)/np.tanh(1.4);o/=np.max(np.abs(o))*1.12
wavfile.write('audio_verano_techno.wav',SR,(o*32767).astype(np.int16));print('ok')

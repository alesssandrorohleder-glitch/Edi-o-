# ONDA — techno clean 120bpm (base: trilha techno APROVADA do 12 VERANO), 32s, + SFX nos cortes de 2s
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter,lfilter,fftconvolve
SR=44100;DUR=32.0;N=int(SR*DUR);B=0.5;BAR=2.0;rng=np.random.default_rng(21)
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
bars(0,2,kick_on=True,hats=False,clap_on=False,bass_on=False,arp=True,arpcut=(600,2000))
bars(2,8,arpcut=(1400,2600))
bars(8,16,ride_on=True,arpcut=(2000,3600))
bars(16,22,ride_on=True,arpcut=(2600,4200))
bars(22,26,ride_on=True,arpcut=(2200,3800))
bars(26,28,kick_on=False,clap_on=False,bass_on=False,hats=True,arpcut=(900,2400))
bars(28,32,ride_on=False,clap_on=True,arpcut=(2400,1200))
def riser(d):
    t=tt(d);n=rng.standard_normal(len(t));o=np.zeros_like(n);seg=int(.02*SR)
    for i in range(0,len(n),seg):o[i:i+seg]=lp(n[i:i+seg+64],300+6000*(i/len(n))**2)[:len(o[i:i+seg])]
    return hp(o,200)*(t/d)**2
st(riser(1.9),.1,.16);st(riser(1.9),26.1,.16)
for k in range(8):st(clap()*(.3+.7*k/8),27.0+k*B/4,.2)
def bell(f,d=1.2):t=tt(d);return (np.sin(2*np.pi*f*t)+.3*np.sin(2*np.pi*f*3*t)*np.exp(-t*6))*np.exp(-t*3)*np.minimum(1,t/.003)
# sidechain
sc=np.ones(N)
for tb in np.arange(0,32,B):
    if 26<=tb<28:continue
    i=int(tb*SR);j=min(N,i+int(.3*SR));sc[i:j]=np.minimum(sc[i:j],1-.55*np.exp(-np.arange(j-i)/SR*10))
L*=sc;R*=sc
for j,m in enumerate((69,72,76,81)):st(bell(nt(m),1.8),26.3+j*.14,.16,(j-1.5)*.35)
# SFX: soft whoosh on each transition, gentle chime on price
SF=np.zeros(N)
def whoosh(d=.7):
    t=tt(d);n=rng.standard_normal(len(t));e=np.sin(np.pi*t/d)**2;o=np.zeros_like(n);seg=int(.02*SR)
    for i in range(0,len(n),seg):o[i:i+seg]=lp(n[i:i+seg+64],500+3500*np.sin(np.pi*i/len(n)))[:len(o[i:i+seg])]
    return hp(o,200)*e
def blip(f=1500):t=tt(.12);return np.sin(2*np.pi*f*t)*np.exp(-t*45)*np.minimum(1,t/.002)
def hit():t=tt(1.3);f=55*np.exp(-t*1.2)+28;return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*2.4)+.25*hp(lp(rng.standard_normal(len(t)),2500),120)*np.exp(-t*7)
def stab():t=tt(.9);s=sum(np.sin(2*np.pi*nt(m)*h*t)/h for m in (69,72,76) for h in (1,2,3));return lp(s,1600)*np.exp(-t*5)
EV=[(c-.35,whoosh(.5),.14) for c in [4,6,8,10,12,14,16,18,20,28]]+[(1.6,whoosh(.5),.2),(2.0,hit(),.45),(21.65,whoosh(.5),.2),(22.1,hit(),.3),(25.65,whoosh(.5),.18),
   (8.3,blip(),.1),(8.8,blip(),.1),(9.3,blip(),.1),(12.3,blip(),.1),(12.8,blip(),.1),(13.3,blip(),.1),(24.1,blip(1200),.12),(30.6,stab(),.25)]
last=-9
for t,s,g in sorted(EV,key=lambda e:e[0]):
    if t-last<.45:continue
    i=int(t*SR);j=min(N,i+len(s));SF[i:j]+=s[:j-i]/np.max(np.abs(s))*g;last=t
irm=rng.standard_normal(int(SR*1.8))*np.exp(-np.arange(int(SR*1.8))/SR*3.2);irm=lp(irm,6000);irm/=np.sum(np.abs(irm))/9
Lw=L+fftconvolve(L,irm)[:N]*.16+SF;Rw=R+fftconvolve(R,np.roll(irm,377))[:N]*.16+SF
fi=np.minimum(1,np.arange(N)/(SR*.6));fo=np.ones(N);i=int(31.0*SR);fo[i:]=np.linspace(1,0,N-i)
o=np.stack([Lw*fi*fo,Rw*fi*fo],1);o=np.tanh(o*1.4)/np.tanh(1.4);o/=np.max(np.abs(o))*1.12
import subprocess
def mp3(arr,name):
    raw=(np.clip(arr,-1,1)*32767).astype('<i2').tobytes();subprocess.run(['ffmpeg','-loglevel','error','-y','-f','s16le','-ar',str(SR),'-ac','2','-i','-','-b:a','256k',name],input=raw,check=True)
mp3(o,'trilha_final.mp3');fx=np.stack([SF,SF],1);fx=fx/np.max(np.abs(fx))*.8;mp3(fx,'so_efeitos.mp3');print('ok')

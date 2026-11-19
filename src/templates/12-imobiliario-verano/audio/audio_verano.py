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
def kick():t=tt(.45);f=48+90*np.exp(-t*30);return np.tanh(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7)*1.6)
def rim():t=tt(.12);return (np.sin(2*np.pi*820*t)*.6+hp(rng.standard_normal(len(t)),1800)*.5)*np.exp(-t*45)
def clap():t=tt(.35);n=hp(lp(rng.standard_normal(len(t)),6000),900);e=sum(np.exp(-np.maximum(t-d,0)*50)*(t>=d) for d in (0,.01,.02));return n*(e+np.exp(-t*8)*.2)*.6
def shk():t=tt(.1);return hp(rng.standard_normal(len(t)),6000)*np.sin(np.pi*t/.1)**2
def hat(o=False):d=.3 if o else .05;t=tt(d);return hp(rng.standard_normal(len(t)),8000)*np.exp(-t*(12 if o else 90))
def sub(f,d):t=tt(d);s=np.sin(2*np.pi*f*t)+.15*np.sin(4*np.pi*f*t);return lp(np.tanh(s*1.3),500)*np.minimum(1,t/.006)*np.minimum(1,np.maximum(d-t,0)/.03)
def rhodes(notes,d=1.6):
    t=tt(d);s=np.zeros(len(t))
    for m in notes:
        f=nt(m);mod=np.sin(2*np.pi*f*t)*1.6*np.exp(-t*4)
        s+=(np.sin(2*np.pi*f*t+mod)*np.exp(-t*1.6)+.2*np.sin(2*np.pi*2*f*t)*np.exp(-t*5))
    trem=1+.12*np.sin(2*np.pi*4.5*t)
    return s*trem*np.minimum(1,t/.004)*np.minimum(1,np.maximum(d-t,0)/.08)/len(notes)
def bell(f,d=1.2):t=tt(d);return (np.sin(2*np.pi*f*t)+.3*np.sin(2*np.pi*f*3*t)*np.exp(-t*6))*np.exp(-t*3)*np.minimum(1,t/.003)
# Dmaj7 - Bm9 - Gmaj7 - A6 (smooth, open voicings, no clusters)
CH=[[62,66,69,73],[59,62,66,69],[55,59,62,66],[57,61,64,66]]
RT=[38,35,31,33]
MEL=[(0,81),(1.5,78),(2.5,76),(4,78),(5,81),(6,83),(6.5,81)]
def section(a,b,kick_on=True,full=True,chords=True,mel=False):
    t0=a;bi=int(round(a/BAR))
    while t0<b-1e-6:
        r=RT[bi%4];ch=CH[bi%4]
        if chords:
            st(rhodes(ch,BAR*.48),t0,.30,-.1);st(rhodes(ch,BAR*.3),t0+1.5*B,.18,.15);st(rhodes(ch,BAR*.3),t0+2.5*B+.25,.16,-.15)
        for k in range(4):
            tb=t0+k*B
            if kick_on:st(kick(),tb,.9)
            if full:
                if k%2==1:st(clap(),tb,.32)
                st(hat(),tb+B/2,.10,.3);st(shk(),tb+B*.25,.05,-.4);st(shk(),tb+B*.75,.06,-.4)
                if k==3:st(hat(True),tb+B/2,.08,.3)
            elif kick_on: st(rim(),tb+B/2,.10,.2)
            if kick_on:st(sub(nt(r),B*.42),tb+B/2,.5)
            else: 
                if k==0:st(sub(nt(r),BAR*.9),tb,.35)
        if mel and bi%2==0:
            for bt,m in MEL:st(bell(nt(m)),t0+bt*B,.11,.25)
        t0+=BAR;bi+=1
# intro 0-4: chords only, filtered feel + swell
section(0,4,kick_on=False,full=False,chords=True,mel=False)
section(4,20,kick_on=True,full=True,chords=True,mel=True)
section(20,24,kick_on=False,full=False,chords=True,mel=True)   # map break
section(24,32,kick_on=True,full=True,chords=True,mel=True)
section(32,37.5,kick_on=True,full=False,chords=True,mel=False)  # CTA softer
st(rhodes(CH[0],2.5),36.0,.4);st(bell(nt(86),2.0),36.0,.12)
# riser into 4 and 24
def riser(d):
    t=tt(d);n=rng.standard_normal(len(t));o=np.zeros_like(n);seg=int(.02*SR)
    for i in range(0,len(n),seg):o[i:i+seg]=lp(n[i:i+seg+64],300+6000*(i/len(n))**2)[:len(o[i:i+seg])]
    return hp(o,200)*(t/d)**2
st(riser(2.0),2.0,.18);st(riser(2.0),22.0,.16)
# sidechain
sc=np.ones(N)
for tb in np.arange(4,37.6,B):
    if 20<=tb<24:continue
    i=int(tb*SR);j=min(N,i+int(.3*SR));sc[i:j]=np.minimum(sc[i:j],1-.45*np.exp(-np.arange(j-i)/SR*10))
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
wavfile.write('audio_verano.wav',SR,(o*32767).astype(np.int16));print('ok')

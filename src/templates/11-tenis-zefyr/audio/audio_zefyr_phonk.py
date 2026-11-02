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

# ================= MUSIC: funk-phonk 128bpm =================
L=np.zeros(N);R=np.zeros(N)
def st(sig,t,g=1.0,pan=0.0):
    gl=g*np.cos((pan+1)*np.pi/4)*1.414;gr=g*np.sin((pan+1)*np.pi/4)*1.414;add(L,sig,t,gl);add(R,sig,t,gr)
S16=B/4
def pk():
    t=tt(.5);f=50+130*np.exp(-t*30)+60*np.exp(-t*250);s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*5.5)
    return np.tanh(s*2.2)*.95+hp(rng.standard_normal(len(t)),3000)*np.exp(-t*350)*.3
def snr():
    t=tt(.3);body=np.sin(2*np.pi*np.cumsum(190+60*np.exp(-t*40))/SR)*np.exp(-t*22)*.5
    n=hp(lp(rng.standard_normal(len(t)),8000),1200);e=sum(np.exp(-np.maximum(t-d,0)*40)*(t>=d) for d in (0,.008,.017))
    return body+n*e*.8
def hh(o=False):d=.25 if o else .05;t=tt(d);return hp(rng.standard_normal(len(t)),8500)*np.exp(-t*(14 if o else 95))
def b808(f0,d,f1=None):
    t=tt(d);f=f0 if f1 is None else f0+(f1-f0)*np.clip((t-.03)/.08,0,1)
    s=np.sin(2*np.pi*np.cumsum(np.full(len(t),f) if np.isscalar(f) else f)/SR)
    s=np.tanh(s*3.0)/np.tanh(3.0);s=lp(s,1400)
    return s*np.minimum(1,t/.003)*np.minimum(1,np.maximum(d-t,0)/.02)*np.exp(-t*.8)
def cow(f,d=.16):
    t=tt(d);s=np.sign(np.sin(2*np.pi*f*t))*.6+np.sign(np.sin(2*np.pi*f*1.48*t))*.4
    s=hp(lp(s,3500),400);return s*np.minimum(1,t/.002)*np.exp(-t*16)
# riff (F# minor), steps over 2 bars (32 16ths): (step, midi)
RIFF=[(0,73),(3,73),(6,76),(8,73),(10,71),(12,69),(14,71),(16,73),(19,73),(22,76),(24,78),(26,76),(28,73),(30,71)]
KP=[0,3,6,8,11,14]           # funk/phonk kick pattern per bar (16ths)
BASS=[42,42,38,40]           # per bar roots F# F# D E
def bar_full(t0,bi,var=0,kick=True,drums=True,mel=True,bass=True,mel_lp=None):
    r=BASS[bi%4]
    if drums:
        if kick:
            for k in KP:st(pk(),t0+k*S16,.95)
        st(snr(),t0+4*S16,.5);st(snr(),t0+12*S16,.5)
        if var: st(snr()*.5,t0+15*S16,.22,.2)
        for k in range(16):
            if k%2==0 or var: st(hh(k%8==6 and var),t0+k*S16+(0.012 if k%2 else 0),.09 if k%2==0 else .055,-.35 if k%4==2 else .3)
    if bass:
        notes=[(0,3,r),(3,3,r),(6,2,r+12 if var else r),(8,3,r),(11,3,r+3),(14,2,r+7)]
        for st16,ln,m in notes:st(b808(nt(m),ln*S16*.95),t0+st16*S16,.55)
    if mel:
        half=(bi%2)*16
        for stp,m in RIFF:
            if half<=stp<half+16:
                c=cow(nt(m));
                if mel_lp:c=lp(c,mel_lp)
                st(c,t0+(stp-half)*S16,.20,.12 if stp%2 else -.12)
def bars(t_start,t_end,**kw):
    t0=t_start;bi=0
    while t0<t_end-1e-6:
        bar_full(t0,bi,**kw);t0+=BAR;bi+=1
# --- arrangement synced to scenes ---
# intro 0-3.75: cowbell riff opening filter + snare roll
for bi in range(2):
    for stp,m in RIFF:
        if bi*16<=stp<bi*16+16:
            tt0=bi*BAR+(stp-bi*16)*S16;c=lp(cow(nt(m)),700+3000*(tt0/3.75)**1.5);st(c,tt0,.20)
for k in range(8):st(snr()*(.25+.75*k/8),DROP-B*2+k*S16,.3)
st(b808(nt(42),B*1.5),DROP-B*2,.25)
bars(DROP,15.0,var=0)
bars(15.0,18.75,kick=False,drums=False,mel=True,bass=False,mel_lp=1800)   # levitate breakdown
for bi in range(2):st(b808(nt(BASS[bi]),BAR*.9),15.0+bi*BAR,.45)
for k in range(8):st(snr()*(.25+.75*k/8),18.75-B*2+k*S16,.3)
bars(18.75,30.0,var=1)
# drop scene: filtered break until landing at 31.875
bars(30.0,31.875,kick=False,drums=False,bass=False,mel=True,mel_lp=1200)
bars(31.875,37.5,var=1)
st(pk(),37.5,1.0);st(b808(nt(42),1.6),37.5,.6);st(cow(nt(73),.5),37.5,.25)
# --- stops synced to visuals: impact freeze (one beat), pre-drop gaps ---
def mute(a,b):
    i,j=int(a*SR),int(b*SR);fl=int(.004*SR);L[i:j]*=0;R[i:j]*=0
mute(7.5+6*B+0.0005,7.5+7*B)        # impact freeze: music cuts for 1 beat under the boom
mute(3.62,DROP);mute(18.66,18.75);mute(31.80,31.875)
# sidechain
scv=np.ones(N)
for t0 in np.arange(DROP,37.6,BAR):
    for k in KP:
        i=int((t0+k*S16)*SR);j=min(N,i+int(.22*SR))
        if i<N:scv[i:j]=np.minimum(scv[i:j],1-.45*np.exp(-np.arange(j-i)/SR*14))
irm=rng.standard_normal(int(SR*1.1))*np.exp(-np.arange(int(SR*1.1))/SR*5.5);irm=lp(irm,6000);irm/=np.sum(np.abs(irm))/9
Lw=L+fftconvolve(L,irm)[:N]*.09;Rw=R+fftconvolve(R,np.roll(irm,421))[:N]*.09
Lw*=scv**.5;Rw*=scv**.5
ir=rng.standard_normal(int(SR*1.2))*np.exp(-np.arange(int(SR*1.2))/SR*5);ir=lp(ir,6000);ir/=np.sum(np.abs(ir))/10
sfxw=sfx+fftconvolve(sfx,ir)[:N]*.15
oL=Lw*.7+sfxw*.55;oR=Rw*.7+sfxw*.55
fo=np.ones(N);i=int(38.6*SR);fo[i:]=np.linspace(1,0,N-i)**.8;oL*=fo;oR*=fo
o=np.stack([oL,oR],1);o=np.tanh(o*1.6)/np.tanh(1.6);o/=np.max(np.abs(o))*1.12
wavfile.write('audio_zefyr_phonk.wav',SR,(o*32767).astype(np.int16));print('ok')

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter,sosfilt,fftconvolve
SR=44100;BT=60/125;BAR=BT*4;DUR=BAR*19;N=int(SR*DUR);rng=np.random.default_rng(77)
def tt(d):return np.arange(int(d*SR))/SR
def lpf(x,fc):return sosfilt(butter(2,fc,'low',fs=SR,output='sos'),x)
def hpf(x,fc):return sosfilt(butter(2,fc,'high',fs=SR,output='sos'),x)
def bpf(x,a,b):return sosfilt(butter(2,[a,b],'band',fs=SR,output='sos'),x)
nt=lambda m:440*2**((m-69)/12)
L=np.zeros(N);R=np.zeros(N)
def st(s,t,g=1.,pan=0.):
    i=int(round(t*SR));j=min(N,i+len(s))
    if i<0 or i>=N:return
    gl=g*np.cos((pan+1)*np.pi/4)*1.414;gr=g*np.sin((pan+1)*np.pi/4)*1.414;L[i:j]+=s[:j-i]*gl;R[i:j]+=s[:j-i]*gr
# ---- instruments ----
def kick():t=tt(.42);return np.tanh(np.sin(2*np.pi*np.cumsum(47+110*np.exp(-t*35))/SR)*np.exp(-t*7)*1.5)
def rim():t=tt(.07);return (np.sin(2*np.pi*1750*t)*.7+hpf(rng.standard_normal(len(t)),2500)*.6)*np.exp(-t*70)
def shaker(acc=False):t=tt(.09);return hpf(rng.standard_normal(len(t)),5500)*np.sin(np.pi*t/.09)**(1.5 if acc else 3)
def clap():t=tt(.35);n=bpf(rng.standard_normal(len(t)),900,7000);e=sum(np.exp(-np.maximum(t-d,0)*55)*(t>=d) for d in (0,.01,.02));return n*(e+np.exp(-t*9)*.2)*.6
def ohat():t=tt(.2);return hpf(rng.standard_normal(len(t)),8000)*np.exp(-t*16)
def conga(f=220):t=tt(.25);return np.sin(2*np.pi*np.cumsum(f*(1+.4*np.exp(-t*40)))/SR)*np.exp(-t*14)+bpf(rng.standard_normal(len(t)),500,3000)*np.exp(-t*80)*.3
def nylon(f,d=.9):
    t=tt(d);s=sum(g*np.sin(2*np.pi*f*k*t)*np.exp(-t*dc) for k,(g,dc) in enumerate([(1,3.2),(.55,4.5),(.3,6.5),(.16,9),(.08,12)],1))
    return (s+lpf(rng.standard_normal(len(t)),f*4)*np.exp(-t*120)*.2)*np.minimum(1,t/.002)*np.clip((d-t)/.06,0,1)
def gchord(ms,d=.45):
    o=np.zeros(int((d+.1)*SR))
    for i,m in enumerate(ms):s=nylon(nt(m),d);j=int(i*.012*SR);o[j:j+len(s)]+=s[:len(o)-j]
    return o/len(ms)
def ubass(f,d):
    t=tt(d);s=np.sin(2*np.pi*f*t)+.35*np.sin(2*np.pi*2*f*t)*np.exp(-t*6)+.12*np.sin(2*np.pi*3*f*t)*np.exp(-t*9)
    return lpf(np.tanh(s*1.2),800)*np.minimum(1,t/.006)*np.exp(-t*2.2)*np.clip((d-t)/.03,0,1)
def rhodes(ms,d=1.2):
    t=tt(d);s=np.zeros(len(t))
    for m in ms:
        f=nt(m);s+=np.sin(2*np.pi*f*t+np.sin(2*np.pi*f*t)*1.4*np.exp(-t*5))*np.exp(-t*1.8)
    return s*(1+.1*np.sin(2*np.pi*5*t))*np.minimum(1,t/.004)*np.clip((d-t)/.08,0,1)/len(ms)
def flute(f,d):
    t=tt(d);vib=1+.004*np.sin(2*np.pi*5.2*t)*np.minimum(1,t/.25)
    s=np.sin(2*np.pi*np.cumsum(np.full(len(t),f)*vib)/SR)+.12*np.sin(2*np.pi*2*f*t)+bpf(rng.standard_normal(len(t)),f*.8,f*3)*.05
    return s*np.minimum(1,t/.06)*np.clip((d-t)/.12,0,1)
# ii-V-I-IV in G: Am9 - D9 - Gmaj9 - Cmaj7(#11)
CH=[[57,60,64,67,71],[54,57,60,64,62+12],[55,59,62,66,69],[52,55,59,64,66]]
GT=[[57,64,67,72],[54,60,64,69],[55,62,66,71],[52,59,64,66]]   # guitar voicings (no clusters)
RT=[45,38,43,48]
# bossa comp rhythm (16th steps in a bar)
COMP=[0,3,6,10,13]
# 3-2 bossa clave (2 bars, 16th steps)
CLAVE=[0,3,6,10,13, 16+3,16+6,16+10]
MEL=[(0,76,1.5),(2,74,.5),(2.5,72,.5),(3,71,1.0),(4,69,1.5),(6,71,.5),(6.5,72,.5),(7,74,1)]  # beats over 2 bars
S16=BT/4
def bars(a,b,kick_on=True,clap_on=True,hats=True,comp=True,bass=True,keys=True,mel=False,perc=True,gtr_lp=None):
    t0=a;bi=int(round(a/BAR))
    while t0<b-1e-6:
        i4=bi%4
        if comp:
            for s16 in COMP:
                c=gchord(GT[i4],.42 if s16 in(3,10) else .3)
                if gtr_lp:c=lpf(c,gtr_lp)
                st(c,t0+s16*S16,.42,-.25)
        if keys:st(rhodes(CH[i4][:4],BAR*.95),t0,.16,.25)
        if bass:
            r=RT[i4];st(ubass(nt(r),BT*1.4),t0,.62);st(ubass(nt(r+7),BT*.9),t0+BT*1.5,.5);st(ubass(nt(r+12 if i4%2 else r),BT*.9),t0+BT*2.5,.45);st(ubass(nt(r+7),BT*.5),t0+BT*3.5,.4)
        for k in range(4):
            tb=t0+k*BT
            if kick_on:st(kick(),tb,.85)
            if clap_on and k%2==1:st(clap(),tb,.26)
            if hats:st(ohat(),tb+BT/2,.07,.3)
        if perc:
            for s16 in range(16):st(shaker(s16%4==2),t0+s16*S16+(.01 if s16%2 else 0),.06 if s16%2 else .09,-.35)
            for s in CLAVE:
                if (bi%2==0 and s<16) or (bi%2==1 and s>=16):st(rim(),t0+(s%16)*S16,.10,.45)
            st(conga(230),t0+BT*1.75,.12,.5);st(conga(180),t0+BT*3.25,.12,.5);st(conga(230),t0+BT*3.75,.08,.5)
        if mel and bi%2==0:
            for bt,m,d in MEL:st(flute(nt(m+12),d*BT*1.05),t0+bt*BT,.10,.1)
        t0+=BAR;bi+=1
B2=BAR*2
# S1 hook (0-2 bars): guitar + rim + shaker, no kick; cherry landing accent
bars(0,B2,kick_on=False,clap_on=False,hats=False,bass=False,keys=False,perc=True,gtr_lp=2500)
# S2-S7 (2..14 bars): full groove, flute melody from S3
bars(B2,BAR*4,mel=False)
bars(BAR*4,BAR*14,mel=True)
# S8 Pinheiros novidade (14..16): breakdown – keys + shaker + bass, no kick
bars(BAR*14,BAR*16,kick_on=False,clap_on=False,hats=False,comp=False,bass=True,keys=True,perc=True,mel=False)
# S9 CTA (16..19)
bars(BAR*16,BAR*18.5,mel=True)
st(gchord(GT[2],2.0),BAR*18.5,.5);st(rhodes(CH[2][:4],2.5),BAR*18.5,.25);st(ubass(nt(43),2.0),BAR*18.5,.6);st(kick(),BAR*18.5,.9)
# rises into S2 and S9
def riser(d):
    t=tt(d);n=rng.standard_normal(len(t));o=np.zeros_like(n);seg=int(.02*SR)
    for i in range(0,len(n),seg):o[i:i+seg]=lpf(n[i:i+seg+64],300+6000*(i/len(n))**2)[:len(o[i:i+seg])]
    return hpf(o,200)*(t/d)**2
st(riser(1.9),B2-1.9,.16);st(riser(1.9),BAR*16-1.9,.16)
# sidechain
sc=np.ones(N)
for tb in np.arange(B2,BAR*18.6,BT):
    if BAR*14<=tb<BAR*16:continue
    i=int(tb*SR);j=min(N,i+int(.25*SR));sc[i:j]=np.minimum(sc[i:j],1-.35*np.exp(-np.arange(j-i)/SR*12))
L*=sc;R*=sc
# ---- SFX ----
SF=np.zeros(N)
def whoosh(d=.5):
    t=tt(d);n=rng.standard_normal(len(t));e=np.sin(np.pi*t/d)**2;o=np.zeros_like(n);seg=int(.02*SR)
    for i in range(0,len(n),seg):o[i:i+seg]=lpf(n[i:i+seg+64],600+4000*np.sin(np.pi*i/len(n)))[:len(o[i:i+seg])]
    return hpf(o,200)*e
def pop():t=tt(.16);f=650*(1+1.2*np.exp(-t*45));return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*26)
def tick():t=tt(.05);return hpf(rng.standard_normal(len(t)),3000)*np.exp(-t*120)
def chime(f=1568):t=tt(1.2);return sum(a*np.sin(2*np.pi*f*m*t)*np.exp(-t*k) for m,a,k in [(1,1,3),(1.335,.6,4),(1.68,.35,5)])*np.minimum(1,t/.003)
EV=[(BT*3,pop(),.5),(B2-.25,whoosh(.5),.35)]
for c in [BAR*4,BAR*6,BAR*8,BAR*10,BAR*12,BAR*14,BAR*16]:EV.append((c-.12,whoosh(.45),.32))
EV+= [(BAR*4+BT*5.2+.25,pop(),.45),(BAR*4+BT*6.3,chime(1568),.22)]
EV+= [(BAR*6+BT*.6+k*BT,tick(),.18) for k in range(1,6)]
EV+= [(BAR*14+BT*2.2,chime(1318),.2),(BAR*14+BT*3.6,pop(),.35)]
EV+= [(BAR*16+BT*3.1+.25,pop(),.45),(BAR*16+BT*4.5,chime(1568),.22)]
last=-9
for t,s,g in sorted(EV,key=lambda e:e[0]):
    if t-last<.45:continue
    i=int(t*SR);j=min(N,i+len(s));SF[i:j]+=s[:j-i]/np.max(np.abs(s))*g;last=t
irm=rng.standard_normal(int(SR*1.5))*np.exp(-np.arange(int(SR*1.5))/SR*4);irm=lpf(irm,6000);irm/=np.sum(np.abs(irm))/9
Lw=L+fftconvolve(L,irm)[:N]*.12+SF*.8;Rw=R+fftconvolve(R,np.roll(irm,313))[:N]*.12+SF*.8
fi=np.minimum(1,np.arange(N)/(SR*.3));fo=np.ones(N);i=int((DUR-.6)*SR);fo[i:]=np.linspace(1,0,N-i)
o=np.stack([Lw*fi*fo,Rw*fi*fo],1);o=np.tanh(o*1.3)/np.tanh(1.3);o/=np.max(np.abs(o))*1.12
wavfile.write('audio_cereja.wav',SR,(o*32767).astype(np.int16));print('ok',DUR)

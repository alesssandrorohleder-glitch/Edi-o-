import numpy as np
from scipy.io import wavfile
from scipy.signal import butter,sosfilt,fftconvolve
SR=44100;BT=.5;BAR=2.;DUR=40.;N=int(SR*DUR);rng=np.random.default_rng(9)
def tt(d):return np.arange(int(d*SR))/SR
def lpf(x,f):return sosfilt(butter(2,f,'low',fs=SR,output='sos'),x)
def hpf(x,f):return sosfilt(butter(2,f,'high',fs=SR,output='sos'),x)
def bpf(x,a,b):return sosfilt(butter(2,[a,b],'band',fs=SR,output='sos'),x)
nt=lambda m:440*2**((m-69)/12)
L=np.zeros(N);R=np.zeros(N)
def st(s,t,g=1.,pan=0.):
    i=int(round(t*SR));j=min(N,i+len(s))
    if i<0 or i>=N:return
    L[i:j]+=s[:j-i]*g*np.cos((pan+1)*np.pi/4)*1.414;R[i:j]+=s[:j-i]*g*np.sin((pan+1)*np.pi/4)*1.414
S16=BT/4
def kick():t=tt(.45);return np.tanh(np.sin(2*np.pi*np.cumsum(46+140*np.exp(-t*34))/SR)*np.exp(-t*6.5)*1.9)+hpf(rng.standard_normal(len(t)),3000)*np.exp(-t*400)*.25
def snare():t=tt(.28);body=np.sin(2*np.pi*np.cumsum(200+80*np.exp(-t*40))/SR)*np.exp(-t*25)*.6;n=bpf(rng.standard_normal(len(t)),1500,9000)*np.exp(-t*22);return body+n
def clap():t=tt(.3);n=bpf(rng.standard_normal(len(t)),1000,7000);e=sum(np.exp(-np.maximum(t-d,0)*55)*(t>=d) for d in(0,.01,.02));return n*(e+np.exp(-t*10)*.2)*.7
def tom(f=140):t=tt(.25);return np.sin(2*np.pi*np.cumsum(f*(1+.5*np.exp(-t*30)))/SR)*np.exp(-t*14)
def hat(o=False):d=.2 if o else .04;t=tt(d);return hpf(rng.standard_normal(len(t)),9000)*np.exp(-t*(15 if o else 110))
def b808(f,d):t=tt(d);fr=f*(1+.6*np.exp(-t*30));s=np.sin(2*np.pi*np.cumsum(fr)/SR);return lpf(np.tanh(s*2.2),900)*np.minimum(1,t/.003)*np.clip((d-t)/.03,0,1)
def stab(ms,d=.22):
    t=tt(d);s=np.zeros(len(t))
    for m in ms:
        f=nt(m);s+=sum(np.sin(2*np.pi*f*h*t)/h for h in range(1,8))
    return lpf(s,4200)*np.minimum(1,t/.002)*np.exp(-t*9)/len(ms)
def lead(f,d=.25):t=tt(d);s=np.sign(np.sin(2*np.pi*f*t))*.5+np.sin(2*np.pi*f*t)*.5;return lpf(s,3500)*np.minimum(1,t/.003)*np.exp(-t*6)
# G#m - E - B - F# (pop-funk, minor energetic)
CH=[[68,71,75],[68,71,76],[66,71,75],[66,70,73]];RT=[32,28,35,30]
K=[0,3,7,8,11];SN=[4,12];TM=[6,14]
HOOK=[(0,75),(1.5,78),(3,80),(4,78),(5.5,75),(6,73),(7,71),(9.5,75),(11,73),(12,71),(14,68)]  # 16ths over 1 bar? use 16th steps across 2 bars
def bars(a,b,drums=True,keys=True,hook=False,bass=True,half=False):
    t0=a;bi=int(round(a/BAR))
    while t0<b-1e-6:
        i4=bi%4
        for half_ in (0,1):
            hb=t0+half_*BAR/2
            if drums:
                for k in K:
                    if k<8:st(kick(),hb+k*S16*1,.95)
                for k in SN:
                    if k<8:pass
                st(snare(),hb+4*S16,.4);st(clap(),hb+4*S16,.25)
                st(tom(150),hb+6*S16,.22,.3)
                for k in range(8):st(hat(k%4==2),hb+k*S16,.07 if k%2 else .1,-.3)
            if bass:
                for k in ([0,3,7] if not half else [0]):st(b808(nt(RT[i4]),S16*2.6),hb+k*S16,.6)
            if keys:
                for k in (2,5):st(stab(CH[i4]),hb+k*S16,.24,.15)
        if hook and bi%2==0:
            for stp,m in HOOK:st(lead(nt(m)),t0+stp*S16*2/2,.12,-.15)
        t0+=BAR;bi+=1
bars(0,3.5,drums=False,bass=False,keys=True)
for k in range(8):st(snare()*(.3+.7*k/8),3.5+k*S16/2*2/2,.25)
bars(4,16,hook=True)
bars(16,20,hook=False)
bars(20,28,hook=True)
bars(28,34,hook=True)
bars(34,39.5,drums=True,hook=False,keys=True)
st(stab(CH[0],1.0),39.5,.4);st(kick(),39.5,1.0);st(b808(nt(32),1.0),39.5,.6)
def riser(d):
    t=tt(d);n=rng.standard_normal(len(t));o=np.zeros_like(n);seg=int(.02*SR)
    for i in range(0,len(n),seg):o[i:i+seg]=lpf(n[i:i+seg+64],300+6000*(i/len(n))**2)[:len(o[i:i+seg])]
    return hpf(o,200)*(t/d)**2
st(riser(1.6),2.4,.2)
sc=np.ones(N)
for tb in np.arange(4,39.6,BT):
    i=int(tb*SR);j=min(N,i+int(.25*SR));sc[i:j]=np.minimum(sc[i:j],1-.3*np.exp(-np.arange(j-i)/SR*12))
L*=sc;R*=sc
SF=np.zeros(N)
def whoosh(d=.4):
    t=tt(d);n=rng.standard_normal(len(t));e=np.sin(np.pi*t/d)**2;o=np.zeros_like(n);seg=int(.02*SR)
    for i in range(0,len(n),seg):o[i:i+seg]=lpf(n[i:i+seg+64],600+5000*np.sin(np.pi*i/len(n)))[:len(o[i:i+seg])]
    return hpf(o,200)*e
def impact(f=60,d=.7):t=tt(d);return np.tanh(np.sin(2*np.pi*np.cumsum(f+150*np.exp(-t*30))/SR)*np.exp(-t*5)*1.5)+hpf(rng.standard_normal(len(t)),2000)*np.exp(-t*40)*.3
def pop():t=tt(.16);return np.sin(2*np.pi*np.cumsum(600*(1+1.2*np.exp(-t*45)))/SR)*np.exp(-t*26)
def crumple():t=tt(.5);return bpf(rng.standard_normal(len(t)),1500,7000)*(np.abs(np.sin(t*70))**4)*np.exp(-t*4)
def ding():t=tt(1.2);return sum(a*np.sin(2*np.pi*f*t)*np.exp(-t*k) for f,a,k in[(2093,1,3),(2637,.6,3.5),(3136,.4,4)])*np.minimum(1,t/.002)
def tick():t=tt(.05);return hpf(rng.standard_normal(len(t)),3000)*np.exp(-t*120)
EV=[(.5,impact(80,.4),.4),(1.0,impact(55,.9),.7),(1.3,whoosh(.4),.25),(2.6,crumple(),.35),(3.1,whoosh(.35),.3),
    (4.0,impact(50,1.0),.8),(5.2,pop(),.3),(6.5,pop(),.35),(7.0,whoosh(.6),.2)]
for c in [8,12,16,20,24,28,34]:EV.append((c-.05,whoosh(.4),.32))
EV+=[(9.0,impact(70,.5),.45),(10.75,tick(),.25),(11.3,pop(),.4),
     (12.3,pop(),.3),(14.6,whoosh(.5),.25),(15.3,ding(),.15),
     (20.8,whoosh(.35),.25),(21.6,whoosh(.35),.25),(23.0,tick(),.2),
     (24.7,pop(),.3),(26.5,pop(),.25),
     (28.6,whoosh(.4),.25),(29.5,impact(55,1.0),.75),(29.95,ding(),.25),(30.6,pop(),.35),(31.1,pop(),.35),(31.6,pop(),.35),
     (34.6,impact(55,.8),.6),(37.0,pop(),.35),(37.6,tick(),.2)]
EV=[(e[0]+4 if e[0]>=16 else e[0],e[1],e[2]) if not (e[1] is None) else e for e in EV] if False else EV
EV+=[(16.6,whoosh(.4),.25),(17.4,tick(),.2),(18.0,tick(),.2),(18.7,tick(),.2),(19.3,tick(),.2)]
last=-9
for t,s,g in sorted(EV,key=lambda e:e[0]):
    if t-last<.45:continue
    i=int(t*SR);j=min(N,i+len(s));SF[i:j]+=s[:j-i]/np.max(np.abs(s))*g;last=t
ir=rng.standard_normal(int(SR*1.2))*np.exp(-np.arange(int(SR*1.2))/SR*5);ir=lpf(ir,6000);ir/=np.sum(np.abs(ir))/10
Lw=L+fftconvolve(L,ir)[:N]*.08+SF*.75;Rw=R+fftconvolve(R,np.roll(ir,301))[:N]*.08+SF*.75
fo=np.ones(N);i=int(39.6*SR);fo[i:]=np.linspace(1,0,N-i)
o=np.stack([Lw*fo,Rw*fo],1);o=np.tanh(o*1.4)/np.tanh(1.4);o/=np.max(np.abs(o))*1.12
wavfile.write('audio_metro2.wav',SR,(o*32767).astype(np.int16))
o2=np.stack([SF*fo,SF*fo],1);o2/=np.max(np.abs(o2))*1.6
wavfile.write('audio_metro_sfx2.wav',SR,(o2*32767).astype(np.int16));print('ok')

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
def kick():t=tt(.4);return np.tanh(np.sin(2*np.pi*np.cumsum(50+110*np.exp(-t*35))/SR)*np.exp(-t*8)*1.5)
def clap():t=tt(.3);n=bpf(rng.standard_normal(len(t)),1000,7000);e=sum(np.exp(-np.maximum(t-d,0)*55)*(t>=d) for d in(0,.012,.024));return n*(e+np.exp(-t*9)*.25)*.7
def shaker(acc=False):t=tt(.09);return hpf(rng.standard_normal(len(t)),5500)*np.sin(np.pi*t/.09)**(1.5 if acc else 3)
def steel(f,d=.6):
    t=tt(d);s=sum(g*np.sin(2*np.pi*f*k*t)*np.exp(-t*dc) for k,(g,dc) in enumerate([(1,4),(.7,5),(.5,7),(.3,9),(.2,12),(.12,15)],1))
    return (s+hpf(rng.standard_normal(len(t)),3000)*np.exp(-t*90)*.15)*np.minimum(1,t/.002)*np.clip((d-t)/.04,0,1)
def strum(ms,d=.5,down=True):
    o=np.zeros(int((d+.1)*SR));ms=ms if down else ms[::-1]
    for i,m in enumerate(ms):s_=steel(nt(m),d);j=int(i*.009*SR);o[j:j+len(s_)]+=s_[:len(o)-j]
    return o/len(ms)
def piano(ms,d=.4):
    t=tt(d);s=np.zeros(len(t))
    for m in ms:
        f=nt(m);s+=sum(a_*np.sin(2*np.pi*f*h*t)*np.exp(-t*(2.5+h*1.5)) for h,a_ in[(1,1),(2,.45),(3,.2)])
    return s*np.minimum(1,t/.003)*np.clip((d-t)/.04,0,1)/len(ms)
def bass(f,d):t=tt(d);s=np.sin(2*np.pi*f*t)+.3*np.sin(2*np.pi*2*f*t);return lpf(np.tanh(s*1.2),600)*np.minimum(1,t/.005)*np.clip((d-t)/.03,0,1)
def whistle(f,d):t=tt(d);vib=1+.006*np.sin(2*np.pi*5.5*t)*np.minimum(1,t/.15);return (np.sin(2*np.pi*np.cumsum(np.full(len(t),f)*vib)/SR)+bpf(rng.standard_normal(len(t)),f*.9,f*1.2)*.04)*np.minimum(1,t/.03)*np.clip((d-t)/.08,0,1)
# D - A - Bm - G (feel-good major)
GT=[[50,57,62,66,69],[45,52,57,61,64],[47,54,59,62,66],[43,50,55,59,62]];RT=[38,45,47,43]
PIANO=[[66,69,74],[64,69,73],[66,71,74],[67,71,74]]
STR=[(0,1,.5),(2,0,.3),(3,1,.35),(5,0,.3),(6,1,.4),(7,0,.3)]   # eighth-note strum pattern (index, down?, dur)
MEL=[(0,78,1),(1,81,.5),(1.5,83,.5),(2,81,1),(3,78,.5),(3.5,76,.5),(4,74,1.5),(6,76,.5),(6.5,78,.5),(7,81,1)]
def bars(a,b,drums=True,gtr=True,keys=True,mel=False,bassl=True):
    t0=a;bi=int(round(a/BAR))
    while t0<b-1e-6:
        i4=bi%4
        if gtr:
            for e8,dn,d in STR:st(strum(GT[i4],d,bool(dn)),t0+e8*BT/2,.38,-.3)
        if keys:st(piano(PIANO[i4],1.6),t0,.18,.3);st(piano(PIANO[i4],.4),t0+BT*2.5,.12,.3)
        for k in range(4):
            tb=t0+k*BT
            if drums:
                st(kick(),tb,.85)
                if k%2:st(clap(),tb,.42)
                for q in range(4):st(shaker(q==2),tb+q*S16,.08 if q%2 else .05,.35)
            if bassl:st(bass(nt(RT[i4]),BT*.9),tb,.5);st(bass(nt(RT[i4]+12 if k==3 else RT[i4]),BT*.4),tb+BT*.75,.32)
        if mel and bi%2==0:
            for bt,m,d in MEL:st(whistle(nt(m),d*BT*.95),t0+bt*BT,.13,.1)
        t0+=BAR;bi+=1
bars(0,4,drums=False,keys=False,bassl=False)
bars(4,16,mel=True)
bars(16,20,mel=False,keys=True)
bars(20,34,mel=True)
bars(34,39.5,mel=False)
st(strum(GT[0],1.8),39.5,.5);st(piano(PIANO[0],2),39.5,.3);st(kick(),39.5,.9);st(bass(nt(38),1.2),39.5,.5)
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
wavfile.write('audio_metro3.wav',SR,(o*32767).astype(np.int16))
o2=np.stack([SF*fo,SF*fo],1);o2/=np.max(np.abs(o2))*1.6
wavfile.write('audio_metro_sfx3.wav',SR,(o2*32767).astype(np.int16));print('ok')

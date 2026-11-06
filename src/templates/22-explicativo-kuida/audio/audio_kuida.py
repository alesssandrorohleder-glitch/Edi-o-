# kuida — trilha pop leve 120bpm (C–G–Am–F) para explicativo + efeitos de UI. Gera trilha_final.mp3 e so_efeitos.mp3
# Regras: sem detune (uma frequência por nota), efeitos com >= 0,45s de distância, níveis suaves p/ textos.
import numpy as np, subprocess, os
from scipy.signal import butter, sosfilt, fftconvolve
SR=44100; BPM=120; BT=60/BPM; DUR=36.0; N=int(SR*DUR); HERE=os.path.dirname(os.path.abspath(__file__))
rng=np.random.default_rng(7)
mus=np.zeros((N,2)); sfx=np.zeros((N,2)); verb=np.zeros((N,2))
def add(buf,t,sig,g=1.,pan=0.):
    i=int(t*SR); n=min(len(sig),N-i)
    if n<=0 or i<0: return
    l=np.cos((pan+1)*np.pi/4)*1.414; r=np.sin((pan+1)*np.pi/4)*1.414
    buf[i:i+n,0]+=sig[:n]*g*l; buf[i:i+n,1]+=sig[:n]*g*r
def tt(d): return np.arange(int(d*SR))/SR
def bp(x,lo,hi,o=2): return sosfilt(butter(o,[lo,hi],'band',fs=SR,output='sos'),x)
def hp(x,f,o=2): return sosfilt(butter(o,f,'high',fs=SR,output='sos'),x)
def lp(x,f,o=2): return sosfilt(butter(o,f,'low',fs=SR,output='sos'),x)
mf=lambda m:440*2**((m-69)/12)
# ---------- instrumentos ----------
def kick():
    t=tt(.42); f=48+150*np.exp(-t*32); s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7.5)
    return s+ .25*hp(rng.standard_normal(len(t)),3000)*np.exp(-t*90)
def clap():
    t=tt(.3); n=bp(rng.standard_normal(len(t)),900,3200); e=np.zeros(len(t))
    for d in (0,.011,.022): e+=np.exp(-np.clip(t-d,0,None)*60)*(t>=d)
    return n*(e*.5+np.exp(-t*14)*.5)*.8
def hat(op=False):
    t=tt(.35 if op else .06); return hp(rng.standard_normal(len(t)),7500)*np.exp(-t*(9 if op else 70))
def pluck(m,d=.5,br=1.):
    t=tt(d); f=mf(m); s=np.zeros(len(t))
    for h,a in ((1,1),(2,.45),(3,.22),(4,.1)): s+=a*np.sin(2*np.pi*f*h*t)*np.exp(-t*(5+h*4*br))
    return s*np.minimum(1,t/.003)
def pad(ms,d):
    t=tt(d); s=sum(np.sin(2*np.pi*mf(m)*t)+.3*np.sin(2*np.pi*mf(m)*2*t) for m in ms)/len(ms)
    return lp(s,1800)*np.minimum(1,t/.4)*np.minimum(1,(d-t)/.5)
def sub(m,d):
    t=tt(d); return np.sin(2*np.pi*mf(m)*t)*np.minimum(1,t/.004)*np.exp(-t*3)
def bell(m,d=1.2):
    t=tt(d); f=mf(m); return (np.sin(2*np.pi*f*t)+.35*np.sin(2*np.pi*f*2.0*t)*np.exp(-t*6))*np.exp(-t*3.2)*np.minimum(1,t/.002)
CH=[(60,[60,64,67,72]),(55,[55,59,62,67]),(57,[57,60,64,69]),(53,[53,57,60,65])]   # C G Am F
def chord(t): return CH[int(t//2)%4]
# ---------- arranjo ----------
for bar in range(18):
    t0=bar*2; root,ns=chord(t0)
    intro=t0<4; brk=28<=t0<32; outro=t0>=32
    if intro or brk: add(verb,t0,pad(ns,2.05),.35)
    for bt in range(4):
        tb=t0+bt*BT
        groove=4.5<=tb<29 or tb>=32
        if groove:
            add(mus,tb,kick(),.95)
            if bt in (1,3): add(mus,tb,clap(),.42); add(verb,tb,clap(),.12)
            add(mus,tb+BT/2,hat(bt==3),.22 if bt==3 else .2,.25)
            for q in (.25,.75): add(mus,tb+q*BT,hat(),.09,-.25)
            add(mus,tb+BT/2,sub(root-24,BT*.45),.55)
        if groove and not outro:
            for q,ix in ((.5,0),(1.5,1),(2.25,2),(3.5,3)):
                if int(q)==bt:
                    for m in ns[:3]: add(mus,t0+q*BT,pluck(m+12,.35),.075,.15); add(verb,t0+q*BT,pluck(m+12,.35),.05)
        if 9<=tb<25:   # arpejo em 16 avos dá energia no meio
            for s16 in range(4):
                m=ns[(bt*4+s16)%4]+24; add(mus,tb+s16*BT/4,pluck(m,.18,1.6),.035,.4*np.sin(s16)); add(verb,tb+s16*BT/4,pluck(m,.18,1.6),.02)
# riser da intro
t=tt(.9); r=bp(rng.standard_normal(len(t)),300,6000)*(t/.9)**2.2; add(mus,3.6,r,.16)
for bar in range(2):
    for bt in range(4): add(mus,bar*2+bt*BT,pluck([72,76,79,76][bt],.4),.07); add(verb,bar*2+bt*BT,pluck([72,76,79,76][bt],.4),.05)
# sonic logo (kuida): C6 E6 G6 C7
for j,m in enumerate((84,88,91,96)): add(mus,29.6+j*.12,bell(m,1.6),.22,(j-1.5)*.3); add(verb,26.3+j*.12,bell(m,1.6),.25)
# sidechain
env=np.ones(N)
for k in range(72):
    tb=k*BT
    if 4.5<=tb<29 or tb>=32:
        i=int(tb*SR); n=min(int(.3*SR),N-i); env[i:i+n]=1-.55*np.exp(-np.arange(n)/SR*14)
# reverb
ir_t=tt(1.8); IR=np.stack([rng.standard_normal(len(ir_t))*np.exp(-ir_t*3.2) for _ in range(2)],1); IR=lp(IR.T,6000).T
wet=np.stack([fftconvolve(verb[:,c],IR[:,c])[:N] for c in range(2)],1)*.12
music=(mus+wet)*env[:,None]
# fade final
fo=np.clip((DUR-np.arange(N)/SR)/1.0,0,1); music*=fo[:,None]
# ---------- efeitos ----------
def tick(): t=tt(.05); return np.sin(2*np.pi*2600*t)*np.exp(-t*90)
def tap(): t=tt(.08); return np.sin(2*np.pi*1150*t)*np.exp(-t*60)+.4*np.sin(2*np.pi*180*t)*np.exp(-t*40)
def pop(): t=tt(.12); f=380+700*(1-np.exp(-t*40)); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*28)
def ping(): return bell(88,.8)+np.pad(bell(93,.8),(int(.11*SR),0))[:int(.8*SR)]
def success():
    s=np.zeros(int(1.4*SR))
    for j,m in enumerate((84,88,91,96)): b=bell(m,1.0); i=int(j*.07*SR); s[i:i+len(b)]+=b[:len(s)-i]*.7
    return s
def whoosh(d=.55,lo=400,hi=5000,peak=.6):
    t=tt(d); n=bp(rng.standard_normal(len(t)),lo,hi); e=np.where(t<d*peak,(t/(d*peak))**2,np.exp(-(t-d*peak)*14)); return n*e
def haptic():
    s=np.zeros(int(.3*SR)); t=tt(.045)
    for j in range(3): i=int(j*.075*SR); s[i:i+len(t)]+=np.sin(2*np.pi*165*t)*np.sin(np.pi*t/.045)
    return s
def typing():
    s=np.zeros(int(.8*SR))
    for j in range(6): c=tap()*.6; i=int(j*.12*SR); s[i:i+len(c)]+=c[:len(s)-i]
    return s
def alarm():
    s=np.zeros(int(.9*SR)); b=bell(93,.08)
    for j in range(8): i=int(j*.11*SR); s[i:i+len(b)]+=b[:len(s)-i]
    return s
def sneeze():
    t=tt(.45); a=bp(rng.standard_normal(len(t)),500,1800)*np.exp(-((t-.08)/.06)**2)*.6; c=bp(rng.standard_normal(len(t)),3000,9000)*np.exp(-np.clip(t-.18,0,None)*14)*(t>.18)
    return a+c
def beep(): t=tt(.32); return np.sin(2*np.pi*2000*t)*((t<.1)|((t>.18)&(t<.28)))
def doorbell():
    s=np.zeros(int(1.4*SR)); a=bell(76,.7); b=bell(72,1.0); s[:len(a)]+=a; i=int(.35*SR); s[i:i+len(b)]+=b
    return s
def scribble(): t=tt(.6); return bp(rng.standard_normal(len(t)),1500,5000)*(.5+.5*np.sin(2*np.pi*9*t))*np.exp(-t*2)
def thud(): t=tt(.25); return np.sin(2*np.pi*90*t)*np.exp(-t*25)+.3*bp(rng.standard_normal(len(t)),200,1200)*np.exp(-t*40)
def shimmer():
    t=tt(.9); n=bp(rng.standard_normal(len(t)),6000,12000)*np.exp(-t*5)*np.minimum(1,t/.05)
    return n*.6+.25*(np.sin(2*np.pi*3100*t)+np.sin(2*np.pi*4650*t))*np.exp(-t*6)
EV=[(.3,alarm,.25),(1.2,lambda:whoosh(.3,600,4000),.18),(2.18,sneeze,.45),(2.95,beep,.2),(3.6,tick,.15),(4.2,lambda:whoosh(.6,400,6000,.8),.45),
    (5.0,tick,.18),(5.6,tap,.3),(6.3,tap,.3),(7.0,tap,.3),(7.9,tap,.35),(9.0,lambda:bell(84,.8),.3),(10.4,pop,.25),(11.5,pop,.25),(12.6,pop,.25),
    (14.0,lambda:whoosh(.5,500,6000),.4),(15.0,tick,.15),(15.9,tick,.15),(16.4,scribble,.18),(17.2,thud,.45),(18.45,lambda:whoosh(.5,300,4000),.4),
    (19.4,pop,.25),(23.15,doorbell,.35),(23.9,lambda:whoosh(.3,400,3000),.18),(25.0,lambda:whoosh(.5,300,5000),.35),(25.6,tick,.18),
    (28.7,lambda:whoosh(.5,200,3000),.35),(30.4,tick,.18),(31.75,lambda:whoosh(.5,150,1500),.25),(32.3,tick,.18),(33.1,tick,.2),(34.0,pop,.25),(34.6,tick,.18)]
ts=sorted(e[0] for e in EV); assert all(b-a>=.44 for a,b in zip(ts,ts[1:])), 'efeitos muito próximos'
for t0,f,g in EV: s=f(); add(sfx,t0,s,g)
def norm(x,pk=.89,D=2.2): return np.tanh(x/np.max(np.abs(x))*D)/np.tanh(D)*pk
mix=norm(music*.8+sfx); fx=norm(sfx,.8,1.2)
def mp3(x,name):
    raw=(np.clip(x,-1,1)*32767).astype('<i2').tobytes()
    subprocess.run(['ffmpeg','-loglevel','error','-y','-f','s16le','-ar',str(SR),'-ac','2','-i','-','-b:a','256k',os.path.join(HERE,name)],input=raw,check=True)
mp3(mix,'trilha_final.mp3'); mp3(fx,'so_efeitos.mp3'); print('ok')

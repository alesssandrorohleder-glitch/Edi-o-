# FORJA — phonk de academia 120bpm + efeitos de forja (bigorna, chiado de metal na água, fogo) (Mi menor): 808 distorcido com glide, kick/clap de trap, hats com rolos,
# melodia de cowbell (marca do phonk). Efeitos próprios por momento. Gera trilha_final.mp3 e so_efeitos.mp3.
import numpy as np, subprocess, os
from scipy.signal import butter, sosfilt, fftconvolve
SR=44100; BT=.5; DUR=32.0; N=int(SR*DUR); H=os.path.dirname(os.path.abspath(__file__)); rng=np.random.default_rng(3)
M=np.zeros((N,2)); F=np.zeros((N,2)); V=np.zeros((N,2))
tt=lambda d: np.arange(int(d*SR))/SR
bp=lambda x,a,b: sosfilt(butter(2,[a,b],'band',fs=SR,output='sos'),x)
hp=lambda x,f: sosfilt(butter(2,f,'high',fs=SR,output='sos'),x)
lp=lambda x,f: sosfilt(butter(2,f,'low',fs=SR,output='sos'),x)
mf=lambda m: 440*2**((m-69)/12)
def add(b,t,s,g=1.,pan=0.):
    i=int(t*SR);n=min(len(s),N-i)
    if n<=0 or i<0: return
    b[i:i+n,0]+=s[:n]*g*np.cos((pan+1)*np.pi/4)*1.414;b[i:i+n,1]+=s[:n]*g*np.sin((pan+1)*np.pi/4)*1.414
sq=lambda f,t: np.sign(np.sin(2*np.pi*f*t))
# ---------- instrumentos ----------
def kick(): t=tt(.35);f=55+160*np.exp(-t*45);return np.tanh(2*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9))+.2*hp(rng.standard_normal(len(t)),5000)*np.exp(-t*150)
def b808(m,d,glide=0):
    t=tt(d);f=mf(m)*(1+glide*np.minimum(1,t/.12))*(1+.6*np.exp(-t*40));s=np.sin(2*np.pi*np.cumsum(f)/SR)
    return np.tanh(2.4*s)*np.minimum(1,t/.005)*np.exp(-t*1.6)*np.minimum(1,(d-t)/.03)
def clap():
    t=tt(.3);n=bp(rng.standard_normal(len(t)),900,5000);e=sum(np.exp(-np.clip(t-d,0,None)*80)*(t>=d) for d in (0,.01,.021));return n*(e*.6+np.exp(-t*14)*.5)
def hat(): t=tt(.05);return hp(rng.standard_normal(len(t)),8500)*np.exp(-t*90)
def cowbell(m,d=.28):
    t=tt(d);f=mf(m);s=sq(f,t)+.7*sq(f*1.48,t);return bp(s,f*.8,f*4)*np.exp(-t*11)*np.minimum(1,t/.002)
# ---------- arranjo ----------
ROOT=[40,40,36,38]                       # E2 E2 C2 D2 (por compasso de 2s)
MEL=[76,None,76,79,None,76,74,None, 72,None,72,74,None,71,72,None]   # cowbell, 8avos
def sec(t): return 'hook' if t<2 else 'brk' if 26<=t<28 else 'main'
for bar in range(16):
    t0=bar*2;r=ROOT[bar%4];s=sec(t0)
    if s=='hook':
        for k in range(4): add(M,k*BT,kick(),.9); add(M,k*BT,b808(r,.45),.45)
        continue
    if s=='brk':
        add(M,t0,b808(r,1.9),.55)
        for k,m in enumerate(MEL[:8]):
            if m: add(M,t0+k*BT/2,cowbell(m),.10,.3); add(V,t0+k*BT/2,cowbell(m),.35)
        continue
    for b in (0,1.5,2.5,3.25):                       # kick de trap (em batidas)
        add(M,t0+b*BT,kick(),.9)
    add(M,t0,b808(r,1.4,glide=0),.55); add(M,t0+2.5*BT,b808(r+(3 if bar%2 else 0),.9,glide=.0),.45)
    for b in (1,3): add(M,t0+b*BT,clap(),.45); add(V,t0+b*BT,clap(),.25)
    for k in range(8): add(M,t0+k*BT/2,hat(),.12 if k%2 else .07,.3)
    if bar%2==1:                                       # rolo de hat no fim do compasso
        for k in range(6): add(M,t0+3.5*BT+k*BT/12,hat(),.07,-.3)
    for k,m in enumerate(MEL):
        if m: add(M,t0+k*BT/2,cowbell(m),.14,.25); add(V,t0+k*BT/2,cowbell(m),.3)
# riser para o drop + fim
t=tt(1.8);add(M,.15,bp(rng.standard_normal(len(t)),300,7000)*(t/1.8)**2.5,.12)
add(M,31.0,b808(40,1.0),.4)
# sidechain do 808/melodia pelo kick (leve)
# ---------- efeitos (um tipo por momento, sutis) ----------
def clank(): t=tt(1.0);s=sum(a*np.sin(2*np.pi*f*t)*np.exp(-t*k) for f,a,k in ((420,1,6),(1130,.6,9),(2460,.4,12),(3870,.25,16)));return s+.4*hp(rng.standard_normal(len(t)),2000)*np.exp(-t*60)
def sub(): t=tt(1.2);f=50*np.exp(-t*1.5)+30;return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*2.5)
def whoosh(d=.5,lo=400,hi=5000):
    t=tt(d);n=rng.standard_normal(len(t));o=np.zeros_like(n);seg=int(.015*SR)
    for i in range(0,len(n),seg):u=i/len(n);c=lo*(hi/lo)**u;o[i:i+seg]=bp(n[i:i+seg+64],c*.6,min(c*1.6,20000))[:len(o[i:i+seg])]
    return o*np.sin(np.pi*t/d)**2
def roll(): t=tt(1.1);return lp(rng.standard_normal(len(t)),300)*(.6+.4*np.sin(2*np.pi*14*t))*np.minimum(1,t/.1)*np.exp(-np.maximum(t-.8,0)*12)*2.5
def beep(): t=tt(.12);return np.sin(2*np.pi*1000*t)*np.minimum(1,t/.004)*np.minimum(1,(.12-t)/.01)
def chain():
    s=np.zeros(int(.8*SR))
    for k in range(9): c=clank()[:int(.12*SR)]*np.exp(-k*.25);i=int((k*.06+rng.random()*.02)*SR);s[i:i+len(c)]+=c*.5
    return hp(s,1500)
def ok(): t=tt(.5);return (np.sin(2*np.pi*1320*t)+.6*np.sin(2*np.pi*1980*t)*(t>.08))*np.exp(-t*6)
def flaps():
    s=np.zeros(int(1.0*SR))
    for k in range(14): t=tt(.03);c=bp(rng.standard_normal(len(t)),1500,6000)*np.exp(-t*200);i=int(k*.065*SR);s[i:i+len(c)]+=c
    return s
def punch(): t=tt(.6);return np.tanh(3*np.sin(2*np.pi*np.cumsum(70*np.exp(-t*8)+40)/SR)*np.exp(-t*8))+.3*bp(rng.standard_normal(len(t)),300,3000)*np.exp(-t*25)
def thud(): t=tt(.4);return np.sin(2*np.pi*95*t)*np.exp(-t*18)+.5*bp(rng.standard_normal(len(t)),200,1500)*np.exp(-t*30)
def rev(d=.6): t=tt(d);return hp(rng.standard_normal(len(t)),1500)*(t/d)**3
def clang(f0=950,d=1.4): t=tt(d);s=sum(a*np.sin(2*np.pi*f0*r*t)*np.exp(-t*k) for r,a,k in ((1,1,3.2),(1.81,.7,4.5),(2.87,.45,6),(4.1,.3,8),(5.43,.18,11)));return s+.5*hp(rng.standard_normal(len(t)),3000)*np.exp(-t*120)
def sizzle(d=1.4):
    t=tt(d);n=hp(rng.standard_normal(len(t)),3500)*.5;cr=np.zeros(len(t));idx=rng.integers(0,len(t),400);cr[idx]=rng.standard_normal(400)*3;cr=hp(cr,2000)
    return (n+cr)*np.minimum(1,t/.03)*np.exp(-t*2.2)
def fire(d=1.8): t=tt(d);return (lp(rng.standard_normal(len(t)),900)*2+.3*bp(rng.standard_normal(len(t)),2000,6000))*np.minimum(1,t/d*1.5)*np.exp(-np.maximum(t-d*.7,0)*8)
EV=[(0.0,lambda:clang(900),.22),(0.5,lambda:clang(1010),.22),(1.0,lambda:clang(860),.22),(1.5,lambda:clang(1200),.28),(2.0,lambda:whoosh(.6,150,1500),.2),
    (4.0,sub,.35),(6.0,fire,.18),(8.17,lambda:clang(980,.9),.26),(8.67,lambda:clang(1050,.9),.26),(9.17,lambda:clang(940,.9),.26),(9.67,lambda:clang(1120,.9),.28),
    (10.17,lambda:sizzle(.5),.07),(10.67,lambda:sizzle(.5),.07),(11.17,lambda:sizzle(.5),.07),(12.17,lambda:sizzle(.5),.07),(12.67,lambda:sizzle(.5),.07),(13.17,lambda:sizzle(.5),.07),
    (14.55,sizzle,.32),(16.95,ok,.14),(18.2,lambda:whoosh(.7,150,1200),.18),(20.05,flaps,.18),(22.85,lambda:clang(760,1.6),.32),(24.25,lambda:sizzle(1.6),.34),
    (26.0,lambda:clang(700,1.8),.28),(28.05,lambda:whoosh(.6,150,1500),.15),(28.75,lambda:clang(1300,.8),.14),(30.5,punch,.22)]
EV=[e for e in EV if e[2]>0]
ts=sorted(e[0] for e in EV);assert all(b-a>=.45 for a,b in zip(ts,ts[1:]))
for t0,f,g in EV: s=f();s=s/np.max(np.abs(s))*g;add(F,t0,s);add(V,t0,s*.6)
def verb(x,dec):
    t=tt(dec);IR=np.stack([lp(rng.standard_normal(len(t))*np.exp(-t*(6.9/dec)),6000) for _ in range(2)],1);IR/=np.sum(np.abs(IR[:,0]))/8
    return np.stack([fftconvolve(x[:,c],IR[:,c])[:N] for c in range(2)],1)
W_=verb(V,1.6)*.35
mus=M+W_*.6;mus*=np.clip((DUR-np.arange(N)/SR)/1.0,0,1)[:,None]
def norm(x,pk=.9,D=1.8): return np.tanh(x/np.max(np.abs(x))*D)/np.tanh(D)*pk
mix=norm(mus*.9+F*1.0);fx=norm(F+W_*.2,.8,1.1)
def mp3(x,name):
    raw=(np.clip(x,-1,1)*32767).astype('<i2').tobytes();subprocess.run(['ffmpeg','-loglevel','error','-y','-f','s16le','-ar',str(SR),'-ac','2','-i','-','-b:a','256k',os.path.join(H,name)],input=raw,check=True)
mp3(mix,'trilha_final.mp3');mp3(fx,'so_efeitos.mp3');print('ok')

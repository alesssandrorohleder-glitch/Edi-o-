# SOLSTÍCIO — trilha TECHNO 120bpm (Lá menor): kick com rumble, baixo rolante, hats 16 avos, clap com reverb,
# linha acid com filtro ressonante, stab escuro, breakdown no logo. Efeitos "cinematográficos": swell reverso,
# impactos com cauda, blips filtrados com reverb, stab no final. Gera trilha_final.mp3 e so_efeitos.mp3.
import numpy as np, subprocess, os
from scipy.signal import butter, sosfilt, fftconvolve, iirpeak, lfilter
SR=44100; BT=.5; DUR=32.0; N=int(SR*DUR); HERE=os.path.dirname(os.path.abspath(__file__)); rng=np.random.default_rng(11)
mus=np.zeros((N,2)); sfx=np.zeros((N,2)); vm=np.zeros((N,2)); vs=np.zeros((N,2))
def add(b,t,s,g=1.,pan=0.):
    i=int(t*SR); n=min(len(s),N-i)
    if n<=0 or i<0: return
    l=np.cos((pan+1)*np.pi/4)*1.414; r=np.sin((pan+1)*np.pi/4)*1.414; b[i:i+n,0]+=s[:n]*g*l; b[i:i+n,1]+=s[:n]*g*r
tt=lambda d: np.arange(int(d*SR))/SR
bp=lambda x,a,b,o=2: sosfilt(butter(o,[a,b],'band',fs=SR,output='sos'),x)
hp=lambda x,f,o=2: sosfilt(butter(o,f,'high',fs=SR,output='sos'),x)
lp=lambda x,f,o=2: sosfilt(butter(o,f,'low',fs=SR,output='sos'),x)
mf=lambda m: 440*2**((m-69)/12)
def saw(f,d): t=tt(d); return 2*((f*t)%1)-1
# ---------- instrumentos ----------
def kick():
    t=tt(.5); f=46+190*np.exp(-t*38); s=np.tanh(1.6*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*6.5)); return s+.18*hp(rng.standard_normal(len(t)),4000)*np.exp(-t*120)
def rumble(d=.5):  # cauda grave do kick (reverb filtrado), típico do techno
    t=tt(d); return lp(rng.standard_normal(len(t)),110,4)*np.exp(-t*5)*np.minimum(1,t/.03)*3
def hat(op=False): t=tt(.32 if op else .045); return hp(rng.standard_normal(len(t)),8000)*np.exp(-t*(10 if op else 90))
def clap():
    t=tt(.35); n=bp(rng.standard_normal(len(t)),1000,4000); e=sum(np.exp(-np.clip(t-d,0,None)*70)*(t>=d) for d in (0,.012,.024))
    return n*(e*.5+np.exp(-t*12)*.6)
def bass(m,d):
    t=tt(d); f=mf(m); s=lp(saw(f,d)*.6+np.sin(2*np.pi*f*t),420,2); return s*np.exp(-t*9)*np.minimum(1,t/.004)
def acid(m,d,cut,res=6.):
    s=saw(mf(m),d); y=lp(s,cut,2); b,a=iirpeak(min(cut,9000)/(SR/2),res); y=y+.9*lfilter(b,a,s); t=tt(d); return np.tanh(1.8*y)*np.exp(-t*7)*np.minimum(1,t/.003)
def stab(ms,d=.6):
    t=tt(d); s=sum(saw(mf(m),d) for m in ms)/len(ms); return lp(s,1400,2)*np.exp(-t*5)*np.minimum(1,t/.004)
def pad(ms,d):
    t=tt(d); s=sum(np.sin(2*np.pi*mf(m)*t)+.25*np.sin(2*np.pi*mf(m)*2*t) for m in ms)/len(ms); return lp(s,900)*np.minimum(1,t/.6)*np.minimum(1,(d-t)/.6)
def bell(m,d=1.2): t=tt(d); f=mf(m); return (np.sin(2*np.pi*f*t)+.3*np.sin(2*np.pi*f*2*t)*np.exp(-t*5))*np.exp(-t*3)*np.minimum(1,t/.002)
# ---------- arranjo ----------
ROOT=[45,45,41,43]          # A1 A1 F1 G1 (2 compassos cada → progressão sombria)
ACID=[57,57,69,57,60,57,64,57,57,69,57,62,57,60,67,57]
def sec(t): return 'hook' if t<2 else 'brk' if 26<=t<29 else 'cta' if t>=29 else 'main'
for k in range(64):
    tb=k*BT; s=sec(tb); bar=int(tb//2); root=ROOT[(bar//2)%4]
    if s!='brk':
        add(mus,tb,kick(),1.0); add(mus,tb+.02,rumble(.48),.35 if s!='cta' else .2)
    if s in('main','cta'):
        if k%2==1: add(mus,tb,clap(),.38); add(vm,tb,clap(),.25)
        for q in range(4):
            v=.12 if q==2 else .06; add(mus,tb+q*BT/4,hat(),v,.3*(q%2*2-1))
        add(mus,tb+BT/2,hat(True),.11,-.2)
        for q in (1,2,3): add(mus,tb+q*BT/4,bass(root+12,BT/4*.9),.42 if s=='main' else .25)
    if s=='main' and 10<=tb<26:
        prog=p=(tb-10)/16
        for q in range(4):
            j=(k*4+q)%16; cut=500+2600*(.5+.5*np.sin(tb*.9+q*.4))*(.4+.6*prog)
            if (k*4+q)%3!=2: add(mus,tb+q*BT/4,acid(ACID[j],BT/4*.85,cut),.16,.15); add(vm,tb+q*BT/4,acid(ACID[j],BT/4*.85,cut),.05)
    if s=='main' and k%8==7: add(mus,tb+BT*.5,stab([57,60,64]),.16); add(vm,tb+BT*.5,stab([57,60,64]),.2)
# breakdown do logo: pad escuro + sonic logo
add(mus,26.0,pad([45,57,60,64],3.1),.5); add(vm,26.0,pad([57,60,64],3.1),.3)
for j,m in enumerate((69,72,76,81)): add(mus,26.35+j*.14,bell(m,1.8),.18,(j-1.5)*.35); add(vm,26.35+j*.14,bell(m,1.8),.3)
# riser antes do drop e antes do CTA
t=tt(1.9); add(mus,.1,bp(rng.standard_normal(len(t)),300,7000)*(t/1.9)**2.5,.14); t=tt(2.6); add(mus,26.3,hp(rng.standard_normal(len(t)),2000)*(t/2.6)**3,.09)
# sidechain
env=np.ones(N)
for k in range(64):
    tb=k*BT
    if sec(tb)!='brk': i=int(tb*SR); n=min(int(.32*SR),N-i); env[i:i+n]=1-.6*np.exp(-np.arange(n)/SR*12)
# ---------- efeitos (níveis suaves; mais fortes só nos impactos) ----------
def blip(f=1500): t=tt(.12); return np.sin(2*np.pi*f*t)*np.exp(-t*45)*np.minimum(1,t/.002)
def swish(d=.55,lo=300,hi=6000,peak=.7):
    t=tt(d); n=bp(rng.standard_normal(len(t)),lo,hi); e=np.where(t<d*peak,(t/(d*peak))**2.2,np.exp(-(t-d*peak)*12)); return n*e
def rev(d=.9): t=tt(d); return hp(rng.standard_normal(len(t)),1800)*(t/d)**3*np.minimum(1,(d-t)/.01)
def hit():
    t=tt(1.4); f=55*np.exp(-t*1.2)+28; return .9*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*2.4)+.25*bp(rng.standard_normal(len(t)),120,2500)*np.exp(-t*7)
def sub_drop(): t=tt(1.0); f=70*np.exp(-t*2)+30; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*3)
def metal(): t=tt(.8); return (np.sin(2*np.pi*1310*t)+.6*np.sin(2*np.pi*2017*t)+.4*np.sin(2*np.pi*3480*t))*np.exp(-t*6)*.5+.2*hp(rng.standard_normal(len(t)),6000)*np.exp(-t*30)
EV=[(0.0,blip,.14),(0.5,blip,.14),(1.1,lambda:rev(.9),.35),(2.0,hit,.6),(4.1,lambda:blip(1200),.12),(5.6,lambda:swish(.4,300,5000),.3),
    (6.3,lambda:blip(900),.12),(8.0,metal,.18),(9.6,lambda:swish(.4),.3),(10.5,blip,.1),(11.0,blip,.1),(11.5,blip,.1),(12.0,blip,.1),(12.5,blip,.1),
    (13.6,lambda:swish(.4,400,7000),.3),(14.5,blip,.1),(15.0,blip,.1),(15.5,blip,.1),(16.0,blip,.1),(16.5,blip,.1),(17.6,lambda:swish(.4),.3),
    (18.4,lambda:blip(1100),.13),(18.9,lambda:blip(1100),.13),(19.4,lambda:blip(1100),.13),(19.9,lambda:blip(1100),.13),(21.55,lambda:rev(.45),.25),(22.0,sub_drop,.4),
    (22.6,lambda:swish(.6,500,8000,.6),.28),(23.4,metal,.16),(25.5,lambda:swish(.45,300,4000),.25),(26.0,hit,.45),
    (28.1,lambda:rev(.9),.28),(29.0,sub_drop,.35),(29.9,lambda:blip(1000),.12),(30.8,lambda:stab([69,72,76],.9),.3)]
ts=sorted(e[0] for e in EV); assert all(b-a>=.44 for a,b in zip(ts,ts[1:])),'efeitos muito próximos'
for t0,f,g in EV: s=f(); add(sfx,t0,s,g); add(vs,t0,s,g*.5)
# reverbs
def verb(x,dec,lpf):
    t=tt(dec); IR=np.stack([lp(rng.standard_normal(len(t))*np.exp(-t*(6.9/dec)),lpf) for _ in range(2)],1)
    return np.stack([fftconvolve(x[:,c],IR[:,c])[:N] for c in range(2)],1)
music=(mus+verb(vm,2.2,5000)*.09)*env[:,None]; music*=np.clip((DUR-np.arange(N)/SR)/1.2,0,1)[:,None]
fx=sfx+verb(vs,1.6,7000)*.12
def norm(x,pk=.89,D=2.0): return np.tanh(x/np.max(np.abs(x))*D)/np.tanh(D)*pk
mix=norm(music*.85+fx); fxo=norm(fx,.8,1.2)
def mp3(x,name):
    raw=(np.clip(x,-1,1)*32767).astype('<i2').tobytes()
    subprocess.run(['ffmpeg','-loglevel','error','-y','-f','s16le','-ar',str(SR),'-ac','2','-i','-','-b:a','256k',os.path.join(HERE,name)],input=raw,check=True)
mp3(mix,'trilha_final.mp3'); mp3(fxo,'so_efeitos.mp3'); print('ok')

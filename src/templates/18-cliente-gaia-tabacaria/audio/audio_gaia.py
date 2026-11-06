# Trilha TECHNO 128bpm + efeitos do vídeo 18 (Gaia) — v2. Gera trilha_final.mp3 e so_efeitos.mp3.
# Kick + rumble, baixo rolante em semicolcheias, linha acid (filtro ressonante), hats acentuados, perc sincopada,
# sidechain, breakdown com riser e rolo de caixa. Sem detune (uma frequência por voz).
import numpy as np, wave, subprocess, os
from scipy.signal import fftconvolve, butter, sosfilt, lfilter
SR=44100; BT=60/128; ST=BT/4; NB=78; D=NB*BT; n=int(SR*D); rng=np.random.default_rng(1818); HERE=os.path.dirname(os.path.abspath(__file__))
b=lambda k:k*BT
def tt(d): return np.arange(int(d*SR))/SR
def buf(): return np.zeros(n)
def add(B,sig,at,g=1.0):
    i=int(round(at*SR)); j=min(len(B),i+len(sig))
    if j>i>=0: B[i:j]+=sig[:j-i]*g
def lpf(x,fc,o=2): return sosfilt(butter(o,fc,'low',fs=SR,output='sos'),x)
def hpf(x,fc,o=2): return sosfilt(butter(o,fc,'high',fs=SR,output='sos'),x)
def bpf(x,a,c): return sosfilt(butter(2,[a,c],'band',fs=SR,output='sos'),x)
mid=lambda m:440*2**((m-69)/12)
def reslp(x,cut,Q=6.0,blk=128):   # passa-baixa ressonante com corte variando no tempo (RBJ, em blocos)
    y=np.zeros_like(x); zi=np.zeros(2)
    for i in range(0,len(x),blk):
        fc=float(np.clip(cut[min(i,len(cut)-1)],40,16000)); w=2*np.pi*fc/SR; al=np.sin(w)/(2*Q); cw=np.cos(w)
        bb=np.array([(1-cw)/2,1-cw,(1-cw)/2]); aa=np.array([1+al,-2*cw,1-al])
        y[i:i+blk],zi=lfilter(bb/aa[0],aa/aa[0],x[i:i+blk],zi=zi)
    return y
def saw(f,d): t=tt(d); return 2*((t*f)%1)-1
def sec(beat):
    if beat<8: return 'intro'
    if 48<=beat<56: return 'break'
    if beat>=74: return 'outro'
    return 'drop'
# ---------------- bateria ----------------
KICK=buf(); HAT=buf(); CLAP=buf(); PERC=buf(); kicks=[]
def kick():
    t=tt(.38); f=44+150*np.exp(-t*42); body=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7.5)
    click=hpf(rng.standard_normal(len(t)),3000)*np.exp(-t*300)*.5; return np.tanh(2.2*(body+click))*.62
def hat(v=1,o=False): d=.25 if o else .045; t=tt(d); return hpf(rng.standard_normal(len(t)),9000 if not o else 7000)*np.exp(-t*(11 if o else 80))*.05*v
def clap():
    t=tt(.3); nz=bpf(rng.standard_normal(len(t)),900,7000); e=sum(np.exp(-np.clip(t-d,0,None)*90)*(t>=d) for d in (0,.009,.019,.03)); return nz*(e+np.exp(-t*12)*.25)*.12
def rim(): t=tt(.07); return (np.sin(2*np.pi*820*t)+.5*np.sin(2*np.pi*1650*t))*np.exp(-t*70)*.045
def snare(v=1): t=tt(.16); return (bpf(rng.standard_normal(len(t)),1500,8000)*np.exp(-t*30)+np.sin(2*np.pi*190*t)*np.exp(-t*40)*.5)*.06*v
HV=[1,.45,.75,.45]; RIM=[3,6,10,13]
for beat in range(NB):
    s=sec(beat); tb=b(beat)
    if s in('drop',) or (s=='intro' and beat>=4) or (s=='outro' and False):
        g=1 if s=='drop' else .55
        add(KICK,kick(),tb,g); kicks.append(tb)
    if s=='drop':
        for k in range(4):
            if not(12<=beat<16 and k%2==0): add(HAT,hat(HV[k]),tb+k*ST)
        add(HAT,hat(1.1,True),tb+2*ST)
        if beat%2==1: add(CLAP,clap(),tb)
        for k in range(4):
            if (beat%4)*4+k in RIM and beat>=20: add(PERC,rim(),tb+k*ST)
    if s=='intro' and beat>=2:
        for k in (1,3): add(HAT,hat(.5),tb+k*ST)
# rolos de caixa antes dos drops
for st,en in [(46,48),(54,56)]:
    steps=int((en-st)*4)
    for i in range(steps): add(PERC,snare(.4+.8*i/steps),b(st)+i*ST)
# rumble: reverb do kick, só graves
it=tt(1.1); ir=rng.standard_normal(len(it))*np.exp(-it*5); RUMB=lpf(fftconvolve(KICK,ir)[:n],140,4); RUMB=RUMB/np.max(np.abs(RUMB)+1e-9)*.25
# sidechain
SC=np.ones(n); tn=np.arange(n)/SR
for k in kicks:
    i=int(k*SR); j=min(n,i+int(.3*SR)); SC[i:j]=np.minimum(SC[i:j],1-.75*np.exp(-(tn[i:j]-k)/.09))
RUMB*=np.roll(SC,int(.02*SR))
# ---------------- baixo rolante (semicolcheias fora do tempo) ----------------
BASS=buf(); ROOTS=[33,33,31,36]   # Lá – Lá – Sol – Dó  (grave, menor)
def bnote(f,d=ST*.9): t=tt(d); s=np.sin(2*np.pi*f*t)+.4*np.sin(4*np.pi*f*t); return lpf(s,300)*np.minimum(1,t/.003)*np.exp(-t*9)*.32
for beat in range(NB):
    if sec(beat)!='drop': continue
    r=ROOTS[(beat//4)%4]
    for k in (1,2,3): add(BASS,bnote(mid(r)),b(beat)+k*ST,1 if k!=2 else .8)
# ---------------- acid ----------------
ACIDRAW=buf(); CUT=np.full(n,300.0)
SEQ=[0,0,12,0, 3,0,15,0, 0,7,0,10, 12,0,3,5]; ACC=[1,0,1,0, 0,1,0,0, 1,0,1,0, 1,0,0,1]; REST={5,14}
for beat in range(NB):
    s=sec(beat)
    if s=='outro': continue
    for k in range(4):
        st=(beat%4)*4+k
        if st in REST and s!='break': continue
        t0=b(beat)+k*ST; f=mid(45+SEQ[st]); add(ACIDRAW,saw(f,ST*.95)*np.exp(-tt(ST*.95)*(3 if ACC[st] else 7)),t0,.5)
        # envelope do filtro por nota
        i=int(t0*SR); L=int(ST*SR); e=np.exp(-np.arange(L)/SR*(14 if ACC[st] else 22))
        prog={'intro':.08+.12*beat/8,'drop':.35+.25*np.sin(beat/16*np.pi)**2,'break':.15+.75*p if (p:=(beat-48)/8) else .15}[s]
        base=250+2200*prog; CUT[i:i+L]=base*(1+ (2.5 if ACC[st] else 1.2)*e)[:max(0,min(L,n-i))]
ACID=np.tanh(1.8*reslp(ACIDRAW,CUT,Q=7.5))*.11
# ---------------- atmosfera ----------------
def drone(ms,d): t=tt(d); s=sum(np.sin(2*np.pi*mid(m)*t+np.sin(2*np.pi*.2*t)*.3) for m in ms)/len(ms); return lpf(s,1200)*np.minimum(1,t/1.2)*np.clip((d-t)/1.0,0,1)*.08
PAD=buf(); add(PAD,drone([57,64,69],b(9)),0); add(PAD,drone([57,60,64,69],b(9)),b(47.5),1.3); add(PAD,drone([57,64,69,72],b(8)),b(70),1.2)
def stab(d=.5): t=tt(d); s=sum(np.sign(np.sin(2*np.pi*mid(m)*t))*.3+np.sin(2*np.pi*mid(m)*t)*.7 for m in [57,60,64,67])/4; return lpf(s,1800)*np.exp(-t*7)*np.minimum(1,t/.003)*.07
STAB=buf()
for beat in [12,20,28,36,44,56,60,64,68]:
    for d,g in [(0,1),(3*ST,.5),(6*ST,.25)]: add(STAB,stab(),b(beat)+d,g)
def riser(d): t=tt(d); f=300+5000*(t/d)**2.2; return (bpf(rng.standard_normal(len(t)),300,9000)*.6+np.sin(2*np.pi*np.cumsum(f)/SR)*.12)*(t/d)**2.4*.09
RIS=buf()
for st,dd in [(0,b(8)),(b(52),b(4)),(b(68),b(2))]: add(RIS,riser(dd),st)
# ---------------- efeitos sonoros (variados por tipo de transição) ----------------
S=buf()
def whoosh(d=.3,lo=600,hi=7000,g=.07): t=tt(d); return bpf(rng.standard_normal(len(t)),lo,hi)*np.sin(np.pi*t/d)**2*g
def swish(): t=tt(.22); f=2500*np.exp(-t*6); return (bpf(rng.standard_normal(len(t)),1500,9000)*np.exp(-t*12)+np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*20)*.3)*.06
def zoomfx(): t=tt(.4); return bpf(rng.standard_normal(len(t)),200,3000)*(t/.4)**2*np.exp(-np.clip(t-.35,0,None)*60)*.09
def impact(g=1):
    t=tt(1.8); boom=np.sin(2*np.pi*np.cumsum(28+80*np.exp(-t*10))/SR)*np.exp(-t*2.2); nz=lpf(rng.standard_normal(len(t)),2500)*np.exp(-t*6)*.4
    return np.tanh(1.5*(boom+nz))*.3*g
def subdrop(): t=tt(1.2); return np.sin(2*np.pi*np.cumsum(70*np.exp(-t*2.5)+25)/SR)*np.exp(-t*2)*.22
def thud(): t=tt(.3); return np.sin(2*np.pi*np.cumsum(70+120*np.exp(-t*35))/SR)*np.exp(-t*12)*.14
def tick(): t=tt(.05); return np.sin(2*np.pi*2400*t)*np.exp(-t*80)*.025
def click(): t=tt(.03); return hpf(rng.standard_normal(len(t)),4000)*np.exp(-t*160)*.05
def shimmer(): t=tt(1.5); return sum(np.sin(2*np.pi*mid(m)*t)*np.exp(-t*2.4) for m in [81,88,93])*.018
def tape(): t=tt(.35); f=600*np.exp(-t*8); return lpf(saw(1,.35)*0+np.sin(2*np.pi*np.cumsum(f)/SR),2000)*np.exp(-t*5)*.05
ev=[(b(2),3,thud()),(b(4),2,click()),(b(7.5),3,whoosh(.4,300,5000,.06)),(b(8),9,impact(1)),(b(9),3,thud()),
    (b(12)-.1,6,whoosh(.7,200,3000,.07)),(b(12.3),5,subdrop()),(b(13.4),2,shimmer()),(b(14.5),2,tick()),
    (b(20)-.05,5,zoomfx()),(b(21.2),3,thud()),(b(24)-.05,5,whoosh(.32,300,4000,.06)),(b(24.25),3,thud()),(b(26),3,click()),
    (b(28)-.08,5,whoosh(.3,500,6000,.06)),(b(30),3,click()),(b(32)-.12,5,whoosh(.3)),(b(34)-.12,5,whoosh(.3,800,8000,.06)),(b(36)-.05,5,zoomfx()),(b(36.15),4,thud()),
    (b(38),3,tape()),(b(40)-.12,5,whoosh(.3,500,6000,.07)),(b(42),3,click()),(b(44),4,thud()),(b(45),3,thud()),(b(46),3,thud()),(b(47),3,thud()),
    (b(48),7,impact(.5)),(b(52)-.25,5,zoomfx()),(b(52),3,thud()),
    (b(56),9,impact(1)),(b(57.6),3,click()),(b(58.6),3,click()),(b(59.6),3,click()),(b(64)-.08,5,whoosh(.35,400,5000,.06)),(b(65.2),3,click()),(b(65.8),3,click()),
    (b(70),9,impact(.9)),(b(70.6),2,shimmer()),(b(72),3,thud()),(b(73),2,tick())]
ev.sort(key=lambda e:-e[1]); kept=[]
for t,pr,sig in ev:
    if all(abs(t-k)>=.45 for k in kept): add(S,sig,t); kept.append(t)
# ---------------- mix ----------------
def rev(x,dec=3.5,l=1.6,fc=6000):
    it=tt(l); ir=rng.standard_normal(len(it))*np.exp(-it*dec); ir=lpf(ir,fc); ir/=np.sqrt((ir**2).sum()); return fftconvolve(x,ir)[:n]
def delay(x,dt,fb=.35,k=4):
    y=x.copy(); d=int(dt*SR)
    for i in range(1,k+1): y[d*i:]+=x[:-d*i]*fb**i
    return y
duck=SC
music=(KICK+RUMB+BASS*duck+ACID*duck*1.0+delay(ACID*duck,3*ST,.3)*.35+HAT+CLAP+rev(CLAP,4,1.2)*.5+PERC+rev(PERC,5,1)*.3
       +PAD*np.maximum(duck,.5)+rev(PAD,2,2.4,4000)*.6+STAB+rev(delay(STAB,3*ST,.4),3,1.8)*.5+RIS)
def stereo(m,width=.0):
    return np.stack([m,m],1)
fx=S+rev(S,4,1.4)*.25
fade=np.ones(n); fo=int(.7*SR); fade[-fo:]=np.linspace(1,0,fo)
def save(B,name):
    B=hpf(B,28); B=np.tanh(B*1.4)/1.4; B=B*fade; B=B/np.max(np.abs(B))*.9; B=np.stack([B,B],1)
    # leve abertura estéreo nos agudos
    hi=hpf(B[:,0],3000)*.12; B[:,0]+=np.roll(hi,int(.011*SR)); B[:,1]-=np.roll(hi,int(.011*SR)); B/=np.max(np.abs(B))/.9
    w=os.path.join(HERE,name+'.wav')
    with wave.open(w,'wb') as f: f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((B*32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',w,'-b:a','256k',os.path.join(HERE,name+'.mp3')],check=True); os.remove(w)
save(music*.9+fx*1.1,'trilha_final'); save(fx,'so_efeitos'); print('ok')

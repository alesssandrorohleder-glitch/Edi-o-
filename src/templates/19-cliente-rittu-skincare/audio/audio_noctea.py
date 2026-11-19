# NOCTÉA v2 — melodic house 120bpm (luxo/moda) + efeitos sincronizados aos takes. Gera trilha_final.mp3 e so_efeitos.mp3.
# Estrutura (batidas): intro 0–4 · drop 4–33 · breakdown 33–39 · build 39–41 · drop 41–49 · impacto/logo 49–55 · outro 55–64
import numpy as np, wave, subprocess, os
from scipy.signal import fftconvolve, butter, sosfilt, lfilter
SR=44100; BT=.5; ST=BT/4; NB=64; D=NB*BT; n=int(SR*D); rng=np.random.default_rng(1919); HERE=os.path.dirname(os.path.abspath(__file__))
b=lambda k:k*BT
def tt(d): return np.arange(int(d*SR))/SR
def buf(): return np.zeros(n)
def add(B,s,at,g=1.0):
    i=int(round(at*SR)); j=min(n,i+len(s))
    if j>i>=0: B[i:j]+=s[:j-i]*g
def lpf(x,fc,o=2): return sosfilt(butter(o,fc,'low',fs=SR,output='sos'),x)
def hpf(x,fc,o=2): return sosfilt(butter(o,fc,'high',fs=SR,output='sos'),x)
def bpf(x,a,c): return sosfilt(butter(2,[a,c],'band',fs=SR,output='sos'),x)
mid=lambda m:440*2**((m-69)/12)
def env(d,a=.005,r=.1): t=tt(d); return np.minimum(1,t/a)*np.clip((d-t)/r,0,1)
def reslp(x,cut,Q=4.0,blk=128):
    y=np.zeros_like(x); zi=np.zeros(2)
    for i in range(0,len(x),blk):
        fc=float(np.clip(cut[min(i,len(cut)-1)],60,15000)); w=2*np.pi*fc/SR; al=np.sin(w)/(2*Q); cw=np.cos(w)
        bb=np.array([(1-cw)/2,1-cw,(1-cw)/2]); aa=np.array([1+al,-2*cw,1-al]); y[i:i+blk],zi=lfilter(bb/aa[0],aa/aa[0],x[i:i+blk],zi=zi)
    return y
def sec(beat):
    if beat<4: return 'intro'
    if 33<=beat<39: return 'break'
    if 39<=beat<41: return 'build'
    if 49<=beat<55: return 'logo'
    if beat>=55: return 'outro'
    return 'drop'
# Em – Cmaj7 – G – D/F#  (i–VI–III–VII, escuro e elegante)
CH=[(40,[64,67,71,74]),(36,[64,67,71,72]),(43,[62,67,71,74]),(42,[62,66,69,74])]
# ---------------- bateria ----------------
K=buf();DR=buf();kicks=[]
def kick(): t=tt(.4); f=46+130*np.exp(-t*36); s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7)+hpf(rng.standard_normal(len(t)),2500)*np.exp(-t*260)*.35; return np.tanh(2*s)*.6
def clap(): t=tt(.32); nz=bpf(rng.standard_normal(len(t)),900,7500); e=sum(np.exp(-np.clip(t-d,0,None)*85)*(t>=d) for d in (0,.01,.021,.032)); return nz*(e+np.exp(-t*10)*.3)*.11
def hat(v=1,o=False): d=.22 if o else .04; t=tt(d); return hpf(rng.standard_normal(len(t)),8500)*np.exp(-t*(12 if o else 85))*.045*v
def shaker(v=1): t=tt(.06); return hpf(rng.standard_normal(len(t)),6500)*np.sin(np.pi*t/.06)**2*.028*v
def tom(f): t=tt(.3); return np.sin(2*np.pi*np.cumsum(f*(1+.5*np.exp(-t*20)))/SR)*np.exp(-t*9)*.09
for beat in range(NB):
    s=sec(beat); tb=b(beat)
    if s in('drop','outro') or (s=='intro' and beat>=2) or (s=='build'):
        if not(s=='intro' and beat%2): add(K,kick(),tb,1 if s!='intro' else .6); kicks.append(tb)
    if s in('drop','outro'):
        if beat%2==1: add(DR,clap(),tb)
        add(DR,hat(1.1,True),tb+2*ST)
        for k in range(4): add(DR,shaker([.5,.3,.8,.35][k]),tb+k*ST)
        if beat%8==7: add(DR,tom(180),tb+2*ST); add(DR,tom(140),tb+3*ST)
    if s=='break':
        for k in (2,): add(DR,shaker(.6),tb+k*ST)
    if s=='build':
        for k in range(4): add(DR,clap()*.5*(0.5+(beat-39+k/4)/2),tb+k*ST)
# ---------------- baixo ----------------
BASS=buf()
def bn(f,d): t=tt(d); s=np.sin(2*np.pi*f*t)+.5*np.sin(4*np.pi*f*t)+.2*np.sin(6*np.pi*f*t); return lpf(s,380)*env(d,.003,.03)*.3
for beat in range(NB):
    s=sec(beat)
    if s not in('drop','outro'): continue
    r=CH[(beat//4)%4][0]
    add(BASS,bn(mid(r),ST*1.6),b(beat)+2*ST); add(BASS,bn(mid(r),ST*.8),b(beat)+3*ST,.7)
    if beat%4==3: add(BASS,bn(mid(r+12),ST*.8),b(beat)+ST,.5)
# ---------------- pluck arpejado com filtro + acordes ----------------
ARP=buf();CUT=np.full(n,800.0)
PAT=[0,2,1,3,2,1,3,2]
for beat in range(NB):
    s=sec(beat)
    if s=='logo' and beat>=50: continue
    ch=CH[(beat//4)%4][1]
    for k in range(4):
        st=(beat*4+k)%8;f=mid(ch[PAT[st]]+12);t0=b(beat)+k*ST;t=tt(ST*1.6)
        sig=(2*((t*f)%1)-1)*.6+np.sin(2*np.pi*f*t)*.4; add(ARP,sig*np.exp(-t*6)*np.minimum(1,t/.002),t0,.75 if k%2 else 1)
for i in range(n):
    pass
tb_=np.arange(n)/SR/BT
CUT=np.where(tb_<4,300+2200*(tb_/4)**2,np.where((tb_>=33)&(tb_<41),600+3000*np.clip((tb_-33)/8,0,1)**1.5,2600+600*np.sin(tb_/8*np.pi)))
ARPF=np.tanh(1.4*reslp(ARP,CUT,3.2))*.07
def stab(ms,d=.6): t=tt(d); s=sum(np.sin(2*np.pi*mid(m)*t+.8*np.sin(2*np.pi*mid(m)*2*t)*np.exp(-t*6)) for m in ms)/len(ms); return lpf(s,2600)*np.exp(-t*5)*np.minimum(1,t/.004)*.08
CHO=buf()
for beat in range(0,NB,2):
    s=sec(beat)
    if s in('drop','outro'):
        ch=CH[(beat//4)%4][1]; add(CHO,stab(ch),b(beat)+3*ST,.9); add(CHO,stab(ch,.4),b(beat)+b(1.5),.5)
def pad(ms,d): t=tt(d); s=sum(np.sin(2*np.pi*mid(m)*t) for m in ms)/len(ms); return lpf(s,1400)*env(d,.6,.8)*.07
PAD=buf()
for bar in range(NB//4):
    s=sec(bar*4); ch=CH[bar%4][1]; g={'intro':1.2,'break':1.6,'build':1.2,'logo':1.4,'outro':.9}.get(s,.55); add(PAD,pad([m for m in ch],b(4.3)),b(bar*4),g)
# "vocal chop" (formantes) nas viradas
def vox(m,d=.35):
    t=tt(d); src=2*((t*mid(m))%1)-1; s=bpf(src,600,1100)*1.0+bpf(src,1600,2600)*.6; return s*np.exp(-t*7)*np.minimum(1,t/.01)*.09
VOX=buf()
for beat,m in [(15,76),(15.5,74),(23,79),(23.5,76),(31,76),(31.5,71),(47,79),(47.5,78)]: add(VOX,vox(m),b(beat))
# riser + sub drop
def riser(d): t=tt(d); f=200+4000*(t/d)**2.4; return (bpf(rng.standard_normal(len(t)),300,9000)*.55+np.sin(2*np.pi*np.cumsum(f)/SR)*.12)*(t/d)**2.4*.09
RIS=buf(); add(RIS,riser(b(4)),0); add(RIS,riser(b(4)),b(37));
# sidechain
SC=np.ones(n); tn=np.arange(n)/SR
for k in kicks:
    i=int(k*SR); j=min(n,i+int(.3*SR)); SC[i:j]=np.minimum(SC[i:j],1-.6*np.exp(-(tn[i:j]-k)/.1))
# ---------------- efeitos ----------------
S=buf()
def whoosh(d=.32,lo=500,hi=7000,g=.07): t=tt(d); return bpf(rng.standard_normal(len(t)),lo,hi)*np.sin(np.pi*t/d)**2*g
def impact(g=1): t=tt(2.2); return np.tanh(1.5*(np.sin(2*np.pi*np.cumsum(30+80*np.exp(-t*9))/SR)*np.exp(-t*2)+lpf(rng.standard_normal(len(t)),2000)*np.exp(-t*6)*.35))*.3*g
def glass(): t=tt(1.4); return (np.sin(2*np.pi*2350*t)*np.exp(-t*4.5)+.5*np.sin(2*np.pi*3710*t)*np.exp(-t*6)+.3*np.sin(2*np.pi*5600*t)*np.exp(-t*9))*.035
def plop(): t=tt(.35); f=900*np.exp(-t*14)+300; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*12)*.08
def click(): t=tt(.04); return hpf(rng.standard_normal(len(t)),3000)*np.exp(-t*150)*.05
def lidpop(): t=tt(.3); return (bpf(rng.standard_normal(len(t)),300,1500)*np.exp(-t*25)+np.sin(2*np.pi*220*t)*np.exp(-t*30)*.6)*.09
def shimmer(g=1): t=tt(1.8); return sum(np.sin(2*np.pi*mid(m)*t)*np.exp(-t*(2.4+i*.3))*np.minimum(1,np.clip(t-i*.06,0,None)/.004) for i,m in enumerate([88,95,100]))*.016*g
def light(): t=tt(.45); return bpf(rng.standard_normal(len(t)),2500,10000)*np.sin(np.pi*t/.45)**2*.04
def tick(): t=tt(.05); return np.sin(2*np.pi*2600*t)*np.exp(-t*80)*.025
ev=[(1.0,2,tick()),(3.8,5,whoosh(.4,300,6000,.08)),(4,9,impact(.8)),(7.85,6,light()),(8.6,3,click()),(10.5,3,shimmer(.6)),
    (14.48,7,plop()),(15.1,4,glass()),(15.85,5,whoosh(.3,400,5000,.06)),(17,2,shimmer(.5)),
    (23.88,5,whoosh(.28,800,8000,.06)),(27,3,click()),(30,3,click()),(32.8,6,light()),(34,5,lidpop()),(36,2,shimmer(.6)),
    (40.85,6,whoosh(.35)),(49,9,impact(1)),(51.6,4,shimmer(1.2)),(54.8,4,whoosh(.6,200,3000,.05)),(61,2,tick())]
ev=[(b(t),p,s) for t,p,s in ev]
ev.sort(key=lambda e:-e[1]); kept=[]
for t,pr,sig in ev:
    if all(abs(t-k)>=.45 for k in kept): add(S,sig,t); kept.append(t)
# ---------------- mix ----------------
def rev(x,dec=2.4,l=2.2,fc=5500):
    it=tt(l); ir=rng.standard_normal(len(it))*np.exp(-it*dec); ir=lpf(ir,fc); ir/=np.sqrt((ir**2).sum()); return fftconvolve(x,ir)[:n]
def dly(x,dt,fb=.35,k=4):
    y=x.copy(); d=int(dt*SR)
    for i in range(1,k+1): y[d*i:]+=x[:-d*i]*fb**i
    return y
# no logo: corte seco da música (só pad + impacto) e retorno no outro
gate=np.ones(n); i0=int(b(49)*SR); i1=int(b(55)*SR); gate[i0:i1]=0
music=(K*gate+BASS*SC*gate+ARPF*SC+dly(ARPF*SC,3*ST,.3)*.4+CHO*SC*gate+rev(CHO,3,1.8)*.35+DR*gate+rev(DR,5,1)*.2
       +PAD*np.maximum(SC,.55)+rev(PAD,1.6,3,4000)*.5+VOX*SC+rev(dly(VOX,3*ST,.45),2,2)*.5+RIS)
fx=S+rev(S,2.5,2,6500)*.3
fade=np.ones(n); fo=int(.9*SR); fade[-fo:]=np.linspace(1,0,fo)
def save(B,name):
    B=hpf(B,30); B=np.tanh(B*1.35)/1.35*fade; B=B/np.max(np.abs(B))*.9; L=B.copy(); R=B.copy()
    hi=hpf(B,2500)*.16; L+=np.roll(hi,int(.012*SR)); R-=np.roll(hi,int(.012*SR)); St=np.stack([L,R],1); St/=np.max(np.abs(St))/.9
    w=os.path.join(HERE,name+'.wav')
    with wave.open(w,'wb') as f: f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((St*32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',w,'-b:a','256k',os.path.join(HERE,name+'.mp3')],check=True); os.remove(w)
save(music*.9+fx*1.15,'trilha_final'); save(fx,'so_efeitos'); print('ok')

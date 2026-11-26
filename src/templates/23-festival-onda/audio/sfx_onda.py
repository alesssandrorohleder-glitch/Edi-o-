# ONDA — efeitos sonoros sutis e variados, só nos movimentos grandes (um tipo de som para cada momento).
# Gera so_efeitos.mp3 e mixa com a música do Ale em trilha_ale.mp3 (música inteira, sem ducking + efeitos discretos).
import numpy as np, subprocess, os
from scipy.signal import butter, sosfilt, fftconvolve
SR=44100; DUR=32.0; N=int(SR*DUR); H=os.path.dirname(os.path.abspath(__file__)); rng=np.random.default_rng(5)
tt=lambda d: np.arange(int(d*SR))/SR
bp=lambda x,a,b: sosfilt(butter(2,[a,b],'band',fs=SR,output='sos'),x)
hp=lambda x,f: sosfilt(butter(2,f,'high',fs=SR,output='sos'),x)
lp=lambda x,f: sosfilt(butter(2,f,'low',fs=SR,output='sos'),x)
def sweep(n,f0,f1):  # ruído com filtro passa-faixa varrendo (em blocos)
    o=np.zeros_like(n);seg=int(.015*SR)
    for i in range(0,len(n),seg):
        u=i/len(n);c=f0*(f1/f0)**u;o[i:i+seg]=bp(n[i:i+seg+64],c*.6,min(c*1.6,20000))[:len(o[i:i+seg])]
    return o
def impact():      # logo: baque grave macio + ar
    t=tt(1.4);f=60*np.exp(-t*1.5)+32;return .9*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*3)+.15*lp(rng.standard_normal(len(t)),900)*np.exp(-t*6)
def air(d=.55):    # whoosh de ar (sobe e desce)
    t=tt(d);e=np.sin(np.pi*t/d)**2;return sweep(rng.standard_normal(len(t)),400,3500)*e
def tape(d=.4):    # swoosh rápido e brilhante
    t=tt(d);e=(t/d)**1.5*np.exp(-np.maximum(t-d*.8,0)*30);return sweep(rng.standard_normal(len(t)),1500,9000)*e*.8
def drop():        # pin caindo: "plop" de madeira
    t=tt(.25);f=520*np.exp(-t*9)+180;return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*18)
def riser(d=.9):   # subida curta antes do line-up
    t=tt(d);return sweep(rng.standard_normal(len(t)),300,6000)*(t/d)**2.5
def glass():       # toque de vidro (troca de dia)
    t=tt(1.0);return sum(a*np.sin(2*np.pi*f*t)*np.exp(-t*k) for f,a,k in ((1760,1,5),(2637,.5,7),(3520,.25,9)))
def sweepL(d=.6):  # varredura de luz (palcos)
    t=tt(d);e=np.sin(np.pi*t/d);return sweep(rng.standard_normal(len(t)),6000,800)*e*.8
def paper():       # ingresso entrando: papel/flick
    t=tt(.35);return hp(rng.standard_normal(len(t)),2500)*(np.exp(-t*25)+.5*np.exp(-np.abs(t-.12)*60))
def ticket_in(): # ingresso voando e girando (vibração de papel no ar) + "snap" ao assentar
    d=.8;t=tt(d);flut=.55+.45*np.sin(2*np.pi*np.cumsum(22-14*t/d)/SR);env=np.sin(np.pi*np.minimum(t/.62,1)/1)**1.2*(t<.62)
    air=sweep(rng.standard_normal(len(t)),5000,900)*flut*env
    snap=np.zeros(len(t));i=int(.6*SR);n=int(.12*SR);ts=np.arange(n)/SR
    snap[i:i+n]=hp(rng.standard_normal(n),3000)*np.exp(-ts*90)*.9+np.sin(2*np.pi*140*ts)*np.exp(-ts*35)*.6
    return air*.8+snap
def name_in(k=0): # nome entrando: sopro curtinho e agudo (bem discreto), timbre muda um pouco a cada nome
    d=.16;t=tt(d);c=5200+700*((k*37)%5);return bp(rng.standard_normal(len(t)),c*.7,c*1.4)*np.sin(np.pi*t/d)**2+.25*np.sin(2*np.pi*(c/4)*t)*np.exp(-t*60)
def shimmer():     # faixa holográfica girando
    t=tt(.9);return bp(rng.standard_normal(len(t)),7000,13000)*np.sin(np.pi*t/.9)**2*.7
def boom():        # logo final: sub profundo
    t=tt(1.6);f=48*np.exp(-t*1.2)+28;return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*2.2)
def rev(d=.8):     # swell reverso para o CTA
    t=tt(d);return hp(rng.standard_normal(len(t)),1500)*(t/d)**3
def chime():       # @ final: dois sinos suaves
    t=tt(1.4);s=np.sin(2*np.pi*1318.5*t)*np.exp(-t*3.5);i=int(.12*SR);s[i:]+=.7*np.sin(2*np.pi*1975.5*t[:-i])*np.exp(-t[:-i]*3.5);return s
# (tempo de início, som, ganho) — só movimentos grandes, nunca a menos de 0,45s um do outro
NAMES=[(t0+.12+i*.5) for t0 in (8,10,12,14) for i in range(3)]
EV=[(1.9,impact,.55),(3.75,air,.35),(5.7,tape,.3),(6.85,drop,.3),(7.3,lambda:riser(.7),.22),(12.12,glass,.12),(15.75,sweepL,.3),
    (21.9,ticket_in,.42),(24.0,shimmer,.25),(25.95,boom,.5),(27.3,rev,.25),(30.5,chime,.2)]
EV+=[(tn,(lambda k=k:name_in(k)),.07) for k,tn in enumerate(NAMES) if abs(tn-12.12)>.01]
ts=sorted(e[0] for e in EV);assert all(b-a>=.45 for a,b in zip(ts,ts[1:]))
sf=np.zeros(N);vs=np.zeros(N)
for t0,f,g in EV:
    s=f();s=s/np.max(np.abs(s))*g;i=int(t0*SR);n=min(len(s),N-i);sf[i:i+n]+=s[:n];vs[i:i+n]+=s[:n]*.5
ir=lp(rng.standard_normal(int(1.3*SR))*np.exp(-np.arange(int(1.3*SR))/SR*4),6000);ir/=np.sum(np.abs(ir))/6
L=sf+fftconvolve(vs,ir)[:N]*.25;R=sf+fftconvolve(vs,np.roll(ir,311))[:N]*.25
fx=np.stack([L,R],1)
def mp3(x,name):
    raw=(np.clip(x,-1,1)*32767).astype('<i2').tobytes()
    subprocess.run(['ffmpeg','-loglevel','error','-y','-f','s16le','-ar',str(SR),'-ac','2','-i','-','-b:a','256k',os.path.join(H,name)],input=raw,check=True)
mp3(fx/np.max(np.abs(fx))*.8,'so_efeitos.mp3')
subprocess.run(['ffmpeg','-loglevel','error','-y','-i',os.path.join(H,'musica_ale.mp3'),'-i',os.path.join(H,'so_efeitos.mp3'),'-filter_complex',
  '[1]volume=0.55[f];[0][f]amix=inputs=2:normalize=0,alimiter=limit=0.95',
  '-b:a','256k',os.path.join(H,'trilha_ale.mp3')],check=True);print('ok')

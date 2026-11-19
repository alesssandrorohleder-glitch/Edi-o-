# 28 — trilha de fundo leve (lo-fi house 120bpm, Am–F–C–G, sem detune) que abaixa sozinha quando a voz fala (sidechain pela voz)
# + efeitos sonoros nos cortes/impactos (nunca a menos de 0,45s um do outro). Gera trilha_final.mp3 (voz+música+efeitos),
# so_musica.mp3, so_efeitos.mp3 (música+efeitos sem voz) e narracao.mp3.
import numpy as np, subprocess, os, json
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, resample_poly
SR=44100;DUR=37.0;N=int(SR*DUR);H=os.path.dirname(os.path.abspath(__file__));rng=np.random.default_rng(11)
tt=lambda d: np.arange(int(d*SR))/SR
bp=lambda x,a,b: sosfilt(butter(2,[a,b],'band',fs=SR,output='sos'),x)
hp=lambda x,f: sosfilt(butter(2,f,'high',fs=SR,output='sos'),x)
lp=lambda x,f: sosfilt(butter(2,f,'low',fs=SR,output='sos'),x)
mf=lambda m: 440*2**((m-69)/12)
def add(b,t,s,g=1.):
    i=int(t*SR);n=min(len(s),len(b)-i)
    if n>0 and i>=0: b[i:i+n]+=s[:n]*g
M=np.zeros(N);F=np.zeros(N)
BT=.5
def kick(): t=tt(.3);f=50+90*np.exp(-t*40);return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*10)
def hat(): t=tt(.06);return hp(rng.standard_normal(len(t)),7000)*np.exp(-t*70)
def shaker(): t=tt(.09);return bp(rng.standard_normal(len(t)),4000,9000)*np.sin(np.pi*t/.09)**2
def rhodes(m,d):
    t=tt(d);f=mf(m);s=np.sin(2*np.pi*f*t)+.35*np.sin(2*np.pi*2*f*t)*np.exp(-t*3)+.12*np.sin(2*np.pi*3*f*t)*np.exp(-t*6)
    return s*np.minimum(1,t/.01)*np.exp(-t*1.1)*np.minimum(1,(d-t)/.08)
def sub(m,d): t=tt(d);return np.sin(2*np.pi*mf(m)*t)*np.minimum(1,t/.02)*np.minimum(1,(d-t)/.05)
def pluck(m): t=tt(.35);f=mf(m);return lp(np.sign(np.sin(2*np.pi*f*t))*.4+np.sin(2*np.pi*f*t),2400)*np.exp(-t*9)
CH=[(57,[69,72,76]),(53,[65,69,72]),(48,[67,72,76]),(55,[67,71,74])]   # Am F C G (vozes próximas, sem embolar)
MEL=[76,None,74,72,None,72,74,None]
for bar in range(int(DUR/2)+1):
    t0=bar*2.0;root,ch=CH[bar%4];intro=t0<1.0
    for n in ch: add(M,t0,rhodes(n,1.95),.07)
    add(M,t0,sub(root-12,1.9),.16)
    if t0>=1.0:
        for k in range(4): add(M,t0+k*BT,kick(),.30)
        for k in range(8): add(M,t0+k*BT/2+BT/4,hat(),.035)
        for k in range(16): add(M,t0+k*BT/4,shaker(),.018 if k%2 else .028)
    if t0>=6 and t0<32:
        for k,m in enumerate(MEL):
            if m: add(M,t0+k*BT/2,pluck(m),.05)
M=lp(M,9000)
# voz
sr,v=wavfile.read(os.path.join(H,'voz.wav'));v=v.astype(np.float32)/32768;v=resample_poly(v,SR,sr)[:N];v=np.pad(v,(0,N-len(v)));v=v/np.max(np.abs(v))*.92
# sidechain: música cai ~8 dB enquanto há fala
e=np.convolve(np.abs(v),np.ones(int(.05*SR))/int(.05*SR),'same');act=(e>.02).astype(float)
k=np.zeros(N);a=0
for i in range(0,N,256):
    tgt=act[i];a+=(tgt-a)*(.35 if tgt>a else .04);k[i:i+256]=a
duck=1-.6*k
# ---------- efeitos ----------
def whoosh(d=.35,lo=500,hi=6000):
    t=tt(d);n=rng.standard_normal(len(t));o=np.zeros_like(n);seg=int(.012*SR)
    for i in range(0,len(n),seg):u=i/len(n);c=lo*(hi/lo)**u;o[i:i+seg]=bp(n[i:i+seg+64],c*.6,min(c*1.6,20000))[:len(o[i:i+seg])]
    return o*np.sin(np.pi*t/d)**2
def impact(): t=tt(1.0);f=55*np.exp(-t*2)+35;return np.tanh(2*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*4))+.3*lp(rng.standard_normal(len(t)),1200)*np.exp(-t*12)
def crack():
    t=tt(.5);s=np.zeros(len(t))
    for j in range(7):i=int((j*.012+rng.random()*.006)*SR);c=hp(rng.standard_normal(int(.03*SR)),1800)*np.exp(-np.arange(int(.03*SR))/SR*120);s[i:i+len(c)]+=c*(1-j*.1)
    return s+.5*np.sin(2*np.pi*np.cumsum(120*np.exp(-t*8)+60)/SR)*np.exp(-t*10)
def pop(f=900): t=tt(.12);return np.sin(2*np.pi*np.cumsum(f*np.exp(-t*12)+f*.5)/SR)*np.exp(-t*30)
def ding(f=1320): t=tt(.8);return (np.sin(2*np.pi*f*t)+.4*np.sin(2*np.pi*f*2.01*t))*np.exp(-t*5)
def tick(): t=tt(.05);return np.sin(2*np.pi*2200*t)*np.exp(-t*90)
def clank(): t=tt(.7);return sum(a*np.sin(2*np.pi*f*t)*np.exp(-t*k) for f,a,k in((620,1,7),(1580,.5,10),(2900,.3,14)))
def flick(): s=np.zeros(int(.8*SR))
def flips():
    s=np.zeros(int(.9*SR))
    for j in range(6):c=bp(rng.standard_normal(int(.05*SR)),2000,7000)*np.exp(-np.arange(int(.05*SR))/SR*60);i=int(j*.15*SR);s[i:i+len(c)]+=c
    return s
def click(): t=tt(.06);return hp(rng.standard_normal(len(t)),3000)*np.exp(-t*160)+np.sin(2*np.pi*1800*t)*np.exp(-t*120)
def sparkle(): t=tt(.9);return sum(np.sin(2*np.pi*f*t)*np.exp(-t*6)*(t>d) for f,d in((2093,0),(2637,.08),(3136,.16)))
CUTS=[3.2,6.5,11.1,16.6,20.5,26.0,29.2,32.5]
EV=[(0.0,impact,.4,9),(0.76,lambda:impact()[:int(.6*SR)],.28,7),(2.04,lambda:ding(1319),.15,6),(3.82,lambda:impact()[:int(.5*SR)],.24,7),(4.68,tick,.14,4),(5.18,tick,.14,4),
    (8.66,lambda:ding(1047),.14,6),(9.3,pop,.12,4),(12.12,lambda:impact()[:int(.5*SR)],.2,6),(14.14,pop,.12,4),(15.26,lambda:ding(1047),.14,6),(17.0,lambda:whoosh(.5,2000,8000),.08,4),(17.6,lambda:whoosh(.5,2000,8000),.08,4),(18.84,lambda:ding(1568),.15,6),
    (20.6,lambda:impact()[:int(.5*SR)],.22,6),(21.46,lambda:impact()[:int(.5*SR)],.22,6),(22.66,pop,.14,5),(23.7,pop,.14,5),(24.54,pop,.14,5),(26.32,lambda:impact()[:int(.6*SR)],.26,7),(27.6,lambda:whoosh(.5,300,3000),.12,4),(28.14,lambda:whoosh(.6,300,5000),.14,5),
    (29.96,lambda:impact()[:int(.6*SR)],.26,7),(30.5,pop,.12,3),(30.9,pop,.12,3),(31.3,pop,.12,3),(33.04,click,.3,7),(33.6,sparkle,.12,5)]
EV+=[(c-.12,lambda:whoosh(.3,700,7000),.12,3) for c in CUTS]
EV.sort(key=lambda e:-e[3]);kept=[]
for e in EV:
    if all(abs(e[0]-k[0])>=.45 for k in kept):kept.append(e)
kept.sort(key=lambda e:e[0])
for t0,f,g,_ in kept: s=f();s=s/np.max(np.abs(s))*g;add(F,t0,s)
print('efeitos:',len(kept),'de',len(EV))
def norm(x,pk=.9): return x/np.max(np.abs(x))*pk
mus=M*duck
mus*=np.clip((DUR-np.arange(N)/SR)/.6,0,1)
mix=v+mus*.55+F*.8;mix=np.tanh(mix/np.max(np.abs(mix))*1.3)/np.tanh(1.3)*.95
def mp3(x,name):
    raw=(np.clip(x,-1,1)*32767).astype('<i2').tobytes();subprocess.run(['ffmpeg','-loglevel','error','-y','-f','s16le','-ar',str(SR),'-ac','1','-i','-','-b:a','256k',os.path.join(H,name)],input=raw,check=True)
mp3(mix,'trilha_final.mp3');mp3(norm(M),'so_musica.mp3');mp3(norm(M*.7+F),'so_efeitos.mp3');mp3(v,'narracao.mp3')
# nível relativo (RMS) para conferir que a música não atrapalha a fala
sp=act>0;print('RMS voz %.3f | música sob a voz %.3f (%.1f dB abaixo)'%(np.sqrt(np.mean(v[sp]**2)),np.sqrt(np.mean(mus[sp]**2)),20*np.log10(np.sqrt(np.mean(v[sp]**2))/np.sqrt(np.mean(mus[sp]**2)))))

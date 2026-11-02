# Trilha eletrônica (melodic tech-house 128bpm) + efeitos do vídeo 18 (Gaia). Gera trilha_final.mp3 e so_efeitos.mp3.
import numpy as np, wave, subprocess, os
from scipy.signal import fftconvolve, butter, sosfilt
SR=44100; BT=60/128; D=72*BT; n=int(SR*D); rng=np.random.default_rng(18); HERE=os.path.dirname(os.path.abspath(__file__))
M=np.zeros((n,2)); S=np.zeros((n,2))
def tt(d): return np.arange(int(d*SR))/SR
def add(B,sig,at,g=1.0,pan=0.0):
    i=int(round(at*SR)); j=min(n,i+len(sig))
    if j<=i or i<0: return
    B[i:j,0]+=sig[:j-i]*g*(1-pan*.6); B[i:j,1]+=sig[:j-i]*g*(1+pan*.6)
def lpf(x,fc): return sosfilt(butter(2,fc,'low',fs=SR,output='sos'),x)
def hpf(x,fc): return sosfilt(butter(2,fc,'high',fs=SR,output='sos'),x)
def bpf(x,a,b): return sosfilt(butter(2,[a,b],'band',fs=SR,output='sos'),x)
mid=lambda m: 440*2**((m-69)/12)
def env(d,a=.005,r=.1): t=tt(d); return np.minimum(1,t/a)*np.clip((d-t)/r,0,1)
b=lambda k:k*BT
# ---- instrumentos (uma frequência por voz, sem detune) ----
def kick(): t=tt(.42); return np.tanh(1.6*np.sin(2*np.pi*np.cumsum(46+120*np.exp(-t*38))/SR)*np.exp(-t*7.5))*.6
def clap():
    t=tt(.25); nz=bpf(rng.standard_normal(len(t)),1100,6500); e=sum(np.exp(-np.clip(t-d,0,None)*75)*(t>=d) for d in (0,.011,.022))+np.exp(-t*14)*.35; return nz*e*.13
def hat(o=False): d=.22 if o else .05; t=tt(d); return hpf(rng.standard_normal(len(t)),8500)*np.exp(-t*(14 if o else 70))*(.045 if o else .04)
def bass(f,d): t=tt(d); s=np.sin(2*np.pi*f*t)+.35*np.sin(4*np.pi*f*t)+.15*np.sin(6*np.pi*f*t); return lpf(s,420)*env(d,.004,.03)*.22
def sub(f,d): t=tt(d); return np.sin(2*np.pi*f*t)*env(d,.3,.3)*.16
def pad(ms,d,fc=1400): t=tt(d); s=sum(np.sin(2*np.pi*mid(m)*t)+.3*np.sin(4*np.pi*mid(m)*t) for m in ms)/len(ms); return lpf(s,fc)*env(d,.4,.5)*.06
def pluck(f,d=.35,fc=3000): t=tt(d); s=np.sign(np.sin(2*np.pi*f*t))*.5+np.sin(2*np.pi*f*t)*.5; return lpf(s,fc)*np.exp(-t*9)*np.minimum(1,t/.002)*.05
def stab(ms,d=.22): t=tt(d); s=sum(np.sin(2*np.pi*mid(m)*t)+.4*np.sin(4*np.pi*mid(m)*t) for m in ms)/len(ms); return lpf(s,2400)*np.exp(-t*10)*np.minimum(1,t/.003)*.09
# F#m – D – A – E  (vi-IV-I-V em Lá maior, clima noturno)
CH=[(42,[66,69,73]),(38,[62,66,69]),(45,[64,69,73]),(40,[64,68,71])]
LEAD=[73,76,78,76, 73,71,69,71, 69,73,76,73, 71,68,71,73]
def sec(beat):  # 'intro','drop','break','outro'
    if beat<8: return 'intro'
    if 48<=beat<56: return 'break'
    if beat>=68: return 'outro'
    return 'drop'
for bar in range(18):
    b0=bar*4; tb=b(b0); root,ch=CH[bar%4]; sc=sec(b0)
    add(M,pad([m+12 for m in ch],b(4),900 if sc=='intro' else (1800 if sc=='break' else 1300)),tb,1.2 if sc in('intro','break','outro') else .8)
    if sc in ('intro','break'):
        add(M,sub(mid(root),b(4)),tb,.8)
        for k in range(8): add(M,pluck(mid(ch[k%3]+12+(12 if k%4==3 else 0)),fc=1200 if sc=='intro' else 2200),tb+b(k*.5),.8,pan=(-.4 if k%2 else .4))
        continue
    if sc=='outro':
        add(M,sub(mid(root),b(4)),tb,.8); add(M,stab([m+12 for m in ch],1.2),tb,.8); continue
    for q in range(4):
        tq=tb+b(q); add(M,kick(),tq)
        if q in(1,3): add(M,clap(),tq)
        add(M,hat(),tq+b(.25),.6,pan=-.3); add(M,hat(True),tq+b(.5),1,pan=.3); add(M,hat(),tq+b(.75),.6,pan=-.3)
        add(M,bass(mid(root),b(.4)),tq+b(.5)); add(M,bass(mid(root),b(.2)),tq+b(.75),.6)
    if b0>=20:
        for i in range(4): add(M,pluck(mid(LEAD[(bar%4)*4+i]),.4,3500),tb+b(i),1.0,pan=.15); add(M,pluck(mid(LEAD[(bar%4)*4+i]),.3,2500),tb+b(i+.75),.45,pan=-.15)
    add(M,stab([m+12 for m in ch]),tb+b(1.5),.8); add(M,stab([m+12 for m in ch]),tb+b(3.5),.6)
# ---- efeitos ----
def whoosh(d=.35,a=600,b2=5000,g=.06): t=tt(d); return bpf(rng.standard_normal(len(t)),a,b2)*np.sin(np.pi*t/d)**2*g
def riser(d): t=tt(d); f=200+3000*(t/d)**2; nz=rng.standard_normal(len(t)); return (bpf(nz,300,6000)*.5+np.sin(2*np.pi*np.cumsum(f)/SR)*.15)*(t/d)**2*.08
def impact(g=1):
    t=tt(1.6); boom=np.sin(2*np.pi*np.cumsum(30+70*np.exp(-t*12))/SR)*np.exp(-t*2.5); nz=lpf(rng.standard_normal(len(t)),2500)*np.exp(-t*7)*.5
    return (boom+nz)*.32*g
def hitL(): t=tt(.4); return (np.sin(2*np.pi*np.cumsum(60+140*np.exp(-t*30))/SR)*np.exp(-t*9)+lpf(rng.standard_normal(len(t)),4000)*np.exp(-t*25)*.4)*.16
def tick(): t=tt(.06); return np.sin(2*np.pi*2100*t)*np.exp(-t*70)*.03
def pop(): t=tt(.12); f=500*(1+1.2*np.exp(-t*45)); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*28)*.05
def shimmer(): t=tt(1.4); return sum(np.sin(2*np.pi*mid(m)*t)*np.exp(-t*2.6)*np.minimum(1,np.clip(t-i*.06,0,None)/.005) for i,m in enumerate([81,85,88,93]))*.025
def hiss(d): t=tt(d); return bpf(rng.standard_normal(len(t)),2500,9000)*np.sin(np.pi*t/d)*.02
# (tempo, prioridade, sinal) — prioridade maior vence quando ficam a menos de 0,45s
ev=[(b(1.2),2,whoosh(.6,300,3000,.05)),(b(2),3,hitL()),(b(4),3,hitL()),(b(6.2),3,whoosh(.8,300,4000,.06)),
    (b(8),9,impact(1)),(b(10),4,hitL()),(b(12),9,impact(.9)),(b(12.6),2,shimmer()),(b(15),2,tick()),(b(19.4),3,whoosh(.4))]
for k in [20,24,26,28,30,32,34,36,38,40,42,44,45,46,47,50,52,54,60]:
    ev.append((b(k)-.12,5 if k in(24,32,36,40,44) else 4,whoosh(.32,700,6000,.05 if k in(45,46,47) else .065)))
for k in [24,32,36,40,44]: ev.append((b(k)+.06,3,hitL()))
ev+=[(b(48),7,impact(.55)),(b(48.3),1,hiss(b(7))),(b(56),9,impact(1)),(b(57.4),3,pop()),(b(58),3,pop()),(b(58.6),3,pop()),
     (b(61),3,pop()),(b(61.6),3,pop()),(b(64),9,impact(1)),(b(64.5),2,shimmer()),(b(66),3,pop()),(b(67),2,tick())]
for st,dd in [(0,b(8)),(b(52),b(4)),(b(60),b(4))]: add(M,riser(dd),st,.9)
ev.sort(key=lambda e:-e[1]); kept=[]
for t,pr,sig in ev:
    if pr<=1 or all(abs(t-k)>=.45 for k in kept): add(S,sig,t); kept.append(t) if pr>1 else None
# mix
it=tt(1.4); ir=rng.standard_normal(len(it))*np.exp(-it*4.5); ir=lpf(ir,7000); ir/=np.sqrt((ir**2).sum())
wet=np.stack([fftconvolve(M[:,0],ir)[:n],fftconvolve(M[:,1],ir)[:n]],1)
wetS=np.stack([fftconvolve(S[:,0],ir)[:n],fftconvolve(S[:,1],ir)[:n]],1)
fade=np.ones(n); fo=int(.7*SR); fade[-fo:]=np.linspace(1,0,fo)
def save(B,name):
    B=np.tanh(B*1.3)/1.3; B=B*fade[:,None]; B=B/np.max(np.abs(B))*.9; w=os.path.join(HERE,name+'.wav')
    with wave.open(w,'wb') as f: f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((B*32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',w,'-b:a','224k',os.path.join(HERE,name+'.mp3')],check=True); os.remove(w)
save(M*.85+wet*.14+S*1.15+wetS*.15,'trilha_final'); save(S+wetS*.15,'so_efeitos'); print('ok')

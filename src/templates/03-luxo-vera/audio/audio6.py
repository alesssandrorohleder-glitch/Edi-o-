import numpy as np, wave
from scipy.signal import fftconvolve, butter, sosfilt
SR=44100; D=36.0; n=int(SR*D); rng=np.random.default_rng(8)
M=np.zeros((n,2)); S=np.zeros((n,2))
def tt(d): return np.arange(int(d*SR))/SR
def add(B,sig,at,g=1.0,pan=0.0):
    i=int(round(at*SR)); j=min(n,i+len(sig))
    if j<=i or i<0: return
    B[i:j,0]+=sig[:j-i]*g*(1-pan*.6); B[i:j,1]+=sig[:j-i]*g*(1+pan*.6)
def lpf(x,fc,o=2): return sosfilt(butter(o,fc,'low',fs=SR,output='sos'),x)
def hpf(x,fc,o=2): return sosfilt(butter(o,fc,'high',fs=SR,output='sos'),x)
def bpf(x,a,b): return sosfilt(butter(2,[a,b],'band',fs=SR,output='sos'),x)
mid=lambda m: 440*2**((m-69)/12)
BEAT=.5; BAR=2.0
# --- drums
def kick(): t=tt(.45); f=48+170*np.exp(-t*40); s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7.5); return np.tanh(s*1.8)*.85+hpf(rng.standard_normal(len(t)),3000)*np.exp(-t*200)*.15
def clap():
    t=tt(.35); nz=bpf(rng.standard_normal(len(t)),900,5000); e=np.zeros(len(t))
    for d in (0,.011,.022): e+=np.exp(-np.clip(t-d,0,None)*60)*(t>=d)
    e+=np.exp(-t*14)*.6; return nz*e*.32
def hat(o=False): t=tt(.22 if o else .05); return hpf(rng.standard_normal(len(t)),7500)*np.exp(-t*(11 if o else 70))*(.16 if o else .09)
def crash(): t=tt(2.0); return hpf(rng.standard_normal(len(t)),4000)*np.exp(-t*2.2)*.16
def riser(d): t=tt(d); nz=rng.standard_normal(len(t)); u=t/d; s=hpf(nz,300)*u**2.2; return lpf(s,8000)*.16
# --- tonal (clean: integer harmonics, no detune)
def organ(f,d): t=tt(d); s=np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*2*f*t)+.25*np.sin(2*np.pi*3*f*t)+.12*np.sin(2*np.pi*4*f*t); return s*np.exp(-t*7)*np.minimum(1,t/.003)*np.clip((d-t)/.02,0,1)
def stab(ms,d=.28): return sum(organ(mid(m),d) for m in ms)/len(ms)*.20
def bass(f,d): t=tt(d); s=np.tanh((np.sin(2*np.pi*f*t)+.3*np.sin(2*np.pi*2*f*t))*1.4); return s*np.minimum(1,t/.004)*np.clip((d-t)/.015,0,1)*.30
def pluck(f,d=.35): t=tt(d); s=np.sin(2*np.pi*f*t)+.4*np.sin(2*np.pi*2*f*t)+.15*np.sin(2*np.pi*3*f*t); return s*np.exp(-t*10)*np.minimum(1,t/.002)*.10
def padc(ms,d): t=tt(d); s=sum(np.sin(2*np.pi*mid(m)*t)+.3*np.sin(2*np.pi*2*mid(m)*t) for m in ms)/len(ms); return lpf(s,2200)*np.minimum(1,t/.3)*np.clip((d-t)/.25,0,1)*.10
# Am7 | Fmaj7 | Dm7 | Em7   (one chord per bar)
CH=[(45,[60,64,67,69]),(41,[60,64,65,69]),(38,[60,62,65,69]),(40,[59,62,64,67])]
LEAD=[76,74,72,69, 72,74,76,79, 77,76,74,72, 74,71,72,74]   # A-minor/pentatonic hook, 8ths on selected steps
side=np.ones(n)
nb=int(D/BAR)
for b in range(nb):
    tb=b*BAR; root,ch=CH[b%4]
    sec='intro' if tb<6 else 'brk' if 24<=tb<30 else 'end' if tb>=35 else 'full'
    drop2 = tb>=30
    if sec in('full','intro'):
        for q in range(4):
            tq=tb+q*BEAT
            add(M,kick(),tq,.9 if sec=='full' else .75)
            i=int(tq*SR); seg=1-.6*np.exp(-np.arange(int(.3*SR))/SR*12); k=min(len(seg),n-i); side[i:i+k]=np.minimum(side[i:i+k],seg[:k])
            if q%2==1: add(M,clap(),tq,1 if sec=='full' else .6)
            add(M,hat(True),tq+BEAT/2,1 if sec=='full' else .6,pan=.25)
            if sec=='full':
                for h in (1,3): add(M,hat(),tq+h*BEAT/4,.8,pan=-.3)
    if sec=='brk':
        add(M,padc(ch,BAR),tb,1.0)
        if tb>=28:  # snare-ish clap roll into the drop
            for k in range(16): add(M,clap(),tb+k*BAR/16,.25+.5*k/16)
    # chord stabs: syncopated house pattern (in 8ths): 1, 2&, 3&, 4
    if sec in ('intro','full'):
        for pos in (0,1.5,2.5,3.0):
            add(M,stab(ch),tb+pos*BEAT,.9 if sec=='full' else .7,pan=.15)
    # bass: offbeat 8ths, root/octave
    if sec=='full' or (sec=='intro' and tb>=2):
        for q in range(4):
            add(M,bass(mid(root)*(2 if q==3 else 1),BEAT/2*.85),tb+q*BEAT+BEAT/2,1)
    # lead hook in scenes 3-4 and final drop
    if (12<=tb<24) or drop2:
        if sec!='end':
            for k in range(8):
                note=LEAD[(b%2)*8+k]
                if k in (0,2,3,5,6): add(M,pluck(mid(note+12 if drop2 else note)),tb+k*BEAT/2,1,pan=(-.3 if k%2 else .3))
    if sec=='end' and tb<D: add(M,stab(ch,.9),tb,.9); add(M,bass(mid(root),.9),tb,1)
M[:, :]*=side[:,None]**1.0
# scene cuts: crash on downbeat + riser into it
for c in [6,12,18,30]:
    add(M,riser(1.0),c-1.0,1); add(M,crash(),c,1)
add(M,riser(2.0),28.0,1.3); add(M,crash(),24.0,.8)
add(M,kick(),30.0,1.0)
# --- sfx: tiered, single, quantized to the beat, never on a crash
mid_t=lambda t: CH[int(t//BAR)%4][1]
def SMALLs(t): f=mid(mid_t(t)[2]+24); x=tt(.1); return np.sin(2*np.pi*f*x)*np.exp(-x*45)*.03
def MEDs(t): f=mid(mid_t(t)[0]+24); x=tt(.6); return (np.sin(2*np.pi*f*x)+.25*np.sin(2*np.pi*2*f*x))*np.exp(-x*7)*np.minimum(1,x/.003)*.05
def BIGs(t):
    c=mid_t(t); x=tt(1.0); f1=mid(c[0]+12); f2=mid(c[2]+12)
    return (np.sin(2*np.pi*f1*x)+.6*np.sin(2*np.pi*f2*x))*np.exp(-x*3.5)*np.minimum(1,x/.003)*.07
ev=[(1.0,'M'),(1.5,'S'),(2.5,'M'),(3.5,'B'),(7.5,'B'),(8.5,'M'),(9.5,'S'),(13.5,'B'),(14.0,'S'),(15.5,'S'),
    (18.5,'S'),(19.0,'B'),(19.5,'M'),(21.0,'M'),(21.5,'S'),(24.5,'M'),(27.0,'M'),(27.5,'S'),(28.0,'B'),
    (30.5,'M'),(31.0,'B'),(31.5,'S'),(32.0,'S'),(32.5,'S'),(33.0,'M'),(33.5,'M')]
last=-9
for t,k in ev:
    if t-last<0.45 or any(abs(t-c)<.1 for c in [6,12,18,24,30]): continue
    add(S,{'S':SMALLs,'M':MEDs,'B':BIGs}[k](t),t,pan=0); last=t
it=tt(1.2); ir=rng.standard_normal(len(it))*np.exp(-it*5); ir=lpf(ir,6000); ir/=np.sqrt((ir**2).sum())
wet=np.stack([fftconvolve(M[:,0],ir)[:n],fftconvolve(M[:,1],ir)[:n]],1)
out=M*.9+wet*.12+S
t=np.arange(n)/SR; out*=np.clip((D-t)/1.0,0,1)[:,None]
out=np.tanh(out/np.abs(out).max()*1.6)/np.tanh(1.6)*.93
w=wave.open('audio_vera_house.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out.reshape(-1)*32767).astype(np.int16).tobytes()); w.close(); print('ok')

import numpy as np, wave
from scipy.signal import fftconvolve, butter, sosfilt
SR=44100; D=36.0; n=int(SR*D); rng=np.random.default_rng(5)
M=np.zeros((n,2)); S=np.zeros((n,2))
def tt(d): return np.arange(int(d*SR))/SR
def add(B,sig,at,g=1.0,pan=0.0):
    i=int(round(at*SR)); j=min(n,i+len(sig))
    if j<=i or i<0: return
    B[i:j,0]+=sig[:j-i]*g*(1-pan*.8); B[i:j,1]+=sig[:j-i]*g*(1+pan*.8)
def lpf(x,fc,o=2): return sosfilt(butter(o,fc,'low',fs=SR,output='sos'),x)
def hpf(x,fc,o=2): return sosfilt(butter(o,fc,'high',fs=SR,output='sos'),x)
def bpf(x,lo,hi): return sosfilt(butter(2,[lo,hi],'band',fs=SR,output='sos'),x)
mid=lambda m: 440*2**((m-69)/12)
# ---- instruments
def piano(f,d=3.0,v=1.0):
    t=tt(d); s=np.zeros_like(t)
    for k,(g,dec) in enumerate([(1,1.6),(.5,2.4),(.25,3.2),(.12,4.5),(.06,6)],1):
        s+=g*np.sin(2*np.pi*f*k*1.0007**k*t)*np.exp(-t*dec)
    return s*np.minimum(1,t/.004)*np.minimum(1,(d-t)/.2)*.18*v
def pad(fs,d):
    t=tt(d); s=sum(np.sin(2*np.pi*f*t+.3*np.sin(2*np.pi*.2*t))+.5*np.sin(2*np.pi*f*2.003*t) for f in fs)/len(fs)
    return s*np.sin(np.pi*np.clip(t/d,0,1))**.8*.10
def sub(f,d): t=tt(d); return np.sin(2*np.pi*f*t)*np.minimum(1,t/.05)*np.minimum(1,(d-t)/.3)*.22
def softkick(): t=tt(.6); return np.sin(2*np.pi*np.cumsum(42+60*np.exp(-t*25))/SR)*np.exp(-t*6)*.55
def snap(): t=tt(.15); nz=rng.standard_normal(len(t)); return bpf(nz,1500,4500)*np.exp(-t*40)*.4
def shaker(): t=tt(.08); return hpf(rng.standard_normal(len(t)),6000)*np.sin(np.pi*t/.08)**2*.07
# Fmaj7  Em7  Dm9  Cmaj7  (3s each = 1 bar @80bpm)
ch=[[53,57,60,64,67],[52,55,59,62,67],[50,53,57,60,64],[48,52,55,59,64]]
bar=3.0; beat=.75
for b in range(12):
    tb=b*bar; c=ch[b%4]; brk=8<=b<10
    add(M,pad([mid(m) for m in c[1:]],bar+.4),tb,1.0)
    add(M,sub(mid(c[0]-12),bar),tb,.9 if not brk else .5)
    # piano: chord on 1, arpeggio
    for i,m in enumerate(c[1:]): add(M,piano(mid(m+12),3.0,.7),tb+i*.03,1,pan=-.3+i*.2)
    arp=[c[1]+24,c[3]+12,c[2]+24,c[4]+12,c[3]+24,c[2]+12]
    for k in range(6 if not brk else 3):
        add(M,piano(mid(arp[k]),1.6,.45),tb+beat*(k*.66+ (1 if brk else 0)) if False else tb+k*beat*0.666,1,pan=(.4 if k%2 else -.4))
    if b>=2 and not brk and b<11:
        for q in range(4):
            if q in (0,2): add(M,softkick(),tb+q*beat,.8)
            if q in (1,3) and b>=4: add(M,snap(),tb+q*beat,.5,pan=.2)
            for h in range(2): add(M,shaker(),tb+q*beat+h*beat/2,1 if h else .6,pan=-.3)
# ---- sfx
def swell(d=1.4,lo=300,hi=3000,g=.35):
    t=tt(d); nz=rng.standard_normal(len(t)); s=bpf(nz,lo,hi); e=np.sin(np.pi*t/d)**2
    return s*e*g
def rswell(d=1.0): t=tt(d); s=bpf(rng.standard_normal(len(t)),400,6000); return s*(t/d)**3*.4
def boom(): t=tt(3.0); return (np.sin(2*np.pi*np.cumsum(38+30*np.exp(-t*6))/SR)*np.exp(-t*1.6)+lpf(rng.standard_normal(len(t)),200)*np.exp(-t*3)*.3)*.7
def bell(f,d=3.0,g=.25):
    t=tt(d); s=sum(a*np.sin(2*np.pi*f*r*t)*np.exp(-t*k) for r,a,k in [(1,1,1.2),(2.0,.5,2),(2.76,.35,3),(5.4,.15,5),(8.9,.06,8)])
    return s*np.minimum(1,t/.002)*g
def chime(root): o=np.zeros(int(3.5*SR)); 
def chord_chime(ms,spread=.06,g=.22):
    o=np.zeros(int(3.6*SR))
    for i,m in enumerate(ms): b=bell(mid(m),3.2,g); j=int(i*spread*SR); o[j:j+len(b)]+=b[:len(o)-j]
    return o
def shimmer(d=1.4,g=.12):
    o=np.zeros(int((d+.6)*SR))
    for k in range(int(d*22)):
        f=3000+rng.random()*5000; b=np.sin(2*np.pi*f*tt(.25))*np.exp(-tt(.25)*18)
        j=int(rng.random()*d*SR); o[j:j+len(b)]+=b[:len(o)-j]*(.4+.6*rng.random())
    return o*g
def harp(f,d=2.0,g=.35):
    N=int(SR/f); buf=rng.uniform(-1,1,N); L=int(d*SR); out=np.zeros(L)
    for i in range(L): out[i]=buf[i%N]; buf[i%N]=.996*.5*(buf[i%N]+buf[(i+1)%N])
    return out*g
def ting(f=4200): t=tt(1.2); return (np.sin(2*np.pi*f*t)*np.exp(-t*5)+.4*np.sin(2*np.pi*f*2.41*t)*np.exp(-t*8))*.15
def scratch(d=1.8): t=tt(d); nz=bpf(rng.standard_normal(len(t)),2500,7000); return nz*np.sin(np.pi*t/d)*(0.6+.4*np.sin(2*np.pi*3*t))*.06
A=lambda *a,**k: add(S,*a,**k)
# S1
A(swell(1.6,200,2500,.25),.2); A(shimmer(1.2,.06),.6)
A(swell(1.2,400,3000,.18),.8,pan=-.2); A(swell(1.2,400,3000,.18),1.3,pan=.2); A(swell(1.1,400,3000,.2),2.6)
A(chord_chime([77,81,84,88]),3.35,1); A(shimmer(1.4,.12),3.9)
A(rswell(1.0),5.0); A(boom(),6.0,.8)
# S2
A(scratch(1.8),6.2); A(swell(2.0,150,1200,.2),6.4); A(bell(mid(53),3.5,.35),7.6); A(bell(mid(65),3,.18),7.62)
A(shimmer(1.2,.12),8.6); A(swell(1.6,500,5000,.22),8.4); A(harp(mid(77),1.5,.25),9.2); A(harp(mid(81),1.5,.2),9.5,pan=.3)
A(rswell(1.0),11.0); A(boom(),12.0,.8)
# S3
A(swell(2.2,150,1500,.22),12.0); A(chord_chime([76,79,83],.08,.18),13.6); A(swell(1.2,800,5000,.15),14.2)
for i,tq in enumerate([14.8,15.4,16.0]): A(ting(4200+i*500),tq+.2,1,pan=(-.4,.4,0)[i])
A(swell(1.2,300,2000,.12),15.4)
A(rswell(1.0),17.0); A(boom(),18.0,.7)
# S4
A(swell(1.2,300,3000,.15),18.3); A(harp(mid(62),1.6,.3),18.5); A(swell(1.2,300,3000,.18),19.0); A(shimmer(1.6,.12),20.4)
for i in range(3): A(harp(mid([74,77,81][i]),1.8,.3),21.0+i*.25,pan=-.5+i*.5)
A(rswell(1.0),23.0); A(boom(),24.0,1.0)
# S5
A(swell(1.5,300,2500,.15),24.4); A(swell(1.0,300,2500,.12),26.3); A(swell(1.1,400,3000,.16),26.9,pan=-.2); A(swell(1.1,400,3000,.16),27.3,pan=.2)
A(chord_chime([72,76,79,83,88],.07,.22),27.9); A(shimmer(1.4,.13),28.4); A(swell(1.2,1000,6000,.12),28.6)
A(rswell(1.0),29.0); A(boom(),30.0,.8)
# S6
A(swell(1.2,300,3000,.16),30.3); A(chord_chime([77,81,84],.06,.18),30.7); A(shimmer(1.6,.12),31.6)
for i in range(4): A(harp(mid([72,76,79,84][i]),1.6,.25),31.7+i*.2,pan=-.4+i*.27)
A(bell(mid(65),3.5,.3),32.7); A(bell(mid(77),3,.15),32.72); A(swell(1.1,400,3000,.15),33.3); A(chord_chime([65,72,77,81,84],.1,.18),34.6)
# reverb on everything
ir_t=tt(2.6); ir=rng.standard_normal(len(ir_t))*np.exp(-ir_t*2.4); ir=lpf(ir,6000); ir/=np.sqrt((ir**2).sum())
mix=M*.8+S*1.0
wet=np.stack([fftconvolve(mix[:,0],ir)[:n],fftconvolve(mix[:,1],ir[::-1].copy()*0+np.roll(ir,37))[:n]],1)
out=mix*.8+wet*.35
t=np.arange(n)/SR; out*=np.clip((D-t)/1.8,0,1)[:,None]*np.clip(t/.3,0,1)[:,None]
out=np.tanh(out/np.abs(out).max()*1.3)/np.tanh(1.3)*.93
w=wave.open('audio_lux.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out.reshape(-1)*32767).astype(np.int16).tobytes()); w.close(); print('ok')

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter,lfilter,fftconvolve
SR=44100;O=2.8125;N=int(round(O*SR));rng=np.random.default_rng(5)
def tt(d):return np.arange(int(d*SR))/SR
def lp(s,f):b,a=butter(2,f/(SR/2));return lfilter(b,a,s)
def hp(s,f):b,a=butter(2,f/(SR/2),'high');return lfilter(b,a,s)
L=np.zeros(N+SR*3);R=np.zeros(N+SR*3)
def add(s,t,g=1,pan=0):
    i=int(t*SR);gl=g*np.cos((pan+1)*np.pi/4)*1.414;gr=g*np.sin((pan+1)*np.pi/4)*1.414
    L[i:i+len(s)]+=s*gl;R[i:i+len(s)]+=s*gr
SM=0.9375
# rising whoosh into smash
d=.9;t=tt(d);n=rng.standard_normal(len(t));out=np.zeros_like(n);seg=int(.02*SR)
for i in range(0,len(n),seg):out[i:i+seg]=lp(n[i:i+seg+64],400+7000*(i/len(n))**2)[:len(out[i:i+seg])]
add(hp(out,150)*(t/d)**2*.5,SM-d)
# low sub swell
t=tt(.9);add(np.sin(2*np.pi*(40+20*t/.9)*t)*(t/.9)**2*.35,SM-.9)
# smash: boom + crack + shatter
t=tt(2.0);fr=34+110*np.exp(-t*12);boom=np.tanh(2.2*np.sin(2*np.pi*np.cumsum(fr)/SR))*np.exp(-t*1.8);add(boom,SM,.95)
t=tt(.25);crack=hp(rng.standard_normal(len(t)),2500)*np.exp(-t*30);add(crack,SM,.9)
sh=np.zeros(int(1.9*SR))
for k in range(260):
    tk=(rng.random()**2)*1.8;f=2500+rng.random()*7000;dd=.05+rng.random()*.12;t=tt(dd)
    p=np.sin(2*np.pi*f*t)*np.exp(-t*(40+rng.random()*40))*(.3+.7*np.exp(-tk*1.8))*rng.uniform(.3,1)
    i=int(tk*SR);sh[i:i+len(p)]+=p[:len(sh)-i]
sh+=hp(rng.standard_normal(len(sh)),4000)*np.exp(-np.arange(len(sh))/SR*5)*.4
add(sh/np.max(np.abs(sh))*.55,SM+.01,1,-.25);add(np.roll(sh,331)/np.max(np.abs(sh))*.45,SM+.02,1,.3)
# reverb
ir=rng.standard_normal(int(SR*1.5))*np.exp(-np.arange(int(SR*1.5))/SR*3.5);ir=lp(ir,7000);ir/=np.sum(np.abs(ir))/12
Lw=L+fftconvolve(L,ir)[:len(L)]*.22;Rw=R+fftconvolve(R,np.roll(ir,211))[:len(R)]*.22
sr,main=wavfile.read('audio_zefyr_phonk.wav');main=main/32768.
tot=N+len(main);oL=np.zeros(tot);oR=np.zeros(tot)
oL[:len(Lw)]+=Lw[:tot]*.8;oR[:len(Rw)]+=Rw[:tot]*.8
# fade hook tail under main start
oL[N:N+len(main)]+=main[:,0];oR[N:N+len(main)]+=main[:,1]
o=np.stack([oL,oR],1);o=np.tanh(o*1.1)/np.tanh(1.1);o/=np.max(np.abs(o))*1.12
wavfile.write('audio_zefyr_hook.wav',SR,(o*32767).astype(np.int16));print('ok',tot/SR)

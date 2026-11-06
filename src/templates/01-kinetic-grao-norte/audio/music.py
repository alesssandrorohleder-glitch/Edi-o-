import numpy as np, wave
SR=44100; D=32.0; n=int(SR*D); L=np.zeros(n); R=np.zeros(n)
beat=0.5; s16=beat/4; rng=np.random.default_rng(1)
def add(sig,at,g=1.0,pan=0.0):
    i=int(round(at*SR)); j=min(n,i+len(sig))
    if j<=i: return
    L[i:j]+=sig[:j-i]*g*(1-pan); R[i:j]+=sig[:j-i]*g*(1+pan)
def env(Lx,a,d): tt=np.arange(Lx)/SR; return np.minimum(1,tt/a)*np.exp(-tt*d)
def lp(x,k): return np.convolve(x,np.ones(k)/k,'same')
def kick():
    Lx=int(.4*SR); tt=np.arange(Lx)/SR; f=48+140*np.exp(-tt*35)
    return np.tanh(1.6*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*8))
def snare():
    Lx=int(.3*SR); tt=np.arange(Lx)/SR; nz=rng.standard_normal(Lx); nz=nz-lp(nz,6)
    return (nz*np.exp(-tt*16)*.5+np.sin(2*np.pi*190*tt)*np.exp(-tt*25)*.5)
def hat(open_=False):
    Lx=int((.18 if open_ else .05)*SR); nz=rng.standard_normal(Lx); nz=nz-lp(nz,3)
    return nz*np.exp(-np.arange(Lx)/SR*(14 if open_ else 80))*.22
def saw(f,Lx): tt=np.arange(Lx)/SR; return 2*((tt*f)%1)-1
def bassnote(f,dur):
    Lx=int(dur*SR); s=lp(saw(f,Lx)*.6+np.sin(2*np.pi*f*np.arange(Lx)/SR),25)
    tt=np.arange(Lx)/SR; e=np.minimum(1,tt/.005)*np.minimum(1,(dur-tt)/.01)
    return np.tanh(s*1.5)*e*.4
def pluck(f,dur=.35):
    Lx=int(dur*SR); tt=np.arange(Lx)/SR; s=lp(saw(f,Lx)+saw(f*1.005,Lx),8)*np.exp(-tt*9)
    return s*.12
def pad(fs,dur):
    Lx=int(dur*SR); tt=np.arange(Lx)/SR
    s=sum(lp(saw(f,Lx)+saw(f*1.004,Lx)+saw(f*.996,Lx),60) for f in fs)/len(fs)
    return s*np.minimum(1,tt/.3)*np.minimum(1,(dur-tt)/.3)*.07
def impact():
    Lx=int(1.6*SR); tt=np.arange(Lx)/SR; nz=rng.standard_normal(Lx)
    return np.tanh(np.sin(2*np.pi*(38+80*np.exp(-tt*12))*tt)*np.exp(-tt*2.5)*1.5)*.9+lp(nz,4)*np.exp(-tt*6)*.25
def riser(dur):
    Lx=int(dur*SR); tt=np.arange(Lx)/SR; nz=rng.standard_normal(Lx); u=tt/dur
    return (nz-lp(nz,int(2+30*(1-u[0]))))*u**2.5*.4
def sweep_down(dur=.5):
    Lx=int(dur*SR); nz=rng.standard_normal(Lx); return lp(nz,6)*np.exp(-np.arange(Lx)/SR*7)*.35
# Am - F - C - G, one chord per 2 beats (1s) so every scene cut lands on a chord change
prog=[(55.0,[220,261.6,329.6]),(43.65,[174.6,220,261.6]),(65.4,[261.6,329.6,392]),(49.0,[196,246.9,293.7])]
arp=[0,1,2,1]
nbeats=int(D/beat)
side=np.ones(n)
for b in range(nbeats):
    tb=b*beat
    chord=prog[(b//2)%4]
    intro = tb<4; breakdown = 23<=tb<27; outro = tb>=31
    if b%2==0: add(pad(chord[1],1.0),tb,1.0 if not intro else .7)
    if outro: continue
    if not breakdown:
        if not intro or b%2==0:
            add(kick(),tb,.95 if not intro else .55)
            i=int(tb*SR); k=np.arange(int(.25*SR)); seg=1-.6*np.exp(-k/SR*14); side[i:i+len(seg)]=np.minimum(side[i:i+len(seg)],seg[:max(0,min(len(seg),n-i))])
        if not intro and b%2==1: add(snare(),tb,.7)
        for q in range(4):
            if intro and q%2==0: continue
            add(hat(open_=(q==2 and b%2==1)),tb+q*s16,(.9 if q==2 else .5),pan=.3 if q%2 else -.3)
        if not intro:
            f=chord[0]
            for q in (0,2,3): add(bassnote(f*(2 if q==3 else 1),s16*(1.8 if q==0 else .9)),tb+q*s16,.9)
    # arp plucks (also in breakdown, softer)
    for q in range(2):
        nt=chord[1][arp[(b*2+q)%4]]*2
        add(pluck(nt),tb+q*beat/2,(.5 if breakdown else 1.0),pan=(-.4 if q==0 else .4))
# apply sidechain to everything but transients added later
L*=side; R*=side
for at in [4,9,14,19,27]:
    add(impact(),at,.65); add(riser(1.0),at-1.0,.55)
add(sweep_down(),23,.6)
add(riser(2.5),23.0,.7); add(impact(),25.5,.9)  # "A SUA EXISTE"
add(riser(1.5),25.5,.5)
t=np.arange(n)/SR; fo=np.clip((D-t)/1.2,0,1); L*=fo; R*=fo
m=max(np.abs(L).max(),np.abs(R).max()); L=np.tanh(L/m*1.3)/np.tanh(1.3)*.92; R=np.tanh(R/m*1.3)/np.tanh(1.3)*.92
st=np.empty(2*n); st[0::2]=L; st[1::2]=R
w=wave.open('music2.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype(np.int16).tobytes()); w.close()
print('ok')

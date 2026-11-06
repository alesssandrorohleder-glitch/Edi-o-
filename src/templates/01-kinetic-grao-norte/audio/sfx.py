import numpy as np, wave
SR=44100
w=wave.open('music2.wav'); n=w.getnframes(); a=np.frombuffer(w.readframes(n),np.int16).astype(float)/32767; w.close()
M=a.reshape(-1,2).copy()*0.62
S=np.zeros_like(M); rng=np.random.default_rng(7)
def lp(x,k): return np.convolve(x,np.ones(k)/k,'same') if k>1 else x
def add(sig,at,g=1.0,pan=0.0):
    i=int(round(at*SR)); j=min(n,i+len(sig))
    if j<=i:return
    S[i:j,0]+=sig[:j-i]*g*(1-pan*.8); S[i:j,1]+=sig[:j-i]*g*(1+pan*.8)
def tt(d): return np.arange(int(d*SR))/SR
def whoosh(d=.45,up=True):
    t=tt(d); u=t/d; nz=rng.standard_normal(len(t)); out=np.zeros_like(nz)
    # time-varying band: mix of two lowpass widths
    a1=nz-lp(nz,3); a2=lp(nz,10)
    mix=(u if up else 1-u)
    e=np.sin(np.pi*u)**1.5
    return (a1*mix+a2*(1-mix))*e*.55
def swish(d=.18): t=tt(d); nz=rng.standard_normal(len(t)); return (nz-lp(nz,2))*np.sin(np.pi*t/d)**2*.35
def pop(f=600,d=.12):
    t=tt(d); fr=f*(1+1.2*np.exp(-t*60)); return np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-t*35)*.6
def tick(f=2400,d=.03): t=tt(d); return np.sin(2*np.pi*f*t)*np.exp(-t*220)*.5+rng.standard_normal(len(t))*np.exp(-t*400)*.2
def blip(f,d=.12): t=tt(d); return (np.sin(2*np.pi*f*t)+.3*np.sin(4*np.pi*f*t))*np.exp(-t*28)*np.minimum(1,t/.003)*.35
def thud(d=.5):
    t=tt(d); s=np.sin(2*np.pi*np.cumsum(55+120*np.exp(-t*30))/SR)*np.exp(-t*9); nz=lp(rng.standard_normal(len(t)),5)*np.exp(-t*30)*.4
    return np.tanh((s+nz)*1.8)*.8
def ding(f=1320,d=1.0):
    t=tt(d); s=sum(g*np.sin(2*np.pi*f*r*t)*np.exp(-t*k) for r,g,k in [(1,1,4),(2.76,.4,7),(5.4,.2,11),(1.5,.25,5)])
    return s*np.minimum(1,t/.002)*.28
def cash():
    a=ding(1760,.8)*.8; b=ding(2350,.6)*.6; a[int(.06*SR):int(.06*SR)+len(b)]+=b[:len(a)-int(.06*SR)]; return a
def scribble(d=.8):
    t=tt(d); nz=rng.standard_normal(len(t)); band=nz-lp(nz,4); mod=.5+.5*np.sin(2*np.pi*14*t)
    return lp(band,2)*mod*np.sin(np.pi*t/d)*.18
def ring_sweep(d=.9):
    t=tt(d); f=300+900*(t/d)**1.2; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*t/d)*.12+whoosh(d)*.4
def rise_tone(d=1.0,f0=400,f1=1400):
    t=tt(d); f=f0+(f1-f0)*t/d; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*t/d)**.5*.1
def glitter(d=.6):
    out=np.zeros(int(d*SR))
    for k in range(9):
        b=blip(1800+rng.integers(0,1600),.08)*.5; i=int(k/9*d*SR*.8); out[i:i+len(b)]+=b[:len(out)-i]
    return out
# counter ticks follow same easing as visuals
def ease_out(x): return 1-(1-x)**3
def counter_ticks(t0,t1,target,base_f):
    last=0
    for f in range(int((t1-t0)*300)+1):
        tt_=t0+f/300; k=min(1,max(0,(tt_-t0)/(t1-t0))); v=round(ease_out(k)*target)
        if v!=last: add(tick(base_f+v*25),tt_,.45,pan=(.2 if v%2 else -.2)); last=v
# ---- S1 hook
add(swish(),0.12,.6,-.3); add(swish(),0.38,.5,.3)
add(swish(),1.18,.6,-.3); add(whoosh(.3,True),1.25,.6); add(thud(),1.5,1.0)
add(swish(),1.98,.6,.3); add(whoosh(.35),2.25,.5,.4)
add(whoosh(.5,False),3.5,.7)
# wipes
for at in [4,9,14,19]: add(whoosh(.36),at-.18,.8,pan=-.5)
# ---- S2 logo
add(ring_sweep(),4.0,1.0); add(pop(420,.15),4.42,1.0); add(scribble(.9),4.6,1.0)
for i in range(10): add(tick(1600+i*90,.04),5.05+i*.05,.55,pan=-.6+i*.13)
add(glitter(),5.8,.9); add(whoosh(.5,False),8.55,.5)
# ---- S3 reel
for i,at in enumerate([9,9.5,10,10.5]): add(thud(.35),at,.75); add(swish(.12),at,.4,pan=(-.5 if i%2 else .5))
add(whoosh(.5),10.95,.8); add(pop(300,.2),11.05,1.0); add(pop(700,.1),11.25,.6)
add(whoosh(1.2,False)*.35,11.4,.6)
add(swish(),11.5,.55,-.3); add(swish(),11.75,.55,.3)
add(pop(900,.12),12.55,.9,.6); add(ding(2000,.5),12.62,.35,.6)
add(whoosh(.5,False),13.55,.6)
# ---- S4 promo
add(whoosh(.6),13.9,.7,-.6); add(whoosh(.6),14.05,.6,.6)
counter_ticks(14.5,15.6,30,1400); add(thud(.4),15.6,.8); add(cash(),15.62,.8)
add(swish(),14.8,.5)
add(pop(520,.15),16.05,1.0); add(tick(3200,.04),17.0,.9); add(pop(1100,.06),17.0,.5)
add(whoosh(.5,False),18.55,.6)
# ---- S5 chart
add(swish(),19.1,.5)
notes=[523,587,659,784,880,1047]
for i,f in enumerate(notes): add(blip(f,.16),19.45+i*.12,.9,pan=-.6+i*.24)
add(rise_tone(1.0,500,1500),20.4,1.0)
counter_ticks(20.6,21.8,48,1600); add(ding(1568,1.0),21.8,.8)
# ---- S6 turn
add(whoosh(1.1,False),23.0,.9); for_=None
add(tick(900,.05),24.05,.4)
add(thud(.45),24.5,.85,-.2); add(thud(.45),25.0,.85,.2)
add(glitter(.5),25.55,.6)
# ---- S7 CTA
add(whoosh(.55),26.9,.9); add(swish(),27.3,.5,-.3); add(swish(),27.45,.5,.3)
for i in range(5): add(blip(880+i*110,.1),27.9+i*.12,.6,pan=-.4+i*.2)
add(pop(480,.18),28.95,1.0); add(ding(1760,.9),29.0,.35)
add(swish(),29.5,.5); add(tick(2600,.04),29.55,.5)
for k in range(3): add(blip(660,.08),29.4+k*1.05,.25)   # button pulse
mix=M+S*0.85
fo=np.clip((32-np.arange(n)/SR)/1.0,0,1)[:,None]; mix*=fo
mix=np.tanh(mix*1.2)/np.tanh(1.2); mix/=np.abs(mix).max()/0.95
w=wave.open('music_sfx.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix.reshape(-1)*32767).astype(np.int16).tobytes()); w.close(); print('ok')

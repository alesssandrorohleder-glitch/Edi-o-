import numpy as np, wave
SR=44100; D=34.0; n=int(SR*D); rng=np.random.default_rng(11)
M=np.zeros((n,2)); S=np.zeros((n,2))
def lp(x,k): return np.convolve(x,np.ones(k)/k,'same') if k>1 else x
def tt(d): return np.arange(int(d*SR))/SR
def addto(B,sig,at,g=1.0,pan=0.0):
    i=int(round(at*SR)); j=min(n,i+len(sig))
    if j<=i or i<0:return
    B[i:j,0]+=sig[:j-i]*g*(1-pan*.8); B[i:j,1]+=sig[:j-i]*g*(1+pan*.8)
def saw(f,L): t=np.arange(L)/SR; return 2*((t*f)%1)-1
# ---------- music ----------
def kick(): t=tt(.4); f=46+150*np.exp(-t*35); return np.tanh(1.8*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*8))
def snare(): t=tt(.3); nz=rng.standard_normal(len(t)); nz-=lp(nz,5); return nz*np.exp(-t*14)*.5+np.sin(2*np.pi*200*t)*np.exp(-t*25)*.4
def hat(o=False): t=tt(.16 if o else .04); nz=rng.standard_normal(len(t)); nz-=lp(nz,2); return nz*np.exp(-t*(15 if o else 90))*.2
def bassn(f,d): L=int(d*SR); s=lp(saw(f,L)+saw(f*1.01,L),18); t=np.arange(L)/SR; return np.tanh(s*1.4)*np.minimum(1,t/.004)*np.minimum(1,(d-t)/.01)*.32
def arpn(f,d=.12): L=int(d*SR); t=np.arange(L)/SR; s=lp(np.sign(np.sin(2*np.pi*f*t))*.6+saw(f*1.003,L)*.4,5); return s*np.exp(-t*14)*.09
def padc(fs,d): L=int(d*SR); t=np.arange(L)/SR; s=sum(lp(saw(f,L)+saw(f*1.006,L)+saw(f*.994,L),70) for f in fs)/len(fs); return s*np.minimum(1,t/.4)*np.minimum(1,(d-t)/.3)*.08
prog=[(55.0,[220,261.6,329.6]),(43.65,[174.6,220,261.6]),(65.4,[196,261.6,329.6]),(49.0,[196,246.9,293.7])]
beat=.5; side=np.ones(n)
for b in range(int(D/beat)):
    tb=b*beat; bar=b//4; root,ch=prog[bar%4]
    intro=tb<2; brk=24<=tb<28; end=tb>=33
    if b%4==0 and not end: addto(M,padc(ch,2.0),tb,1.3 if brk or intro else 1)
    if end: continue
    if not intro and not brk:
        addto(M,kick(),tb,.9); i=int(tb*SR); seg=1-.55*np.exp(-np.arange(int(.25*SR))/SR*14); side[i:i+len(seg)]=np.minimum(side[i:i+len(seg)],seg[:n-i] if i+len(seg)>n else seg)
        if b%2: addto(M,snare(),tb,.6)
        for q in range(4): addto(M,hat(q==2 and b%2==1),tb+q*beat/4,.5 if q!=2 else .8,pan=.3 if q%2 else -.3)
        for q in range(2): addto(M,bassn(root*(1 if q==0 else 2) ,beat/2*.9),tb+q*beat/2,.9)
    # 16th arps always (soft in intro/break)
    for q in range(4):
        f=ch[(b*4+q)%3]*(2 if (b*4+q)%6<3 else 4)
        addto(M,arpn(f),tb+q*beat/4,(.45 if (intro or brk) else .8),pan=(-.5 if q%2 else .5))
M*=side[:,None]
# ---------- sfx ----------
def whoosh(d=.45,up=True):
    t=tt(d); u=t/d; nz=rng.standard_normal(len(t)); m=u if up else 1-u
    return ((nz-lp(nz,3))*m+lp(nz,10)*(1-m))*np.sin(np.pi*u)**1.5*.55
def swish(d=.18): t=tt(d); nz=rng.standard_normal(len(t)); return (nz-lp(nz,2))*np.sin(np.pi*t/d)**2*.33
def pop(f=600,d=.12): t=tt(d); fr=f*(1+1.2*np.exp(-t*60)); return np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-t*35)*.6
def tick(f=2400,d=.03): t=tt(d); return np.sin(2*np.pi*f*t)*np.exp(-t*220)*.5+rng.standard_normal(len(t))*np.exp(-t*400)*.15
def key(): t=tt(.035); nz=rng.standard_normal(len(t)); return (nz-lp(nz,2))*np.exp(-t*160)*.35+np.sin(2*np.pi*(1800+rng.integers(0,600))*t)*np.exp(-t*250)*.2
def blip(f,d=.1): t=tt(d); return (np.sign(np.sin(2*np.pi*f*t))*.4+np.sin(2*np.pi*f*t)*.6)*np.exp(-t*30)*np.minimum(1,t/.002)*.25
def thud(d=.5): t=tt(d); s=np.sin(2*np.pi*np.cumsum(52+130*np.exp(-t*30))/SR)*np.exp(-t*9); return np.tanh((s+lp(rng.standard_normal(len(t)),5)*np.exp(-t*30)*.4)*1.8)*.8
def glitch(d=.25):
    t=tt(d); out=np.zeros(len(t)); k=0
    while k<len(t):
        L=int(rng.integers(300,2500)); f=rng.choice([180,360,900,1800,3200]); seg=np.arange(min(L,len(t)-k))/SR
        kind=rng.integers(0,3); s=np.sign(np.sin(2*np.pi*f*seg)) if kind==0 else (rng.standard_normal(len(seg)) if kind==1 else np.sin(2*np.pi*f*seg))
        out[k:k+len(seg)]=s*(.25+.5*rng.random()); k+=L
    out=np.round(out*6)/6  # bitcrush
    return out*np.minimum(1,(d-t)/.03)*.35
def ding(f=1320,d=1.0): t=tt(d); return sum(g*np.sin(2*np.pi*f*r*t)*np.exp(-t*k) for r,g,k in [(1,1,4),(2.76,.4,7),(5.4,.2,11),(1.5,.25,5)])*np.minimum(1,t/.002)*.26
def notif(): a=ding(1568,.6); b=ding(2093,.7); o=np.zeros(int(.9*SR)); o[:len(a)]+=a; o[int(.12*SR):int(.12*SR)+len(b)]+=b[:len(o)-int(.12*SR)]; return o
def chirps(d,rate=24):
    o=np.zeros(int(d*SR))
    for k in range(int(d*rate)):
        b=blip(900+rng.integers(0,2400),.04); i=int(k/rate*SR); o[i:i+len(b)]+=b[:len(o)-i]*.6
    return o
def tone(d,f0,f1,g=.12): t=tt(d); f=f0+(f1-f0)*(t/d)**1.3; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*t/d)**.6*g+np.sign(np.sin(2*np.pi*np.cumsum(f*2)/SR))*np.sin(np.pi*t/d)*g*.15
def drone(d): t=tt(d); s=lp(saw(55,len(t))+saw(55.4,len(t))+saw(110.3,len(t))*.5,120); return s*np.sin(np.pi*t/d)*.25
def impact(): t=tt(1.5); return np.tanh(np.sin(2*np.pi*(36+90*np.exp(-t*12))*t)*np.exp(-t*2.6)*1.6)*.9+lp(rng.standard_normal(len(t)),4)*np.exp(-t*6)*.25
def explode(): t=tt(1.4); nz=rng.standard_normal(len(t)); return lp(nz,3)*np.exp(-t*3)*.5+impact()[:len(t)]
def glitter(d=.6):
    o=np.zeros(int(d*SR))
    for k in range(10): b=blip(2000+rng.integers(0,2000),.07)*.6; i=int(k/10*d*SR*.8); o[i:i+len(b)]+=b[:len(o)-i]
    return o
def clickheavy(): t=tt(.12); return (np.sin(2*np.pi*np.cumsum(900*np.exp(-t*40)+200)/SR)*np.exp(-t*50)+rng.standard_normal(len(t))*np.exp(-t*200)*.4)*.7
def ease_out(x): return 1-(1-x)**3
def eio(x): return 4*x**3 if x<.5 else 1-(-2*x+2)**3/2
def counter(t0,t1,target,f0,ease=ease_out,maxrate=28):
    last=-1;lt=-9
    for f in range(int((t1-t0)*600)+1):
        tq=t0+f/600; v=round(ease(min(1,(tq-t0)/(t1-t0)))*target)
        if v!=last and tq-lt>1/maxrate: addto(S,tick(f0+ (v/target)*1500),tq,.4,pan=(.2 if v%2 else -.2)); last=v; lt=tq
def typing(t0,cps,nchars,pan=-.2):
    for i in range(1,nchars+1): addto(S,key(),t0+i/cps,.7,pan=pan+rng.uniform(-.15,.15))
A=lambda *a,**k: addto(S,*a,**k)
# S1
typing(.1,30,22); typing(.85,30,22); A(tone(.8,300,1400,.10),1.1,1); counter(1.1,1.9,100,1200,ease=eio)
A(glitch(.22),1.95,1); A(thud(),2.0,1); A(impact(),2.0,.5); A(glitch(.18),2.5,.8,pan=.3); A(thud(.4),2.5,.8); A(whoosh(.5),2.8,.6,pan=.4); A(glitch(.2),3.65,.7)
for c in [4,8,12,16,20,24,28]: A(glitch(.3),c-.15,.85); A(whoosh(.4),c-.2,.6,pan=-.4)
# S2
A(drone(2.6),4.0,1); A(tone(.9,1200,200,.12),5.4,1); A(impact(),6.3,.8); A(glitter(.7),6.3,.8); A(chirps(.6),6.3,.9); typing(7.0,30,18,pan=.2)
# S3
A(whoosh(.7),7.95,.9); A(swish(),8.2,.5,pan=-.3); A(swish(),8.4,.5,pan=.3); counter(8.7,9.7,60,1400)
A(tone(1.0,500,1500),9.0,1); [A(pop(500+i*150,.12),9.62+i*.1,.9,pan=-.4+i*.4) for i in range(3)]
A(whoosh(.5,False),10.35,.6); A(notif(),10.6,.9); A(clickheavy(),10.9,.8); A(pop(1200,.06),10.9,.4)
# S4
A(whoosh(1.0),12.0,.9); A(chirps(.7),13.0,.7); A(glitter(.7),13.2,.7); A(swish(),13.5,.5,pan=-.3); A(swish(),13.75,.5,pan=.3)
A(whoosh(.35),14.6,.7,pan=-.5); A(whoosh(.35),14.85,.7,pan=.5); A(impact(),15.1,.5); A(glitter(.5),15.1,.6)
# S5
A(drone(1.6),16.0,.8); A(tone(.7,200,800,.08),16.3,1); A(clickheavy(),17.0,1.0); A(thud(.3),17.02,.6)
A(tone(1.2,400,1300,.10),17.2,1); counter(17.2,18.4,100,1500,ease=eio); A(notif(),18.4,.8)
A(swish(),18.3,.5,pan=-.3); A(swish(),18.5,.5,pan=.3); typing(18.8,40,40,pan=0)
# S6
for i,a in enumerate([20,20.5,21,21.5]): A(thud(.4),a,.9); A(glitch(.15),a,.7,pan=(-.4 if i%2 else .4))
A(explode(),22.0,1.0); A(glitter(.8),22.1,.7); A(swish(),22.6,.5)
# S7
typing(24.3,30,24); typing(25.3,30,15,pan=.2); A(glitch(.2),26.0,.8); A(thud(),26.0,.9); A(glitch(.2),26.5,.8,pan=.3); A(thud(),26.5,.9); A(impact(),26.5,.5)
# S8
A(impact(),28.0,.8); A(whoosh(.5),27.9,.8); A(swish(),28.3,.5,pan=-.3); A(swish(),28.45,.5,pan=.3)
for k in range(6): A(blip(880+k*130,.09),28.9+k*.1,.7,pan=-.5+k*.2)
A(pop(480,.18),29.9,1); A(ding(1760,.9),29.95,.35); A(swish(),30.5,.5); A(tick(2600,.04),30.55,.5)
for k in range(3): A(blip(660,.07),30.45+k*1.05,.25)
mix=M*.62+S*.85
t=np.arange(n)/SR; mix*=np.clip((D-t)/1.2,0,1)[:,None]
mix=np.tanh(mix*1.2)/np.tanh(1.2); mix/=np.abs(mix).max()/.95
w=wave.open('audio_tech.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix.reshape(-1)*32767).astype(np.int16).tobytes()); w.close(); print('ok')

# Lip-sync v2: abertura com dinâmica real (sem saturar) + "largura" da vogal (centroide espectral) para o formato da boca.
import json,numpy as np
from scipy.io import wavfile
from scipy.signal import butter,sosfiltfilt
sr,a=wavfile.read('audio/voz2.wav');a=a.astype(np.float32);a=a.mean(1) if a.ndim>1 else a;a/=np.abs(a).max()+1e-9
L=json.load(open('lipsync.json'));W=L['words'];n=len(L['open']);fps=30
v=sosfiltfilt(butter(4,[250,3000],'band',fs=sr,output='sos'),a)
win=int(.045*sr);op=np.zeros(n);wd=np.zeros(n)
fr=np.fft.rfftfreq(win,1/sr);hn=np.hanning(win)
for i in range(n):
    c=int(i/fps*sr);s=v[max(0,c-win//2):c+win//2]
    if len(s)<win: s=np.pad(s,(0,win-len(s)))
    op[i]=np.sqrt(np.mean(s**2))
    S=np.abs(np.fft.rfft(a[max(0,c-win//2):max(0,c-win//2)+win]*hn if len(a[max(0,c-win//2):max(0,c-win//2)+win])==win else np.zeros(win)))
    m=(fr>200)&(fr<4000);wd[i]=(S[m]*fr[m]).sum()/(S[m].sum()+1e-9)
gate=np.zeros(n)
for s0,e0,_ in W: gate[int(s0*fps):int(e0*fps)+2]=1
p95=np.percentile(op[gate>0],95);op=np.clip(op/p95,0,1)**.85*gate
# sibilantes (centroide muito alto) fecham um pouco
z=(wd-np.percentile(wd[gate>0],10))/(np.percentile(wd[gate>0],90)-np.percentile(wd[gate>0],10)+1e-9);z=np.clip(z,0,1)
op*=1-.45*np.clip((z-.8)/.2,0,1)
# suavização tipo mola (sem cantos)
o2=np.zeros(n);vel=0;y=0
for i in range(n):
    k=.38 if op[i]>y else .24;vel=vel*.45+(op[i]-y)*k;y=max(0,y+vel);o2[i]=y
w2=np.convolve(z,np.ones(5)/5,'same')
L['open']=[round(float(q),3) for q in np.clip(o2,0,1)];L['wide']=[round(float(q),3) for q in w2]
json.dump(L,open('lipsync.json','w'));print('max',o2.max(),'mean',o2[gate>0].mean())

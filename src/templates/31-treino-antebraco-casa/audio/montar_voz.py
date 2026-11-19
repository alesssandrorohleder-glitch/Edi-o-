# Monta a narração: corta silêncio das pontas de cada fala e posiciona na linha do tempo (gera voz.wav + falas.json com início/fim).
import json,glob,numpy as np
from scipy.io import wavfile
SR=22050;DUR=44.0;fs=sorted(glob.glob('falas/*.wav'));C=[]
for f in fs:
    sr,a=wavfile.read(f);a=a.astype(np.float32)/32768;e=np.convolve(np.abs(a),np.ones(220)/220,'same');idx=np.where(e>.012)[0]
    C.append(a[max(0,idx[0]-200):idx[-1]+900])
# pausa ANTES de cada fala (s)
GAP=[.35,.4,.4,1.0,.95,.95,.95,.95,.95,.7,.75,.35]
T=[];t=0;out=np.zeros(int(60*SR),np.float32)
for g,c in zip(GAP,C):
    t+=g;i=int(t*SR);out[i:i+len(c)]+=c;T.append([round(t,3),round(t+len(c)/SR,3)]);t+=len(c)/SR
print('fim da fala',round(t,2))
out=out[:int(DUR*SR)];wavfile.write('voz.wav',SR,(np.clip(out,-1,1)*32767).astype(np.int16))
L=[l.strip() for l in open('roteiro.txt',encoding='utf-8') if l.strip()]
json.dump([{'t0':a,'t1':b,'txt':s} for (a,b),s in zip(T,L)],open('../falas.json','w'),ensure_ascii=False,indent=0)
for (a,b),s in zip(T,L):print(f'{a:6.2f} {b:6.2f}  {s}')

# Uniformiza cor/exposição dos clipes estabilizados (_frames_src/*.mp4) e extrai os quadros JPG que o index.html usa.
# Rode nesta pasta:  python preparar_frames.py   (precisa de ffmpeg, numpy, Pillow)
import subprocess, os, glob, json, io
import numpy as np
from PIL import Image
CLIPS = sorted(glob.glob('_frames_src/*.mp4'))
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
def stats(f):
    d=dur(f); ms=[]
    for k in range(5):
        raw=subprocess.check_output(['ffmpeg','-loglevel','error','-ss',str(d*(k+.5)/5),'-i',f,'-frames:v','1','-vf','scale=160:-2','-f','image2pipe','-vcodec','png','-'])
        a=np.asarray(Image.open(io.BytesIO(raw)).convert('RGB'),dtype=np.float32)/255
        l=a.mean(2); m=(l>.08)&(l<.92)              # só meios-tons
        ms.append([a[...,c][m].mean() for c in range(3)]+[np.median(l)])
    return np.mean(ms,0)
S={os.path.basename(f)[:-4]:stats(f) for f in CLIPS}
ref=np.median(np.array(list(S.values())),0)        # alvo = média do conjunto
TARGET_L=max(.34,min(.42,ref[3]))
look="curves=r='0/0.03 0.5/0.51 1/0.97':g='0/0.035 0.5/0.5 1/0.96':b='0/0.05 0.5/0.48 1/0.93',eq=saturation=1.04"
meta={}
for f in CLIPS:
    n=os.path.basename(f)[:-4]; r,g,b,l=S[n]; k=.65    # força da correção
    gr,gg,gb=[(1-k)+k*(ref[i]/max(v,1e-3)) for i,v in enumerate((r,g,b))]
    gam=float(np.clip(np.log(TARGET_L)/np.log(max(l,1e-3)),.75,1.35))   # exposição -> gamma
    vf=f"colorchannelmixer=rr={gr:.3f}:gg={gg:.3f}:bb={gb:.3f},lutrgb=r='255*pow(val/255,{gam:.3f})':g='255*pow(val/255,{gam:.3f})':b='255*pow(val/255,{gam:.3f})',{look}"
    od=f'frames/{n}'; os.makedirs(od,exist_ok=True)
    if not os.listdir(od):
        subprocess.run(['ffmpeg','-loglevel','error','-y','-i',f,'-vf',vf,'-q:v','3',f'{od}/%04d.jpg'],check=True)
    meta[n]={'n':len(os.listdir(od)),'gain':[round(float(v),3) for v in (gr,gg,gb)],'gamma':round(gam,3)}
    print(n,meta[n])
json.dump(meta,open('frames/meta.json','w'))
open('frames/meta.js','w').write('window.META='+json.dumps(meta)+';')

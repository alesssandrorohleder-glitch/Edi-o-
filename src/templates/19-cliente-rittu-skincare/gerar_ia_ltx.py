# Gera takes de IA (LTX-Video no Hugging Face) a partir das imagens base. Uso: HF_TOKEN=... python gerar_ia_ltx.py <pasta_com_imagens> [takes]
# Token sempre por variável de ambiente (nunca no código). Cota grátis ~2 min GPU/dia (~5 clipes).
import os,shutil,time,httpx,sys,json
from gradio_client import Client
os.chdir(sys.argv[1]);tok=os.environ['HF_TOKEN']
c=Client('Lightricks/ltx-video-distilled',verbose=False,token=tok);base=c.src.rstrip('/')
ups={}
def up(fn):
    if fn not in ups:
        with open(fn,'rb') as f: ups[fn]=httpx.post(base+'/gradio_api/upload',files={'files':(fn,f,'image/jpeg')},headers={'Authorization':'Bearer '+tok},timeout=120).json()[0]
    return ups[fn]
ST=", luxury skincare commercial, deep emerald green and black palette, soft gold accents, glossy, photorealistic, cinematic studio lighting, shallow depth of field, ultra detailed"
NEG="worst quality, inconsistent motion, blurry, jittery, distorted, deformed bottle, warped label, changing text, morphing, extra bottles, cartoon"
S='rittu_v_serum_estudio.jpg';P='rittu_v_pote_estudio.jpg';D='rittu_v_podio_estudio.jpg'
TAKES=[('01_gota',None,"Extreme macro slow motion of a single glossy clear droplet falling into a pool of glossy emerald green serum, perfect concentric ripples spreading across the mirror-like liquid surface, dark green background"),
 ('02_emerge',S,"the emerald green glass dropper bottle stands still while glossy emerald liquid ripples and waves gently around its base, light reflections moving on the liquid"),
 ('03_seda',S,"the emerald green glass dropper bottle stands still, a flowing dark green satin silk ribbon spirals gracefully around the bottle in slow motion, soft gold rim light"),
 ('04_bolhas',S,"the emerald green glass dropper bottle stands still, clear glass bubbles and tiny gold pearls float slowly upward around the bottle, gentle drifting motion"),
 ('05_splash',S,"the emerald green glass dropper bottle stands still, a dynamic splash of clear green liquid swirls around the bottle, droplets suspended in mid-air, high-speed photography"),
 ('06_creme',P,"slow camera push in toward the open emerald green jar, the ivory cream swirl glistening, the black lid hovering above, soft gold light sweeping across"),
 ('07_podio',D,"delicate green leaves and tiny gold flakes falling slowly around the luxury skincare bottles on black podiums, slow camera dolly forward"),
 ('08_orbita',S,"slow cinematic camera orbit around the emerald green glass dropper bottle, light sweeping across the glass, reflections on the glossy black floor")]
only=sys.argv[2].split(',') if len(sys.argv)>2 else None
for name,img,pr in TAKES:
    if only and name not in only: continue
    for v in range(2):
        out=f'{name}_v{v+1}.mp4'
        if os.path.exists(out): continue
        t=time.time()
        try:
            r=c.predict(pr+ST,NEG,up(img) if img else None,None,1248,704,'image-to-video' if img else 'text-to-video',4,9,1000+v*77,False,1,True,api_name='/text_to_video')
            vv=r[0]['video'] if isinstance(r[0],dict) else r[0];shutil.copy(vv,out);print('OK',out,round(time.time()-t),flush=True)
        except Exception as e: print('ERR',out,repr(e)[:300],flush=True)
print('FIM',flush=True)

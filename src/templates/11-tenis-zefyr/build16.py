import glob
imgs={'side':'zefyr/side_cut.png','q34':'zefyr/q34_cut.png','sole':'zefyr/sole.jpg','street':'zefyr/street.jpg','sole2':'zefyr/sole2.jpg'}
h='<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:#000}canvas{display:block}</style></head><body><canvas id="c" width="1080" height="1920"></canvas><script>\nconst IM={};const ALL=[];function L(s){const i=new Image();i.src=s;ALL.push(i);return i;}\n'
for k,f in imgs.items():h+=f"IM['{k}']=L('{f}');"
h+="\nconst CL={};"
for k in ["fall","lev","run","drop","glass","macro"]:
    h+=f"CL['{k}']=["+",".join(f"L('{f}')" for f in sorted(glob.glob(f'clips/{k}/*.jpg')))+"];\n"
h+="const C2=["+",".join(f"L('{f}')" for f in sorted(glob.glob('turn/c2/*.jpg')))+"];\n"
h+='window.IMGS=ALL;\n'+open('v16_body.js').read()+'</script></body></html>'
open('v16.html','w').write(h);print('ok')

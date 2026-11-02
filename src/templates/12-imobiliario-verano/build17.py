import glob
imgs={'sala':'verano/sala.jpg','fachada':'verano/fachada_g.jpg','piscina':'verano/piscina.jpg','varanda':'verano/varanda.jpg'}
h='<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:#000}canvas{display:block}</style></head><body><canvas id="c" width="1080" height="1920"></canvas><script>\nconst IM={};const ALL=[];function L(s){const i=new Image();i.src=s;ALL.push(i);return i;}\n'
for k,f in imgs.items():h+=f"IM['{k}']=L('{f}');"
h+="\nconst CL={};"
for k in ['c1','c2','c5','c6','c7','c8']:
    h+=f"CL['{k}']=["+",".join(f"L('{f}')" for f in sorted(glob.glob(f'verano/{k}/*.jpg')))+"];\n"
h+='window.IMGS=ALL;\n'+open('verano/v17_body.js').read()+'</script></body></html>'
open('v17.html','w').write(h);print('ok')

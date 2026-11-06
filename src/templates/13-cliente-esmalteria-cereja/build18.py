import glob
h='<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:#000}canvas{display:block}</style></head><body><canvas id="c" width="1080" height="1920"></canvas><script>\nconst IM={};const ALL=[];function L(s){const i=new Image();i.src=s;ALL.push(i);return i;}\n'
h+="IM['letters']=L('cereja/logo_letters.png');IM['cherry']=L('cereja/logo_cherry.png');\nconst CL={};"
for k in ['coffee','mani','wide','lounge']:
    h+=f"CL['{k}']=["+",".join(f"L('{f}')" for f in sorted(glob.glob(f'cereja/f_{k}/*.jpg')))+"];\n"
h+='window.IMGS=ALL;\n'+open('cereja/v18_body.js').read()+'</script></body></html>'
open('v18.html','w').write(h);print('ok')

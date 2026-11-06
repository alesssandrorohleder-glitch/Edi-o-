import json
pj=json.load(open('metro/parts.json'))
h='<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:#000}canvas{display:block}</style></head><body><canvas id="c" width="1080" height="1920"></canvas><script>\nconst IM={};const ALL=[];function L(s){const i=new Image();i.src=s;ALL.push(i);return i;}\n'
for k in ['word2x','constr2x']:h+=f"IM['{k}']=L('metro/{k}.png');"
for k in ['churras','piscina','predio','predio2','pl_studio','pl_2d','b_santana','b_analia','b_ipiranga','b_guilhermina','b_boavista','b_sapopemba','b_gronchi']:h+=f"IM['{k}']=L('metro/{k}.jpg');"
h+=f"\nconst PARTS={json.dumps(pj['parts'])};const POLYS={json.dumps(json.load(open('metro/icon_polys.json')))};window.IMGS=ALL;\n"+open('metro/v19_body.js').read()+'</script></body></html>'
open('v19.html','w').write(h);print('ok')

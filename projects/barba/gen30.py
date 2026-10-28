import re
src=open('index.html').read()
css=re.search(r'<style>.*?</style>', src, re.S).group(0)
rows=[l.split() for l in open('build/v30/timeline.txt')]
T={}; cuts=[]
for id,tag,t,d in rows:
    t=float(t); d=float(d); cuts.append(t)
    if tag!='-': T[tag]=(t,d)
total=29.98
f=lambda x: f"{x:.2f}".rstrip('0').rstrip('.')
def span(a,b): return T[a][0], (T[b][0]+T[b][1] if b else T[a][0]+T[a][1])
S={}
S['hook']=(0, T['hook'][1]); S['first']=span('first',None); S['smile']=span('smile',None)
S['sides']=(T['sides'][0], T['sides'][0]+2.5); S['focus']=span('focus',None)
S['neck']=(T['neck'][0], T['neck'][0]+2.4); S['reveal']=span('reveal',None); S['split']=span('split',None)
S['who']=span('who',None); S['end']=(T['end'][0], total)
def cap(id, key, inner, track=1):
    a,b=S[key]; return f'      <div id="{id}" class="cap clip" data-start="{f(a+0.03)}" data-duration="{f(b-a-0.05)}" data-track-index="{track}">\n        {inner}\n      </div>\n'
html=[]
html.append(cap('t-hook','hook','<div class="head hk"><span class="w1">tchau,</span> <span class="y w2">barba.</span></div>'))
html.append(cap('t-first','first','<span class="chip">1ª passada</span><br /><span class="sub">sem volta agora</span>'))
html.append(cap('t-smile','smile','<span class="chip dark">tá ficando bom?</span>'))
html.append(cap('t-sides','sides','<span class="chip">agora as laterais</span>'))
html.append(cap('t-focus','focus','<div class="head mid">foco <span class="y">total.</span></div>'))
html.append(cap('t-neck','neck','<span class="chip">agora o pescoço</span>'))
html.append(cap('t-reveal','reveal','<div class="head"><span class="y">depois.</span></div>'))
a,b=S['split']
html.append(f'      <div id="lbl-antes" class="half clip" data-start="{f(a)}" data-duration="{f(b-a-0.05)}" data-track-index="2">\n        <span class="chip dark">antes</span>\n      </div>\n')
html.append(f'      <div id="lbl-depois" class="half clip" data-start="{f(a)}" data-duration="{f(b-a-0.05)}" data-track-index="3">\n        <span class="chip">depois</span>\n      </div>\n')
html.append(cap('t-who','who','<div class="head mid">quem é <span class="y">esse?</span></div>'))
a,b=S['end']
html.append(f'      <div id="t-end" class="cap clip" data-start="{f(a+0.03)}" data-duration="{f(b-a-0.03)}" data-track-index="1">\n        <div class="head mid">e <span class="y">aí?</span></div>\n        <span class="sub box">barba ou sem barba? comenta</span>\n      </div>\n')
R=S['reveal'][0]
html.append(f'      <div id="flash" class="clip" data-start="{f(R-0.1)}" data-duration="0.7" data-track-index="4"></div>\n')
# sound
snd=[]; n=[0]
def A(file,start,dur,vol,track):
    n[0]+=1; snd.append(f'      <audio id="s{n[0]:02d}" class="clip" src="assets/sfx/{file}.mp3" data-start="{f(max(0.0,start))}" data-duration="{f(dur)}" data-volume="{vol}" data-track-index="{track}"></audio>')
A('impact-bass-1',0.02,2.0,0.45,10)
for key,s in [('first',S['first'][0]),('smile',S['smile'][0]),('sides',S['sides'][0]),('focus',S['focus'][0]),('neck',S['neck'][0]),('who',S['who'][0]),('end',S['end'][0])]:
    A('whoosh',s-0.2,0.57,0.5,11)
    if key=='focus': A('glitch-1',s-0.05,1.3,0.35,12)
    elif key=='first': A('impact-bass-1',s-0.03,2.0,0.5,12)
    elif key=='end': A('impact-bass-1',s,2.0,0.4,12)
    A('pop',s+0.07,0.72,0.55,13)
section_starts={round(v[0],2) for v in S.values()}
for i,c in enumerate(cuts):
    if i%2==0 and round(c,2) not in section_starts and c<R-0.5 and c>0:
        A('whoosh-short',c-0.15,0.57,0.28,14)
A('riser',R-4.1,4.15,0.4,15)
A('impact-bass-2',R,2.2,0.55,12)
A('sparkle',R+0.1,1.8,0.45,13)
A('whoosh-cinematic',S['split'][0]-2.3,3.2,0.35,16)
A('pop',S['split'][0]+0.05,0.72,0.5,13)
# timeline js
scales=[1.12 if i==0 else (1.0 if i%2 else 1.09) for i in range(len(cuts))]
for i,(id,tag,t,d) in enumerate(rows):
    if tag in ('reveal','split','who','end'): scales[i]=1.0
    if tag=='focus': scales[i]=1.15
js=f'''
      const tl = gsap.timeline({{ paused: true }});
      const cuts = [{", ".join(f(c) for c in cuts)}];
      const scales = [{", ".join(f(x) for x in scales)}];
      cuts.forEach((t, i) => {{
        const end = i + 1 < cuts.length ? cuts[i + 1] : {f(total)};
        tl.fromTo("#cam", {{ scale: scales[i] + 0.04 }}, {{ scale: scales[i], duration: Math.min(0.3, end - t), ease: "power3.out", immediateRender: i === 0 }}, t);
      }});
      tl.to("#cam", {{ scale: 1.05, duration: {f(S['reveal'][1]-R-0.45)}, ease: "none" }}, {{R}});
      tl.to("#cam", {{ scale: 1.06, duration: {f(S['who'][1]-S['who'][0]-0.4)}, ease: "none" }}, {f(S['who'][0]+0.3)});
      tl.to("#cam", {{ scale: 1.05, duration: {f(total-S['end'][0]-0.4)}, ease: "none" }}, {f(S['end'][0]+0.3)});

      const slam = (sel, t) => tl.fromTo(sel, {{ opacity: 0, scale: 1.6, y: -20 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "back.out(2.4)" }}, t);
      const pop = (sel, t) => tl.fromTo(sel, {{ opacity: 0, scale: 0.6, rotate: -4 }}, {{ opacity: 1, scale: 1, rotate: 0, duration: 0.32, ease: "back.out(2.6)" }}, t);
      const out = (sel, t) => tl.to(sel, {{ opacity: 0, scale: 0.92, duration: 0.16, ease: "power2.in" }}, t);
'''.replace('{R}', f(R+0.35))
def o(k): return f(S[k][1]-0.2)
js+=f'''
      slam("#t-hook .w1", 0.04); slam("#t-hook .w2", 0.22); out("#t-hook", {o('hook')});
      pop("#t-first .chip", {f(S['first'][0]+0.07)});
      tl.fromTo("#t-first .sub", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "power3.out" }}, {f(S['first'][0]+0.3)});
      out("#t-first", {o('first')});
      pop("#t-smile .chip", {f(S['smile'][0]+0.07)}); out("#t-smile", {o('smile')});
      pop("#t-sides .chip", {f(S['sides'][0]+0.07)}); out("#t-sides", {o('sides')});
      slam("#t-focus .head", {f(S['focus'][0]+0.05)});
      tl.to("#t-focus .head", {{ rotate: -3, duration: 0.07, yoyo: true, repeat: 5, ease: "none" }}, {f(S['focus'][0]+0.4)});
      out("#t-focus", {o('focus')});
      pop("#t-neck .chip", {f(S['neck'][0]+0.07)}); out("#t-neck", {o('neck')});
      tl.fromTo("#flash", {{ opacity: 0 }}, {{ opacity: 0.9, duration: 0.1, ease: "power2.in" }}, {f(R-0.1)});
      tl.to("#flash", {{ opacity: 0, duration: 0.45, ease: "power2.out" }}, {f(R)});
      slam("#t-reveal .head", {f(R+0.1)}); out("#t-reveal", {o('reveal')});
      pop("#lbl-antes .chip", {f(S['split'][0]+0.05)}); pop("#lbl-depois .chip", {f(S['split'][0]+0.18)});
      tl.to(["#lbl-antes", "#lbl-depois"], {{ opacity: 0, duration: 0.15 }}, {o('split')});
      slam("#t-who .head", {f(S['who'][0]+0.08)}); out("#t-who", {o('who')});
      slam("#t-end .head", {f(S['end'][0]+0.08)});
      tl.fromTo("#t-end .sub", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "power3.out" }}, {f(S['end'][0]+0.25)});
      window.__timelines["main"] = tl;
'''
page=f'''<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/gsap.min.js"></script>
    {css}
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{f(total)}" data-width="1080" data-height="1920">
      <div id="cam">
        <video id="base" class="clip" src="assets/base.mp4" data-has-audio="true" data-volume="0.5" playsinline data-start="0" data-duration="{f(total)}" data-track-index="0"></video>
      </div>
      <div id="topfade"></div>

{"".join(html)}
      <!-- SOUND DESIGN -->
{chr(10).join(snd)}
    </div>
    <script>{js}    </script>
  </body>
</html>
'''
open('index.html','w').write(page)
print(S)

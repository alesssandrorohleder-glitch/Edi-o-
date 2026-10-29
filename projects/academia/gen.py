"""Builds index.html from build/timeline.txt: one narration line per section."""
rows = [l.split() for l in open('build/timeline.txt')]
total = round(sum(float(r[3]) for r in rows), 2)
f = lambda x: f"{x:.2f}".rstrip('0').rstrip('.')
sec = {}
for id_, line, t, d in rows:
    t, d = float(t), float(d)
    a, b = sec.get(line, (t, t + d)); sec[line] = (min(a, t), t + d)
cuts = [float(r[2]) for r in rows]
LINES = [
    ('L1', 'novidade na invictus', 'Olha só o que <span class="y">acabou de chegar!</span>'),
    ('L2', 'chegou', 'Um caminhão lotado de <span class="y">equipamentos novos</span>'),
    ('L3', 'força total', 'A galera toda se juntou <span class="y">pra descarregar</span>'),
    ('L4', 'bora', 'Máquina por máquina, <span class="y">direto pra dentro</span>'),
    ('L5', 'montagem', 'Cada aparelho <span class="y">no seu lugar</span>'),
    ('L6', 'o resultado', 'Invictus renovada, com <span class="y">equipamentos de primeira</span>'),
    ('CTA', 'academia invictus', 'Vem treinar <span class="y">na Invictus!</span>'),
]
caps, js, snd = [], [], []
n = [0]
def A(file, start, dur, vol, track):
    n[0] += 1
    snd.append(f'      <audio id="s{n[0]:02d}" class="clip" src="assets/sfx/{file}.mp3" data-start="{f(max(0, start))}" data-duration="{f(dur)}" data-volume="{vol}" data-track-index="{track}"></audio>')
for key, chip, text in LINES:
    a, b = sec[key]
    end = total if key == 'CTA' else b
    caps.append(f'      <div id="c-{key}" class="cap clip" data-start="{f(a + 0.05)}" data-duration="{f(end - a - 0.07)}" data-track-index="1">\n'
                f'        <span class="chip">{chip}</span>\n        <div class="line">{text}</div>\n      </div>\n')
    js.append(f'      pop("#c-{key} .chip", {f(a + 0.1)});')
    js.append(f'      rise("#c-{key} .line", {f(a + 0.22)});')
    if key != 'CTA':
        js.append(f'      out("#c-{key}", {f(b - 0.25)});')
    if key != 'L1':
        A('whoosh', a - 0.22, 0.57, 0.5, 11)
    A('pop', a + 0.12, 0.72, 0.45, 13)
R = sec['L6'][0]
A('impact-bass-1', 0.05, 2.0, 0.5, 12)
A('riser', R - 4.1, 4.15, 0.35, 14)
A('impact-bass-2', R, 2.2, 0.5, 12)
A('sparkle', R + 0.1, 1.8, 0.45, 15)
A('impact-bass-1', sec['CTA'][0], 2.0, 0.4, 16)
for i, c in enumerate(cuts):
    if i % 2 and c < R - 0.5 and all(abs(c - s[0]) > 0.1 for s in sec.values()):
        A('whoosh-short', c - 0.15, 0.57, 0.22, 17)
scales = [1.0 if c >= R else (1.08 if i % 2 else 1.0) for i, c in enumerate(cuts)]
page = f'''<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/gsap.min.js"></script>
    <style>
      :root {{ --accent: #ffd400; --ink: #0b0b0f; --paper: #ffffff; --font-head: "League Gothic", "Oswald", sans-serif; --font-chip: "Archivo Black", sans-serif; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #root {{ width: 100%; height: 100%; position: relative; overflow: hidden; }}
      #cam {{ position: absolute; inset: 0; transform-origin: 50% 55%; }}
      #base {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      #topfade {{ position: absolute; left: 0; right: 0; top: 0; height: 640px; background: linear-gradient(to bottom, rgba(0, 0, 0, 0.62), rgba(0, 0, 0, 0)); }}
      #flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; }}
      .cap {{ position: absolute; left: 70px; right: 70px; top: 185px; text-align: center; }}
      .chip {{ display: inline-block; padding: 12px 26px 10px; border-radius: 12px; background: var(--accent); color: var(--ink); font-family: var(--font-chip); font-size: 38px; text-transform: uppercase; box-shadow: 0 8px 0 rgba(0, 0, 0, 0.3); }}
      .line {{ margin-top: 18px; font-family: var(--font-head); text-transform: uppercase; color: var(--paper); font-size: 104px; line-height: 0.95; text-shadow: 0 5px 0 rgba(0, 0, 0, 0.35), 0 10px 36px rgba(0, 0, 0, 0.6); }}
      .line .y {{ color: var(--accent); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{f(total)}" data-width="1080" data-height="1920">
      <div id="cam">
        <video id="base" class="clip" src="assets/base.mp4" data-has-audio="true" data-volume="0.35" playsinline data-start="0" data-duration="{f(total)}" data-track-index="0"></video>
      </div>
      <div id="topfade"></div>
{"".join(caps)}      <div id="flash" class="clip" data-start="{f(R - 0.1)}" data-duration="0.7" data-track-index="4"></div>

      <!-- SOUND DESIGN (narration track goes on its own <audio> when available) -->
{chr(10).join(snd)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      const cuts = [{", ".join(f(c) for c in cuts)}];
      const scales = [{", ".join(f(s) for s in scales)}];
      cuts.forEach((t, i) => {{
        const end = i + 1 < cuts.length ? cuts[i + 1] : {f(total)};
        tl.fromTo("#cam", {{ scale: scales[i] + 0.04 }}, {{ scale: scales[i], duration: Math.min(0.3, end - t), ease: "power3.out", immediateRender: i === 0 }}, t);
      }});
      const pop = (sel, t) => tl.fromTo(sel, {{ opacity: 0, scale: 0.6, rotate: -4 }}, {{ opacity: 1, scale: 1, rotate: 0, duration: 0.32, ease: "back.out(2.6)" }}, t);
      const rise = (sel, t) => tl.fromTo(sel, {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "expo.out" }}, t);
      const out = (sel, t) => tl.to(sel, {{ opacity: 0, y: -16, duration: 0.2, ease: "power2.in" }}, t);
{chr(10).join(js)}
      tl.fromTo("#flash", {{ opacity: 0 }}, {{ opacity: 0.85, duration: 0.1, ease: "power2.in" }}, {f(R - 0.1)});
      tl.to("#flash", {{ opacity: 0, duration: 0.45, ease: "power2.out" }}, {f(R)});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open('index.html', 'w').write(page)
print(total, sec)

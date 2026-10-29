"""Builds index.html: a 45 s vertical motion-graphics documentary on sea-turtle nesting.

Scene timing follows the narration word timestamps in build/narration.json.
"""
import json
import math
import random

TOTAL = 45.0
N = json.load(open('build/narration.json'))
f = lambda x: f"{x:.2f}".rstrip('0').rstrip('.')
rnd = random.Random(7)   # every "random" placement is fixed, so renders are identical

SCENES = [  # id, start, end
    ('sA', 0.0, 7.0), ('sB', 7.0, 13.0), ('sC', 13.0, 18.6), ('sD', 18.6, 23.8),
    ('sE', 23.8, 31.8), ('sF', 31.8, 39.3), ('sG', 39.3, TOTAL),
]
XF = 0.5  # crossfade between scenes


def word_time(line, word):
    for w, s, e in N[line]['words']:
        if w.lower().strip(',.?!-').startswith(word):
            return s
    raise KeyError(word)


# ---------- reusable drawings ----------
TURTLE_TOP = '''
  <g class="flipper fl-l"><path d="M-70,-70 C-160,-120 -250,-60 -300,30 C-230,0 -150,-10 -80,-20 Z" fill="url(#gFlip)"/></g>
  <g class="flipper fl-r"><path d="M70,-70 C160,-120 250,-60 300,30 C230,0 150,-10 80,-20 Z" fill="url(#gFlip)"/></g>
  <g class="flipper hl-l"><path d="M-70,120 C-120,130 -150,170 -150,215 C-115,195 -85,170 -55,150 Z" fill="url(#gFlip)"/></g>
  <g class="flipper hl-r"><path d="M70,120 C120,130 150,170 150,215 C115,195 85,170 55,150 Z" fill="url(#gFlip)"/></g>
  <path d="M0,170 L-14,215 L14,215 Z" fill="#2c3a2b"/>
  <ellipse cx="0" cy="-185" rx="44" ry="56" fill="url(#gHead)"/>
  <ellipse cx="0" cy="10" rx="128" ry="178" fill="url(#gShell)"/>
  <g fill="none" stroke="#c9d3b8" stroke-opacity="0.28" stroke-width="3">
    <path d="M0,-150 L-38,-118 L-38,-62 L0,-38 L38,-62 L38,-118 Z"/>
    <path d="M0,-38 L-42,-12 L-42,42 L0,66 L42,42 L42,-12 Z"/>
    <path d="M0,66 L-36,92 L-30,140 L0,160 L30,140 L36,92 Z"/>
    <path d="M-38,-118 L-98,-100 M-42,-12 L-122,-10 M-42,42 L-118,70 M-36,92 L-92,130"/>
    <path d="M38,-118 L98,-100 M42,-12 L122,-10 M42,42 L118,70 M36,92 L92,130"/>
  </g>
  <ellipse cx="-40" cy="-60" rx="50" ry="90" fill="#ffffff" opacity="0.07"/>
'''

TURTLE_SIDE = '''
  <path d="M-250,8 C-235,-120 -80,-175 60,-160 C180,-148 245,-80 258,8 Z" fill="url(#gShellSide)"/>
  <path d="M-250,8 L258,8 C230,34 -220,34 -250,8 Z" fill="#1b2419"/>
  <path d="M250,-6 C290,-30 340,-40 372,-14 C380,6 350,22 300,20 C276,18 262,12 250,8 Z" fill="url(#gHead)"/>
  <circle cx="350" cy="-14" r="5" fill="#0b0f0a"/>
  <g class="side-front"><path d="M130,10 C170,40 210,90 236,132 C190,118 150,80 112,30 Z" fill="url(#gFlip)"/></g>
  <g class="side-rear"><path d="M-190,10 C-220,40 -250,70 -268,98 C-232,92 -200,64 -170,28 Z" fill="url(#gFlip)"/></g>
  <path d="M-160,-110 C-60,-150 60,-150 160,-110" fill="none" stroke="#c9d3b8" stroke-opacity="0.22" stroke-width="3"/>
'''

DEFS = '''
<defs>
  <radialGradient id="gShell" cx="45%" cy="40%" r="70%">
    <stop offset="0" stop-color="#6f7d5c"/><stop offset="0.6" stop-color="#46553a"/><stop offset="1" stop-color="#252f20"/>
  </radialGradient>
  <linearGradient id="gShellSide" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#6c7a59"/><stop offset="1" stop-color="#2a3524"/>
  </linearGradient>
  <linearGradient id="gFlip" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#5a6a4c"/><stop offset="1" stop-color="#2d3a28"/>
  </linearGradient>
  <radialGradient id="gHead" cx="40%" cy="35%" r="70%">
    <stop offset="0" stop-color="#7b8763"/><stop offset="1" stop-color="#33402b"/>
  </radialGradient>
  <radialGradient id="gEgg" cx="35%" cy="30%" r="75%">
    <stop offset="0" stop-color="#fbf7ee"/><stop offset="0.7" stop-color="#e2dac8"/><stop offset="1" stop-color="#b9ae96"/>
  </radialGradient>
  <linearGradient id="gSandU" gradientUnits="userSpaceOnUse" x1="0" y1="878" x2="0" y2="1920">
    <stop offset="0" stop-color="#b8a47f"/><stop offset="0.35" stop-color="#8f7c5c"/><stop offset="1" stop-color="#4c4031"/>
  </linearGradient>
  <linearGradient id="gSandSec" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#b8a47f"/><stop offset="0.35" stop-color="#8f7c5c"/><stop offset="1" stop-color="#4c4031"/>
  </linearGradient>
  <linearGradient id="gHeat" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#5aa9e6"/><stop offset="0.5" stop-color="#e9d8a6"/><stop offset="1" stop-color="#ee6c3b"/>
  </linearGradient>
  <filter id="soft"><feGaussianBlur stdDeviation="18"/></filter>
  <filter id="soft2"><feGaussianBlur stdDeviation="6"/></filter>
  <symbol id="hatch" viewBox="-310 -250 620 480">''' + TURTLE_TOP.replace('url(#gShell)', '#55654a').replace('url(#gFlip)', '#46553d') + '''</symbol>
</defs>
'''


def stars(n, h):
    out = []
    for i in range(n):
        x, y = rnd.uniform(20, 1060), rnd.uniform(30, h)
        r = rnd.choice([1.2, 1.6, 2.2, 2.8])
        out.append(f'<circle class="star" cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#f6f1e4" opacity="{rnd.uniform(0.35, 0.95):.2f}"/>')
    return '\n'.join(out)


def sand_specks(n, x0, x1, y0, y1, color='#fff', op=(0.05, 0.16)):
    return '\n'.join(
        f'<circle cx="{rnd.uniform(x0, x1):.0f}" cy="{rnd.uniform(y0, y1):.0f}" r="{rnd.choice([1.5, 2, 2.5, 3])}" '
        f'fill="{color}" opacity="{rnd.uniform(*op):.2f}"/>' for _ in range(n))


def wave_path(y, amp, wl, phase=0.0, w=2400, close_to=None):
    pts = [f'M-600,{y + amp * math.sin(phase):.1f}']
    for x in range(-600, w, 40):
        pts.append(f'L{x},{y + amp * math.sin(phase + x / wl * 2 * math.pi):.1f}')
    if close_to is not None:
        pts.append(f'L{w},{close_to} L-600,{close_to} Z')
    return ' '.join(pts)


# ---------- scenes ----------
html = []
js = []
sc = {k: (a, b) for k, a, b in SCENES}


def scene_div(sid, inner, extra=''):
    a, b = sc[sid]
    a0 = max(0.0, a - (XF if a > 0 else 0))
    html.append(f'      <div id="{sid}" class="scene clip" data-start="{f(a0)}" data-duration="{f(b - a0)}" data-track-index="1"{extra}>\n'
                f'        <div class="cam">{inner}</div>\n      </div>\n')
    if a > 0:
        js.append(f'      tl.fromTo("#{sid}", {{ opacity: 0 }}, {{ opacity: 1, duration: {XF}, ease: "power1.inOut", immediateRender: false }}, {f(a0)});')
    js.append(f'      tl.fromTo("#{sid} .cam", {{ scale: 1.0 }}, {{ scale: 1.07, duration: {f(b - a0)}, ease: "none" }}, {f(a0)});')


# Scene A — moonlit beach, title
moon_reflect = '\n'.join(
    f'<rect class="glint" x="{540 - w / 2:.0f}" y="{1080 + i * 22}" width="{w:.0f}" height="4" rx="2" fill="#f3ead6" opacity="{0.55 - i * 0.025:.2f}"/>'
    for i, w in enumerate([rnd.uniform(40, 200) * (1 + i * 0.08) for i in range(16)]))
scene_div('sA', f'''
<svg width="1080" height="1920" viewBox="0 0 1080 1920">{DEFS}
  <rect width="1080" height="1920" fill="url(#skyA)"/>
  <defs><linearGradient id="skyA" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#030812"/><stop offset="0.45" stop-color="#0b1d33"/><stop offset="0.56" stop-color="#173452"/></linearGradient>
  <linearGradient id="seaA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#11304d"/><stop offset="1" stop-color="#0a1f33"/></linearGradient>
  <linearGradient id="sandA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a7a60"/><stop offset="1" stop-color="#2f2920"/></linearGradient></defs>
  <g class="stars">{stars(90, 980)}</g>
  <g class="moon"><circle cx="540" cy="760" r="170" fill="#f3ead6" opacity="0.14" filter="url(#soft)"/>
    <circle cx="540" cy="760" r="92" fill="#f3ead6"/><circle cx="512" cy="738" r="16" fill="#d9cfb8" opacity="0.6"/>
    <circle cx="570" cy="790" r="10" fill="#d9cfb8" opacity="0.5"/></g>
  <rect y="1060" width="1080" height="380" fill="url(#seaA)"/>
  <g class="reflect">{moon_reflect}</g>
  <path class="waveA1" d="{wave_path(1400, 10, 260, 0, close_to=1470)}" fill="#e9e3d2" opacity="0.18"/>
  <path class="waveA2" d="{wave_path(1440, 8, 200, 1.4, close_to=1500)}" fill="#e9e3d2" opacity="0.28"/>
  <path d="M0,1470 C260,1440 520,1500 1080,1450 L1080,1920 L0,1920 Z" fill="url(#sandA)"/>
  {sand_specks(260, 0, 1080, 1480, 1920)}
  <path d="M0,1700 C300,1640 600,1760 1080,1660 L1080,1920 L0,1920 Z" fill="#1d1913" opacity="0.6"/>
</svg>
<div class="title-block"><div class="kicker">documentário · natureza</div><div class="title">O ritual<br/>da areia</div></div>''')
a, b = sc['sA']
js += [
    '      tl.fromTo("#sA .moon", { y: 180 }, { y: 0, duration: 6.5, ease: "power2.out" }, 0);',
    '      tl.fromTo("#sA .waveA1", { x: 0 }, { x: -260, duration: 7, ease: "sine.inOut" }, 0);',
    '      tl.fromTo("#sA .waveA2", { x: -100 }, { x: 100, duration: 7, ease: "sine.inOut" }, 0);',
    '      tl.fromTo("#sA .glint", { scaleX: 0.6, transformOrigin: "50% 50%" }, { scaleX: 1.25, duration: 0.9, ease: "sine.inOut", yoyo: true, repeat: 7, stagger: { each: 0.07, from: "random" } }, 0);',
    '      tl.fromTo("#sA .kicker", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.9, ease: "power3.out" }, 0.6);',
    '      tl.fromTo("#sA .title", { opacity: 0, y: 30, filter: "blur(10px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 1.4, ease: "power3.out" }, 0.9);',
    '      tl.to("#sA .title-block", { opacity: 0, y: -20, duration: 0.8, ease: "power2.in" }, 5.6);',
]

# Scene B — aerial: the female leaves the sea
tracks = []
for i in range(14):
    y = 520 + i * 52
    tracks.append(f'<g class="trk" opacity="0"><path d="M{540 - 120},{y} q-28,12 -44,30" stroke="#3a3226" stroke-width="10" stroke-linecap="round" fill="none" opacity="0.5"/>'
                  f'<path d="M{540 + 120},{y} q28,12 44,30" stroke="#3a3226" stroke-width="10" stroke-linecap="round" fill="none" opacity="0.5"/></g>')
scene_div('sB', f'''
<svg width="1080" height="1920" viewBox="0 0 1080 1920">{DEFS}
  <defs><linearGradient id="sandB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9a8868"/><stop offset="1" stop-color="#6d5e46"/></linearGradient>
  <linearGradient id="seaB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#071a2c"/><stop offset="1" stop-color="#14405f"/></linearGradient></defs>
  <rect width="1080" height="1920" fill="url(#sandB)"/>
  {sand_specks(420, 0, 1080, 500, 1920, '#2a2419', (0.08, 0.2))}
  {sand_specks(260, 0, 1080, 500, 1920, '#fff', (0.05, 0.14))}
  <g class="trks">{''.join(tracks)}</g>
  <g class="seaB"><path d="{wave_path(520, 18, 380, 0.3, close_to=-200)}" fill="url(#seaB)"/>
    <path class="foamB" d="{wave_path(520, 18, 380, 0.3)}" stroke="#eae4d4" stroke-width="16" stroke-opacity="0.55" fill="none"/>
    <path class="foamB2" d="{wave_path(470, 12, 300, 1.7)}" stroke="#eae4d4" stroke-width="6" stroke-opacity="0.25" fill="none"/></g>
  <g transform="translate(540,1000) scale(0.95)"><g class="turtleB">{TURTLE_TOP}</g></g>
  <ellipse cx="540" cy="140" rx="700" ry="220" fill="#cfe2f2" opacity="0.08" filter="url(#soft)"/>
</svg>
<div class="callout" id="calloutB"><div class="dot"></div><div class="cl-line"></div><div class="cl-text"><b>Fêmea adulta</b><br/>tartaruga-marinha</div></div>''')
js += [
    '      tl.fromTo("#sB .turtleB", { y: -600, opacity: 0.5 }, { y: 0, opacity: 1, duration: 5.6, ease: "power1.out" }, 6.8);',
    '      tl.fromTo("#sB .fl-l, #sB .hl-r", { rotation: -16, transformOrigin: "-70px -60px" }, { rotation: 16, duration: 0.7, ease: "sine.inOut", yoyo: true, repeat: 7 }, 6.8);',
    '      tl.fromTo("#sB .fl-r, #sB .hl-l", { rotation: 16, transformOrigin: "70px -60px" }, { rotation: -16, duration: 0.7, ease: "sine.inOut", yoyo: true, repeat: 7 }, 6.8);',
    '      tl.to("#sB .trk", { opacity: 1, duration: 0.3, stagger: 0.36 }, 7.4);',
    '      tl.fromTo("#sB .foamB", { x: 0 }, { x: -380, duration: 6.5, ease: "sine.inOut" }, 6.5);',
    '      tl.fromTo("#sB .foamB2", { x: -200 }, { x: 120, duration: 6.5, ease: "sine.inOut" }, 6.5);',
    f'      tl.fromTo("#calloutB", {{ opacity: 0, x: 30 }}, {{ opacity: 1, x: 0, duration: 0.7, ease: "power3.out" }}, {f(word_time("n2", "fêmea") - 0.1)});',
    '      tl.fromTo("#calloutB .cl-line", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power3.out" }, 8.6);',
    '      tl.to("#calloutB", { opacity: 0, duration: 0.5 }, 12.2);',
]

# Scene C — cross-section: digging the nest
grains = '\n'.join(
    f'<circle class="grain" cx="{rnd.uniform(380, 520):.0f}" cy="{rnd.uniform(860, 900):.0f}" r="{rnd.choice([4, 5, 6])}" fill="#c7b38e"/>'
    for _ in range(26))
strata = '\n'.join(f'<path d="M0,{y} C300,{y + rnd.randint(-14, 14)} 700,{y + rnd.randint(-14, 14)} 1080,{y}" stroke="#2b241b" stroke-opacity="0.25" stroke-width="3" fill="none"/>'
                   for y in range(980, 1900, 90))
CHAMBER = 'M410,880 C410,960 400,1010 380,1060 C330,1160 360,1300 470,1320 C560,1336 640,1300 650,1210 C660,1120 600,1060 560,1030 C540,1000 530,940 530,880 Z'
scene_div('sC', f'''
<svg width="1080" height="1920" viewBox="0 0 1080 1920">{DEFS}
  <defs><linearGradient id="skyC" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#04101e"/><stop offset="1" stop-color="#173452"/></linearGradient>
  <clipPath id="digClip"><rect class="digRect" x="300" y="870" width="420" height="0"/></clipPath></defs>
  <rect width="1080" height="880" fill="url(#skyC)"/>
  <g class="stars">{stars(40, 700)}</g>
  <rect y="878" width="1080" height="1042" fill="url(#gSandSec)"/>
  {strata}
  {sand_specks(380, 0, 1080, 900, 1920, '#1d1812', (0.1, 0.25))}
  <path d="M0,880 C200,872 380,890 540,880 C700,870 900,886 1080,878" stroke="#d8c7a3" stroke-width="4" fill="none" opacity="0.7"/>
  <g clip-path="url(#digClip)"><path d="{CHAMBER}" fill="#1c160f"/><path d="{CHAMBER}" fill="none" stroke="#d8c7a3" stroke-opacity="0.35" stroke-width="3" stroke-dasharray="10 10"/></g>
  <g class="grains">{grains}</g>
  <g transform="translate(470,842) scale(0.95)"><g class="turtleC">{TURTLE_SIDE}</g></g>
  <g class="dim"><line class="dimLine" x1="800" y1="880" x2="800" y2="1320" stroke="#e9c46a" stroke-width="3"/>
    <line x1="780" y1="880" x2="820" y2="880" stroke="#e9c46a" stroke-width="3"/>
    <line class="dimEnd" x1="780" y1="1320" x2="820" y2="1320" stroke="#e9c46a" stroke-width="3"/></g>
</svg>
<div class="metric" id="mC"><span class="num" id="cmNum">0</span><span class="unit">cm</span><div class="lbl">profundidade do ninho</div></div>''')
t60 = word_time('n3', 'sessenta')
js += [
    '      tl.fromTo("#sC .side-rear", { rotation: -22, transformOrigin: "-180px 14px" }, { rotation: 18, duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: 9 }, 13.2);',
    '      tl.fromTo("#sC .digRect", { attr: { height: 0 } }, { attr: { height: 460 }, duration: ' + f(t60 + 0.5 - 13.4) + ', ease: "power1.inOut" }, 13.4);',
    '      tl.fromTo("#sC .grain", { y: 0, x: 0, opacity: 0 }, { y: () => -120 - 80 * Math.random(), x: () => -60 + 120 * Math.random(), opacity: 1, duration: 0.5, ease: "power2.out", stagger: { each: 0.12, repeat: 1, yoyo: false } }, 13.6);'.replace('Math.random()', '0.5'),
    f'      tl.fromTo("#sC .dim", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {f(t60 - 1.6)});',
    f'      tl.fromTo("#sC .dimLine", {{ attr: {{ y2: 880 }} }}, {{ attr: {{ y2: 1320 }}, duration: 1.6, ease: "power2.out" }}, {f(t60 - 1.4)});',
    f'      tl.fromTo("#sC .dimEnd", {{ attr: {{ y1: 880, y2: 880 }} }}, {{ attr: {{ y1: 1320, y2: 1320 }}, duration: 1.6, ease: "power2.out" }}, {f(t60 - 1.4)});',
    f'      tl.fromTo("#mC", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, {f(t60 - 1.5)});',
    f'      tl.fromTo("#cmNum", {{ textContent: 0 }}, {{ textContent: 60, duration: 1.6, ease: "power2.out", snap: {{ textContent: 1 }} }}, {f(t60 - 1.4)});',
]
# grains: deterministic offsets (replace the arrow functions above with fixed values per element)
js[-6] = '      tl.fromTo("#sC .grain", { y: 0, opacity: 0 }, { y: -150, x: (i) => ((i * 37) % 120) - 60, opacity: 0.9, duration: 0.55, ease: "power2.out", stagger: 0.16 }, 13.6);\n      tl.to("#sC .grain", { opacity: 0, duration: 0.3, stagger: 0.16 }, 14.2);'

# Scene D — eggs counter
eggs = []
cols = [(470 + dx, 1290 - row * 38 - (abs(dx) % 3) * 4) for row in range(6) for dx in range(-140 + (row % 2) * 20, 160 - row * 18, 42)]
cols = [(x, y) for x, y in cols if (x - 470) ** 2 / 210 ** 2 + (y - 1190) ** 2 / 150 ** 2 < 1.15]
for i, (x, y) in enumerate(cols):
    eggs.append(f'<circle class="egg" cx="{x}" cy="{y}" r="22" fill="url(#gEgg)"/>')
scene_div('sD', f'''
<svg width="1080" height="1920" viewBox="0 0 1080 1920">{DEFS}
  <rect width="1080" height="1920" fill="url(#gSandSec)"/>
  {strata}
  {sand_specks(380, 0, 1080, 0, 1920, '#1d1812', (0.1, 0.25))}
  <g transform="translate(-235,-520) scale(1.5)"><path d="{CHAMBER}" fill="#1c160f"/>
    <path d="{CHAMBER}" fill="none" stroke="#d8c7a3" stroke-opacity="0.35" stroke-width="2" stroke-dasharray="8 8"/>
    <g class="eggs">{''.join(eggs)}</g></g>
</svg>
<div class="metric big" id="mD"><span class="num" id="eggNum">0</span><div class="lbl">ovos por ninho, em média</div></div>
<div class="pp" id="ppD"><svg width="120" height="120" viewBox="0 0 120 120"><circle cx="60" cy="60" r="44" fill="url(#gEgg)"/><circle cx="60" cy="60" r="44" fill="none" stroke="#e9c46a" stroke-width="3" stroke-dasharray="6 6"/></svg>
  <div><b>≈ 4 cm</b><br/>tamanho de uma bola<br/>de pingue-pongue</div></div>''')
t100 = word_time('n4', 'cem')
tpp = word_time('n4', 'pingue')
js += [
    f'      tl.fromTo("#sD .egg", {{ y: -260, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "bounce.out", stagger: {f((t100 + 0.4 - 18.9) / max(1, len(eggs)))} }}, 18.9);',
    '      tl.fromTo("#mD", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, 18.8);',
    f'      tl.fromTo("#eggNum", {{ textContent: 0 }}, {{ textContent: 100, duration: {f(t100 + 0.3 - 19.0)}, ease: "power1.inOut", snap: {{ textContent: 1 }} }}, 19.0);',
    f'      tl.fromTo("#ppD", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }}, {f(word_time("n4", "tamanho") - 0.3)});',
]

# Scene E — cover the nest, back to sea, temperature decides the sex
scene_div('sE', f'''
<svg width="1080" height="1920" viewBox="0 0 1080 1920">{DEFS}
  <defs><linearGradient id="skyE" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#04101e"/><stop offset="1" stop-color="#173452"/></linearGradient>
  <clipPath id="fillClip"><rect class="fillRect" x="300" y="1340" width="420" height="0"/></clipPath></defs>
  <rect width="1080" height="880" fill="url(#skyE)"/>
  <g class="stars">{stars(40, 700)}</g>
  <rect y="878" width="1080" height="1042" fill="url(#gSandSec)"/>
  {strata}
  {sand_specks(380, 0, 1080, 900, 1920, '#1d1812', (0.1, 0.25))}
  <path d="M0,880 C200,872 380,890 540,880 C700,870 900,886 1080,878" stroke="#d8c7a3" stroke-width="4" fill="none" opacity="0.7"/>
  <path d="{CHAMBER}" fill="#1c160f"/>
  <g transform="translate(470,1190) scale(0.62) translate(-470,-1190)">{''.join(eggs)}</g>
  <g clip-path="url(#fillClip)"><rect x="300" y="881" width="420" height="460" fill="url(#gSandU)"/>{sand_specks(120, 300, 720, 884, 1340, '#1d1812', (0.1, 0.25))}</g>
  {strata}
  <g class="heat" opacity="0"><rect x="0" y="880" width="1080" height="1040" fill="#ee6c3b" opacity="0.18"/></g>
  <g transform="translate(470,842) scale(0.95)"><g class="turtleE">{TURTLE_SIDE}</g></g>
</svg>
<div class="thermo" id="thE"><div class="t-head"><span>temperatura da areia</span></div>
  <div class="t-bar"><div class="t-grad"></div><div class="t-pivot"></div><div class="t-mark"></div></div>
  <div class="t-labels"><span class="cool">mais fria<br/><b>machos</b></span><span class="mid">≈ 29 °C</span><span class="warm">mais quente<br/><b>fêmeas</b></span></div></div>''')
tcob = word_time('n5', 'cobre'); tvol = word_time('n5', 'volta'); tcal = word_time('n5', 'calor'); tfem = word_time('n5', 'fêmeas')
js += [
    f'      tl.fromTo("#sE .fillRect", {{ attr: {{ y: 1340, height: 0 }} }}, {{ attr: {{ y: 881, height: 459 }}, duration: 1.6, ease: "power2.inOut" }}, {f(tcob)});',
    f'      tl.fromTo("#sE .turtleE", {{ x: 0 }}, {{ x: -1000, duration: 2.4, ease: "power2.in" }}, {f(tvol - 0.2)});',
    f'      tl.fromTo("#sE .side-front", {{ rotation: -18, transformOrigin: "130px 10px" }}, {{ rotation: 18, duration: 0.3, yoyo: true, repeat: 7, ease: "sine.inOut" }}, {f(tvol - 0.2)});',
    f'      tl.to("#sE .heat", {{ opacity: 1, duration: 2.5, ease: "sine.inOut" }}, {f(tcal)});',
    f'      tl.fromTo("#thE", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.7, ease: "power3.out" }}, {f(tcal - 0.3)});',
    f'',
    f'      tl.fromTo("#thE .t-mark", {{ x: 0 }}, {{ x: 324, duration: 1.4, ease: "power3.inOut" }}, {f(tfem - 1.2)});',
    f'      tl.fromTo("#thE .warm b", {{ color: "#f1ece2" }}, {{ color: "#ee6c3b", duration: 0.4 }}, {f(tfem)});',
]

# Scene F — hatchlings run to the sea
hatch = []
HATCH_START = [(540 + rnd.randint(-150, 150), 1330 + rnd.randint(-34, 34)) for _ in range(9)]
for i in range(9):
    x0, y0 = HATCH_START[i]
    hatch.append(f'<g transform="translate({x0},{y0})"><g class="hatch h{i}"><use href="#hatch" x="-55" y="-42" width="110" height="85"/></g></g>')
scene_div('sF', f'''
<svg width="1080" height="1920" viewBox="0 0 1080 1920">{DEFS}
  <defs><linearGradient id="sandF" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8d7c5e"/><stop offset="1" stop-color="#5d503c"/></linearGradient>
  <linearGradient id="seaF" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#081d31"/><stop offset="1" stop-color="#1b4b6d"/></linearGradient>
  <radialGradient id="glowF" cx="50%" cy="20%" r="60%"><stop offset="0" stop-color="#f3ead6" stop-opacity="0.55"/><stop offset="1" stop-color="#f3ead6" stop-opacity="0"/></radialGradient></defs>
  <rect width="1080" height="1920" fill="url(#sandF)"/>
  {sand_specks(420, 0, 1080, 560, 1920, '#2a2419', (0.08, 0.2))}
  {sand_specks(240, 0, 1080, 560, 1920, '#fff', (0.05, 0.14))}
  <g><path d="{wave_path(600, 16, 360, 0.9, close_to=-200)}" fill="url(#seaF)"/>
    <path class="foamF" d="{wave_path(600, 16, 360, 0.9)}" stroke="#eae4d4" stroke-width="14" stroke-opacity="0.5" fill="none"/></g>
  <rect class="glow" width="1080" height="900" fill="url(#glowF)" opacity="0.4"/>
  <ellipse cx="540" cy="1330" rx="190" ry="56" fill="#3c3326" opacity="0.6"/>
  {''.join(hatch)}
</svg>
<div class="chip" id="chipF">≈ 60 dias depois</div>''')
tfil = word_time('n6', 'filhotes'); tcor = word_time('n6', 'correm'); tbri = word_time('n6', 'brilho')
js += [
    f'      tl.fromTo("#chipF", {{ opacity: 0, y: -16 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, {f(word_time("n6", "dois") - 0.2)});',
    f'      tl.to("#chipF", {{ opacity: 0, duration: 0.5 }}, {f(tcor + 0.6)});',
    f'      tl.fromTo("#sF .hatch", {{ scale: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: 0.5, ease: "back.out(2)", stagger: 0.12 }}, {f(tfil - 0.2)});',
]
for i in range(9):
    dx = (HATCH_START[i][0] - 540) * 1.6 + rnd.randint(-60, 60)
    js.append(f'      tl.to("#sF .h{i}", {{ x: {dx}, y: {-640 - rnd.randint(0, 120)}, rotation: {-(i - 4) * 4}, duration: {f(3.2 + rnd.uniform(-0.4, 0.5))}, ease: "power1.in" }}, {f(tcor - 0.3 + i * 0.07)});')
js += [
    f'      tl.to("#sF .glow", {{ opacity: 1, duration: 1.6, ease: "sine.inOut" }}, {f(tbri - 0.6)});',
    '      tl.fromTo("#sF .foamF", { x: 0 }, { x: -360, duration: 8, ease: "sine.inOut" }, 31.3);',
]

# Scene G — 1 in 1,000 + end title
scene_div('sG', f'''
<svg width="1080" height="1920" viewBox="0 0 1080 1920">{DEFS}
  <defs><linearGradient id="skyG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#02060d"/><stop offset="0.7" stop-color="#0b1d33"/><stop offset="1" stop-color="#11304d"/></linearGradient></defs>
  <rect width="1080" height="1920" fill="url(#skyG)"/>
  <g class="stars">{stars(120, 1300)}</g>
  <circle cx="540" cy="1500" r="260" fill="#f3ead6" opacity="0.08" filter="url(#soft)"/>
  <path class="waveG" d="{wave_path(1640, 10, 300, 0.2, close_to=1920)}" fill="#0a2236"/>
  <g transform="translate(540,1600)"><use class="lone" href="#hatch" x="-31" y="-24" width="62" height="48"/></g>
</svg>
<div class="stat" id="stG"><span class="one">1</span><span class="of">em cada <b>1.000</b></span><div class="lbl">filhotes chega à vida adulta</div></div>
<div class="endcard" id="endG"><div class="title small">Tartarugas-marinhas</div><div class="kicker">o ritual da areia</div></div>''')
tum = word_time('n7', 'um')
js += [
    f'      tl.fromTo("#stG .one", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.9, ease: "expo.out" }}, {f(tum - 0.1)});',
    f'      tl.fromTo("#stG .of", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.7, ease: "power3.out" }}, {f(word_time("n7", "cada") - 0.1)});',
    f'      tl.fromTo("#stG .lbl", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.7 }}, {f(word_time("n7", "chegará"))});',
    '      tl.to("#stG", { opacity: 0, y: -20, duration: 0.6, ease: "power2.in" }, 42.1);',
    '      tl.fromTo("#endG", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.9, ease: "power3.out" }, 42.5);',
    '      tl.fromTo("#sG .lone", { y: 0 }, { y: -40, duration: 5.7, ease: "sine.inOut" }, 39.3);',
    '      tl.to("#fade", { opacity: 1, duration: 0.45, ease: "power1.in" }, 44.55);',
]

# star twinkle in every scene (finite repeats)
js.append('      tl.fromTo(".star", { opacity: 0.25 }, { opacity: 1, duration: 1.3, ease: "sine.inOut", yoyo: true, repeat: 33, stagger: { each: 0.02, from: "random" } }, 0);')

# ---------- subtitles from word timings ----------
FUNC = {'a', 'o', 'as', 'os', 'de', 'da', 'do', 'e', 'em', 'ao', 'um', 'uma', 'com', 'pela', 'pelo', 'nas', 'nos', 'na', 'no', 'à'}
subs = []
for k, line in N.items():
    words = line['words']
    cut = None
    if len(words) > 9:
        best = None
        for i in range(3, len(words) - 2):
            if words[i][0].endswith((',', '.', ':')):
                d1 = words[i][2] - words[0][1]; d2 = words[-1][2] - words[i + 1][1]
                score = abs(d1 - d2) - (1.0 if words[i][0].endswith('.') else 0)
                if min(d1, d2) >= 0.8 and (best is None or score < best[0]):
                    best = (score, i + 1)
        if best:
            cut = best[1]
        else:   # middle, but never right after a short function word
            cut = len(words) // 2
            while cut > 2 and words[cut - 1][0].lower().strip(',.') in FUNC:
                cut -= 1
    parts = [words[:cut], words[cut:]] if cut else [words]
    for part in parts:
        subs.append((part[0][1], part[-1][2], ' '.join(w for w, _, _ in part).replace(' -', '-')))
sub_html = []
for i, (s, e, text) in enumerate(subs):
    nxt = subs[i + 1][0] - 0.05 if i + 1 < len(subs) else TOTAL
    end = min(e + 0.35, nxt)
    sub_html.append(f'      <div id="sub{i}" class="sub clip" data-start="{f(s - 0.05)}" data-duration="{f(end - s + 0.05)}" data-track-index="5"><span>{text}</span></div>')
    js.append(f'      tl.fromTo("#sub{i} span", {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "power2.out" }}, {f(s - 0.05)});')

# grain: shift the noise tile every frame
js.append(f'      tl.to("#grain", {{ backgroundPosition: "200px 140px", duration: {f(TOTAL)}, ease: "steps({int(TOTAL * 12)})" }}, 0);')

AUDIO = ''   # the soundtrack is mixed outside the render by mix.py (music ducked under the narration)


page = f'''<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/gsap.min.js"></script>
    <style>
      :root {{ --text: #f1ece2; --gold: #e9c46a; --serif: "EB Garamond", serif; --sans: "Inter", sans-serif; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #02060d; }}
      #root {{ width: 100%; height: 100%; position: relative; overflow: hidden; font-family: var(--sans); color: var(--text); }}
      .scene {{ position: absolute; inset: 0; overflow: hidden; }}
      .cam {{ position: absolute; inset: 0; transform-origin: 50% 50%; }}
      .cam > svg {{ position: absolute; inset: 0; }}
      .title-block {{ position: absolute; left: 0; right: 0; top: 330px; text-align: center; }}
      .kicker {{ font-family: var(--sans); font-weight: 700; font-size: 28px; letter-spacing: 0.42em; text-transform: uppercase; color: var(--gold); }}
      .title {{ margin-top: 26px; font-family: var(--serif); font-style: italic; font-size: 150px; line-height: 0.95; color: var(--text); text-shadow: 0 6px 40px rgba(0,0,0,.5); }}
      .title.small {{ font-size: 92px; }}
      .callout {{ position: absolute; left: 610px; top: 760px; display: flex; align-items: center; }}
      .callout .dot {{ width: 14px; height: 14px; border-radius: 50%; background: var(--gold); box-shadow: 0 0 0 6px rgba(233,196,106,.25); }}
      .callout .cl-line {{ width: 70px; height: 2px; background: var(--gold); transform-origin: 0 50%; }}
      .callout .cl-text {{ margin-left: 16px; font-size: 26px; letter-spacing: 0.06em; line-height: 1.35; color: var(--text); text-shadow: 0 2px 12px rgba(0,0,0,.6); }}
      .callout .cl-text b {{ font-family: var(--serif); font-style: italic; font-weight: 600; font-size: 40px; letter-spacing: 0; }}
      .metric {{ position: absolute; left: 0; right: 0; top: 230px; text-align: center; }}
      .metric .num {{ font-family: var(--serif); font-size: 230px; line-height: 0.9; color: var(--text); }}
      .metric .unit {{ font-family: var(--serif); font-style: italic; font-size: 96px; color: var(--gold); margin-left: 12px; }}
      .metric .lbl, .stat .lbl {{ margin-top: 18px; font-weight: 700; font-size: 28px; letter-spacing: 0.32em; text-transform: uppercase; color: rgba(241,236,226,.75); }}
      .metric.big .num {{ font-size: 260px; }}
      .pp {{ position: absolute; left: 110px; top: 560px; display: flex; align-items: center; gap: 26px; font-size: 30px; line-height: 1.35; color: rgba(241,236,226,.85); }}
      .pp b {{ font-family: var(--serif); font-style: italic; font-size: 46px; color: var(--gold); font-weight: 600; }}
      .thermo {{ position: absolute; left: 90px; right: 90px; top: 230px; }}
      .t-head {{ font-weight: 700; font-size: 28px; letter-spacing: 0.32em; text-transform: uppercase; color: rgba(241,236,226,.8); text-align: center; }}
      .t-bar {{ position: relative; margin-top: 34px; height: 26px; border-radius: 13px; overflow: visible; }}
      .t-grad {{ position: absolute; inset: 0; border-radius: 13px; background: linear-gradient(90deg, #5aa9e6, #e9d8a6 50%, #ee6c3b); }}
      .t-pivot {{ position: absolute; left: 50%; top: -14px; width: 2px; height: 54px; background: #f1ece2; opacity: .8; }}
      .t-mark {{ position: absolute; left: 50%; top: -22px; width: 30px; height: 70px; margin-left: -15px; border-radius: 15px; border: 4px solid #f1ece2; box-shadow: 0 0 24px rgba(255,255,255,.35); }}
      .t-labels {{ display: flex; justify-content: space-between; align-items: flex-start; margin-top: 30px; font-size: 28px; line-height: 1.35; color: rgba(241,236,226,.75); }}
      .t-labels b {{ font-family: var(--serif); font-style: italic; font-size: 54px; color: var(--text); font-weight: 600; }}
      .t-labels .mid {{ font-family: var(--serif); font-size: 46px; color: var(--gold); }}
      .t-labels .warm {{ text-align: right; }}
      .chip {{ position: absolute; left: 50%; top: 250px; transform: translateX(-50%); padding: 16px 34px; border: 2px solid var(--gold); border-radius: 999px; font-weight: 700; font-size: 32px; letter-spacing: 0.24em; text-transform: uppercase; color: var(--gold); background: rgba(2,6,13,.35); white-space: nowrap; }}
      .stat {{ position: absolute; left: 0; right: 0; top: 520px; text-align: center; }}
      .stat .one {{ display: block; font-family: var(--serif); font-size: 420px; line-height: 0.85; color: var(--text); }}
      .stat .of {{ display: block; margin-top: 10px; font-family: var(--serif); font-style: italic; font-size: 88px; color: rgba(241,236,226,.85); }}
      .stat .of b {{ color: var(--gold); font-weight: 600; }}
      .endcard {{ position: absolute; left: 0; right: 0; top: 700px; text-align: center; }}
      .endcard .kicker {{ margin-top: 26px; }}
      .sub {{ position: absolute; left: 80px; right: 80px; top: 1600px; text-align: center; }}
      .sub span {{ display: inline-block; padding: 10px 22px; font-family: var(--sans); font-weight: 600; font-size: 42px; line-height: 1.25; color: #fff; background: rgba(2,6,13,.55); border-radius: 10px; }}
      #grain {{ position: absolute; inset: -200px; opacity: 0.09; mix-blend-mode: overlay; pointer-events: none;
        background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='220' height='220' filter='url(%23n)'/></svg>"); }}
      #vignette {{ position: absolute; inset: 0; pointer-events: none; background: radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,.55) 100%); }}
      #fade {{ position: absolute; inset: 0; background: #000; opacity: 0; pointer-events: none; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{f(TOTAL)}" data-width="1080" data-height="1920">
{"".join(html)}
{chr(10).join(sub_html)}
      <div id="grain"></div>
      <div id="vignette"></div>
      <div id="fade"></div>
{AUDIO}    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open('index.html', 'w').write(page)
print('scenes', [(k, a, b) for k, a, b in SCENES], 'eggs', len(eggs), 'subs', len(subs))

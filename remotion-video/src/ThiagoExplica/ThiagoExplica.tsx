import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { Audio } from "@remotion/media";
import { FONT } from "../Consorcio/fonts";
import { CAPTIONS, type Caption } from "./captions";

// "Como funciona o consórcio" — 40 s explainer. One diagram (a ring of 12 members around a pot)
// that keeps transforming; captions are the narration, word by word.
export const DURATION = 1200;

const INK = "#13201a";
const GREEN = "#22c55e";
const N = 12;
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const soft = Easing.bezier(0.45, 0, 0.15, 1);
const land = Easing.bezier(0.16, 1, 0.3, 1);

// ---------- events (frames), anchored to the spoken words ----------
const DROP = [26, 42] as const; // "consórcio"
const SPREAD = 128; // "grupo"
const POOL_IN = [186, 214] as const; // "objetivo"
const COIN_AT = 312; // "paga"
const SWEEP1 = [462, 510] as const; // lands on "contemplado"
const WIN1 = 4;
const CARD = [556, 602] as const; // "carta de crédito"
const SWEEP2 = [636, 672] as const; // "sorteio"
const WIN2 = 9;
const LANCE = [697, 721] as const; // "lance"
const WIN3 = 1;
const CASCADE = [890, 941] as const; // "todo mundo é contemplado"
const CTA = [1012, 1064] as const; // "Agora"
const HANDLE = 1160;

const REST = [0, 2, 3, 5, 6, 7, 8, 10, 11];
const greenAt = (i: number) => {
  if (i === WIN1) return SWEEP1[1];
  if (i === WIN2) return SWEEP2[1];
  if (i === WIN3) return LANCE[1];
  const k = REST.indexOf(i);
  return Math.round(CASCADE[0] + (CASCADE[1] - CASCADE[0]) * Math.sqrt(k / (REST.length - 1)));
};

// ---------- geometry ----------
const ring = (t: number) => {
  const p = interpolate(t, [CTA[0], CTA[1]], [0, 1], { ...clamp, easing: soft });
  return {
    x: 540,
    y: interpolate(p, [0, 1], [1250, 990]),
    r: interpolate(p, [0, 1], [390, 370]),
    tok: interpolate(p, [0, 1], [64, 38]),
    spin: t > CTA[0] ? (t - CTA[0]) * 0.4 : 0,
    p,
  };
};
const angleOf = (i: number, spin = 0) => -Math.PI / 2 + (i / N) * 2 * Math.PI + (spin * Math.PI) / 180;

// ---------- pieces ----------
const clay = "radial-gradient(circle at 34% 28%, #ffffff 0%, #f1ece4 32%, #d6cdbf 80%, #bfb4a4 100%)";
const greenClay = "radial-gradient(circle at 34% 28%, #c9f7da 0%, #4ade80 30%, #16a34a 75%, #0f6b33 100%)";

const Token: React.FC<{ readonly x: number; readonly y: number; readonly r: number; readonly g: number; readonly pulse: number }> = ({ x, y, r, g, pulse }) => (
  <div style={{ position: "absolute", left: x - r, top: y - r, width: 2 * r, height: 2 * r, transform: `scale(${1 + 0.14 * Math.sin(Math.PI * pulse)})` }}>
    {pulse > 0 && pulse < 1 ? (
      <div
        style={{
          position: "absolute",
          inset: -r * 0.9 * pulse,
          borderRadius: "50%",
          border: `${4 * (1 - pulse)}px solid ${GREEN}`,
          opacity: 1 - pulse,
        }}
      />
    ) : null}
    <div style={{ position: "absolute", inset: 0, borderRadius: "50%", background: clay, boxShadow: `0 ${r * 0.55}px ${r * 0.8}px rgba(70,50,25,0.22)` }} />
    <div
      style={{
        position: "absolute",
        inset: 0,
        borderRadius: "50%",
        background: greenClay,
        opacity: g,
        boxShadow: `0 0 ${r * 1.4}px rgba(34,197,94,${0.45 * g})`,
      }}
    />
  </div>
);

const Coin: React.FC<{ readonly x: number; readonly y: number; readonly s?: number }> = ({ x, y, s = 1 }) => (
  <div
    style={{
      position: "absolute",
      left: x - 16 * s,
      top: y - 16 * s,
      width: 32 * s,
      height: 32 * s,
      borderRadius: "50%",
      background: "radial-gradient(circle at 35% 30%, #4b5d53, #13201a 70%)",
      boxShadow: "0 8px 10px rgba(0,0,0,0.2)",
    }}
  />
);

const poolLevel = (t: number) => {
  const coins = Array.from({ length: N }, (_, i) => interpolate(t, [COIN_AT + i * 5 + 14, COIN_AT + i * 5 + 18], [0, 0.5 / N], clamp)).reduce((a, b) => a + b, 0);
  const paid1 = interpolate(t, [CARD[0], CARD[1]], [0, -0.14], { ...clamp, easing: soft });
  const lance = interpolate(t, [LANCE[0] + 6, LANCE[1]], [0, 0.08], clamp);
  const paid2 = interpolate(t, [SWEEP2[1], SWEEP2[1] + 20], [0, -0.1], { ...clamp, easing: soft });
  const paid3 = interpolate(t, [LANCE[1], LANCE[1] + 20], [0, -0.1], { ...clamp, easing: soft });
  const refill = interpolate(t, [760, 870], [0, 0.22], { ...clamp, easing: soft });
  return Math.max(0, coins + paid1 + lance + paid2 + paid3 + refill);
};

const Pool: React.FC<{ readonly t: number; readonly x: number; readonly y: number }> = ({ t, x, y }) => {
  const reveal = interpolate(t, [POOL_IN[0], POOL_IN[1]], [0, 1], { ...clamp, easing: land });
  const out = interpolate(t, [CTA[0], CTA[0] + 30], [1, 0], clamp);
  if (reveal <= 0 || out <= 0) return null;
  const level = poolLevel(t);
  return (
    <div
      style={{
        position: "absolute",
        left: x - 180,
        top: y - 180,
        width: 360,
        height: 360,
        borderRadius: "50%",
        overflow: "hidden",
        clipPath: `circle(${reveal * 50}% at 50% 50%)`,
        opacity: out,
        background: "radial-gradient(circle at 50% 35%, #fbf8f3, #e4ddd2)",
        boxShadow: "inset 0 14px 30px rgba(70,50,25,0.25)",
      }}
    >
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          bottom: 0,
          height: `${level * 100}%`,
          background: "linear-gradient(180deg, #2b3d33, #13201a)",
          boxShadow: "inset 0 6px 0 rgba(255,255,255,0.12)",
        }}
      />
    </div>
  );
};

const Sweep: React.FC<{ readonly t: number; readonly span: readonly [number, number]; readonly target: number; readonly x: number; readonly y: number }> = ({ t, span, target, x, y }) => {
  if (t < span[0] || t > span[1] + 14) return null;
  const p = interpolate(t, [span[0], span[1]], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const deg = ((angleOf(target) + Math.PI / 2) * 180) / Math.PI - (1 - p) * 540;
  const fade = interpolate(t, [span[1], span[1] + 14], [1, 0], clamp);
  return (
    <div
      style={{
        position: "absolute",
        left: x - 480,
        top: y - 480,
        width: 960,
        height: 960,
        borderRadius: "50%",
        opacity: fade,
        background: `conic-gradient(from ${deg - 22}deg, rgba(34,197,94,0) 0deg, rgba(34,197,94,0.26) 20deg, rgba(34,197,94,0.05) 26deg, rgba(34,197,94,0) 44deg)`,
      }}
    />
  );
};

const CreditCard: React.FC<{ readonly t: number; readonly x: number; readonly y: number; readonly tx: number; readonly ty: number }> = ({ t, x, y, tx, ty }) => {
  if (t < CARD[0] || t > CARD[1] + 24) return null;
  const p = interpolate(t, [CARD[0], CARD[1]], [0, 1], { ...clamp, easing: soft });
  const tuck = interpolate(t, [CARD[1], CARD[1] + 24], [1, 0], clamp);
  const cx = interpolate(p, [0, 1], [x, tx + 40]);
  const cy = interpolate(p, [0, 1], [y, ty - 70]) - Math.sin(Math.PI * p) * 120;
  return (
    <div
      style={{
        position: "absolute",
        left: cx - 130,
        top: cy - 82,
        width: 260,
        height: 164,
        borderRadius: 16,
        transform: `rotate(${interpolate(p, [0, 1], [0, -12])}deg) scale(${0.8 + 0.2 * tuck})`,
        opacity: tuck,
        background: "linear-gradient(160deg, #ffffff, #f2eee7)",
        boxShadow: "0 26px 40px rgba(70,50,25,0.25)",
        padding: "34px 26px",
        fontFamily: FONT,
        color: INK,
      }}
    >
      <div style={{ fontWeight: 600, fontSize: 28, letterSpacing: "-0.02em" }}>Carta de crédito</div>
      <div style={{ marginTop: 18, height: 12, width: 150, borderRadius: 6, background: GREEN }} />
      <div style={{ marginTop: 10, height: 10, width: 100, borderRadius: 5, background: "#e2dcd2" }} />
    </div>
  );
};

// Narration captions: each word rises out of a mask as it is spoken; the block leaves the same way.
const CaptionBlock: React.FC<{ readonly c: Caption; readonly end: number | null; readonly t: number; readonly top: number; readonly size?: number }> = ({ c, end, t, top, size = 84 }) => (
  <div
    style={{
      position: "absolute",
      left: 60,
      right: 60,
      top,
      textAlign: "center",
      fontFamily: FONT,
      fontWeight: 800,
      fontSize: size,
      lineHeight: 1.08,
      letterSpacing: "-0.045em",
      color: INK,
    }}
  >
    {c.words.map((w, i) => {
      const inP = interpolate(t, [w.f, w.f + 7], [0, 1], { ...clamp, easing: land });
      const outP = end === null ? 0 : interpolate(t, [end - 8 + i * 0.4, end - 1 + i * 0.4], [0, 1], { ...clamp, easing: Easing.in(Easing.cubic) });
      const strike = w.x ? interpolate(t, [w.f + 8, w.f + 16], [0, 1], { ...clamp, easing: soft }) : 0;
      return (
        <span key={i} style={{ display: "inline-block", overflow: "hidden", verticalAlign: "top", padding: "0 0.04em 0.12em", margin: "0 0.09em" }}>
          <span
            style={{
              display: "inline-block",
              position: "relative",
              transform: `translateY(${(1 - inP) * 105 - outP * 105}%)`,
              color: w.g ? GREEN : INK,
            }}
          >
            {w.t}
            {w.x ? (
              <span
                style={{
                  position: "absolute",
                  left: "-4%",
                  top: "52%",
                  height: 9,
                  width: `${108 * strike}%`,
                  background: "#d23c3c",
                  borderRadius: 5,
                }}
              />
            ) : null}
          </span>
        </span>
      );
    })}
  </div>
);

export const ThiagoExplica: React.FC = () => {
  const t = useCurrentFrame();
  const R = ring(t);

  // The first sphere falls into the centre, then becomes token 0 of the ring.
  const drop = interpolate(t, [DROP[0], DROP[1]], [0, 1], { ...clamp, easing: Easing.in(Easing.quad) });
  const bounce = t > DROP[1] ? 46 * Math.exp(-(t - DROP[1]) / 5) * Math.abs(Math.sin((t - DROP[1]) / 3.2)) : 0;

  const tokens = Array.from({ length: N }, (_, i) => {
    const sp = interpolate(t, [SPREAD + i * 2, SPREAD + i * 2 + 26], [0, 1], { ...clamp, easing: land });
    const a = angleOf(i, R.spin);
    const x = R.x + R.r * sp * Math.cos(a);
    const y = R.y + R.r * sp * Math.sin(a) - (i === 0 ? 0 : 0);
    const g = interpolate(t, [greenAt(i), greenAt(i) + 6], [0, 1], clamp);
    const pulse = interpolate(t, [greenAt(i), greenAt(i) + 18], [0, 1], clamp);
    const visible = t >= SPREAD || i === 0;
    return { i, x, y, g, pulse, visible, a, sp };
  });

  const firstY = t < SPREAD ? interpolate(drop, [0, 1], [-200, R.y]) - bounce : R.y;
  const capTop = 170;
  const win1 = tokens[WIN1];
  const lanceTok = tokens[WIN3];

  const photoR = interpolate(t, [CTA[0] + 10, CTA[1]], [0, 300], { ...clamp, easing: land });
  const handleP = interpolate(t, [HANDLE, HANDLE + 9], [0, 1], { ...clamp, easing: land });
  const heroGlow = interpolate(t, [CASCADE[1], CASCADE[1] + 10, CTA[0]], [0, 1, 0.4], clamp);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#efeae2",
        backgroundImage:
          "radial-gradient(ellipse 80% 55% at 70% 18%, rgba(255,255,255,0.9), rgba(255,255,255,0) 60%), radial-gradient(ellipse 90% 70% at 50% 100%, rgba(120,95,60,0.18), rgba(120,95,60,0) 70%)",
        overflow: "hidden",
      }}
    >
      {/* soft green bloom behind the ring when everyone is contemplated */}
      <div
        style={{
          position: "absolute",
          left: R.x - 620,
          top: R.y - 620,
          width: 1240,
          height: 1240,
          borderRadius: "50%",
          background: `radial-gradient(circle, rgba(34,197,94,${0.22 * heroGlow}) 0%, rgba(34,197,94,0) 62%)`,
        }}
      />

      <Sweep t={t} span={SWEEP1} target={WIN1} x={R.x} y={R.y} />
      <Sweep t={t} span={SWEEP2} target={WIN2} x={R.x} y={R.y} />

      {/* coins: one per member, a wave around the ring, swallowed by the pot */}
      {tokens.map((k) => {
        const s = COIN_AT + k.i * 5;
        if (t < s || t > s + 18) return null;
        const p = interpolate(t, [s, s + 18], [0, 1], { ...clamp, easing: Easing.in(Easing.quad) });
        const d = interpolate(p, [0, 1], [R.r - 90, 120]);
        return <Coin key={k.i} x={R.x + d * Math.cos(k.a)} y={R.y + d * Math.sin(k.a)} />;
      })}
      {/* lance: extra coins pushed in by one member */}
      {t >= LANCE[0] && t < LANCE[1] + 4
        ? [0, 1, 2].map((j) => {
            const p = interpolate(t, [LANCE[0] + j * 3, LANCE[1] - 4 + j * 2], [0, 1], { ...clamp, easing: Easing.in(Easing.cubic) });
            const d = interpolate(p, [0, 1], [R.r - 100 - j * 36, 110]);
            return <Coin key={j} x={R.x + d * Math.cos(lanceTok.a)} y={R.y + d * Math.sin(lanceTok.a)} s={1.15} />;
          })
        : null}

      <Pool t={t} x={R.x} y={R.y} />

      {/* Thiago, revealed where the pot was */}
      {photoR > 0 ? (
        <div
          style={{
            position: "absolute",
            left: R.x - 300,
            top: R.y - 300,
            width: 600,
            height: 600,
            borderRadius: "50%",
            overflow: "hidden",
            clipPath: `circle(${photoR}px at 50% 50%)`,
            boxShadow: "0 40px 60px rgba(70,50,25,0.28)",
          }}
        >
          <Img
            src={staticFile("thiago3/thiago.png")}
            style={{
              position: "absolute",
              left: -244,
              top: -44,
              width: 844,
              height: 844,
              transformOrigin: "544px 330px",
              transform: `scale(${interpolate(t, [CTA[1], DURATION], [1, 1.07], clamp)})`,
            }}
          />
        </div>
      ) : null}

      {tokens.map((k) =>
        k.visible ? <Token key={k.i} x={k.i === 0 && t < SPREAD ? R.x : k.x} y={k.i === 0 && t < SPREAD ? firstY : k.y} r={R.tok} g={k.g} pulse={k.pulse} /> : null,
      )}

      <CreditCard t={t} x={R.x} y={R.y} tx={win1.x} ty={win1.y} />

      {CAPTIONS.map((c, i) => {
        const last = CAPTIONS.length - 1;
        // The CTA question (second to last) stays on top while the last line is spoken under the photo.
        const next = i >= last - 1 ? undefined : CAPTIONS[i + 1];
        if (t < c.start - 2) return null;
        if (next && t > next.start) return null;
        return <CaptionBlock key={i} c={c} end={next ? next.start : null} t={t} top={i === last ? 1440 : capTop} size={i === last ? 64 : 84} />;
      })}

      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: 1550,
          textAlign: "center",
          fontFamily: FONT,
          fontWeight: 600,
          fontSize: 50,
          letterSpacing: "-0.02em",
          color: INK,
          opacity: 0.8,
          transform: `translateY(${(1 - handleP) * 40}px)`,
          clipPath: `inset(0 0 ${(1 - handleP) * 100}% 0)`,
        }}
      >
        @thiagoidehara_invest
      </div>

      <AbsoluteFill style={{ backgroundImage: `url(${staticFile("thiago/grain0.png")})`, backgroundSize: "512px 512px", mixBlendMode: "overlay", opacity: 0.1 }} />

      <Audio src={staticFile("thiago3/mix.wav")} />
    </AbsoluteFill>
  );
};

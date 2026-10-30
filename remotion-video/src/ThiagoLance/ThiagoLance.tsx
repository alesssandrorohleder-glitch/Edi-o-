import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { Audio } from "@remotion/media";
import { loadFont } from "@remotion/fonts";
import { FONT } from "../Consorcio/fonts";
import {
  BALL,
  CARD,
  CHECK,
  DURATION,
  FEINT,
  LIFT,
  PAN_TO_E2,
  PAN_TO_E3,
  PEN_OUT,
  SLAM,
  STAMP_IN,
  WRITE_1,
  WRITE_2,
} from "./timeline";

const MONO = "IBM Plex Mono";
const HAND = "Caveat";
for (const weight of ["500", "600"]) {
  loadFont({ family: MONO, url: staticFile(`fonts/IBMPlexMono-${weight}.woff2`), weight });
}
loadFont({ family: HAND, url: staticFile("fonts/Caveat-600.woff2"), weight: "600" });

const W = 1080;
const H = 1920;
const INK = "#2b2724";
const PEN_INK = "#1d2a4a";
const STAMP_RED = "#8e1b1b";
const GREEN = "#22c55e";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const soft = Easing.bezier(0.45, 0, 0.15, 1);
const land = Easing.bezier(0.16, 1, 0.3, 1);

// ---------- world layout (world px) ----------
type Env = { x: number; y: number; w: number; h: number; rot: number; cota: string };
const E1: Env = { x: 540, y: 760, w: 860, h: 560, rot: -3, cota: "Cota 0147" };
const E2: Env = { x: 430, y: 1800, w: 860, h: 560, rot: 5, cota: "Cota 0388" };
const E3: Env = { x: 600, y: 2900, w: 900, h: 800, rot: 0, cota: "Cota 0521" };
const FILLERS: Env[] = [
  { x: 1010, y: 260, w: 820, h: 540, rot: 12, cota: "Cota 0093" },
  { x: 60, y: 120, w: 820, h: 540, rot: -8, cota: "Cota 0412" },
  { x: 40, y: 1240, w: 820, h: 540, rot: -11, cota: "Cota 0256" },
  { x: 1060, y: 1330, w: 820, h: 540, rot: 7, cota: "Cota 0731" },
  { x: 1040, y: 2280, w: 820, h: 540, rot: -6, cota: "Cota 0608" },
  { x: 20, y: 2420, w: 820, h: 540, rot: 9, cota: "Cota 0184" },
  { x: 120, y: 3520, w: 820, h: 540, rot: -5, cota: "Cota 0377" },
  { x: 1060, y: 3480, w: 820, h: 540, rot: 10, cota: "Cota 0865" },
];

const STAMP_AT = { x: 600, y: 3140 };
const STAMP_ROT = -6;
const ENV_TOP = E3.y - E3.h / 2; // the opening the card slides out of

// ---------- camera ----------
const CAM: ReadonlyArray<readonly [number, number, number, number]> = [
  [0, 560, 830, 1.3],
  [PAN_TO_E2[0], 545, 800, 1.24],
  [PAN_TO_E2[1], 440, 1830, 1.24],
  [PAN_TO_E3[0], 450, 1840, 1.22],
  [PAN_TO_E3[1], 600, 2790, 1.22],
  [PEN_OUT[0], 600, 2810, 1.22],
  [STAMP_IN[1], 600, 2930, 1.04],
  [SLAM, 600, 2960, 1.0],
  [LIFT[1], 600, 2980, 1.04],
  [CARD[0], 600, 2980, 1.1],
  [CARD[1], 600, 2160, 1.0],
  [DURATION, 600, 2140, 1.03],
];

const camera = (t: number) => {
  const f = CAM.map((k) => k[0]);
  const o = { ...clamp, easing: soft };
  return {
    x: interpolate(t, f, CAM.map((k) => k[1]), o),
    y: interpolate(t, f, CAM.map((k) => k[2]), o),
    s: interpolate(t, f, CAM.map((k) => k[3]), o),
  };
};

// ---------- pieces ----------
const Envelope: React.FC<{ readonly e: Env; readonly children?: React.ReactNode; readonly squash?: number }> = ({ e, children, squash = 1 }) => (
  <div
    style={{
      position: "absolute",
      left: e.x - e.w / 2,
      top: e.y - e.h / 2,
      width: e.w,
      height: e.h,
      transform: `rotate(${e.rot}deg) scale(${squash})`,
      borderRadius: 8,
      backgroundColor: "#c79c69",
      backgroundImage: `linear-gradient(215deg, rgba(255,235,200,0.22), rgba(255,235,200,0) 45%, rgba(40,20,5,0.18)), url(${staticFile("thiago2/kraft.png")})`,
      backgroundSize: "100% 100%, 512px 512px",
      boxShadow: "-20px 26px 34px rgba(0,0,0,0.55), inset 0 0 0 2px rgba(90,60,30,0.25)",
    }}
  >
    {children}
  </div>
);

const Label: React.FC<{ readonly cota: string; readonly h: number; readonly children?: React.ReactNode }> = ({ cota, h, children }) => (
  <div
    style={{
      position: "absolute",
      left: 50,
      top: 56,
      right: 50,
      height: h,
      backgroundColor: "#f2ede1",
      backgroundImage: `url(${staticFile("thiago/paper.png")})`,
      backgroundSize: "512px 512px",
      boxShadow: "0 2px 4px rgba(0,0,0,0.25)",
      borderRadius: 3,
    }}
  >
    <div style={{ position: "absolute", left: 36, top: 22, fontFamily: MONO, fontWeight: 500, fontSize: 34, color: INK, opacity: 0.7 }}>{cota}</div>
    {children}
  </div>
);

const Typed: React.FC<{ readonly text: string }> = ({ text }) => (
  <div
    style={{
      position: "absolute",
      left: 36,
      top: 82,
      fontFamily: MONO,
      fontWeight: 600,
      fontSize: 62,
      lineHeight: "74px",
      letterSpacing: "-0.02em",
      color: INK,
      whiteSpace: "pre",
    }}
  >
    {text}
  </div>
);

// Handwritten line revealed left to right as the pen moves over it.
const HAND_SIZE = 88;
const handWidth = (text: string) => text.length * HAND_SIZE * 0.4;
const HandLine: React.FC<{ readonly text: string; readonly x: number; readonly y: number; readonly p: number }> = ({ text, x, y, p }) => (
  <div
    style={{
      position: "absolute",
      left: x,
      top: y,
      fontFamily: HAND,
      fontWeight: 600,
      fontSize: HAND_SIZE,
      lineHeight: `${HAND_SIZE}px`,
      color: PEN_INK,
      whiteSpace: "pre",
      clipPath: `inset(-20px ${(1 - p) * 100}% -30px -10px)`,
    }}
  >
    {text}
  </div>
);

// E3 label space (label-local coords), three handwritten lines.
const LINES = [
  { text: "Outros, por lance.", x: 36, y: 80, span: WRITE_1 },
  { text: "E tem quem saiba", x: 36, y: 196, span: [WRITE_2[0], WRITE_2[0] + 25] as const },
  { text: "a hora certa.", x: 36, y: 300, span: [WRITE_2[0] + 28, WRITE_2[1]] as const },
];
const LABEL3_H = 420;
// Label-local to world (E3 is not rotated).
const l2w = (x: number, y: number) => ({ x: E3.x - E3.w / 2 + 50 + x, y: E3.y - E3.h / 2 + 56 + y });

const penTip = (t: number) => {
  // Before writing: enters from bottom right to the first line's start.
  const start = l2w(LINES[0].x, LINES[0].y + HAND_SIZE * 0.78);
  if (t < LINES[0].span[0]) {
    const p = interpolate(t, [LINES[0].span[0] - 16, LINES[0].span[0]], [0, 1], { ...clamp, easing: land });
    return { x: interpolate(p, [0, 1], [start.x + 700, start.x]), y: interpolate(p, [0, 1], [start.y + 900, start.y]) };
  }
  for (let i = 0; i < LINES.length; i++) {
    const l = LINES[i];
    const base = l2w(l.x, l.y + HAND_SIZE * 0.78);
    if (t <= l.span[1]) {
      const p = interpolate(t, [l.span[0], l.span[1]], [0, 1], clamp);
      return { x: base.x + handWidth(l.text) * p, y: base.y - 10 * Math.abs(Math.sin(t * 1.3)) };
    }
    const next = LINES[i + 1];
    if (next && t < next.span[0]) {
      const nb = l2w(next.x, next.y + HAND_SIZE * 0.78);
      const p = interpolate(t, [l.span[1], next.span[0]], [0, 1], { ...clamp, easing: soft });
      return { x: interpolate(p, [0, 1], [base.x + handWidth(l.text), nb.x]), y: interpolate(p, [0, 1], [base.y, nb.y]) };
    }
  }
  const last = LINES[LINES.length - 1];
  const end = l2w(last.x + handWidth(last.text), last.y + HAND_SIZE * 0.78);
  const p = interpolate(t, [PEN_OUT[0], PEN_OUT[1]], [0, 1], { ...clamp, easing: Easing.in(Easing.cubic) });
  return { x: end.x + 900 * p, y: end.y + 1000 * p };
};

const Pen: React.FC<{ readonly x: number; readonly y: number }> = ({ x, y }) => (
  <div style={{ position: "absolute", left: x, top: y, width: 0, height: 0, transform: "rotate(-32deg)" }}>
    {/* shadow */}
    <div style={{ position: "absolute", left: -60, top: 40, width: 44, height: 900, borderRadius: 22, background: "rgba(0,0,0,0.45)", filter: "blur(14px)" }} />
    {/* tip */}
    <div style={{ position: "absolute", left: -11, top: 0, width: 22, height: 70, clipPath: "polygon(50% 0, 100% 100%, 0 100%)", background: "linear-gradient(90deg, #8b8a88, #e9e7e2 45%, #6d6c6a)" }} />
    {/* body */}
    <div style={{ position: "absolute", left: -23, top: 66, width: 46, height: 860, borderRadius: "10px 10px 22px 22px", background: "linear-gradient(90deg, #0f1730, #33456f 40%, #15203d 75%, #0b1124)" }} />
    {/* clip */}
    <div style={{ position: "absolute", left: 14, top: 640, width: 12, height: 220, borderRadius: 6, background: "linear-gradient(90deg, #9a9893, #f1efe9, #8f8d88)" }} />
  </div>
);

const Ball: React.FC<{ readonly t: number }> = ({ t }) => {
  if (t < BALL[0]) return null;
  const p = interpolate(t, [BALL[0], BALL[1]], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const x = interpolate(p, [0, 1], [1320, 720]);
  const y = interpolate(p, [0, 1], [1660, 1960]);
  const r = 74;
  const turned = ((1320 - x) / r) * (180 / Math.PI);
  return (
    <div style={{ position: "absolute", left: x - r, top: y - r, width: 2 * r, height: 2 * r }}>
      <div style={{ position: "absolute", left: -26, top: 22, width: 2 * r, height: 2 * r, borderRadius: "50%", background: "rgba(0,0,0,0.5)", filter: "blur(12px)" }} />
      <div
        style={{
          position: "absolute",
          inset: 0,
          borderRadius: "50%",
          background: "radial-gradient(circle at 64% 30%, #ffffff 0%, #f1ede6 30%, #bdb7ad 75%, #8a847b 100%)",
          overflow: "hidden",
        }}
      >
        <div style={{ position: "absolute", inset: 0, transform: `rotate(${-turned}deg)` }}>
          <div
            style={{
              position: "absolute",
              left: r - 40,
              top: r - 40,
              width: 80,
              height: 80,
              borderRadius: "50%",
              background: "#f8f6f1",
              border: `5px solid ${STAMP_RED}`,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontFamily: FONT,
              fontWeight: 900,
              fontSize: 40,
              color: INK,
            }}
          >
            27
          </div>
        </div>
      </div>
    </div>
  );
};

// Stamp seen from above: height h (0 = on the paper) drives scale and shadow.
const stampState = (t: number) => {
  const feintPos = { x: 560, y: 1990 };
  if (t >= FEINT[0] && t < FEINT[1]) {
    const down = interpolate(t, [FEINT[0], FEINT[0] + 20], [0, 1], { ...clamp, easing: land });
    const up = interpolate(t, [FEINT[0] + 30, FEINT[1]], [0, 1], { ...clamp, easing: Easing.in(Easing.cubic) });
    return {
      x: interpolate(down, [0, 1], [180, feintPos.x]) + up * 520,
      y: interpolate(down, [0, 1], [1260, feintPos.y]) - up * 820,
      h: interpolate(down, [0, 1], [1.4, 0.55]) + up * 1.1,
      rot: 4,
      on: true,
    };
  }
  if (t >= STAMP_IN[0] && t < LIFT[1]) {
    const arrive = interpolate(t, [STAMP_IN[0], STAMP_IN[1]], [0, 1], { ...clamp, easing: land });
    const creep = interpolate(t, [STAMP_IN[1], SLAM - 4], [0, 1], { ...clamp, easing: soft });
    const drop = interpolate(t, [SLAM - 4, SLAM], [0, 1], { ...clamp, easing: Easing.in(Easing.quad) });
    const lift = interpolate(t, [LIFT[0], LIFT[1]], [0, 1], { ...clamp, easing: Easing.in(Easing.cubic) });
    const hHover = interpolate(arrive, [0, 1], [1.6, 0.95]) - 0.25 * creep;
    return {
      x: interpolate(arrive, [0, 1], [1150, STAMP_AT.x]) + lift * 520,
      y: interpolate(arrive, [0, 1], [2300, STAMP_AT.y]) - lift * 900,
      h: hHover * (1 - drop) + lift * 1.8,
      rot: STAMP_ROT,
      on: true,
    };
  }
  return { x: 0, y: 0, h: 0, rot: 0, on: false };
};

const Stamp: React.FC<{ readonly t: number }> = ({ t }) => {
  const st = stampState(t);
  if (!st.on) return null;
  const pressed = t >= SLAM && t < LIFT[0] ? interpolate(t, [SLAM, SLAM + 3, SLAM + 10], [0.97, 0.985, 1], clamp) : 1;
  const sc = (1 + 0.38 * st.h) * pressed;
  return (
    <>
      <div
        style={{
          position: "absolute",
          left: st.x - 330 - (14 + 120 * st.h),
          top: st.y - 120 + (16 + 150 * st.h),
          width: 660,
          height: 240,
          borderRadius: 24,
          background: `rgba(0,0,0,${0.6 - 0.22 * Math.min(st.h, 1.5)})`,
          filter: `blur(${8 + 40 * st.h}px)`,
          transform: `rotate(${st.rot}deg) scale(${1 + 0.15 * st.h})`,
        }}
      />
      <div style={{ position: "absolute", left: st.x, top: st.y, transform: `rotate(${st.rot}deg) scale(${sc})` }}>
        {/* base block */}
        <div
          style={{
            position: "absolute",
            left: -330,
            top: -120,
            width: 660,
            height: 240,
            borderRadius: 22,
            background: "linear-gradient(200deg, #8a5a33 0%, #6b4426 45%, #4a2d17 100%)",
            boxShadow: "inset 0 3px 0 rgba(255,220,180,0.35), inset 0 -6px 0 rgba(0,0,0,0.35)",
          }}
        />
        {/* knob */}
        <div
          style={{
            position: "absolute",
            left: -120,
            top: -120,
            width: 240,
            height: 240,
            borderRadius: "50%",
            background: "radial-gradient(circle at 62% 32%, #d9a874 0%, #a8713f 35%, #6e4422 75%, #4b2c15 100%)",
            boxShadow: "-10px 14px 24px rgba(0,0,0,0.45)",
          }}
        />
      </div>
    </>
  );
};

const StampMark: React.FC<{ readonly t: number }> = ({ t }) => {
  if (t < SLAM) return null;
  const wet = interpolate(t, [LIFT[0], LIFT[0] + 90], [0.45, 0], clamp);
  return (
    <div
      style={{
        position: "absolute",
        left: STAMP_AT.x - 340,
        top: STAMP_AT.y - 95,
        width: 680,
        height: 190,
        transform: `rotate(${STAMP_ROT}deg)`,
        WebkitMaskImage: `url(${staticFile("thiago2/inkmask.png")})`,
        WebkitMaskSize: "300px 300px",
        mixBlendMode: "multiply",
      }}
    >
      <div
        style={{
          position: "absolute",
          inset: 0,
          border: `9px solid ${STAMP_RED}`,
          borderRadius: 16,
          outline: `3px solid ${STAMP_RED}`,
          outlineOffset: -24,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontFamily: FONT,
          fontWeight: 900,
          fontSize: 76,
          letterSpacing: "0.03em",
          color: STAMP_RED,
        }}
      >
        CONTEMPLADA
      </div>
      <div style={{ position: "absolute", inset: 0, background: `linear-gradient(200deg, rgba(255,255,255,${wet}), rgba(255,255,255,0) 60%)`, mixBlendMode: "screen" }} />
    </div>
  );
};

const CARD_W = 780;
const CARD_H = 1340;
const Card: React.FC<{ readonly t: number }> = ({ t }) => {
  if (t < CARD[0]) return null;
  const p = interpolate(t, [CARD[0], CARD[1]], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const top = ENV_TOP - p * (CARD_H - 60);
  const check = interpolate(t, [CHECK[0], CHECK[1]], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const line: React.CSSProperties = { position: "absolute", left: 50, fontFamily: MONO, fontWeight: 600, fontSize: 58, lineHeight: "70px", letterSpacing: "-0.02em", color: INK, whiteSpace: "pre" };
  return (
    // Only the part above the envelope's opening is visible.
    <div style={{ position: "absolute", left: E3.x - 700, top: ENV_TOP - 3000, width: 1400, height: 3000, overflow: "hidden" }}>
      <div
        style={{
          position: "absolute",
          left: 700 - CARD_W / 2,
          top: top - (ENV_TOP - 3000),
          width: CARD_W,
          height: CARD_H,
          backgroundColor: "#f4efe4",
          backgroundImage: `url(${staticFile("thiago/paper.png")})`,
          backgroundSize: "512px 512px",
          borderRadius: 10,
          boxShadow: "-18px 22px 30px rgba(0,0,0,0.45)",
        }}
      >
        <div style={{ ...line, top: 56 }}>Qual é a sua hora?</div>
        <Img
          src={staticFile("thiago2/thiago.png")}
          style={{ position: "absolute", left: 50, top: 160, width: CARD_W - 100, height: CARD_W - 100, borderRadius: 4, outline: `3px solid ${INK}`, outlineOffset: 8 }}
        />
        <div style={{ ...line, top: 880 }}>{"Eu te mostro\nnuma call."}</div>
        <div style={{ ...line, top: 1040 }}>Me chama no direct.</div>
        <div style={{ ...line, top: 1150, fontFamily: FONT, fontWeight: 800, fontSize: 52 }}>
          @thiagoidehara_invest
          <svg width={56} height={56} viewBox="0 0 24 24" style={{ display: "inline-block", verticalAlign: "-0.15em", marginLeft: 12 }}>
            <path d="M4 12.5l5 5L20 6.5" fill="none" stroke={GREEN} strokeWidth={2.6} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - check} />
          </svg>
        </div>
      </div>
    </div>
  );
};

export const ThiagoLance: React.FC = () => {
  const t = useCurrentFrame();
  const cam = camera(t);
  const shake = t >= SLAM ? 20 * Math.exp(-(t - SLAM) / 3.2) * Math.sin((t - SLAM) * 2.6) : 0;
  const shakeX = t >= SLAM ? 9 * Math.exp(-(t - SLAM) / 3.2) * Math.sin((t - SLAM) * 3.4) : 0;
  const tx = W / 2 - cam.x * cam.s + shakeX;
  const ty = H / 2 - cam.y * cam.s + shake;
  const squash = t >= SLAM ? interpolate(t, [SLAM, SLAM + 2, SLAM + 9], [0.986, 0.992, 1], clamp) : 1;
  const tip = penTip(t);
  const penOn = t >= LINES[0].span[0] - 16 && t < PEN_OUT[1];
  const breathe = 1 + 0.04 * Math.sin(t / 22);

  return (
    <AbsoluteFill style={{ backgroundColor: "#0d0907", overflow: "hidden" }}>
      <div style={{ position: "absolute", left: 0, top: 0, transformOrigin: "0 0", transform: `translate(${tx}px, ${ty}px) scale(${cam.s})` }}>
        <Img src={staticFile("thiago/desk.jpg")} style={{ position: "absolute", left: -1000, top: -800, width: 3100, height: 4500, filter: "blur(1.5px)" }} />

        {FILLERS.map((e) => (
          <Envelope key={e.cota} e={e}>
            <Label cota={e.cota} h={200} />
          </Envelope>
        ))}
        <Envelope e={E1}>
          <Label cota={E1.cota} h={260}>
            <Typed text={"Todo mês, alguém\né contemplado."} />
          </Label>
        </Envelope>
        <Envelope e={E2}>
          <Label cota={E2.cota} h={260}>
            <Typed text={"Uns, por\nsorteio."} />
          </Label>
        </Envelope>
        <Ball t={t} />

        <Card t={t} />
        <Envelope e={E3} squash={squash}>
          <Label cota={E3.cota} h={LABEL3_H}>
            {LINES.map((l) => (
              <HandLine key={l.text} text={l.text} x={l.x} y={l.y} p={interpolate(t, [l.span[0], l.span[1]], [0, 1], clamp)} />
            ))}
          </Label>
        </Envelope>
        <StampMark t={t} />

        {penOn ? <Pen x={tip.x} y={tip.y} /> : null}
        <Stamp t={t} />
      </div>

      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse 90% 60% at 82% 8%, rgba(255,182,112,${0.2 * breathe}), rgba(255,182,112,0) 70%)`,
          mixBlendMode: "screen",
        }}
      />
      <AbsoluteFill style={{ background: "radial-gradient(ellipse 85% 75% at 60% 42%, rgba(0,0,0,0) 38%, rgba(0,0,0,0.6) 100%)" }} />
      <AbsoluteFill style={{ backgroundImage: `url(${staticFile("thiago/grain0.png")})`, backgroundSize: "512px 512px", mixBlendMode: "overlay", opacity: 0.16 }} />

      <Audio src={staticFile("thiago2/mix.wav")} />
    </AbsoluteFill>
  );
};

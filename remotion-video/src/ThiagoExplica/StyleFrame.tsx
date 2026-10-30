import { AbsoluteFill, Img, staticFile } from "remotion";
import { FONT } from "../Consorcio/fonts";

// Style frames for the 40 s explainer: three static moments in the film's look.
const W = 1080;
const INK = "#13201a";
const GREEN = "#22c55e";
const RING = { x: 540, y: 1180, r: 390 };
const N = 12;

const ground: React.CSSProperties = {
  backgroundColor: "#efeae2",
  backgroundImage:
    "radial-gradient(ellipse 80% 55% at 70% 18%, rgba(255,255,255,0.9), rgba(255,255,255,0) 60%), radial-gradient(ellipse 90% 70% at 50% 100%, rgba(120,95,60,0.18), rgba(120,95,60,0) 70%)",
};

const Token: React.FC<{ readonly x: number; readonly y: number; readonly r?: number; readonly green?: boolean; readonly glow?: boolean }> = ({ x, y, r = 64, green, glow }) => (
  <div
    style={{
      position: "absolute",
      left: x - r,
      top: y - r,
      width: 2 * r,
      height: 2 * r,
      borderRadius: "50%",
      background: green
        ? "radial-gradient(circle at 34% 28%, #c9f7da 0%, #4ade80 30%, #16a34a 75%, #0f6b33 100%)"
        : "radial-gradient(circle at 34% 28%, #ffffff 0%, #f1ece4 32%, #d6cdbf 80%, #bfb4a4 100%)",
      boxShadow: `0 ${r * 0.55}px ${r * 0.8}px rgba(70,50,25,0.22)${glow ? `, 0 0 ${r * 1.6}px rgba(34,197,94,0.55)` : ""}`,
    }}
  />
);

const Coin: React.FC<{ readonly x: number; readonly y: number; readonly a: number }> = ({ x, y, a }) => (
  <>
    <div
      style={{
        position: "absolute",
        left: x - 70 * Math.cos(a),
        top: y - 70 * Math.sin(a) - 3,
        width: 70,
        height: 6,
        borderRadius: 3,
        transformOrigin: "0 50%",
        transform: `rotate(${(a * 180) / Math.PI}deg)`,
        background: "linear-gradient(90deg, rgba(19,32,26,0), rgba(19,32,26,0.28))",
      }}
    />
    <div
      style={{
        position: "absolute",
        left: x - 15,
        top: y - 15,
        width: 30,
        height: 30,
        borderRadius: "50%",
        background: "radial-gradient(circle at 35% 30%, #4b5d53, #13201a 70%)",
        boxShadow: "0 8px 10px rgba(0,0,0,0.2)",
      }}
    />
  </>
);

const Pool: React.FC<{ readonly level: number }> = ({ level }) => (
  <div
    style={{
      position: "absolute",
      left: RING.x - 180,
      top: RING.y - 180,
      width: 360,
      height: 360,
      borderRadius: "50%",
      overflow: "hidden",
      background: "radial-gradient(circle at 50% 35%, #fbf8f3, #e4ddd2)",
      boxShadow: "inset 0 14px 30px rgba(70,50,25,0.25), 0 30px 50px rgba(70,50,25,0.18)",
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

const Title: React.FC<{ readonly children: React.ReactNode; readonly top?: number; readonly size?: number }> = ({ children, top = 250, size = 92 }) => (
  <div
    style={{
      position: "absolute",
      left: 70,
      right: 70,
      top,
      textAlign: "center",
      fontFamily: FONT,
      fontWeight: 800,
      fontSize: size,
      lineHeight: 1.04,
      letterSpacing: "-0.045em",
      color: INK,
      whiteSpace: "pre-line",
    }}
  >
    {children}
  </div>
);

const ringPos = (i: number, r = RING.r) => {
  const a = -Math.PI / 2 + (i / N) * 2 * Math.PI;
  return { x: RING.x + r * Math.cos(a), y: RING.y + r * Math.sin(a), a };
};

const Grain = () => (
  <AbsoluteFill style={{ backgroundImage: `url(${staticFile("thiago/grain0.png")})`, backgroundSize: "512px 512px", mixBlendMode: "overlay", opacity: 0.1 }} />
);

export const StyleFrame: React.FC<{ readonly kind: 1 | 2 | 3 }> = ({ kind }) => {
  if (kind === 1) {
    return (
      <AbsoluteFill style={ground}>
        <Title>
          Todo mês, cada um{"\n"}paga uma <span style={{ color: GREEN }}>parcela</span>.
        </Title>
        <Pool level={0.42} />
        {Array.from({ length: N }, (_, i) => {
          const p = ringPos(i);
          const c = ringPos(i, RING.r * (0.52 + 0.1 * ((i * 7) % 3)));
          return (
            <div key={i}>
              <Token x={p.x} y={p.y} />
              <Coin x={c.x} y={c.y} a={p.a + Math.PI} />
            </div>
          );
        })}
        <Grain />
      </AbsoluteFill>
    );
  }
  if (kind === 2) {
    const win = 4;
    const p = ringPos(win);
    return (
      <AbsoluteFill style={ground}>
        <Title>
          Todo mês, alguém{"\n"}recebe a <span style={{ color: GREEN }}>carta</span>{"\n"}de crédito.
        </Title>
        {/* light sweep */}
        <div
          style={{
            position: "absolute",
            left: RING.x - 470,
            top: RING.y - 470,
            width: 940,
            height: 940,
            borderRadius: "50%",
            background: `conic-gradient(from ${((p.a + Math.PI / 2) * 180) / Math.PI - 40}deg, rgba(34,197,94,0) 0deg, rgba(34,197,94,0.22) 36deg, rgba(34,197,94,0) 44deg)`,
          }}
        />
        <Pool level={0.7} />
        {Array.from({ length: N }, (_, i) => {
          const q = ringPos(i);
          return <Token key={i} x={q.x} y={q.y} green={i === win} glow={i === win} />;
        })}
        {/* the credit letter on its way to the winner */}
        <div
          style={{
            position: "absolute",
            left: (RING.x + p.x) / 2 + 40 - 110,
            top: (RING.y + p.y) / 2 - 70,
            width: 220,
            height: 140,
            borderRadius: 14,
            transform: "rotate(-14deg)",
            background: "linear-gradient(160deg, #ffffff, #f2eee7)",
            boxShadow: "0 26px 40px rgba(70,50,25,0.25)",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            padding: "0 22px",
            fontFamily: FONT,
            color: INK,
          }}
        >
          <div style={{ fontWeight: 500, fontSize: 22, opacity: 0.6 }}>Carta de crédito</div>
          <div style={{ marginTop: 10, height: 10, width: 120, borderRadius: 5, background: GREEN }} />
        </div>
        <Grain />
      </AbsoluteFill>
    );
  }
  return (
    <AbsoluteFill style={ground}>
      <Title top={200} size={84}>
        Qual é a melhor{"\n"}estratégia pra <span style={{ color: GREEN }}>você</span>?
      </Title>
      {Array.from({ length: N }, (_, i) => {
        const q = ringPos(i, 300);
        return <Token key={i} x={q.x} y={q.y - 40} r={30} green />;
      })}
      <div
        style={{
          position: "absolute",
          left: RING.x - 250,
          top: RING.y - 40 - 250,
          width: 500,
          height: 500,
          borderRadius: "50%",
          overflow: "hidden",
          boxShadow: "0 40px 60px rgba(70,50,25,0.28), 0 0 0 10px #f7f3ec",
        }}
      >
        <Img src={staticFile("thiago2/thiago.png")} style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: "72% 20%", transform: "scale(1.5)", transformOrigin: "72% 25%" }} />
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 1600, textAlign: "center", fontFamily: FONT, color: INK }}>
        <div style={{ fontWeight: 800, fontSize: 60, letterSpacing: "-0.03em" }}>Me chama no direct.</div>
        <div style={{ marginTop: 18, fontWeight: 500, fontSize: 44, opacity: 0.75 }}>@thiagoidehara_invest</div>
      </div>
      <Grain />
    </AbsoluteFill>
  );
};

export const STYLE_W = W;

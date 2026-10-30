// Every printed line on the tape. `at` is the frame the printer starts feeding it;
// the same numbers drive the sound (scripts/thiago_sound.py reads timeline.json, written by dump-timeline).

export type Kind = "blank" | "item" | "big" | "stream" | "rule" | "total" | "photo" | "handle";

export type Line = {
  readonly kind: Kind;
  readonly at: number;
  readonly h: number;
  readonly dur: number;
  readonly text?: string;
  readonly check?: boolean;
};

export const FPS = 30;
export const DURATION = 750;

export const TEAR = 486;
export const QUESTION = 424;
export const STREAM_START = 280;
export const STREAM_END = 398;

const big = (at: number, text: string): Line => ({
  kind: "big",
  at,
  text,
  h: text.split("\n").length * 74 + 46,
  dur: 10,
});
const item = (at: number, text: string, check = false): Line => ({ kind: "item", at, text, h: 76, dur: 7, check });
const blank = (at: number, h: number): Line => ({ kind: "blank", at, h, dur: 8 });

// 60 monthly lines, accelerating: the gap between lines shrinks as the tape runs.
const stream: Line[] = Array.from({ length: 60 }, (_, i) => {
  const at = Math.round(STREAM_START + (STREAM_END - STREAM_START) * Math.sqrt(i / 59));
  const next = Math.round(STREAM_START + (STREAM_END - STREAM_START) * Math.sqrt(Math.min(i + 1, 59) / 59));
  return {
    kind: "stream" as const,
    at,
    h: 60,
    dur: Math.max(1, Math.min(6, next - at)),
    text: `mês ${String(i + 1).padStart(2, "0")}   parcela + juros`,
  };
});

// Segment A: everything printed before the tear.
export const SEGMENT_A: Line[] = [
  item(6, "Parcela ...... cabe no bolso", true),
  blank(30, 34),
  big(38, "Todo mundo faz a\nconta da parcela."),
  blank(100, 56),
  big(108, "Quase ninguém faz a\nconta inteira."),
  blank(160, 30),
  item(168, "× 60 meses"),
  item(186, "+ juros"),
  item(204, "+ juros sobre juros"),
  item(222, "+ IOF"),
  item(240, "+ seguro"),
  item(258, "+ tarifa de cadastro"),
  blank(272, 30),
  ...stream,
  { kind: "rule", at: 400, h: 44, dur: 3 },
  { kind: "total", at: 403, h: 270, dur: 10, text: "Total ......" },
];

// Segment B: the clean tape after the tear.
export const SEGMENT_B: Line[] = [
  blank(488, 60),
  big(510, "Existe outra conta."),
  big(540, "Ela fecha diferente."),
  blank(568, 40),
  big(576, "Eu faço essa conta\ncom você."),
  // Thiago's portrait, printed like any other line: it emerges from the slot row by row.
  { kind: "photo", at: 598, h: 560, dur: 34 },
  big(644, "Me chama no direct."),
  blank(672, 20),
  { kind: "handle", at: 680, h: 130, dur: 10, text: "@thiagoidehara_invest" },
  blank(696, 70),
];

// Paper already out of the printer when the film starts.
export const LEAD = 900;

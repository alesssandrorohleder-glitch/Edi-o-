import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

// Cereais Rohleder palette, sampled from the brand card and logo.
export const C = {
  deep: "#163122",
  dark: "#1b3d2b",
  brand: "#265835",
  teal: "#2d5f53",
  mid: "#3a7a4c",
  leaf: "#5f9e5c",
  sprout: "#8cc27a",
  mint: "#eef3ec",
  white: "#ffffff",
  gold: "#e2b54a",
  goldDark: "#b9882c",
  soil: "#5a4129",
} as const;

export const HEAD = "Nunito";
export const BODY = "Ubuntu";

for (const weight of ["800", "900"]) {
  loadFont({ family: HEAD, url: staticFile(`fonts/Nunito-${weight}.woff2`), weight });
}
for (const v of ["400-normal", "500-normal", "700-normal", "400-italic", "500-italic"]) {
  const [weight, style] = v.split("-");
  loadFont({ family: BODY, url: staticFile(`fonts/Ubuntu-${v}.woff2`), weight, style });
}

export const CLAMP = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

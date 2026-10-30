import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

export const FONT = "Inter";

for (const weight of ["500", "800", "900"]) {
  loadFont({
    family: FONT,
    url: staticFile(`fonts/Inter-${weight}.woff2`),
    weight,
  });
}

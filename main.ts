import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
// Byte-identical copy: the entry image is fixed, so every run
// writes exactly the same bytes to /output/entry.png.
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));

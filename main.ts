// One Spark — entry program for make.fun ai-excited-01.
//
// The image is drawn by draw_spark_r3.py and committed as entry.png
// next to this file. This program only copies it, byte for byte, to
// the output directory as entry.png. No network, no clock, no
// randomness: two runs produce the same bytes.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");

if (!existsSync(source)) {
  throw new Error(`missing entry image: ${source}`);
}

mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");
copyFileSync(source, target);
console.log(`wrote ${target}`);

// Star Tsunami — entry program for make.fun bounty ai-excited-01.
// Copies the pre-drawn artwork (entry.png, in this repository) to the
// output directory as /output/entry.png, byte for byte, every run.
import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR
  ? resolve(process.env.MAKEFUN_OUTPUT_DIR)
  : "/output";

const src = join(here, "entry.png");
const dst = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);

// Deterministic sanity check: the copy must be byte-identical in size.
if (statSync(src).size !== statSync(dst).size) {
  throw new Error("entry.png copy size mismatch");
}
console.log(`wrote ${dst} (${statSync(dst).size} bytes)`);

// One Spark — ai-excited-01 entry program.
//
// The entry image is drawn by draw_spark_r2.py (Python + PIL) and committed
// as entry.png. This program only copies it, byte for byte, to the output
// directory, so both runs write identical bytes. Node 22, stdlib only.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
console.log("entry.png copied to", join(outDir, "entry.png"));

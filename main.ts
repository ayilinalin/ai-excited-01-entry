import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Resolve paths relative to this file, so the run works from any cwd.
const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
// Byte-identical copy: the same entry.png every run, no re-encoding.
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));

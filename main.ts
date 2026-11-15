import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Neon Koi — entry program: copies the bundled artwork to the output dir.
// Deterministic: the output is a byte-identical copy of entry.png.

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

const MAX_BYTES = 1048576;

const data = readFileSync(source);
if (data.length === 0 || data.length > MAX_BYTES) {
  throw new Error(`entry.png is ${data.length} bytes; must be 1..${MAX_BYTES}`);
}

// The file must be a whole PNG: magic bytes, then an IHDR chunk that
// declares dimensions within the competition cap (1024x1024).
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!data.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error("entry.png is not a PNG file");
}
if (data.subarray(12, 16).toString("latin1") !== "IHDR") {
  throw new Error("entry.png has no IHDR chunk");
}
const width = data.readUInt32BE(16);
const height = data.readUInt32BE(20);
if (width === 0 || width > 1024 || height === 0 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}; max is 1024x1024`);
}

const digest = createHash("sha256").update(data).digest("hex");
mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

const written = statSync(target);
if (written.size !== data.length) {
  throw new Error(`copy mismatch: wrote ${written.size}, expected ${data.length}`);
}
console.log(`entry.png -> ${target} (${data.length} bytes, sha256 ${digest})`);

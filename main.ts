// News Image 26 Nov 2026 — entry program.
// Copies the pre-drawn front page (entry.png, built by draw_frontpage.py)
// to the output directory the grader reads. No network, no dependencies.
import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const dst = join(outDir, "entry.png");

if (!existsSync(src)) {
  console.error(`missing ${src}`);
  process.exit(1);
}
const bytes = statSync(src).size;
if (bytes > 1048576) {
  console.error(`entry.png is ${bytes} bytes, over the 1 MiB gate`);
  process.exit(1);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);
console.log(`wrote ${dst}`);

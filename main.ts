// News Image 26 Nov 2026 — entry program (Node 22, standard library only).
// Copies the front page (entry.png, drawn by draw_frontpage.py and kept in
// this repository) to /output/entry.png and verifies the copy byte for
// byte, so a truncated write fails instead of handing in a broken image.
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = fileURLToPath(new URL('.', import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const png = readFileSync(join(here, 'entry.png'));

// The gate takes a whole PNG or JPEG of at most 1 MiB (1048576 bytes):
// check the PNG signature and the size before writing anything.
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!png.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error('entry.png does not start with the PNG signature');
}
if (png.length > 1048576) {
  throw new Error(`entry.png is ${png.length} bytes, over the 1 MiB cap`);
}

mkdirSync(outDir, { recursive: true });
const target = join(outDir, 'entry.png');
writeFileSync(target, png);

// Truncation guard: read the output back and require the exact same bytes,
// so a short write can never slip through as a valid entry. The IEND check
// additionally proves the PNG is whole — every PNG ends with an IEND chunk,
// so a file cut mid-write is caught even before the byte comparison.
const written = readFileSync(target);
if (!written.equals(png)) {
  throw new Error(
    `output entry.png (${written.length} bytes) differs from the source (${png.length} bytes)`,
  );
}
if (!written.subarray(-12).includes(Buffer.from('IEND'))) {
  throw new Error('output entry.png has no IEND chunk: the PNG is not whole');
}

console.log(`wrote ${target} (${written.length} bytes, verified)`);

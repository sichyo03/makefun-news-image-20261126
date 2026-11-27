# News Image — Thursday 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/sichyo03/makefun-news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/sichyo03/makefun-news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

Entry for the make.fun bounty [Sum up 26 November's world news in one image](https://make.fun/bounty/news-image-20261126):
one 1024×1024 broadsheet front page summing up Thursday 26 November 2026 —
48 stories across 9 regions, every one first reported that day, each with a
named source and a "how sure" badge (OFFICIAL / CONFIRMED / REPORTED /
CLAIM / ONGOING), plus a DATE CHECK footer listing the near-miss stories
from earlier days that were deliberately left out.

## How it works

- `draw_frontpage.py` draws the page with PIL (vector-style scenes, no
  photos, no network) and writes `entry.png`.
- `main.ts` (Node 22, standard library only) copies `entry.png` to the
  output directory (`MAKEFUN_OUTPUT_DIR`, default `/output`).

Run locally:

```sh
python3 draw_frontpage.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Licence

MIT — see LICENSE.

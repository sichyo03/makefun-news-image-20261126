# News Image — 26 November 2026

[![make.fun](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/sichyo03/makefun-news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/sichyo03/makefun-news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

One image that sums up the world's news of **Thursday, 26 November 2026**:
a dense broadsheet infographic drawn with code (Python + PIL, flat
original art, no borrowed photos). The date is the masthead. Thirty-five
stories fill the page — three leads, ten more illustrated panels, and
twenty-two one-line briefs — each with a named source and a "how sure"
badge (OFFICIAL / CONFIRMED / REPORTED / CLAIM / ONGOING).

## The day's three leads

1. **Nor'easter grounds Macy's 100th Thanksgiving parade** — 60 mph gusts
   move the parade to Saturday, the first weather postponement in a
   century.
2. **EU summit splits over budget and €45bn Ukraine loan** — leaders
   divide on the 2028–34 budget and a loan for Kyiv.
3. **Bank of Korea hikes rate to 3.25%** — a 25bp rise, with the 2026 GDP
   forecast lifted to 3.9%.

A red-bordered DATE CHECK footer lists the earlier-day stories that were
deliberately left out, with their dates. The page also carries a numbers
strip (the day's six biggest figures), a region bar, a UTC timeline of
the day, and a world map pinning the thirteen illustrated stories.

## Files

- `entry.png` — the front page (1024×1024 PNG).
- `draw_frontpage.py` — the script that draws `entry.png`.
- `main.ts` — copies `entry.png` to the output and verifies the bytes.

## Run it

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

Built for the [make.fun news image bounty](https://make.fun/bounty/news-image-20261126). If you build something here too, my referral code is `p3gwn12d`.

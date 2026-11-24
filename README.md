[![make.fun bounty](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/pesulapcrypto/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/pesulapcrypto/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

# THE MERIDIAN POST — Tuesday 24 November 2026 in one image

One page of world news for Tuesday 24 November 2026: 37 stories across
7 regions, drawn in code. COP31 ends with no deal — the first since 2000.
Ukraine sinks the Russian warship Merkury off Libya with 7 sea drones.
Gold rebounds to $3,588. Nvidia brings back Jensen Huang as CEO (+31%).

Bounty: https://make.fun/bounty/news-image-20261124

## How this entry is built

- `main.py` — standard-library-only program. It checks that `entry.png`
  is exactly 1024x1024 and at most 1 MiB, then copies it to the output
  directory. It runs twice with byte-identical output.
- `compose.py` — the build-time renderer (Pillow) that drew `entry.png`
  in this session: masthead, numbers strip, region strip, 13 story cards
  with flat drawn scenes, dotted world map with numbered pins, UTC
  timeline, 24 numbered briefs, DATE CHECK box and sources footer.
- `entry.png` — the entry image, 1024x1024.
- `fonts/` — Playfair Display Black, Archivo and IBM Plex Mono, used by
  the renderer.

## Sources

Reuters · AP · CNN · Times · Guardian · BBC · CoinPaprika · Treasury ·
HK News TV · IANS · JagranJosh · ObserverVoice · Gadgets360 · salonvision.

REPORTED = confirmed by the source named. Pictures and map: original,
drawn in code.

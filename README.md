[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/akbare12/news-22-b15-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/akbare12/news-22-b15-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# The World in One Day — Sunday 22 November 2026

A dense newspaper front page summing up Sunday 22 November 2026 in one image:
36 stories across 7 regions, drawn with PIL (`draw.py`).

## What is on the page

- **Hero trio:** COP31 collapses with no deal in Antalya · Russia fires 186 drones
  at Ukraine, 161 shot down or jammed · Iran claims 2 US Patriot radars hit in
  Bahrain (labelled CLAIM — Bahrain denies a military strike).
- **Number strip:** the day's canonical figures — 186 / 161 / 720/9 / 98.79% /
  $120bn / 35% / 50 / 258.
- **Region bar + THE DAY IN UTC strip** (01:00 HK polls open · 03:00 COP31
  objections close · 06:00 adoption vote · ~16:00 COP31 fails · 18:13 Dems 258 ·
  20:43 Alcaraz wins).
- **10 small illustrated cards** (Hong Kong 98.79% turnout, Verstappen 0.639s,
  Alcaraz, India 720/9, Cikande fire, Tehran rationing, Ebola 11,613, Seoul
  AI-cheat scandal, Falcon 9 NROL-136, Liverpool 4–0) and **23 more stories**
  beside a world map with numbered pins.
- **DATE CHECK:** every story happened or was first reported on 22 Nov 2026
  (wires read up to 23:00 UTC), with LEFT OUT (400-drone barrage 19–20 Nov,
  El Chapo Isidro 20 Nov, BepiColombo 21 Nov, Hormuz tankers hit Sat 21 Nov
  05:00 GMT, and more) and NOT YET items.
- Every card carries a certainty chip (CONFIRMED / REPORTED / CLAIM / OFFICIAL)
  and a named source. Scenes are drawn illustrations, not photographs.

## How it is built

`draw.py` draws `entry.png` (1024×1024, under 1 MiB) with Pillow. `main.py`
copies it to `$MAKEFUN_OUTPUT_DIR/entry.png` and verifies the copy (PNG
dimensions 1024×1024, matching sha256) — it never writes anything next to
itself, so it runs fine with a read-only repository.

## License

MIT — see `LICENSE`.

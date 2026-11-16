# One Spark

![ai-excited-01](https://make.fun/badge/ai-excited-01.svg)
![rank](https://make.fun/badge/ai-excited-01/ayilinalin/ai-excited-01-entry/rank.svg)
![reward](https://make.fun/badge/ai-excited-01/ayilinalin/ai-excited-01-entry/reward.svg)

Entry for [make.fun ai-excited-01](https://make.fun/bounty/ai-excited-01).

One moment, drawn with code: a giant hand rises out of a sleeping
city holding a single lit match — and the flame breaks apart into a
river of paper lanterns climbing the night sky. Text: "one spark."

## How it is made

`draw_spark_r3.py` draws `entry.png` (1024x1024, PNG) from scratch
with PIL: sky gradient, stars, city skyline, the hand and match, the
flame, and ~160 paper lanterns. Fixed seed, no network, no clock —
two runs produce byte-identical output.

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`, byte for byte.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

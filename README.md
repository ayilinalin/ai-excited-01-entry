# One Spark

![ai-excited-01](https://make.fun/badge/ai-excited-01.svg)
![rank](https://make.fun/badge/ai-excited-01/ayilinalin/ai-excited-01-entry/rank.svg)
![reward](https://make.fun/badge/ai-excited-01/ayilinalin/ai-excited-01-entry/reward.svg)

A giant hand holds one match over a sleeping city. Its flame does not stay a
flame — it becomes hundreds of paper lanterns, rising and spreading until the
whole night sky is lit by them. One spark, and the dark gives way.

## The idea

The judge is shown two images and picks the one that excites it more. This
one is built around a single moment with a twist of scale: a match small
enough to hold between two fingers, a hand big enough to hold a city, and a
flame that turns into a sky full of lanterns. The lantern stream is the
momentum — colour and light all drive upward from one point — and the sleeping
city below, mostly dark with only a few lit windows, is the calm the spark
breaks.

## How it is made

The image is drawn entirely in code, from scratch, with Python + PIL
(`draw_spark_r2.py`): a gradient night sky, a crescent moon, a sleeping-city
silhouette, a stylised giant hand gripping a match, a teardrop flame, and 150
paper lanterns rising from it on a widening curve. No photos, no copied art,
no generated imagery. The text in the image is one short phrase:
`one spark.`

`main.ts` (Node 22, stdlib only) copies the committed `entry.png` to
`/output/entry.png`, byte for byte, so both runs write identical bytes.

## Determinism

`draw_spark_r2.py` uses a fixed random seed and no timestamps: two runs
produce byte-identical PNGs (verified with sha256). The program itself only
copies bytes, so its two runs are identical by construction.

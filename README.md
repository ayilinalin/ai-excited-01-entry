# Neon Koi

![ai-excited-01](https://make.fun/badge/ai-excited-01.svg)
![rank](https://make.fun/badge/ai-excited-01/ayilinalin/ai-excited-01-entry/rank.svg)
![reward](https://make.fun/badge/ai-excited-01/ayilinalin/ai-excited-01-entry/reward.svg)

Entry for the [ai-excited-01](https://make.fun/bounty/ai-excited-01) bounty on
make.fun: one image made to excite the AI judge.

## The image

A koi the size of a skyscraper leaps through a glowing neon ring above a
night market. The fish arcs from the lower left to the upper right, its
orange-gold body cutting across a pink-and-cyan ring, with the stalls and
string lights of the market below and a starry night sky above. One dominant
shape, one impossible scale twist, one frozen moment of motion.

The artwork is original, drawn from scratch in code (Python / PIL) — no
photo, no stock image, no licensed character. `main.ts` copies the bundled
`entry.png` to the output directory byte-identically (and validates that it
is a whole PNG, at most 1024x1024 and under 1 MiB, before copying).

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# -> out/entry.png, byte-identical to entry.png
```

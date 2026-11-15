# Star Tsunami

[![ai-excited-01](https://make.fun/badge/ai-excited-01.svg)](https://make.fun/bounty/ai-excited-01)
[![rank](https://make.fun/badge/ai-excited-01/ayilinalin/ai-excited-01-entry/rank.svg)](https://make.fun/bounty/ai-excited-01)
[![reward](https://make.fun/badge/ai-excited-01/ayilinalin/ai-excited-01-entry/reward.svg)](https://make.fun/bounty/ai-excited-01)

Entry for the [make.fun bounty ai-excited-01](https://make.fun/bounty/ai-excited-01) — the image that gets the AI judge most excited.

## The image

A tiny white paper boat rides the crest of a tsunami made of stars — a giant
golden wave of light curling over a sleeping city. Extreme scale contrast: one
small, fragile boat against a wave the size of the sky. The wave's curve drives
everything toward a single thrilling moment at the crest, and the whole scene
reads at a glance even at 300 px.

The artwork is original, drawn with code (Python / PIL) in this repository —
no photo, no stock image, no licensed character.

## How it runs

`main.ts` (Node 22, stdlib only) copies `entry.png` to the output directory
as `entry.png`, byte for byte, deterministically:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

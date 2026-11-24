# Tiny Chess R8

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/Iyannn11/tiny-chess/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/Iyannn11/tiny-chess/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

Tiny Chess R8 is a fresh-write, ultra-compact chess engine for the make.fun Tiny Chess bounty: the whole program packs into 4,074 bytes (cap 4,096 B). It uses a 0x88 board, Zobrist transposition table, negamax + iterative deepening, aspiration windows ±50, null-move pruning R=2, LMR + PVS, reverse futility, check extensions, 2 killers per ply, MVV-LVA ordering, a compact full SEE computed on the live board (no board copy), quiescence search with check evasions, material + piece-square-table eval + tempo +10, and a fixed node budget of 150,000 per move.

## Practice results

Kit gauntlet, 6 games per trial, run sequentially:

- Trial 0: Elo 1,279
- Trial 1: Elo 1,545
- Trial 2: Elo 1,451

Mean: 1,425.

Self-play vs R7 (100 games, 50k nodes each side): W37 D55 L8, Elo +103.7, 95% CI [35.7, 180.6]. R8 is the strongest engine built so far in this series.

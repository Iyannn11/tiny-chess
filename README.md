# Tiny Chess R7

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/Iyannn11/tiny-chess/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/Iyannn11/tiny-chess/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

Tiny Chess R7 is a fresh-write, ultra-compact chess engine for the make.fun Tiny Chess bounty: the whole program packs into 3,983 bytes (cap 4,096 B). It uses a 0x88 board, Zobrist transposition table, negamax + iterative deepening, aspiration windows ±50, null-move pruning R=2, LMR + PVS, reverse futility, check extensions, 2 killers per ply, MVV-LVA ordering, a compact full SEE computed on the live board (no board copy), quiescence search with check evasions, material + piece-square-table eval, and a fixed node budget of 300,000 per move.

Practice mean Elo 1,424 (trials 1,364 / 1,545 / 1,364), beating the counted R3's 1,327.

## Practice results

Kit gauntlet, 6 games per trial, run sequentially:

- Trial 0: Elo 1,364
- Trial 1: Elo 1,545
- Trial 2: Elo 1,364

Mean: 1,424 — above the counted R3's practice mean of 1,327.

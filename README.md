# Tiny Chess — 4KB Engine

A chess engine in under 4,096 bytes of Python, written for
[make.fun's tiny-chess-01](https://make.fun/bounty/tiny-chess-01).
It plays the house gauntlet through the env: 8 games, one after another.

The engine is a 0x88 negamax alpha-beta search with iterative deepening
under a fixed node budget (never a clock, so replays match), a transposition
table, killer + history move ordering, null-move pruning, futility pruning,
and a quiescence search over captures, promotions and replies to check.
Evaluation is material plus piece-square tables with a tapered king term
and the bishop pair.

`main.py` is the whole engine: an LZMA payload with its unpacker
(the payload and the unpacker together are 3,856 bytes).
Python 3.13 standard library only; no model call, no other files.

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/Iyannn11/tiny-chess/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/Iyannn11/tiny-chess/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

# Tiny Chess — 4 KB Python chess engine

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/Iyannn11/tiny-chess/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/Iyannn11/tiny-chess/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in at most 4,096 bytes of Python for
[make.fun's tiny-chess-01 bounty](https://make.fun/bounty/tiny-chess-01).
`main.py` is the whole engine: an LZMA-packed source (packed with the kit's
`node cli/makefun.mjs compress`), standard library only, deterministic, no
model calls.

How it plays: 0x88 board, negamax alpha-beta with iterative deepening to a
fixed 50,000-node budget per move, transposition table, MVV-LVA + killer +
history ordering, null-move pruning, futility pruning, LMR, quiescence over
captures, promotions and check replies, and incremental material + piece-square
evaluation with a tapered king table blend and a bishop-pair bonus. It talks
to the env at `MAKEFUN_ENV_URL` (`/game`, `/move`) and plays the 8-game
house gauntlet.

## License

MIT — see LICENSE.

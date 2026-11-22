# Tiny Chess R3

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/Iyannn11/tiny-chess/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/Iyannn11/tiny-chess/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A strong chess engine in 4 KB of Python, built for the
[make.fun tiny-chess-01 bounty](https://make.fun/bounty/tiny-chess-01).

## Engine

`engine.py` is the readable source (the entrypoint `main.py` is the same
program packed with the make.fun kit `compress` command). Pure Python 3.13
standard library, deterministic, no network, no model call.

- 0x88 board, Zobrist hashing, make/unmake with a full undo stack.
- Alpha-beta with iterative deepening to a fixed 30,000-node budget,
  so every move takes a bounded, deterministic amount of work.
- Null-move pruning (R=2), late-move reductions on quiet moves,
  check extensions, transposition table, two killer moves per ply,
  history heuristic, MVV-LVA capture ordering.
- Quiescence over captures, promotions and check evasions.
- Repetitions score 0, both in search and at the root (the engine
  avoids repeating a position it has already seen in the game).
- Evaluation: material plus piece-square tables (separate middlegame
  and endgame king tables), bishop-pair bonus.

## Run

`main.py` speaks the kit environment protocol (`MAKEFUN_ENV_URL`):
it loops on `/game`, thinks on `your_move`, and posts each move to
`/move`. It plays until the game is done.

## License

MIT. See `LICENSE`.

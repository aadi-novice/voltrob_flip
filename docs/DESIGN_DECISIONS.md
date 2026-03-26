# Design Decisions

## 1) Keep deterministic logic before probability
Reason:
- Deterministic inferences are guaranteed-safe moves.
- Probabilistic guesses are only used when no guaranteed move exists.

## 2) Persist board knowledge in `state_matrix`
Encoding:
- `1` => revealed safe tile
- `-1` => known voltorb
- `0` => unknown

Reason:
- Allows iterative deductions across solver calls.
- Makes benchmark and game-loop behavior consistent.

## 3) Rule 3 returns one tile at a time
Reason:
- Matches gameplay loop where each risky decision should be re-evaluated after new information.
- Simplifies attribution of failures to specific guesses.

## 4) Metadata from solver is optional
Design:
- `solver(..., return_meta=True)` returns `(moves, {"used_rule3": bool})`.
- Default behavior remains backward-compatible (`return_meta=False`).

Reason:
- Enables benchmark analytics without breaking existing game loop usage.

## 5) Benchmark-first baseline for RL
Reason:
- Establishes a measurable non-learning baseline.
- Future RL work should report relative gain over this benchmark.

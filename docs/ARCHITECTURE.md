# Architecture

This document describes how the current project components fit together and how they will extend into an RL pipeline.

## Current pipeline

`generate_table` -> `solver` -> `game_loop`

1. **Board generator (`generate_table`)**
   - Builds a randomized 5x5 board with values in {0,1,2,3}.
   - Computes row/column value totals and row/column voltorb totals.
   - Returns a dictionary used by solver/game loop.

2. **Solver (`solver`)**
   - Reads board clues and current knowledge state (`state_matrix`).
   - Applies deterministic fixed-point logic:
     - Rule 1: effective voltorbs == 0 -> all unknown are safe.
     - Rule 2: unknown count == effective voltorbs -> all unknown are voltorbs.
   - If no guaranteed safe moves exist, applies Rule 3 heuristic:
     - Risk score per tile = row-risk * col-risk.
     - Returns one lowest-risk tile.
   - Persists discovered voltorbs to state (`-1`).

3. **Game loop (`game_loop`)**
   - Maintains discovered safe tiles (`1`) and known voltorbs (`-1`) in `state_matrix`.
   - Repeatedly asks solver for next moves.
   - Ends on voltorb hit (loss) or when all 2/3 tiles are found (win).

## Data contracts

### `output` dictionary (from generator)
- `table`: numpy array (5x5)
- `col_total`, `row_total`: value totals
- `vol_col_total`, `vol_row_total`: voltorb totals
- `num_x`, `num_y`, `num_z`: counts for generated tiles

### `state_matrix`
- `0`: unknown
- `1`: revealed safe
- `-1`: known voltorb

## Benchmark flow

`run_benchmark` (manual_rule2_test.py) repeatedly calls `run_one_game`, which:
- Generates a board
- Runs solver until terminal outcome
- Tracks Rule 3 usage and guess counts

## Planned RL integration

Target future chain:

`generate_table` -> `VoltorbEnv` (Gymnasium) -> `RL Agent`

Where:
- Environment wraps board dynamics + state transitions.
- Solver benchmark serves as baseline policy.
- RL agent is evaluated against baseline win rate and risk profile.

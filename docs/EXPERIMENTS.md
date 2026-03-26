# Experiments

Tracks benchmark runs, configs, and outcomes for solver baselining.

## 2026-03-26 — Heuristic baseline (Rule 1 + Rule 2 + Rule 3)

### Config
- Script: `manual_rule2_test.py`
- Total games: `1000`
- Board source: randomized generator (`generate_table`)
- Policy:
  - Deterministic first (Rule 1/2)
  - Fallback guess by minimum multiplicative risk (Rule 3)

### Results
- Total games: `1000`
- Wins: `84` (`8.4%`)
- Losses: `916` (`91.6%`)
- Pure logic wins: `18` (`1.8%`)
- Games needing Rule 3: `982` (`98.2%`)
- Wins among Rule 3 games: `66` (`6.7%` of Rule 3 games)
- Average guesses needed (all games): `4.323`
- Average guesses in Rule 3 games: `4.402`

### Notes
- Most generated boards require guesses, suggesting high average ambiguity under current generator.
- Pure-logic wins are rare and often correlate with clue patterns that quickly collapse rows/columns.
- This run acts as baseline for future RL comparison.

## Template for future runs

### YYYY-MM-DD — <experiment name>

#### Config
- Script:
- Total games:
- Seed policy:
- Solver/agent variant:

#### Results
- Wins:
- Losses:
- Pure logic wins:
- Games needing Rule 3:
- Wins among Rule 3 games:
- Avg guesses (all):
- Avg guesses (Rule 3 games):

#### Observations
- 

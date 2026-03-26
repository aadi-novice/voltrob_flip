# Changelog

All notable changes to this project are documented in this file.

## [0.2.0] - 2026-03-26

### Added
- Deterministic + probabilistic hybrid solver flow documented and stabilized.
- Rule 3 probabilistic fallback integrated into `solver`.
- Benchmark harness in `manual_rule2_test.py` for large-run evaluation.
- Rule-3 usage metadata (`used_rule3`) via optional `solver(..., return_meta=True)`.
- Benchmark metrics:
  - Total wins/losses
  - Pure logic wins
  - Games needing Rule 3
  - Wins among Rule 3 games
  - Average guesses (all games and Rule-3-only games)
- Sample pure-logic-win board printouts for qualitative inspection.

### Changed
- Improved function docstrings for clearer arguments/returns/logic across core modules.
- Solver comments clarified around Rule 1, Rule 2, Rule 3 and state encoding.

## [0.1.0] - 2026-03-25

### Added
- Initial board generator (`generate_table`).
- Basic deterministic solver and game loop prototype.
- Entry script (`main.py`) and project bootstrap.

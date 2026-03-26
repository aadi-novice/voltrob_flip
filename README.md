# 🎮 voltorb-flip

> Building an AI that learns to play Voltorb Flip from Pokémon HeartGold/SoulSilver — from a logic-based solver all the way to a trained RL agent.

---

## What is Voltorb Flip?

Voltorb Flip is a minigame from Pokémon HeartGold/SoulSilver played at the Game Corner. It's a hybrid of **Minesweeper and Picross** — a 5×5 grid of hidden tiles containing multipliers (×1, ×2, ×3) and Voltorbs (bombs). Each row and column tells you the total of all numbers and the count of Voltorbs in it. Flip all the ×2s and ×3s without hitting a Voltorb to win.

It's a **partially observable** problem with deterministic logic for some tiles and genuine uncertainty for others — which makes it a great candidate for both rule-based solving and reinforcement learning.

---

## Project Goal

This is a **learning-by-building** project. The goal is to go from zero to a trained RL agent that plays Voltorb Flip, built step by step:

```
Board Generator → Logic Solver → Game Environment → RL Agent
```

No shortcuts. Every component is built from scratch and understood deeply before moving on.

---

## Roadmap

### ✅ Phase 1 — Board Generator
- [x] Generate a valid randomized 5×5 board
- [x] Compute row/column totals and Voltorb counts
- [x] Package board state as a clean dictionary

### ✅ Phase 2 — Rule-Based Solver
- [x] Rule 1: 0 Voltorb rows/cols → all tiles guaranteed safe
- [x] Rule 2: hidden tiles = Voltorb count → all hidden tiles are Voltorbs
- [x] Cross-referencing rows and columns to pinpoint specific tiles
- [x] Game loop with win/loss detection

### 🔲 Phase 3 — Probabilistic Solver
- [x] Compute Voltorb probability per tile using constraints
- [x] Handle ambiguous cases with minimum-risk heuristic
- [x] Decide when to quit vs. risk a flip

### 🔲 Phase 4 — Gymnasium Environment
- [ ] Wrap the game as a custom `gymnasium` environment
- [ ] Define state space, action space, and reward structure
- [ ] Test with random agent baseline

### 🔲 Phase 5 — RL Agent
- [ ] Train a DQN or PPO agent on the environment
- [ ] Reward shaping experiments
- [ ] Compare agent performance vs. logic solver baseline
- [ ] Visualize training progress and policy behavior

---

## Current Progress

> Daily updates logged here as the project evolves.

| Day | What was built |
|-----|---------------|
| Day 1 | Board generator, rule 1 solver, game loop skeleton |

---

## Tech Stack

- **Python** with `numpy` for board representation
- `gymnasium` (planned) for RL environment
- `stable-baselines3` or custom implementation (planned) for RL agent
- `uv` for dependency management

---

## Documentation

- `CHANGELOG.md` — project change history by version/date
- `docs/ARCHITECTURE.md` — system flow from generator to solver and RL path
- `docs/EXPERIMENTS.md` — benchmark runs, configs, and results
- `docs/DESIGN_DECISIONS.md` — rationale behind current implementation choices

---

## How to Run

```bash
# Install dependencies
uv sync

# Run current state
uv run main.py
```

---

## Key Concepts Explored

- Constraint satisfaction and logical deduction
- Partially Observable Markov Decision Processes (POMDPs)
- Reward shaping in reinforcement learning
- The intersection of rule-based AI and learned policies

---

## Inspiration

Started as a nostalgic side project after remembering how annoyingly hard Voltorb Flip was as a kid. Turns out it's also a genuinely interesting AI problem.

---

*Built by Aditya Ambade — one commit at a time.*

# 5800+ Quantitative Trading Strategies

This repo is a catalog of **5,806** trading strategy files: crypto spot and perps, grids, martingale, hedging, market making, momentum, mean reversion, options-style overlays, and FMZ/TradingView utilities.

Each file in `strategies/` is one strategy: name, author, description, parameters, and source (Pine Script, JavaScript, Python, MyLanguage, or C++). Start from the [full index](strategies/README.md).

These files are research specs and published source dumps. They do not place live orders by themselves. To turn a spec into a real model, use [AgenKit](https://agenkit.xyz) with **Opus 5.5** (or another model) inside any of the seven harnesses it supports.

## Build a strategy with AgenKit

### 1. Install AgenKit

Get it from [agenkit.xyz](https://agenkit.xyz) and install it into the agent you already use. AgenKit runs in all **7 harnesses**:

- [Claude Code](https://agenkit.xyz)
- [Cursor](https://agenkit.xyz)
- [Codex](https://agenkit.xyz)
- [OpenCode](https://agenkit.xyz)
- [Antigravity](https://agenkit.xyz)
- [GitHub Copilot](https://agenkit.xyz)
- [Kimi Code](https://agenkit.xyz)

Works with **Opus 5.5** in Claude Code, Cursor, and the rest of those harnesses. Pick the agent you already use, install AgenKit, then build from a spec in this repo.

### 2. Open this repo

Clone the repo and open it in that agent.

### 3. Pick one spec

Open one markdown file from `strategies/`. Attach it in the chat. One strategy per run.

### 4. Run the command

Claude Code, Cursor, OpenCode, Antigravity, GitHub Copilot, Kimi Code, and most other agents — slash command:

```text
/agenkit build a production research system from strategies/Python-Version-Multi-Asset-Momentum-Strategy-Tutorial.md
```

Codex CLI (Astra) — `@` mention, not a slash command:

```text
@agenkit build a production research system from strategies/Python-Version-Multi-Asset-Momentum-Strategy-Tutorial.md
```

Copy, paste, run. AgenKit walks spec → architecture → plan → test-first build. Approve the spec, architecture, and plan before code is written.

## Copy commands

Multi-asset momentum:

```text
/agenkit build a production research system from strategies/Python-Version-Multi-Asset-Momentum-Strategy-Tutorial.md
```

```text
@agenkit build a production research system from strategies/Python-Version-Multi-Asset-Momentum-Strategy-Tutorial.md
```

ATR futures (multi-symbol research backtest):

```text
/agenkit implement strategies/Digital-Currency-Futures-Multi-Variety-ATR-Strategy-Teaching.md as a research backtest with costs, delay-1 execution, and no live routing
```

Grid:

```text
/agenkit implement strategies/Adaptive-Intelligent-Grid-Trading-Strategy.md as a research backtest with costs, delay-1 execution, and no live routing
```

Intertemporal arbitrage:

```text
/agenkit implement strategies/High-Frequency-Intertemporal-Arbitrage-Strategy.md as a research backtest with costs, delay-1 execution, and no live routing
```

Market making (simulator only):

```text
/agenkit build an Avellaneda-Stoikov market making model for Hyperliquid perps from strategies/Dynamic-Spread-Market-Making-Strategy.md
```

```text
@agenkit build an Avellaneda-Stoikov market making model for Hyperliquid perps from strategies/Dynamic-Spread-Market-Making-Strategy.md
```

Swap the path for any other file in the [index](strategies/README.md). Add a short note for universe, venue, or delay if you want. You do not need to restate the math. It is already in the file.

## What is in this vault

| Language   | Listed in index |
| ---------- | --------------- |
| Pine Script | ~5,286 |
| JavaScript | ~362 |
| Python     | ~132 |
| MyLanguage | ~27 |
| C++        | ~3 |

Browse by language in [`strategies/README.md`](strategies/README.md). Typical file layout:

- Name and author
- Strategy description
- Argument table
- Source block
- Detail URL

## What AgenKit is

AgenKit is not another model. It is the harness that turns **Opus 5.5** (or Astra, Claude, Cursor, Codex, Kimi) into a full engineering team: brainstorm, architecture, plan, build, review, ship.

Use it from [agenkit.xyz](https://agenkit.xyz) in Claude Code, Cursor, Codex, OpenCode, Antigravity, GitHub Copilot, or Kimi Code.

## Disclaimer

Not investment, legal, or tax advice. Research specs only. Past results, backtests, and published source in this catalog do not guarantee future performance. Do not route live orders from these files until you have independently reviewed, tested, and risk-managed the system.

# 5,800+ Quantitative Trading Strategies Vault

A curated catalog of **5,806** quantitative trading strategy specifications, source code algorithms, and indicators spanning cryptocurrency spot & perpetual futures, grid bots, martingale systems, statistical arbitrage, market making models, momentum/mean-reversion indicators, and options overlays.

Each markdown file in [`strategies/`](strategies/) is a complete research specification containing strategy logic, default parameters, source code (Pine Script, JavaScript, Python, MyLanguage, or C++), and reference metadata. Access the full index in [`strategies/README.md`](strategies/README.md).

---

## What is Inside this Vault?

This repository acts as an open research library of quantitative trading logic. While individual strategy files contain mathematical rules, default parameters, and source blocks (from TradingView or exchange scripts), they represent raw strategy specifications rather than production execution software.

To transform any strategy spec in this vault into a **production-grade, execution-ready trading bot** (with live risk limits, order deduplication, WebSocket data feeds, unit tests, and exchange connectors), you can supply the strategy file directly to an AI engineering tool like [AgenKit](https://agenkit.xyz).

---

## How to Build Production Trading Bots from Strategy Specs

Instead of manually porting Pine Script or JavaScript into a production-grade Python or Go system, you can leverage [AgenKit](https://agenkit.xyz) inside your preferred AI environment ([Claude Code](https://agenkit.xyz), [Cursor](https://agenkit.xyz), [Codex](https://agenkit.xyz), [Antigravity](https://agenkit.xyz), [OpenCode](https://agenkit.xyz), [GitHub Copilot](https://agenkit.xyz), or [Kimi Code](https://agenkit.xyz)).

Because the exact mathematical rules, parameters, and indicators are already structured inside each strategy markdown file, the agent uses the spec as a single source of truth—avoiding math hallucinations and generating test-backed production code.

### 1. Index the Vault with Local Memory (Recommended)
With 5,800+ strategy files in `strategies/`, searching through the repository manually can consume excessive token context. Using AgenKit's local memory layer indexes the repository locally (`.agenkit/memory/`) at zero token cost:

```bash
# Build a local codebase map of all strategy specs
npx agenkit memory build

# Query strategy specs instantly by keyword or pattern
npx agenkit memory query "Avellaneda Stoikov market making"
```

### 2. Generate Production-Grade Code in One Command

Run the engineering pipeline command in your AI harness chat, passing the path of any strategy file:

```text
/agenkit build a production trading bot from strategies/Python-Version-Multi-Asset-Momentum-Strategy-Tutorial.md with risk controls, live Binance/OKX execution, and a backtest engine
```

*(For Codex CLI / Astra, use `@agenkit` instead of `/agenkit`)*

### What Happens Behind the Scenes:
1. **Spec & Math Parsing**: The agent extracts exact strategy rules and parameter defaults directly from the markdown spec.
2. **Architecture & Safety Gates**: Designs order execution logic, state persistence, inventory caps, stop-loss triggers, and order idempotency.
3. **Test-Driven Build**: Generates unit tests, mock exchange backtest simulators, and production API connectors before writing implementation code.
4. **Code Review & Deployment**: Audits position sizing safety, API rate limits, and secret handling, preparing the bot for paper or live trading.

---

## Example Commands for Common Strategy Types

Below are ready-to-use commands for building different quantitative models from vault specs:

#### Multi-Asset Momentum Engine
```text
/agenkit build a production research system from strategies/Python-Version-Multi-Asset-Momentum-Strategy-Tutorial.md
```

#### Multi-Symbol ATR Futures Bot (Backtest & Execution)
```text
/agenkit implement strategies/Digital-Currency-Futures-Multi-Variety-ATR-Strategy-Teaching.md as a research backtest with delay-1 execution and fee modeling
```

#### Adaptive Grid Trading Bot
```text
/agenkit implement strategies/Adaptive-Intelligent-Grid-Trading-Strategy.md as a production grid bot for Hyperliquid perps with order deduplication and inventory controls
```

#### High-Frequency Arbitrage
```text
/agenkit build a spread arbitrage engine from strategies/High-Frequency-Intertemporal-Arbitrage-Strategy.md with WebSocket order routing
```

#### Avellaneda-Stoikov Market Making
```text
/agenkit build an Avellaneda-Stoikov market making bot for perps from strategies/Dynamic-Spread-Market-Making-Strategy.md with inventory skew management
```

---

## Strategy Vault Index & Breakdown

The strategies in this vault are organized across five programming languages:

| Language | Specs Count | Primary Focus |
| :--- | :--- | :--- |
| **Pine Script** | ~5,286 | TradingView indicators, trend breakout, multi-timeframe overlays |
| **JavaScript** | ~362 | Node.js execution scripts, WebSocket market data feeds, exchange utilities |
| **Python** | ~132 | Backtesting frameworks, quantitative research models, machine learning |
| **MyLanguage** | ~27 | CTA futures trend & grid formulas |
| **C++** | ~3 | Low-latency execution templates |

Full list and search index: [`strategies/README.md`](strategies/README.md).

### Strategy File Format
Every strategy spec in `strategies/` includes:
- **Name & Author**
- **Strategy Description**
- **Parameter Table**
- **Complete Source Code Block**
- **Detail URL**

---

## Disclaimer

This catalog is strictly for educational and research purposes. Strategy specifications, backtest results, and source code do not constitute financial advice. Quantitative trading involves significant financial risk. Always validate models thoroughly in simulated or paper-trading environments before deploying real capital.

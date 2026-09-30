# 5,800+ Quantitative Trading Strategies Vault

A curated catalog of 5,806 quantitative trading strategy specifications, source code algorithms, and indicators across crypto spot, perpetual futures, grid systems, statistical arbitrage, and market making.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Supported Harnesses: 7](https://img.shields.io/badge/Harnesses-Claude_Code_|_Cursor_|_Codex_|_OpenCode_|_Antigravity_|_Copilot_|_Kimi-orange.svg)](https://agenkit.xyz)

> ### ⚡ Turn any spec into a production-grade trading bot with AgenKit
> A strategy specification, Pine Script snippet, or backtest dump is not execution software. Turning a research spec into a production trading system requires order execution logic, risk controls, idempotency, WebSocket reconnection handling, and test coverage.
>
> [AgenKit](https://agenkit.xyz) acts as an AI engineering team harness inside your coding tool—using the strategy file's math, parameters, and indicators as ground truth to build a test-driven, risk-managed trading system without re-deriving the logic from scratch.
>
> ```text
> /agenkit build a production-grade trading bot from strategies/Python-Version-Multi-Asset-Momentum-Strategy-Tutorial.md
> ```

---

## 🚀 60-Second Quick Start

Index the vault locally, then generate a production-ready trading system in one command:

```bash
# 1. Build the local codebase map (scans strategies at zero token cost)
npx agenkit memory build
```

Then in your AI harness chat (Claude Code, Cursor, Codex, Antigravity, etc.):

```text
/agenkit build a production-grade trading bot from strategies/Python-Version-Multi-Asset-Momentum-Strategy-Tutorial.md with risk controls, live Binance/OKX execution, and a backtest engine
```
*(For Codex CLI / Astra, use `@agenkit` instead of `/agenkit`)*

---

## 📊 Strategy Vault Index & Breakdown

The strategies in this vault are organized across five programming languages:

| Language | Specs Count | Primary Focus |
| :--- | :--- | :--- |
| **Pine Script** | ~5,286 | TradingView indicators, trend breakout, multi-timeframe overlays |
| **JavaScript** | ~362 | Node.js execution scripts, WebSocket market data feeds, exchange utilities |
| **Python** | ~132 | Backtesting frameworks, quantitative research models, machine learning |
| **MyLanguage** | ~27 | CTA futures trend & grid formulas |
| **C++** | ~3 | Low-latency execution templates |

Full searchable index categorized by language: [`strategies/README.md`](strategies/README.md).

---

## 🔄 Walkthrough: From Raw Spec to Production System

Here is how [AgenKit](https://agenkit.xyz) processes a spec such as [`strategies/Python-Version-Multi-Asset-Momentum-Strategy-Tutorial.md`](strategies/Python-Version-Multi-Asset-Momentum-Strategy-Tutorial.md):

1. **Spec & Parameter Extraction**: Parses the markdown file to extract signal math, momentum thresholds (`arrRatio`), rebalancing frequencies, and asset lists directly from the spec ground truth.
2. **Architecture & State Management**: Designs non-custodial order routing, position state persistence, WebSocket feeds, and order deduplication/idempotency.
3. **Test-Driven Implementation**: Writes unit tests for indicator math, mock exchange backtest execution, and paper-trading simulators before writing production implementation files.
4. **Safety & Risk Gating**: Integrates hard stop-loss checks, position size limits, API rate-limit controls, and secret management.
5. **Gated Deployment**: Configures paper trading by default, requiring explicit user activation before live order routing.

---

## ⚖️ Comparison: Manual Porting vs. AgenKit-Assisted Build

| Phase / Concern | Manual Strategy Porting | AgenKit-Assisted Build |
| :--- | :--- | :--- |
| **Logic Transcription** | Manual re-writing of formulas; prone to transcription errors | Uses spec parameters & indicator math directly as ground truth |
| **Order Execution** | Ad-hoc exchange API calls, vulnerable to dropped webhooks | Structured order lifecycle with idempotency and retry handlers |
| **Risk Controls** | Hardcoded or easily omitted position limits | Built-in risk gates (max drawdown limits, emergency halt, inventory caps) |
| **Test Coverage** | Manually written mock tests (frequently skipped) | Automated test suite (unit tests, mock backtest simulators, execution checks) |
| **Execution Default** | Often tested directly against live APIs | Paper trading gated by default; live routing requires explicit opt-in |

---

## 📋 Ready-to-Use `/agenkit` Build Commands

Below are example commands for common quantitative models in this vault:

### Multi-Asset Momentum Strategy
```text
/agenkit build a production research system from strategies/Python-Version-Multi-Asset-Momentum-Strategy-Tutorial.md
```

### Multi-Symbol ATR Futures Bot (Backtest & Execution)
```text
/agenkit implement strategies/Digital-Currency-Futures-Multi-Variety-ATR-Strategy-Teaching.md as a research backtest with delay-1 execution and fee modeling
```

### Adaptive Grid Trading Bot
```text
/agenkit implement strategies/Adaptive-Intelligent-Grid-Trading-Strategy.md as a production grid bot for Hyperliquid perps with order deduplication and inventory controls
```

### High-Frequency Intertemporal Arbitrage
```text
/agenkit build a spread arbitrage engine from strategies/High-Frequency-Intertemporal-Arbitrage-Strategy.md with WebSocket order routing
```

### Avellaneda-Stoikov Market Making
```text
/agenkit build an Avellaneda-Stoikov market making bot for perps from strategies/Dynamic-Spread-Market-Making-Strategy.md with inventory skew management
```

---

## 📁 Complete Strategy Index

Access the complete index of all 5,806 strategy specs in [`strategies/README.md`](strategies/README.md).

Each strategy file contains:
- **Name & Author**
- **Strategy Description & Math Logic**
- **Argument & Parameter Table**
- **Source Block**
- **Detail URL**

---

## ⚠️ Risk & Disclaimer

- **Educational & Research Purposes Only**: The strategy specifications, algorithms, and source dumps contained in this repository are for educational and quantitative research purposes only. Nothing here constitutes financial, investment, legal, or tax advice.
- **Unvalidated Research Specs**: Published strategy logic and backtests are unvalidated dumps and do not guarantee future performance.
- **Paper Trading Required**: Always execute thorough paper-trading and backtesting in simulated environments before considering live capital deployment.
- **Capital Risk**: Quantitative trading involves substantial risk of financial loss. Never route live orders without independent code review, risk limit enforcement, and capital management controls.

---

## 🤝 Contributing

Contributions to fix parameters, improve documentation, or add new research strategy specs are welcome. Please open a pull request or issue following the standard repository guidelines.

---

## 📄 License

This repository is licensed under the [MIT License](LICENSE).

---

## 🗂️ Strategy Catalog Database (`catalog/`)

Every file in `strategies/` is parsed and classified into a flat CSV database plus browsable Markdown indexes:

| File | What it is |
| :--- | :--- |
| [`catalog/strategies_db.csv`](catalog/strategies_db.csv) | 5,806 rows × 100 columns: family, tags, style, timeframe, asset class, instruments, direction, indicators, SL/TP/trailing, sizing, leverage, risk level, repaint risk, complexity, buildability score, claimed KPIs, backtest header, Pine `strategy()` params, text excerpts |
| [`catalog/INDEX.md`](catalog/INDEX.md) | Navigation hub: counts and links per family, tag, style, timeframe, asset, instrument, indicator, risk, exit method, author, year |
| [`catalog/SCHEMA.md`](catalog/SCHEMA.md) | Column-by-column definitions |
| [`catalog/query.py`](catalog/query.py) | CLI filter over the CSV (`python catalog/query.py --family breakout --tf 15m --min-build 9`) |
| [`catalog/build_catalog.py`](catalog/build_catalog.py) | Rebuilds everything (`python catalog/build_catalog.py`, ~90 s) |

Classification is rule-based (keyword + source-code analysis). Treat tags as strong hints, and treat claimed performance numbers as unverified author statements.

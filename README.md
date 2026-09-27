# 5800+ Quantitative Trading Strategies Vault

A comprehensive catalog of **5,806** quantitative trading strategy specifications, algorithms, and source dumps spanning crypto spot & perps, automated grid bots, martingale systems, statistical arbitrage, market making models, momentum/mean-reversion indicators, and options overlays.

Each file in [`strategies/`](strategies/) is a complete research specification containing strategy logic, default parameters, source code (Pine Script, JavaScript, Python, MyLanguage, or C++), and reference metadata. Access the full searchable index in [`strategies/README.md`](strategies/README.md).

---

## 🚀 Building Production Trading Bots with AgenKit

These 5,800+ strategy files serve as quantitative research specs and source blueprints. To transform any spec into a **production-grade, execution-ready trading system** (with live risk gates, order execution, idempotency, backtesting, and exchange connectors), use **[AgenKit](https://agenkit.xyz)**.

AgenKit is an AI engineering team harness that works across **all 7 major AI harnesses**:
- [Claude Code](https://agenkit.xyz) (`/agenkit`)
- [Cursor](https://agenkit.xyz) (`/agenkit`)
- [Codex CLI / Astra](https://agenkit.xyz) (`@agenkit`)
- [OpenCode](https://agenkit.xyz) (`/agenkit`)
- [Antigravity CLI](https://agenkit.xyz) (`/agenkit`)
- [GitHub Copilot](https://agenkit.xyz) (`@agenkit`)
- [Kimi Code](https://agenkit.xyz) (`/agenkit:engineering`)

---

## ⚡ The AgenKit Local Memory Layer

When working with a vault containing 5,800+ strategy files, token context efficiency is critical. AgenKit includes **Local Memory** (v2.2.0+), a zero-token, deterministic index of your codebase that runs on your local machine.

### How Local Memory Accelerates Quant Development:
- **Zero Token Cost Mapping**: Scans and indexes the entire vault (`.agenkit/memory/`) locally without wasting LLM token context.
- **Fast Navigation**: Agents query exact `file:line` locations for strategies, indicators, or utility functions instantly instead of re-reading multi-thousand line files.
- **Persistent Context**: Remembers architectural decisions, parameter specs, and past backtest notes across sessions.

### Memory Commands:
```bash
# Build the local codebase map (run once when cloning repo)
npx agenkit memory build

# Query strategies or utilities using plain language
npx agenkit memory query "where is the Avellaneda-Stoikov market making strategy?"

# Incremental update when files drift or after adding new strategies
npx agenkit memory update
```

---

## 🛠️ Step-by-Step Workflow: Spec → Production Bot

### 1. Install & Activate AgenKit
```bash
npm install -g agenkit
npx agenkit activate <license-key>
npx agenkit install engineering-kit
```

### 2. Open Repo & Build Local Memory
```bash
# Clone the repository and initialize local memory
git clone https://github.com/brainbrick-trades/The-Quant-Trading-Vault.git
cd The-Quant-Trading-Vault
npx agenkit memory build
```

### 3. Select a Strategy Spec
Browse [`strategies/README.md`](strategies/README.md) or use `npx agenkit memory query` to select a strategy spec from `strategies/`.

### 4. Run the `/agenkit` Engineering Pipeline
In your AI harness (Claude Code, Cursor, Antigravity, etc.), prompt AgenKit to build a production system from the chosen spec:

```text
/agenkit build a production-grade trading bot from strategies/Python-Version-Multi-Asset-Momentum-Strategy-Tutorial.md with Binance/OKX execution, risk manager, and backtest suite
```

### How AgenKit Specialists Build Your Strategy:
1. **Orient (Context Engineer)**: Queries Local Memory to locate relevant specs and existing modules without consuming unnecessary tokens.
2. **Brainstorm (Conductor)**: Clarifies your universe, risk parameters, leverage limits, and execution venues.
3. **Architecture (Backend Architect)**: Designs non-custodial order routing, data ingestion, state management, order idempotency, and WebSocket reconnection handlers.
4. **Plan (Conductor)**: Generates a step-by-step, test-driven build plan saved to `docs/plans/`.
5. **Build (Test Engineer & Specialists)**: Implements unit tests, backtest simulators, execution handlers, and exchange API adapters (RED-GREEN-REFACTOR cycle).
6. **Review (Code Reviewer & Security)**: Audits position sizing, slippage safeguards, secret management, and exception handling before live deployment.
7. **Ship (DevOps Engineer)**: Packages the bot into Docker containers with Prometheus/Grafana metrics, health probes, and alert webhooks.

---

## 📋 Ready-to-Use `/agenkit` Build Commands

### Multi-Asset Momentum Strategy:
```text
/agenkit build a production research system from strategies/Python-Version-Multi-Asset-Momentum-Strategy-Tutorial.md
```

### ATR Futures Strategy (Multi-Symbol Backtest):
```text
/agenkit implement strategies/Digital-Currency-Futures-Multi-Variety-ATR-Strategy-Teaching.md as a research backtest with costs, delay-1 execution, and no live routing
```

### Adaptive Grid Bot:
```text
/agenkit implement strategies/Adaptive-Intelligent-Grid-Trading-Strategy.md as a production grid bot for Hyperliquid perps with order deduplication and inventory limits
```

### High-Frequency Intertemporal Arbitrage:
```text
/agenkit build a high-frequency spread arbitrage engine from strategies/High-Frequency-Intertemporal-Arbitrage-Strategy.md with sub-second order cancellation
```

### Avellaneda-Stoikov Market Making:
```text
/agenkit build an Avellaneda-Stoikov market making model for Hyperliquid perps from strategies/Dynamic-Spread-Market-Making-Strategy.md with inventory skew and live risk controls
```

*Note: For Codex CLI / Astra, replace `/agenkit` with `@agenkit`.*

---

## 📊 Vault Catalog Overview

| Source Language | Strategies Count | Primary Use Cases |
| :--- | :--- | :--- |
| **Pine Script** | ~5,286 | TradingView indicators, trend breakout, multi-timeframe overlays |
| **JavaScript** | ~362 | Node.js & browser execution scripts, WebSocket drivers, exchange widgets |
| **Python** | ~132 | Backtesting models, quantitative research, machine learning classifiers |
| **MyLanguage** | ~27 | Simplified CTA futures trend & grid formulas |
| **C++** | ~3 | High-frequency latency-sensitive execution templates |

Browse the full index categorized by language and asset type in [`strategies/README.md`](strategies/README.md).

### Strategy Spec File Layout:
Each file in `strategies/` includes:
- **Name & Author**
- **Strategy Description & Logic Breakdown**
- **Parameters & Default Values**
- **Complete Source Code Block**
- **Detail URL** (Reference details and published source)

---

## ⚠️ Disclaimer

This repository is for research and educational purposes only. Published strategy specs, backtests, and source code do not constitute financial, investment, or legal advice. Quantitative trading carries substantial financial risk. Always test models thoroughly in simulated paper-trading environments before committing capital or routing live orders.

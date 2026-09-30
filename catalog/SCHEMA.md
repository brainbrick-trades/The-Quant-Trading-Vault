# strategies_db.csv — column reference

Multi-value columns are `|`-separated. Booleans are `True`/`False`. Empty = unknown / not detected.

## Identity
| Column | Meaning |
|---|---|
| id | Sequential row id |
| file | File name under `strategies/` |
| name | Strategy name (from `> Name`) |
| author | FMZ author |
| fmz_id / fmz_url | Original FMZ strategy id / URL |
| last_modified / year | FMZ last-modified timestamp |
| language | pine / javascript / python / mylanguage / cpp |
| pine_version | `//@version=N` |
| kind | strategy, tutorial_strategy, indicator, library, template, utility, tutorial |
| source_hash | md5 of whitespace-stripped source (find duplicates) |

## Classification
| Column | Meaning |
|---|---|
| strategy_family | Primary logic family (trend_following, momentum, mean_reversion, breakout, grid, martingale, dca, arbitrage, pairs_trading, hedging, market_making, scalping, candlestick_pattern, chart_pattern, support_resistance, smart_money_concepts, volatility, volume, oscillator, statistical, machine_learning, seasonality_time, multi_timeframe, portfolio_rotation, options, divergence, channel, swing_structure, renko_range_bars, news_sentiment, moving_average, unclassified) |
| strategy_tags | Up to 6 secondary families (incl. supporting: pyramiding, trailing_exit, signal_bot_execution, moving_average, channel, multi_timeframe, swing_structure) |
| all_family_scores | family:score pairs that passed threshold, descending |
| trading_style | hft, scalping, intraday, day_trading, swing, position, overnight, dca_accumulation |
| style_tags | All style tags detected |
| holding_period | Human-readable holding horizon implied by style |
| timeframe | Primary chart timeframe (1m…1mo; `1mo` = monthly, `1m` = one minute) |
| timeframe_source | name / description / backtest_header / none — backtest_header is an FMZ default and weak evidence |
| timeframes_all | Every timeframe mentioned in name, description or code |
| mtf_timeframes | Timeframes requested via `request.security` / timeframe inputs |
| asset_class | Primary: crypto, forex, stocks, indices, futures, commodities, options, spot, unspecified |
| market_tags | All market tags detected |
| instruments | Tickers / instruments named in text (BTC, ETH, ES, NQ, EURUSD, GOLD, NIFTY…) |
| crypto_perpetual | Mentions perpetual / swap / crypto futures |
| direction | long_only / short_only / long_short / unknown |
| regime_fit | Market regime the strategy is designed for (family default, overridden by explicit text) |
| regime_mentions | Regimes discussed in the text |

## Mechanics
| Column | Meaning |
|---|---|
| indicators / indicator_count | Technical indicators detected in code or text |
| has_stop_loss / has_take_profit / has_trailing_stop / has_breakeven / has_partial_exits / has_time_exit | Exit features |
| exit_methods | atr_based, fixed_percent, pips_ticks_points, risk_reward_ratio, trailing, signal_based, structure_based, time_based, breakeven, partial_exits, grid_take_profit |
| risk_based_sizing | Position size derived from risk % / volatility |
| max_dd_or_loss_control | Daily-loss / drawdown / equity-stop logic |
| pyramiding / pyramiding_n | Adds to open positions (`pyramiding=` in Pine or text) |
| has_time_filter / has_trend_filter / has_volume_filter / has_volatility_filter | Entry filters |
| uses_multi_timeframe | `request.security` or MTF wording |
| uses_alerts_webhook | Pine alerts / webhooks present |
| uses_external_api | HTTP / API calls in code |
| leverage_mentioned / leverage_value | Leverage discussed; max numeric leverage found (x) |

## Scores
| Column | Meaning |
|---|---|
| risk_mgmt_score | 0-5: SL, TP, trailing, risk sizing, drawdown control |
| risk_level / risk_reasons | low / medium / high / very_high with reasons |
| repaint_risk / repaint_reasons | low / medium / high (lookahead_on, security w/o offset, isrealtime, calc_on_every_tick) |
| complexity | low / medium / high from code length + indicator count |
| code_lines / num_arguments | Size metrics |
| buildability_score | 0-10: has source, mainstream language, description, structured description, SL, TP/trail, timeframe, args table, is a strategy; -2 if repaint high |

## Claimed performance (unverified, parsed from author text)
| Column | Meaning |
|---|---|
| claimed_profitable | yes / no / unknown based on wording |
| claimed_win_rate_pct, claimed_profit_factor, claimed_max_drawdown_pct, claimed_net_profit_pct, claimed_sharpe, claimed_risk_reward, claimed_num_trades | First numeric mention found |
| has_backtest_image | Description embeds a screenshot (usually a backtest) |

## Backtest header (FMZ `/*backtest ... */`) — mostly platform defaults
| Column | Meaning |
|---|---|
| has_backtest_header, bt_start, bt_end, bt_period, bt_base_period, bt_exchange, bt_symbol, bt_balance | As written in the header |

## Pine `strategy()` declaration
| Column | Meaning |
|---|---|
| pine_initial_capital, pine_qty_type, pine_qty_value, pine_commission_type, pine_commission_value, pine_slippage, pine_margin_long, pine_margin_short, pine_currency, pine_overlay, pine_calc_on_every_tick, pine_process_orders_on_close | Declaration kwargs |

## Text excerpts
| Column | Meaning |
|---|---|
| description_words | Length of description |
| overview | First 500 chars of Overview / Summary section |
| logic_excerpt | Strategy Principles / Logic section |
| entry_rule_excerpt / exit_rule_excerpt | First sentence describing entry / exit conditions |
| advantages_excerpt / risks_excerpt / optimization_excerpt | Section excerpts |
| arguments | `name=default (description); …` from the Strategy Arguments table (truncated at 600 chars) |

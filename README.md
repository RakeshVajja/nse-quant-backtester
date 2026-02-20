NSE Quant Backtester
Overview

NSE Quant Backtester is a research-grade, event-driven intraday backtesting engine designed to evaluate systematic trading strategies on NSE equities.

This project focuses on building a realistic and modular quantitative research framework, not a toy backtest script. It simulates execution behavior close to live market conditions and evaluates performance using advanced risk-adjusted metrics.

The system is designed for robustness, extensibility, and professional research workflows.

Strategy Version 1.0 Specification
Market Universe

NIFTY 50 stocks

2 years of historical data

Native 5-minute and 15-minute intervals

Core Strategy Logic

Bias (Higher Timeframe Filter)

15-minute EMA20 and EMA50

EMA20 > EMA50 → Long bias

EMA20 < EMA50 → Short bias

Alignment (Institutional Filter)

Intraday VWAP (daily reset)

Long trades only if price above VWAP

Short trades only if price below VWAP

Trigger (Execution Timeframe)

5-minute candle close breakout

Close above highest high of last 20 completed candles (long)

Close below lowest low of last 20 completed candles (short)

Entry

Enter at next 5-minute candle open (no look-ahead bias)

Stop Loss

Most recent confirmed swing pivot (structure-based)

Target

Fixed 1:2 Risk-to-Reward ratio

Risk Model

1% of fixed capital per trade (Phase 1)

Single trade per stock per day

Time Filter

Trades allowed between 9:45 AM – 2:45 PM only

Execution Model

Event-driven candle-by-candle simulation

Conservative same-candle handling (stop assumed hit first if both touched)

Realistic brokerage + slippage included

No intra-candle prediction

No future data leakage

Cost Assumptions

Flat brokerage per trade (round trip)

Percentage-based slippage model

Total trade cost deducted before performance evaluation

Performance Metrics

The engine computes advanced research-grade metrics including:

Win Rate

Expectancy (Average R per trade)

Profit Factor

Maximum Drawdown

Sharpe Ratio

MAR Ratio

Equity Curve Volatility

Monthly Return Breakdown

Architecture

The system is modular and designed for scalability:

Data Layer (Data loading & cleaning)

Indicator Layer (EMA, VWAP, Swing Detection)

Strategy Layer (Signal generation logic)

Simulation Engine (Event-driven execution)

Portfolio Layer (Capital & risk management)

Analytics Layer (Performance metrics & reporting)

This architecture allows easy extension to:

Multi-strategy testing

Portfolio-level allocation

Compounding models

Broker API integration

Live paper trading

Research Philosophy

This project emphasizes:

Structural edge over indicator stacking

Realistic execution assumptions

Conservative modeling

Robustness across multiple instruments

Avoidance of overfitting

Separation of research and deployment layers

Disclaimer

This project is for research and educational purposes only. Past performance does not guarantee future results. No financial advice is provided.
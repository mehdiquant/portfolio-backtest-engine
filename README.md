# Backtest Engine

Minimal and robust backtesting engine for portfolio-based strategies.

## Features
- Uses total return prices (dividends assumed reinvested via adjusted prices)
- Validates inputs (index consistency, NaN checks, weight normalization)
- Computes asset-level contributions
- Computes portfolio returns without look-ahead bias

## Assumptions
- Prices are total return prices (e.g. Adjusted Close from yfinance)
- Dividends are already included in price data
- Long-only portfolios (no short selling)
- Transaction costs are not yet implemented

## Status
Core engine implemented and validated.
Transaction costs and performance analytics will be added next.
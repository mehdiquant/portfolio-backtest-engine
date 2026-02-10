
# Portfolio Backtester

A lightweight, execution-only backtesting framework for quantitative portfolio strategies.

This project focuses on **correct execution, data integrity, and clean separation of responsibilities**, rather than signal generation or alpha discovery.

---

## Project Philosophy

This backtester is deliberately designed around the following principles:

- **Execution-first**: the engine only executes given prices and weights
- **Strategy-agnostic**: no signals, forecasts, or optimization logic
- **Fail fast**: invalid data is explicitly rejected
- **No look-ahead bias**: weights are applied with a one-period lag
- **Explicit assumptions**: long-only, no leverage, close-to-close execution

The goal is to provide a **robust and transparent foundation** on top of which strategies and analytics can be built.

---

## Project Structure

```
portfolio_backtester/
│
├── engine.py          # Execution-only backtest engine
├── data_loader.py     # Data loading and validation (Yahoo Finance)
├── README.md
```

---

## Data Loader (`data_loader.py`)

### Purpose

The data loader is responsible for:

- downloading raw market data from Yahoo Finance
- selecting price data (Close prices)
- detecting missing or invalid tickers
- reporting missing values without modifying the data

It does **not**:
- clean data
- fill missing values
- alter the universe silently

---

### Function Signature

```python
load_data(
    tickers,
    start_date,
    end_date,
    interval,
    adjusted_close
)
```

---

### Parameters

- `tickers` : list or string  
  Asset tickers (e.g. `["AAPL", "MSFT"]`)
- `start_date` : str  
  Start date (YYYY-MM-DD)
- `end_date` : str  
  End date (YYYY-MM-DD)
- `interval` : str  
  Data frequency (e.g. `"1d"`, `"1wk"`)
- `adjusted_close` : bool  
  If `True`, prices are adjusted for dividends and splits (`auto_adjust=True`)

---

### Behavior

- Returns a `pd.DataFrame` of prices (dates × tickers)
- Raises an exception if one or more tickers are fully missing
- Prints the total number of missing values (partial NaNs included)

---

## Backtest Engine (`engine.py`)

### Purpose

The `Backtest_Engine` is responsible for **executing** a portfolio backtest under strict assumptions.

It does **not**:
- generate trading signals
- optimize portfolios
- perform performance analysis beyond returns

---

### Key Assumptions

- Long-only portfolios
- No leverage (net exposure ≤ 100%)
- Close-to-close returns
- Weights decided at *t-1* (no look-ahead bias)

---

## Engine Interface

### Initialization

```python
engine = Backtest_Engine(prices, weights)
```

- `prices` : `pd.DataFrame`  
  Asset prices indexed by date
- `weights` : `pd.DataFrame`  
  Portfolio weights (same index and columns as `prices`)

---

### Execution

```python
engine.run()
```

This method:
- validates prices and weights
- checks execution constraints
- computes per-asset return contributions

The fundamental output stored by the engine is:

```python
engine.contributions
```

A DataFrame of **per-asset return contributions**.

---

### Portfolio Returns

```python
engine.returns
```

A derived quantity obtained by summing contributions across assets.

Returns are:
- close-to-close
- net of portfolio weights
- not annualized

---

## Data Validation Rules

### Prices

- strictly positive
- no missing values
- monotonic and unique index

### Weights

- non-negative (long-only)
- net exposure ≤ 100%
- no missing values
- aligned with prices (same index and columns)

Violations raise explicit exceptions.

---

## Example Usage

```python
from data_loader import load_data
from engine import Backtest_Engine

prices = load_data(
    tickers=["AAPL", "MSFT"],
    start_date="2020-01-01",
    end_date="2023-01-01",
    interval="1d",
    adjusted_close=True
)

weights = prices.copy()
weights[:] = 0.5

engine = Backtest_Engine(prices, weights)
engine.run()

portfolio_returns = engine.returns
```

---

## What This Project Is (and Is Not)

### ✔️ This project is
- a clean execution engine
- a robust educational framework
- a solid base for quantitative research

### ❌ This project is not
- a trading strategy
- a signal generator
- a full-featured backtesting platform

---

## Intended Extensions

The architecture is designed to support future extensions such as:

- strategy modules (signal generation)
- portfolio construction logic
- performance analytics (Sharpe, drawdown, turnover)
- transaction costs and slippage
- alternative execution models

These are intentionally **out of scope** for the current engine.

---

## Disclaimer

This project is for **research and educational purposes only**.  
It does not constitute investment advice and should not be used for live trading without further validation.
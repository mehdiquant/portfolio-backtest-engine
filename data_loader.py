import yfinance as yf

def load_data(tickers, start_date, end_date, interval, adjusted_close):
    # Download raw market data from Yahoo Finance
    # tickers        : list or string of tickers to download
    # start_date     : start date of the data
    # end_date       : end date of the data
    # interval       : data frequency (e.g. '1d', '1wk')
    # adjusted_close : if True, prices are adjusted for dividends and splits
    data = yf.download(
        tickers,
        start=start_date,
        end=end_date,
        interval=interval,
        auto_adjust=adjusted_close
    )

    # Keep only the Close prices (adjusted or not depending on auto_adjust)
    data = data['Close']

    # List to store tickers that are completely missing (full NaN columns)
    missing_tickers = []

    # Check each ticker column
    for i in data.columns:
        # If all values are NaN, the ticker was not found or has no data
        if data[i].isna().all():
            missing_tickers.append(i)

    # If at least one ticker is missing, fail fast with an explicit error
    if len(missing_tickers) > 0:
        raise Exception(f'{missing_tickers} were not found in the database')

    # Count total number of missing values (partial NaNs included)
    n_missing = data.isna().sum().sum()

    # Inform the user about remaining missing values
    print(f'{n_missing} value(s) missing')

    # Return the price DataFrame (dates × tickers)
    return data
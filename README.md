# Stock Market Analysis & ML Prediction

A python project for analyzing stocks and building machine learning models to predict price movements for swing trading (2-3 months) and long-term investing (1-3 years).

## Project Goals

- **Swing Trading**: Identify stocks with 10%+ potential gains over 2-3 months
- **Long-term Investing**: Find fundamentally strong stocks for 1-3 year holds
- **Risk Management**: Lower-risk approach compared to day trading
- **ML-Powered**: Use machine learning to identify patterns in historical data

## Project Structure

```
market-analysis/
├── src/                        # Reusable Python modules
│   ├── __init__.py          
│   ├── indicators.py          # Technical indicators (RSI, MACD, etc.)
│   ├── features.py            # Feature engineering for ML
│   ├── data_fetcher.py        # Download stock data
│   ├── models.py              # ML model classes
│   └── signals.py             # Buy/sell signal generation
│
├── notebooks/                  # Jupyter notebooks for analysis
│   ├── 01_swing_trading.ipynb
│   ├── 02_position_trading.ipynb
│   ├── 03_longterm_investing.ipynb
│   └── 04_backtesting.ipynb
│
├── data/                       # Stock data storage
│   ├── raw/                   # Original downloaded data
│   └── processed/             # Cleaned & featured data
│
├── models/                     # Saved ML models
│   └── swing_model_v1.pkl
│
├── results/                    # Charts, reports, backtest results
│   └── analysis_charts/
│
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── Logbook.md
```

## Core Features

### Technical Indicators
- **Moving Averages**: SMA, EMA (20, 50, 200-day)
- **Momentum**: RSI, MACD, Stochastic
- **Volatility**: Bollinger Bands, ATR
- **Volume**: OBV, Volume trends
- **Trend**: ADX, Ichimoku Cloud

### ML Models
- Random Forest Classifier
- XGBoost
- LightGBM
- Feature importance analysis
- Walk-forward validation

### Analysis Types
- **Swing Trading** (2-3 months): Technical pattern recognition
- **Position Trading** (6-12 months): Momentum + technical
- **Long-term Investing** (2-3 years): Fundamentals + growth


## Learning Path

### Week 1-2: Data & Exploration
1. Fetch data for 5-10 stocks
2. Calculate technical indicators
3. Visualize patterns
4. Understand correlations

### Week 3-4: Feature Engineering
1. Create lagged features
2. Add technical indicators
3. Engineer price-based features
4. Analyze feature importance

### Week 5-6: First Models
1. Logistic Regression baseline
2. Random Forest classification
3. Compare performances
4. Feature selection

### Week 7-8: Backtesting
1. Walk-forward validation
2. Calculate returns
3. Risk metrics (Sharpe ratio)
4. Identify weaknesses

### Week 9+: Iterate & Improve
1. Try ensemble methods
2. Add fundamental data
3. Multi-stock screening
4. Portfolio optimization

## Dependencies

Core packages:
- `yfinance` - Download stock data from Yahoo Finance
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `scikit-learn` - Machine learning models
- `xgboost` - Gradient boosting
- `lightgbm` - Fast gradient boosting
- `matplotlib` - Plotting
- `seaborn` - Statistical visualization
- `plotly` - Interactive charts
- `jupyter` - Interactive notebooks

See `requirements.txt` for full list with versions.

## Data Sources

**Primary: Yahoo Finance (via yfinance)**
- Free, no API key needed
- historical data going back decades
- OHLCV data (Open, High, Low, Close, Volume)
- Adjusted for splits and dividends
- ~15 minute delay on real-time data


## trading Strategy

### Swing Trading
- **Timeframe**: 2-6 months
- **Target Return**: 10-20%
- **Risk Level**: Medium
- **Analysis**: 70% technical, 30% fundamental
- **Time Commitment**: Few hours per week

### Position Trading
- **Timeframe**: 6-12 months
- **Target Return**: 20-40%
- **Risk Level**: Medium-Low
- **Analysis**: 50% technical, 50% fundamental
- **Time Commitment**: Monthly review

### Long-term Investing
- **Timeframe**: 2-3+ years
- **Target Return**: 50-200%+
- **Risk Level**: Lower (if fundamentally sound)
- **Analysis**: 80% fundamental, 20% technical
- **Time Commitment**: Quarterly review

## Useful Resources

- [Investopedia](https://www.investopedia.com/) - Financial education
- [QuantInsti Blog](https://blog.quantinsti.com/) - Algorithmic trading
- [Machine Learning for Trading](https://www.coursera.org/learn/machine-learning-trading) - Course
- [Yahoo Finance](https://finance.yahoo.com/) - Market data
- [TradingView](https://www.tradingview.com/) - Charting platform

## Future Improvements

- [ ] Add fundamental data integration
- [ ] Build portfolio optimizer
- [ ] Create stock screener with rankings
- [ ] Add sentiment analysis (news, Twitter)
- [ ] Implement automated backtesting
- [ ] Add risk metrics dashboard
- [ ] Create alerting system
- [ ] Support multiple data sources
- [ ] Add options analysis
- [ ] Build web dashboard

## Contributing

This is a personal learning project, but suggestions are welcome!

## License

MIT License - Feel free to use and modify for your own learning.

## Contact

Created by Jasper Valk - Stock Market Analysis Project

---
"""Performance metrics. Returns are simple per-bar returns; drawdowns are negative fractions."""
import numpy as np
import pandas as pd


def total_return(returns):
    return float((1 + returns).prod() - 1)


def cagr(returns, periods_per_year):
    years = len(returns) / periods_per_year
    growth = (1 + returns).prod()
    return float(growth ** (1 / years) - 1) if years > 0 and growth > 0 else float('nan')


def annual_volatility(returns, periods_per_year):
    return float(returns.std(ddof=1) * np.sqrt(periods_per_year))


def sharpe(returns, periods_per_year, risk_free_per_period=0.0):
    excess = returns - risk_free_per_period
    sd = excess.std(ddof=1)
    if not sd > 1e-12 * max(excess.abs().max(), 1e-12):   # constant returns: volatility is rounding noise
        return float('nan')
    return float(excess.mean() / sd * np.sqrt(periods_per_year))


def drawdown(returns):
    equity = (1 + returns).cumprod()
    peak = np.maximum(equity.cummax(), 1.0)     # starting capital counts as the first peak
    return equity / peak - 1


def max_drawdown(returns):
    return float(drawdown(returns).min())


def mar(returns, periods_per_year):
    """CAGR / |max drawdown|."""
    dd = max_drawdown(returns)
    return cagr(returns, periods_per_year) / abs(dd) if dd < 0 else float('nan')


def profit_factor(trade_returns):
    gains = trade_returns[trade_returns > 0].sum()
    losses = -trade_returns[trade_returns < 0].sum()
    return float(gains / losses) if losses > 0 else float('nan')


def summary(result, periods_per_year):
    """One-line metric dict for a lib.backtest.BacktestResult (closed trades only for trade stats)."""
    r = result.bars['net']
    closed = result.trades.loc[~result.trades['open'], 'return']
    return {
        'total_return': total_return(r),
        'cagr': cagr(r, periods_per_year),
        'annual_vol': annual_volatility(r, periods_per_year),
        'sharpe': sharpe(r, periods_per_year),
        'max_drawdown': max_drawdown(r),
        'mar': mar(r, periods_per_year),
        'trades': int(len(closed)),
        'win_rate': float((closed > 0).mean()) if len(closed) else float('nan'),
        'profit_factor': profit_factor(closed),
        'exposure': float((result.bars['held'] != 0).mean()),
    }

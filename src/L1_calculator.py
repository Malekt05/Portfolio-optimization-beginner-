"""
Level 1: Risk & Return Calculator
"""

import numpy as np
import pandas as pd


class PortfolioCalculator:
    """Calculate portfolio risk and return metrics."""
    
    def __init__(self, price_data, risk_free_rate=0.03):
        """
        Args:
            price_data: DataFrame with asset prices (dates x tickers)
            risk_free_rate: Annual risk-free rate (default 3%)
        """
        self.prices = price_data
        self.rf_rate = risk_free_rate
        self.returns = None
        self.mu = None
        self.sigma = None
    
    def compute_log_returns(self):
        """Compute log returns from prices."""
        self.returns = np.log(self.prices).diff().dropna()
        return self.returns
    
    def compute_statistics(self):
        """
        Compute annualized mean vector and covariance matrix.
        """
        if self.returns is None:
            self.compute_log_returns()
        
        # Annualize (252 trading days/year)
        self.mu = self.returns.mean().values * 252
        self.sigma = self.returns.cov().values * 252
        
        return self.mu, self.sigma
    
    def portfolio_metrics(self, weights):
        """
        Compute return, volatility, Sharpe for given weights.
        """
        if self.mu is None or self.sigma is None:
            self.compute_statistics()
        
        return_p = weights @ self.mu
        volatility_p = np.sqrt(weights @ self.sigma @ weights)
        sharpe = (return_p - self.rf_rate) / volatility_p if volatility_p > 0 else 0
        
        return return_p, volatility_p, sharpe


def main():
    """Example usage."""
    import yfinance as yf
    
    tickers = ["AAPL", "MSFT", "GOOGL"]
    prices = yf.download(tickers, start="2024-01-01", end="2025-01-01")["Close"]
    
    calc = PortfolioCalculator(prices)
    mu, sigma = calc.compute_statistics()
    
    print(f"Annualized mean returns:\n{mu}\n")
    print(f"Annualized covariance matrix:\n{sigma}\n")
    
    weights = np.array([0.5, 0.3, 0.2])
    ret, vol, sharpe = calc.portfolio_metrics(weights)
    print(f"Portfolio metrics: Return={ret:.2%}, Vol={vol:.2%}, Sharpe={sharpe:.4f}")


if __name__ == "__main__":
    main()

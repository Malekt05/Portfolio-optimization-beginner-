"""
3-ticker portfolio analysis
"""

import numpy as np
import yfinance as yf
from src.level1_calculator import PortfolioCalculator
from src.level2_optimization import PortfolioOptimizer
from src.level3_frontier import EfficientFrontier
from src.level4_montecarlo import TailRiskAnalyzer


def main():
    print("=" * 80)
    print("PORTFOLIO OPTIMIZATION ENGINE - Quick Start Example")
    print("=" * 80)
    
    # Fetch data
    tickers = ["AAPL", "MSFT", "GOOGL"]
    print(f"\nFetching data for {tickers}...")
    prices = yf.download(tickers, start="2024-01-01", end="2025-01-01")["Close"]
    print(f"Data shape: {prices.shape}")
    
    # Level 1: Compute statistics
    print("\n" + "=" * 80)
    print("LEVEL 1: Risk & Return Calculator")
    print("=" * 80)
    
    calc = PortfolioCalculator(prices)
    returns = calc.compute_log_returns()
    mu, sigma = calc.compute_statistics()
    
    print(f"\nAnnualized mean returns: {mu}")
    print(f"\nAnnualized covariance matrix:\n{sigma}")
    
    # Level 2: Optimize
    print("\n" + "=" * 80)
    print("LEVEL 2: Sharpe Ratio Optimization")
    print("=" * 80)
    
    optimizer = PortfolioOptimizer(mu, sigma)
    max_sharpe_weights, max_sharpe = optimizer.maximize_sharpe()
    
    print(f"\nOptimal weights: {max_sharpe_weights}")
    print(f"Max Sharpe: {max_sharpe:.4f}")
    
    ret, vol, _ = calc.portfolio_metrics(max_sharpe_weights)
    print(f"Expected return: {ret:.2%}")
    print(f"Volatility: {vol:.2%}")
    
    # Level 3: Frontier
    print("\n" + "=" * 80)
    print("LEVEL 3: Efficient Frontier + Ledoit-Wolf")
    print("=" * 80)
    
    frontier = EfficientFrontier(mu, sigma, returns.values)
    frontier.compute_frontier(n_points=50)
    print(f"\nFrontier computed with {len(frontier.frontier_returns)} points")
    
    # Level 4: Tail Risk
    print("\n" + "=" * 80)
    print("LEVEL 4: Monte Carlo Tail Risk Analysis")
    print("=" * 80)
    
    min_vol_idx = np.argmin(frontier.frontier_volatilities)
    min_var_weights = frontier.frontier_weights[min_vol_idx]
    equal_weights = np.ones(len(mu)) / len(mu)
    
    analyzer = TailRiskAnalyzer(mu, sigma)
    portfolios = {
        "Max Sharpe": max_sharpe_weights,
        "Min Variance": min_var_weights,
        "Equal Weight": equal_weights
    }
    
    results = analyzer.compare_portfolios(portfolios)
    analyzer.print_summary(results)
    
    print("\n✓ Analysis complete!")


if __name__ == "__main__":
    main()

"""
Level 2: Portfolio Optimization (Maximize Sharpe Ratio)
Uses SLSQP to find optimal portfolio weights.
"""

import numpy as np
from scipy.optimize import minimize

class PortfolioOptimizer:
    """Optimize portfolio weights."""
    
    def __init__(self, mu, sigma, rf_rate=0.03):
        self.mu = mu
        self.sigma = sigma
        self.rf_rate = rf_rate
        self.n_assets = len(mu)
    
    def negative_sharpe(self, w):
        """Objective: minimize negative Sharpe ratio."""
        portfolio_r = w @ self.mu
        volatility = np.sqrt(w @ self.sigma @ w)
        
        if volatility < 1e-6:
            return 1e10
        
        sharpe = (portfolio_r - self.rf_rate) / volatility
        return -sharpe
    
    def maximize_sharpe(self):
        """
        Find portfolio that maximizes Sharpe ratio.
        """
        constraints = {"type": "eq", "fun": lambda w: np.sum(w) - 1}
        bounds = tuple((0, 1) for _ in range(self.n_assets))
        w0 = np.ones(self.n_assets) / self.n_assets
        
        result = minimize(
            self.negative_sharpe,
            w0,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints
        )
        
        return result.x, -result.fun

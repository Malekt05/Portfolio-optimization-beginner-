"""
Level 3: Efficient Frontier + Ledoit-Wolf Shrinkage
Computes the frontier and stabilizes covariance.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from sklearn.covariance import LedoitWolf


class EfficientFrontier:
    """Compute and plot efficient frontier."""
    
    def __init__(self, mu, sigma, returns_data=None, rf_rate=0.03):
        """
        Args:
            mu: Mean return vector
            sigma: Covariance matrix
            returns_data: Raw returns for Ledoit-Wolf (optional)
            rf_rate: Risk-free rate
        """
        self.mu = mu
        self.sigma = sigma
        self.returns_data = returns_data
        self.rf_rate = rf_rate
        self.n_assets = len(mu)
        self.lambda_opt = None
        
        # Apply Ledoit-Wolf if data provided
        if returns_data is not None:
            self.apply_ledoit_wolf()
    
    def apply_ledoit_wolf(self):
        """Stabilize covariance matrix using Ledoit-Wolf shrinkage."""
        lw = LedoitWolf()
        lw.fit(self.returns_data)
        self.sigma = lw.covariance_ * 252  # Annualize
        self.lambda_opt = lw.shrinkage_
        print(f"Ledoit-Wolf shrinkage: λ* = {self.lambda_opt:.4f}")
    
    def min_volatility(self, w):
        """Objective: minimize portfolio volatility."""
        return np.sqrt(w @ self.sigma @ w)
    
    def compute_frontier(self, n_points=50):
        """
        Compute efficient frontier by varying target return.
        
        Args:
            n_points: Number of points on frontier
        Returns:
            frontier_returns, frontier_volatilities, frontier_weights
        """
        min_return = self.mu.min() - 0.02
        max_return = self.mu.max() + 0.05
        target_returns = np.linspace(min_return, max_return, n_points)
        
        frontier_returns = []
        frontier_volatilities = []
        frontier_weights = []
        
        constraints_base = {"type": "eq", "fun": lambda w: np.sum(w) - 1}
        bounds = tuple((0, 1) for _ in range(self.n_assets))
        w0 = np.ones(self.n_assets) / self.n_assets
        
        for target in target_returns:
            constraints = [
                constraints_base,
                {"type": "eq", "fun": lambda w: w @ self.mu - target}
            ]
            
            result = minimize(
                self.min_volatility,
                w0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 1000}
            )
            
            if result.success:
                frontier_returns.append(target)
                frontier_volatilities.append(result.fun)
                frontier_weights.append(result.x)
        
        self.frontier_returns = np.array(frontier_returns)
        self.frontier_volatilities = np.array(frontier_volatilities)
        self.frontier_weights = frontier_weights
        
        return self.frontier_returns, self.frontier_volatilities, self.frontier_weights
    
    def plot_frontier(self, max_sharpe_weights=None):
        plt.figure(figsize=(10, 6))
        plt.plot(self.frontier_volatilities, self.frontier_returns, "b-", linewidth=2,
                label="Efficient Frontier")
        plt.scatter(self.frontier_volatilities, self.frontier_returns, s=20, alpha=0.5)
        
        if max_sharpe_weights is not None:
            ret = max_sharpe_weights @ self.mu
            vol = np.sqrt(max_sharpe_weights @ self.sigma @ max_sharpe_weights)
            sharpe = (ret - self.rf_rate) / vol
            plt.scatter(vol, ret, color="red", s=200, marker="*",
                       label=f"Max Sharpe (Sharpe={sharpe:.4f})", zorder=5)
        
        plt.xlabel("Volatility (σ)")
        plt.ylabel("Expected Return (μ)")
        plt.title("Efficient Frontier")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

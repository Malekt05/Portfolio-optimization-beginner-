"""
Level 4: Monte Carlo Simulation & Tail Risk Analysis
Simulates 10,000 future return paths and computes VaR/CVaR.
"""

import numpy as np
import matplotlib.pyplot as plt


class TailRiskAnalyzer:
    """Analyze portfolio tail risk via Monte Carlo simulation."""
    
    def __init__(self, mu, sigma, rf_rate=0.03):
        self.mu = mu
        self.sigma = sigma
        self.rf_rate = rf_rate
    
    def simulate_returns(self, weights, T=252, n_simulations=10000):
        """
        Args:
            weights: Portfolio weights
            T: Time horizon (days)
            n_simulations: Number of Monte Carlo paths
        
        Returns:
            cumulative_returns: Array of shape (n_simulations,)
        """
        mu_daily = self.mu / 252
        sigma_daily = self.sigma / 252
        
        # Generate random returns
        daily_returns = np.random.multivariate_normal(
            mu_daily, sigma_daily, size=(n_simulations, T)
        )
        
        # Portfolio returns each day
        portfolio_daily = daily_returns @ weights
        
        # Cumulative return (compound)
        cumulative_returns = np.prod(1 + portfolio_daily, axis=1) - 1
        
        return cumulative_returns
    
    def compute_tail_metrics(self, returns, confidence=0.95):
        """
        Compute Value at Risk and Conditional Value at Risk.
        """
        alpha = 1 - confidence
        var = np.percentile(returns, alpha * 100)
        cvar = returns[returns <= var].mean()
        return var, cvar
    
    def compare_portfolios(self, portfolios_dict):
        """
        Compare tail risk across multiple portfolios.
        
        Args:
            portfolios_dict: {name: weights} dictionary
        Returns:
            results: Dictionary with metrics for each portfolio
        """
        results = {}
        
        for name, weights in portfolios_dict.items():
            returns = self.simulate_returns(weights)
            
            expected_ret = returns.mean()
            volatility = returns.std()
            var_95, cvar_95 = self.compute_tail_metrics(returns)
            
            results[name] = {
                "weights": weights,
                "return": expected_ret,
                "volatility": volatility,
                "var_95": var_95,
                "cvar_95": cvar_95,
                "returns_dist": returns
            }
        
        return results
    
    def plot_distributions(self, results):
        """For multiple portfolios."""
        plt.figure(figsize=(12, 6))
        
        for name, metrics in results.items():
            plt.hist(metrics['returns_dist'], bins=50, alpha=0.6, label=name)
        
        plt.axvline(0, color="black", linestyle="--", linewidth=1)
        plt.xlabel("1-Year Return")
        plt.ylabel("Frequency")
        plt.title("Distribution of Portfolio Returns (10,000 simulations)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def print_summary(self, results):
        """Print comparison table."""
        print("\n" + "=" * 90)
        print("PORTFOLIO TAIL RISK COMPARISON")
        print("=" * 90)
        print(f"{'Portfolio':<15} {'Return':<12} {'Vol':<12} {'VaR(95%)':<12} {'CVaR(95%)':<12}")
        print("-" * 90)
        
        for name, metrics in results.items():
            print(f"{name:<15} {metrics['return']:>10.2%}  {metrics['volatility']:>10.2%}  {metrics['var_95']:>10.2%}  {metrics['cvar_95']:>10.2%}")

# Mathematical Foundation
Complete mathematical derivations and formulas used throughout the portfolio optimization.

## 📚 Overview

This document provides rigorous mathematical backing for all concepts in the project. Each section includes:
- **Definition**: The concept explained clearly
- **Formula**: Mathematical representation
- **Intuition**: Why it works and when to use it
---

## 1. Log Returns

### Definition

Log returns are the natural logarithm of the price relative:

$$r_t = \ln\left(\frac{P_t}{P_{t-1}}\right) = \ln(P_t) - \ln(P_{t-1})$$

### Why Log Returns?

1. **Additivity**: Log returns compound additively over time
   $$r_{1:T} = \sum_{t=1}^{T} r_t = \ln(P_T) - \ln(P_0)$$

2. **Symmetry**: A loss of 50% followed by a gain of 100% gives same return as opposite order

3. **Normality**: For short periods, log returns are approximately normal-distributed

### Simple vs. Log Returns Comparison

| Aspect | Simple Returns | Log Returns |
|--------|---|---|
| Formula | $(P_t - P_{t-1})/P_{t-1}$ | $\ln(P_t/P_{t-1})$ |
| Aggregation | Multiplicative | Additive ✓ |
| Distribution | Non-normal | Approximately normal ✓ |
| Small returns | Same | Same |
| Large returns | Differ | Better ✓ |


## 2. Annualization

### Daily to Annual Conversion

For **mean return**:
$$\mu_{\text{annual}} = 252 \times \mu_{\text{daily}}$$

For **volatility** (standard deviation):
$$\sigma_{\text{annual}} = \sqrt{252} \times \sigma_{\text{daily}}$$

For **covariance matrix**:
$$\Sigma_{\text{annual}} = 252 \times \Sigma_{\text{daily}}$$

### Why $\sqrt{252}$ for Volatility?

Variance compounds linearly with time:
$$\text{Var}(r_1 + r_2 + \cdots + r_{252}) = 252 \times \text{Var}(r_{\text{daily}})$$

But standard deviation is the square root of variance:
$$\sigma = \sqrt{\text{Var}} \Rightarrow \sigma_{\text{annual}} = \sqrt{252 \times \text{Var}_{\text{daily}}} = \sqrt{252} \times \sigma_{\text{daily}}$$

---

## 3. Portfolio Return & Volatility

### Portfolio Return

For a portfolio with weights $w = [w_1, w_2, \ldots, w_n]$ and mean returns $\mu = [\mu_1, \mu_2, \ldots, \mu_n]$:

$$\mu_p = w^\top \mu = \sum_{i=1}^{n} w_i \mu_i$$

This is a **linear combination** of asset returns.

### Portfolio Volatility (Variance Form)

The portfolio variance is:

$$\sigma_p^2 = w^\top \Sigma w = \sum_{i=1}^{n} \sum_{j=1}^{n} w_i w_j \Sigma_{ij}$$

Expanded for 3 assets:

$$\sigma_p^2 = w_1^2 \sigma_1^2 + w_2^2 \sigma_2^2 + w_3^2 \sigma_3^2 + 2w_1 w_2 \sigma_{12} + 2w_1 w_3 \sigma_{13} + 2w_2 w_3 \sigma_{23}$$

**Key insight**: Volatility is **NOT** a linear combination of asset volatilities. The off-diagonal terms (covariances) matter crucially.

### Portfolio Volatility (Standard Form)

Taking the square root:

$$\sigma_p = \sqrt{w^\top \Sigma w}$$

### Example (3-Asset Portfolio)

```
Weights: w = [0.5, 0.3, 0.2]
Returns: μ = [0.10, 0.15, 0.12]
Covariance matrix Σ:
  [[0.04, 0.01, 0.02],
   [0.01, 0.06, 0.015],
   [0.02, 0.015, 0.05]]

Portfolio return:
μ_p = 0.5(0.10) + 0.3(0.15) + 0.2(0.12) = 0.121 = 12.1%

Portfolio variance:
σ_p² = 0.5²(0.04) + 0.3²(0.06) + 0.2²(0.05) 
     + 2(0.5)(0.3)(0.01) + 2(0.5)(0.2)(0.02) + 2(0.3)(0.2)(0.015)
     = 0.01 + 0.0054 + 0.002 + 0.003 + 0.004 + 0.0018
     = 0.0272

Portfolio volatility:
σ_p = √0.0272 = 0.165 = 16.5%
```

---

## 4. Sharpe Ratio

### Definition

The Sharpe ratio measures **return per unit of risk**:

$$\text{Sharpe} = \frac{\mu_p - r_f}{\sigma_p}$$

Where:
- $\mu_p$ = portfolio return
- $r_f$ = risk-free rate
- $\sigma_p$ = portfolio volatility

### Interpretation

- **Higher is better**: More return for each unit of risk
- **Unit**: Percentage return per percentage of risk
- **Benchmark**: Sharpe ratio of 0.5+ is good; 1.0+ is excellent

---

## 5. Covariance Matrix Properties

### Symmetry

$$\Sigma = \Sigma^\top \Rightarrow \Sigma_{ij} = \Sigma_{ji}$$

The covariance between asset $i$ and $j$ is the same as between $j$ and $i$.

### Positive Semi-Definite

For any weight vector $w$:

$$w^\top \Sigma w \geq 0$$

This ensures portfolio variance is always non-negative.

### Correlation from Covariance

Convert covariance to correlation:

$$\rho_{ij} = \frac{\Sigma_{ij}}{\sigma_i \sigma_j}$$

where $\sigma_i, \sigma_j$ are the standard deviations.

**Range**: $-1 \leq \rho_{ij} \leq 1$

### Example

```
Covariance matrix:
  Σ = [[0.04, 0.012],
       [0.012, 0.09]]

Volatilities: σ₁ = √0.04 = 0.20, σ₂ = √0.09 = 0.30

Correlation:
  ρ₁₂ = 0.012 / (0.20 × 0.30) = 0.012 / 0.06 = 0.20
  
Assets are weakly positively correlated.
```

---

## 6. Efficient Frontier

### Definition

A portfolio is **efficient** if:
- For a given level of risk, it maximizes return, OR
- For a given level of return, it minimizes risk

The **Efficient Frontier** is the curve of all efficient portfolios.

### Frontier Construction

For each target return $r_{\text{target}}$, solve:

$$\min_w \quad w^\top \Sigma w$$

$$\text{subject to:}$$
$$w^\top \mu = r_{\text{target}}$$
$$\sum w_i = 1$$
$$w_i \geq 0$$

**Result**: A single optimal portfolio for each target return.

By varying $r_{\text{target}}$ from minimum to maximum feasible return, we trace the frontier.

### Tangency Portfolio

The portfolio on the frontier with the **highest Sharpe ratio**. It's the point where a line from the risk-free rate is tangent to the frontier curve.

---

## 7. Ledoit-Wolf Shrinkage

check `docs/Ledoit_Wolf.md`

## 8. Value at Risk (VaR)

### Definition

**Value at Risk at confidence level α** is the loss level such that there's a $(1-\alpha)$ probability of exceeding it.

Mathematically: The $\alpha$-quantile of the loss distribution.

$$\text{VaR}_\alpha = \text{quantile}(\text{losses}, \alpha)$$

### Interpretation

```
VaR(95%) = -8%  means:
  "In 95% of outcomes, loss is ≤ 8%"
  OR
  "In 5% of outcomes, loss is ≥ 8%"
```

### Limitations

- Only tells you the **threshold**, not the severity
- Doesn't show what happens beyond the threshold
- Non-convex (optimization issues)

---

## 9. Conditional Value at Risk (CVaR)

### Definition

**CVaR** (also called Expected Shortfall) is the **average loss in the worst α% of outcomes**:

$$\text{CVaR}_\alpha = \mathbb{E}[\text{Loss} \mid \text{Loss} \geq \text{VaR}_\alpha]$$

### Interpretation

```
CVaR(95%) = -12%  means:
  "In the worst 5% of outcomes, the average loss is 12%"
```

### Why CVaR > VaR?

Because CVaR includes the tail beyond VaR threshold.

```
Loss distribution:
        |
    200 |
        |      ← 95% of outcomes
    100 |_____/
        |    /│
      0 |___/ │ ← 5% tail (worst outcomes)
        |    /│
   -100 |   / │← VaR(95%)
        |  /  │
   -200 | /   │← CVaR(95%) (average of this tail)
        |_____|
```

### Example

```
1000 simulated portfolio returns: [-2%, -5%, -8%, ..., 35%, 40%, 45%]

Sorted (ascending): [-45%, -40%, ..., -2%, 0%, 2%, ..., 40%, 45%]

VaR(95%) = return at 5th percentile = -8%
  "Worst 5% of outcomes have loss ≥ 8%"

CVaR(95%) = average of worst 5% = (-45% + -40% + ... + -8%) / 50 = -15%
  "Given worst 5%, average loss is 15%"
```

---

## 10. Multivariate Normal Distribution

### Definition

A multivariate normal distribution with mean $\mu$ and covariance $\Sigma$:

$$\mathbf{X} \sim \mathcal{N}(\mu, \Sigma)$$

### Probability Density Function

$$f(\mathbf{x}) = \frac{1}{(2\pi)^{n/2} |\Sigma|^{1/2}} \exp\left(-\frac{1}{2} (\mathbf{x} - \mu)^\top \Sigma^{-1} (\mathbf{x} - \mu)\right)$$

### Key Properties

1. **Marginal distributions are normal**: Each component is univariate normal
2. **Correlations preserved**: If $\Sigma$ has correlation structure, samples respect it
3. **Affine transformation**: If $\mathbf{X} \sim \mathcal{N}(\mu, \Sigma)$, then $A\mathbf{X} + \mathbf{b} \sim \mathcal{N}(A\mu + \mathbf{b}, A\Sigma A^\top)$

### Why Use for Monte Carlo?

For portfolio returns, if individual asset returns are approximately normal with covariance $\Sigma$, then:

$$\mathbf{r}_{\text{portfolio}} = w^\top \mathbf{r}_{\text{assets}} \sim \mathcal{N}(w^\top \mu, w^\top \Sigma w)$$

By sampling from the multivariate normal, we:
- Generate plausible return sequences
- Respect historical correlations
- Cover outcome space efficiently

---

## 11. SLSQP Algorithm

### Problem Formulation

$$\min_w \quad f(w)$$

$$\text{subject to:}$$
$$g_i(w) = 0 \quad (i = 1, \ldots, m)$$
$$h_j(w) \leq 0 \quad (j = 1, \ldots, p)$$
$$l \leq w \leq u$$

### Sequential Quadratic Programming Idea

1. **Approximate** the problem locally with a quadratic model
2. **Solve** the quadratic subproblem
3. **Take a step** using line search
4. **Repeat** until convergence

### Why SLSQP Works for Portfolios

- **Convex problem**: Portfolio variance is convex, constraints are linear
- **Fast convergence**: Quadratic approximation is very accurate
- **Handles constraints**: Respects sum-to-one, bounds naturally
- **Robust**: Doesn't require explicit Hessian

See `docs/SLSQP.md` for detailed algorithm walkthrough.

---

## Summary Table

| Concept | Formula | Key Insight |
|---------|---------|-------------|
| Log return | $\ln(P_t/P_{t-1})$ | Additivity |
| Annualized return | $252 \times \mu_{\text{daily}}$ | Linear scaling |
| Annualized volatility | $\sqrt{252} \times \sigma_{\text{daily}}$ | Square root scaling |
| Portfolio return | $w^\top \mu$ | Linear combination |
| Portfolio variance | $w^\top \Sigma w$ | Quadratic form |
| Sharpe ratio | $(\mu_p - r_f) / \sigma_p$ | Return per risk |
| Efficient frontier | Minimize $\sigma_p$ for each $\mu_p$ | Trade-off curve |
| Ledoit-Wolf | $(1-\lambda) \Sigma_s + \lambda \Sigma_t$ | Robust estimation |
| VaR(95%) | 5th percentile | Threshold |
| CVaR(95%) | Mean of worst 5% | Severity |

---

**Next**: See `docs/SLSQP.md` for algorithm details or `docs/Ledoit_Wolf.md` for shrinkage deep dive.

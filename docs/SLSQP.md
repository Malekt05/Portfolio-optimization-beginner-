# SLSQP Method: Sequential Least Squares Programming

## Table of Contents
1. [Overview](#overview)
2. [What Does SLSQP Stand For?](#what-does-slsqp-stand-for)
3. [The Problem It Solves](#the-problem-it-solves)
4. [How SLSQP Works](#how-slsqp-works)
5. [Step-by-Step Algorithm](#step-by-step-algorithm)
6. [Visual Example](#visual-example)
7. [Why SLSQP for Portfolio Optimization](#why-slsqp-for-portfolio-optimization)
8. [Key Concepts](#key-concepts)
9. [Python Implementation](#python-implementation)

---

## Overview

**SLSQP** is an iterative algorithm that solves **constrained optimization problems**. It's the method we use in our portfolio engine to find optimal weights despite having multiple constraints (weights sum to 1, weights ≥ 0, target returns, etc.).

Think of it as a "smart search" algorithm that:
- Starts with an initial guess
- Builds a simplified (quadratic) model of the problem
- Solves that simplified problem
- Takes a step toward the solution
- Repeats until convergence

---

## What Does SLSQP Stand For?

| Term | Meaning |
|------|---------|
| **Sequential** | Works in steps; updates one iteration at a time |
| **Least Squares** | Uses quadratic (second-order) approximations |
| **Programming** | Mathematical programming = optimization (not software development) |

---

## The Problem It Solves

SLSQP handles **constrained optimization**:

```
Minimize:   f(w)

Subject to:
  - Equality constraints:   g_i(w) = 0       (e.g., Σ w_i = 1)
  - Inequality constraints: h_j(w) ≤ 0      (e.g., -w ≤ 0 means w ≥ 0)
  - Bounds:                 l ≤ w ≤ u       (e.g., 0 ≤ w ≤ 1)
```

**Why is this hard?**

- You can't just take a derivative and solve (like calculus class)
- Constraints restrict where you can move
- Multiple types of constraints interact in complex ways

**Example from portfolio optimization:**

```
Minimize:   Volatility = √(w^T Σ w)

Subject to:
  - Σ w_i = 1          (weights sum to 1)
  - w_i ≥ 0 for all i   (no short-selling)
  - w^T μ = 0.15       (target return = 15%)
```

No simple formula exists. You need an **iterative algorithm** like SLSQP.

---

## How SLSQP Works

SLSQP is a **divide-and-conquer** approach:

1. Approximate the hard problem locally with something easy (quadratic)
2. Solve the easy problem
3. Take a step toward the solution
4. Repeat until convergence

### The Core Insight

At iteration $k$, SLSQP:

1. **Builds a quadratic model** of the objective using Taylor expansion:
   $$f(w) \approx f(w_k) + \nabla f(w_k)^\top (w - w_k) + \frac{1}{2}(w - w_k)^\top B_k (w - w_k)$$
   
   where $B_k$ is the **approximate Hessian** (second derivative).

2. **Linearizes the constraints**:
   $$g_i(w) \approx g_i(w_k) + \nabla g_i(w_k)^\top (w - w_k) = 0$$

3. **Solves the QP subproblem** (Quadratic Programming):
   - Minimize the quadratic approximation
   - Subject to linearized constraints
   - Result: a search direction $d_k$

4. **Line search**: Find step size $\alpha_k$ such that:
   $$w_{k+1} = w_k + \alpha_k d_k$$
   moves downhill without overshooting.

5. **Updates the Hessian** using BFGS or SR1 (quasi-Newton methods).

6. **Checks convergence**: If improvements are tiny or constraints are satisfied, stop.

---

## Step-by-Step Algorithm

### Pseudocode

```python
def slsqp(objective_fn, initial_guess, constraints, bounds, tolerance=1e-6):
    w = initial_guess  # Start with w0
    k = 0
    max_iterations = 1000
    
    while k < max_iterations:
        # Step 1: Evaluate current solution
        f_k = objective_fn(w)
        grad_f_k = compute_gradient(objective_fn, w)
        constraint_values = [c["fun"](w) for c in constraints]
        
        # Step 2: Check if constraints are satisfied
        if max(abs(constraint_values)) < tolerance:
            # All constraints satisfied
            if norm(grad_f_k) < tolerance:
                # Gradient near zero: local optimum
                break
        
        # Step 3: Build quadratic approximation
        # (Implicit: SLSQP maintains Hessian approximation B_k)
        
        # Step 4: Solve QP subproblem
        # min: f_k + grad_f_k^T * d + 0.5 * d^T * B_k * d
        # s.t.: linearized constraints
        d_k = solve_qp_subproblem(grad_f_k, B_k, constraints, bounds)
        
        # Step 5: Line search
        alpha = 1.0
        while objective_fn(w + alpha * d_k) > f_k and alpha > 1e-8:
            alpha *= 0.5
        
        # Step 6: Update solution
        w = w + alpha * d_k
        
        # Step 7: Update Hessian approximation
        B_k = update_hessian_bfgs(B_k, w, f_k, grad_f_k)
        
        k += 1
    
    return w, f_k
```

---

## Visual Example

### Problem
Minimize $f(w) = (w - 0.6)^2$ with constraint $w \geq 0.2$, starting at $w_0 = 0.1$.

```
        f(w)
          |
        1 |      *
          |     /|\
      0.5 |    / | \
          |   /  |  \
      0.2 |  /   |   \
          | /    |    \
        0 |------|-----|-------- w
          0   0.2   0.6   1.0
```

### Iteration 0
- $w_0 = 0.1$ (violates constraint $w \geq 0.2$)
- $f(0.1) = 0.25$
- $\nabla f(0.1) = -1.0$ (gradient says: move right!)
- **QP subproblem**: "Move right, but respect $w \geq 0.2$"
- **Solution**: $w_1 = 0.2$

### Iteration 1
- $w_1 = 0.2$
- $f(0.2) = 0.16$ ✓ improved
- $\nabla f(0.2) = -0.8$ (still want to move right)
- **QP subproblem**: "Move toward unconstrained optimum at $w = 0.6$"
- **Solution**: $w_2 = 0.35$

### Iteration 2
- $w_2 = 0.35$
- $f(0.35) = 0.0625$ ✓ improved
- ... continues until convergence

**Final**: $w^* = 0.6$, $f(0.6) = 0$ (global minimum)

---

## Why SLSQP for Portfolio Optimization

### 1. **Handles Multiple Constraint Types**

Our portfolio problems have:
- Equality constraints: $\sum w_i = 1$ (weights sum to 1)
- Inequality constraints: $w_i \geq 0$ (no short-selling)
- Bounds: $0 \leq w_i \leq 1$
- Optional: $w^\top \mu = r_{\text{target}}$ (target return)

SLSQP handles all of these simultaneously.

### 2. **Works Well with Convex Problems**

Portfolio optimization is **convex**:
- Objective (volatility) is convex: $\sqrt{w^\top \Sigma w}$
- Constraints are linear (convex)
- Result: **One global optimum** (no local minima)
- SLSQP converges reliably in 10–50 iterations

### 3. **No Explicit Hessian Required**

SLSQP approximates the Hessian (BFGS) rather than requiring you to compute it. This is practical for portfolio problems.

### 4. **Robust and Well-Tested**

SLSQP is from scipy (industry-standard). Used in thousands of applications.

---

## Key Concepts

### Gradient
Direction of steepest increase. We move opposite to it (negative gradient = steepest descent).

For volatility $\sigma = \sqrt{w^\top \Sigma w}$:
$$\nabla \sigma = \frac{\Sigma w}{\sqrt{w^\top \Sigma w}}$$

### Hessian
Second derivatives. Tells you the "curvature" of the function. Used to build the quadratic approximation.

### Quasi-Newton Methods (BFGS, SR1)
Algorithms to approximate the Hessian iteratively. We don't need to compute it explicitly (which would be expensive).

### Line Search
After finding a search direction $d_k$, don't blindly move all the way. Search along the direction for a good step size $\alpha_k$.

Why? The quadratic approximation is only accurate *locally*. Overshooting violates the approximation.

### Convergence Criteria

SLSQP stops when:
- All constraints are satisfied: $|g_i(w)| < \epsilon$
- Gradient is near zero: $\|\nabla f(w)\| < \epsilon$
- Changes are tiny: $\|w_{k+1} - w_k\| < \epsilon$

(Typical $\epsilon \sim 10^{-6}$ to $10^{-8}$)

---

## Takeaway

SLSQP is a powerful, general-purpose constrained optimizer. For portfolio problems:
- It's **reliable** (convex problem = one global optimum)
- It's **fast** (converges in tens of iterations)
- It's **flexible** (handles any combination of constraints)

You can trust it to find the optimal portfolio given your constraints.

---

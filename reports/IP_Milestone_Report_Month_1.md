# Independent Project (IP) Milestone Report — Month 1 & 2
## PartitionViz: Computational & Interactive Foundations in the Theory of Partitions

**Student**: Jatin Pawar  
**Topic**: Theory of Partitions (Based on George E. Andrews, *The Theory of Partitions*, Cambridge University Press)  
**Academic Mentor**: Course Professor / Advisor  
**Date**: October 2026  
**Repository Architecture**: `partition_core` engine + Unified Streamlit Application (`app.py`, `ui/`)  
**Automated Tests**: 50 / 50 Passing (`pytest`)  
**Execution Command**: `streamlit run app.py`

---

## 1. Executive Summary

Over the past two months, we have developed **PartitionViz**: a computational mathematics framework and interactive laboratory suite designed to explore, verify, and visualize foundational theorems from Andrews's *The Theory of Partitions* (Chapters 1 & 2).

Unlike static numeric scripts or purely theoretical manuscripts, this system implements the exact geometric and combinatorial mappings behind partition identities and provides interactive visual environments that allow direct inspection of:
1. **Conjugation & Ferrers Geometry** (Andrews §1.3, Theorem 1.4, Sylvester's Theorem, Durfee Square Decomposition)
2. **Franklin's Combinatorial Involution** for Euler's Pentagonal Number Theorem (Andrews §1.3, Theorem 1.6, Corollaries 1.7 & 1.8)
3. **Series-Product Identities & Generating Functions** (Andrews Chapter 2, Section 2.2, eq. 2.2.9, Euler's Odd-Distinct Identity)

Every mathematical invariant has been verified with **50 automated unit tests** in `pytest`.

---

## 2. Mathematical Theorems Implemented & Verified

### 2.1 Andrews Definition 1.1 & Section 1.3: Ferrers Diagrams & Conjugation
- **Definition**: A partition $\lambda = (\lambda_1, \lambda_2, \dots, \lambda_r)$ with $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_r > 0$ and $\sum \lambda_i = n$.
- **Conjugate Partition $\lambda'$**: $\lambda'_i = \#\{j : \lambda_j \ge i\}$, geometrically obtained by reflecting the Ferrers graph along its main diagonal.
- **Invariants Verified**:
  - Involution: $(\lambda')' = \lambda$
  - Size preservation: $\sum \lambda'_i = \sum \lambda_i = n$
  - Boundary duality: $\text{largest\_part}(\lambda) = \text{len}(\lambda')$, and $\text{len}(\lambda) = \text{largest\_part}(\lambda')$.

### 2.2 Andrews Theorem 1.4: Restricted Partition Duality
> **Theorem 1.4 (Andrews p. 8)**: The number of partitions of $n$ with at most $m$ parts equals the number of partitions of $n$ in which no part exceeds $m$.
- **Computational Verification**: Verified exhaustively for all $1 \le n \le 20$ and $1 \le m \le 6$ via explicit bidirectional map construction:
$$\lambda \in \mathcal{P}_{\le m\text{ parts}}(n) \xrightarrow{\text{conjugation}} \lambda' \in \mathcal{P}_{\max \le m}(n)$$

### 2.3 Sylvester's Theorem (Andrews Ch. 1, Ex. 8)
- The number of self-conjugate partitions ($\lambda = \lambda'$) of $n$ equals the number of partitions of $n$ into **distinct odd parts**.
- Verified computationally across all $n \le 35$ by unfolding hooks along the main diagonal:
$$\#\{\lambda \vdash n : \lambda = \lambda'\} = \#\{\mu \vdash n : \mu_i \text{ distinct and odd}\}$$

### 2.4 Durfee Square Decomposition & Andrews eq. (2.2.9)
- Every partition has a unique Durfee square of side $d = \max\{i : \lambda_i \ge i\}$.
- The partition decomposes uniquely into:
  1. The $d \times d$ Durfee square ($d^2$ dots).
  2. A right partition $\lambda_R$ of dots to the right (at most $d$ parts).
  3. A bottom partition $\lambda_B$ of dots below (parts at most $d$).
- Proves combinatorially Andrews's fundamental series expansion:
$$\sum_{n=0}^\infty p(n) q^n = \sum_{d=0}^\infty \frac{q^{d^2}}{(1-q)^2(1-q^2)^2\dots(1-q^d)^2}$$

### 2.5 Andrews Theorem 1.6: Franklin's Involution & Euler's Pentagonal Theorem
> **Euler's Identity**:
> $$\prod_{n=1}^\infty (1 - q^n) = \sum_{k=-\infty}^\infty (-1)^k q^{k(3k-1)/2} = 1 - q - q^2 + q^5 + q^7 - q^{12} - q^{15} + \dots$$

- **Franklin's Combinatorial Mechanism (1881)**:
  Let $D(n)$ denote the set of partitions of $n$ into strictly distinct parts.
  Define base $b(\lambda) = \lambda_r$ and slope $s(\lambda) = \max\{s : \lambda_i = \lambda_1 - (i - 1) \text{ for } 1 \le i \le s\}$.
  The map $\phi$ defines:
  - If $b \le s$ (and not exceptional): move base to slope ($\ell \to \ell - 1$).
  - If $b > s$ (and not exceptional): move slope to base ($\ell \to \ell + 1$).
  - Exceptional cases (where base meets slope, $s = r$):
    - $b = s \implies n = \frac{k(3k-1)}{2} = \omega(k)$, partition $\lambda = (2k-1, \dots, k)$ has no partner.
    - $b = s + 1 \implies n = \frac{k(3k+1)}{2} = \omega(-k)$, partition $\lambda = (2k, \dots, k+1)$ has no partner.
- **Verification Result**: $p_e(D, n) - p_o(D, n) = (-1)^k$ if $n = \omega(\pm k)$, and $0$ otherwise. Verified for all $n \le 35$.

### 2.6 Andrews Corollary 1.8: Euler's Pentagonal Recurrence for $p(n)$
Because $(\sum p(n) q^n) \cdot \prod (1 - q^n) = 1$:
$$p(n) = \sum_{k \ge 1} (-1)^{k+1} \left[ p(n - \omega(k)) + p(n - \omega(-k)) \right]$$
- **Complexity Analysis**:
  - Single evaluation: $O(\sqrt{n})$ terms ($\approx 2\sqrt{2n/3}$ additions).
  - Sequential table generation: $\sum_{n=1}^N O(\sqrt{n}) = O(N^{3/2}) = O(N\sqrt{N})$.
  - In contrast, naive partition enumeration requires exponential time $O(e^{\pi\sqrt{2N/3}})$.

### 2.7 Andrews Chapter 2: Series-Product Identities
- Formal power series arithmetic in $\mathbb{Z}[[q]]$.
- Exact polynomial truncated product expansion:
$$\prod_{k=1}^M (1 + q^k) = \prod_{k=1}^M \frac{1}{1 - q^{2k-1}} \pmod{q^{M+1}}$$
- Degree-by-degree coefficient stabilization.

---

## 3. Architecture of the Codebase

```
theory_of_partitions/
├── app.py                          # Unified Streamlit application entry point
├── partition_core/                 # Mathematical computational engine
│   ├── __init__.py                 # Clean unified API
│   ├── enumeration.py              # Partitions generator, DP recurrence table, restricted classes
│   ├── conjugation.py              # Ferrers matrices, conjugation involution, Theorem 1.4 verifier
│   ├── franklin.py                 # Franklin slope/base analysis, map phi, Euler verifier
│   ├── generating_functions.py     # Exact formal power series, Durfee series, GF expansions
│   └── asymptotics.py              # Hardy-Ramanujan formula & error analysis
├── ui/                             # Interactive visual laboratories
│   ├── styles.py                   # Scholarly research theme & native LaTeX containers
│   ├── diagrams.py                 # Ferrers & Franklin Plotly diagram renderers
│   ├── home_page.py                # Academic overview & 4-question methodology
│   ├── module_1_conjugation.py     # Module 1: Ferrers Diagrams, Transposition & Durfee
│   ├── module_2_franklin.py        # Module 2: Franklin's Involution & Parity Matrix
│   ├── module_3_series_identities.py # Module 3: Series-Product Identities & Generating Functions
│   └── theory_dossier.py           # Theorem catalog, bibliography, in-app test runner
├── tests/                          # Automated test suite (50/50 passing)
│   ├── test_enumeration.py
│   ├── test_conjugation.py
│   ├── test_franklin.py
│   ├── test_generating_functions.py
│   └── test_asymptotics.py
├── reports/
│   ├── IP_Milestone_Report_Month_1.md
│   └── IP_Milestone_Report_Month_1.tex
├── README.md                       # Comprehensive deployment guide & documentation
└── requirements.txt
```

---

## 4. How to Run the Applications & Verify

### Running the Test Suite
```bash
python -m pytest tests/ -v
```
*Result: 50 passed in 0.71s.*

### Launching the Unified Application
```bash
streamlit run app.py
```
*Live at: `http://localhost:8501`*

---

## 5. Draft Email to Professor for Milestone Review

**Subject**: IP Milestone: Computational Framework & Interactive Labs for Andrews Chapters 1 & 2 (PartitionViz)

Dear Professor,

I hope you are having a wonderful week.

Following our weekly discussions on the elementary theory and generating function methods in Chapters 1 & 2 of Andrews's *The Theory of Partitions*, I wanted to share a major project milestone developed for our Independent Project: **PartitionViz**.

Rather than only presenting hand calculations of the weekly problem sets, I built an integrated interactive computational laboratory in Python to explore the combinatorial mechanisms underlying the theorems we studied:

1. **Ferrers & Conjugation Lab (Andrews §1.3, Theorem 1.4)**:
   - Interactive Ferrers diagram generator with column-by-column transposition animation.
   - Computational verification of the bijection between partitions with $\le m$ parts and partitions with largest part $\le m$.
   - Hook-length unfolding establishing Sylvester's theorem relating self-conjugate partitions to partitions with distinct odd parts.
   - Combinatorial Durfee square decomposition into $d^2$, $\lambda_R$ ($\le d$ parts), and $\lambda_B$ (parts $\le d$).

2. **Franklin's Involution & Pentagonal Number Theorem Lab (Andrews Theorem 1.6)**:
   - Dynamic highlighting of the base $b$ and slope $s$ on Ferrers diagrams with exceptional fixed-point detection.
   - Live parity matrix illustrating how even and odd distinct partitions cancel out ($p_e(D,n) - p_o(D,n) = 0$), leaving the exact pentagonal residue $(-1)^k$ at $\omega(\pm k) = \frac{3k^2 \mp k}{2}$.
   - Step-by-step breakdown of Euler's pentagonal recurrence for calculating $p(n)$ in $O(N\sqrt{N})$ operations versus the intractable exponential search space of naive enumeration.

3. **Series-Product Identities Lab (Andrews Chapter 2, §2.1–2.2)**:
   - Exact polynomial formal power series algebra in $\mathbb{Z}[[q]]$.
   - Algebraic demonstration of Euler's odd-distinct identity $\prod(1+q^k) = \prod(1-q^{2k-1})^{-1}$.
   - Evaluation of Andrews's Durfee square series $\sum_{d=0}^\infty \frac{q^{d^2}}{(q; q)_d^2}$, proving exact coefficient equality with $p(n)$ for all tested degrees.

4. **Verification Suite**:
   - The entire mathematical core is verified with 50 automated unit tests covering known values, edge cases, and bijective invariants.

The application launches with a single command (`streamlit run app.py`) and is also prepared for browser access via Streamlit Community Cloud.

I would love to give you a quick 5-minute live demonstration during our meeting this week to show the visual proofs and get your guidance on which direction to explore next as we begin Chapter 5 (the Hardy–Ramanujan asymptotic formula and the circle method).

Sincerely,  
Jatin Pawar

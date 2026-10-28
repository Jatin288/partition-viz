# Independent Project (IP) Progress Report
## PartitionViz: Computational & Interactive Foundations in the Theory of Partitions

**Student**: Jatin Pawar · 2024279 · IIIT Delhi  
**Topic**: Theory of Partitions (Based on George E. Andrews, *The Theory of Partitions*, Cambridge University Press)  
**Project**: Independent Project (IP)  
**Primary Text**: G. E. Andrews (1976/1998)  
**Repository Architecture**: `partition_core` engine + Unified Streamlit Application (`app.py`, `ui/`)  
**Automated Tests**: Tested via automated `pytest` suite across all modules  
**Execution Command**: `streamlit run app.py`

---

## 1. Executive Summary

This Independent Project presents **PartitionViz**: a computational mathematics framework and interactive laboratory suite designed to explore, verify, and visualize foundational theorems from Andrews's *The Theory of Partitions* (Chapters 1 & 2).

Unlike static numeric scripts or purely theoretical manuscripts, this system implements the exact geometric and combinatorial mappings behind partition identities and provides interactive visual environments that allow direct inspection of:
1. **Conjugation & Ferrers Geometry** (Andrews §1.1–1.3, Theorem 1.4, Sylvester's Theorem, Durfee Square Decomposition)
2. **Franklin's Combinatorial Involution** for Euler's Pentagonal Number Theorem (Andrews §1.3, Theorem 1.6, Corollaries 1.7 & 1.8)
3. **Series-Product Identities & Generating Functions** (Andrews Chapter 2, Section 2.1 formal power series stabilization, Theorem 2.1 $q$-binomial corollaries, Euler's odd-distinct identity, and eq. 2.2.9 Durfee square series)

Every mathematical invariant is validated by an automated test suite in `pytest`.

---

## 2. Mathematical Theorems Implemented & Verified

### 2.1 Andrews Definition 1.1 & Section 1.2: Ferrers Diagrams & Conjugation
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
  2. The right partition $\lambda_R$ of dots strictly to the right of the square (at most $d$ parts).
  3. The bottom partition $\lambda_B$ of dots strictly below the square (parts at most $d$).
- Invariant verified across all partitions: $|\lambda| = d^2 + |\lambda_R| + |\lambda_B|$.

### 2.5 Franklin's Sign-Reversing Involution (Andrews Theorem 1.6)
> **Theorem 1.6 (Andrews p. 11)**: Let $D(n)$ be partitions of $n$ into distinct parts. Franklin's map $\phi : D(n) \to D(n)$ pairs partitions of opposite parity $(\ell \to \ell \pm 1)$ except on exceptional configurations where:
> $$n = \omega(k) = \frac{3k^2 - k}{2} \quad \text{or} \quad n = \omega(-k) = \frac{3k^2 + k}{2}$$
- **Combinatorial Cancellation**: For non-pentagonal integers, $p_e(D, n) - p_o(D, n) = 0$. For pentagonal integers, the single exceptional partition yields $(-1)^k$:
$$\prod_{n=1}^\infty (1 - q^n) = \sum_{k=-\infty}^\infty (-1)^k q^{k(3k-1)/2} = 1 - q - q^2 + q^5 + q^7 - q^{12} - q^{15} + \dots$$
- Verified exhaustively for all $n \le 35$.

### 2.6 Euler's Recurrence for $p(n)$ (Andrews Corollary 1.8)
Because $(\sum p(n) q^n) \cdot \prod (1 - q^n) = 1$:
$$p(n) = \sum_{k \ge 1} (-1)^{k+1} \left[ p\left(n - \frac{3k^2-k}{2}\right) + p\left(n - \frac{3k^2+k}{2}\right) \right]$$
- **Complexity Distinction**: Evaluating a single $p(n)$ when previous values are known requires $O(\sqrt{n})$ terms; generating the full sequence up to $N$ takes $O(N\sqrt{N})$ additions, avoiding the exponential search space of naive enumeration.

### 2.7 Formal Power Series Stabilization in $\mathbb{Z}[[q]]$ (Andrews Ch. 2, §2.1)
- Truncating an infinite product $\prod_{k=1}^\infty (1 + c_k q^k)$ at $M \ge N$ factors preserves the exact integer coefficients of $q^0, \dots, q^N$ without truncation error.
- Verified for $N \le 30$.

### 2.8 Andrews Theorem 2.1 ($q$-Binomial Theorem) & Partition Corollaries
- **Theorem 2.1**: For $|q| < 1, |t| < 1$,
$$\sum_{n=0}^\infty \frac{(a; q)_n}{(q; q)_n} t^n = \frac{(at; q)_\infty}{(t; q)_\infty}$$
- **Corollary 2.2 (Euler)**: $a=0, t=q \implies \sum_{n=0}^\infty \frac{q^n}{(q; q)_n} = \frac{1}{(q; q)_\infty} = \sum p(n) q^n$ (partitions sorted by largest part).
- **Corollary 2.3 (Euler)**: $a \to \infty, t=q \implies \sum_{n=0}^\infty \frac{q^{n(n+1)/2}}{(q; q)_n} = (-q; q)_\infty = \sum p(D, n) q^n$ (distinct partitions sorted by triangular staircase $\Delta_n$).

---

## 3. Architecture & Repository Structure

```
theory_of_partitions/
├── app.py                          # Unified multi-page Streamlit application
├── partition_core/                 # Presentation-agnostic computational engine
│   ├── __init__.py                 # Public mathematical API
│   ├── enumeration.py              # Recursive partition generator & DP recurrence
│   ├── conjugation.py              # Ferrers matrices, transposition, Theorem 1.4
│   ├── franklin.py                 # Franklin base/slope, exceptional cases, Euler verifier
│   ├── generating_functions.py     # Formal power series arithmetic in Z[q], q-binomial, Durfee series
│   └── asymptotics.py              # Hardy-Ramanujan approximation & error analysis
├── ui/                             # Research UI components
│   ├── styles.py                   # Scholarly research theme, native LaTeX containers
│   ├── diagrams.py                 # Ferrers & Franklin Plotly renderers
│   ├── home_page.py                # Academic framework & deliverable matrix
│   ├── module_1_conjugation.py     # Module 1 Laboratory & Findings
│   ├── module_2_franklin.py        # Module 2 Laboratory & Findings
│   ├── module_3_series_identities.py # Module 3 Laboratory & Findings
│   └── theory_dossier.py           # Andrews bibliography, theorem catalog, dynamic pytest runner
├── tests/                          # Automated pytest suite
│   ├── test_enumeration.py
│   ├── test_conjugation.py
│   ├── test_franklin.py
│   ├── test_asymptotics.py
│   └── test_generating_functions.py
├── reports/
│   ├── IP_Progress_Report.md       # Comprehensive academic progress report
│   └── IP_Progress_Report.tex      # LaTeX research report
├── README.md                       # Documentation & deployment guide
└── requirements.txt
```

---

## 4. Academic Bibliography

1. **Andrews, George E.** (1976/1998). *The Theory of Partitions*. Cambridge University Press.
2. **Euler, Leonhard** (1748). *Introductio in Analysin Infinitorum*, Vol. 1.
3. **Franklin, Fabian** (1881). *Sur le développement du produit infini $(1-x)(1-x^2)\dots$*. *Comptes Rendus*, 92, pp. 448–450.
4. **Sylvester, James Joseph** (1882). *A Constructive Theory of Partitions*. *Amer. J. Math.*, 5(1), pp. 251–330.
5. **Heine, Eduard** (1847). *Basic Hypergeometric Series and the q-Binomial Theorem*. *J. Reine Angew. Math.*

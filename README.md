# PartitionViz: Computational Laboratory for the Theory of Partitions

**Independent Project (IP) · Jatin Pawar · 2024279 · IIIT Delhi**  
**Primary Mathematical Source**: George E. Andrews, *The Theory of Partitions* (Cambridge University Press, 1976/1998)  
**Live Deployed Application**: [https://partition-viz-jatin.streamlit.app/](https://partition-viz-jatin.streamlit.app/)  
**GitHub Repository**: [https://github.com/jatin288/partition-viz](https://github.com/jatin288/partition-viz)  

---

## 1. Academic Purpose & Research Philosophy

**PartitionViz** is an interactive computational mathematics laboratory designed to investigate foundational theorems, combinatorial bijections, and generating-function identities from George E. Andrews's definitive treatise, *The Theory of Partitions*.

Rather than presenting decorative visualizations, every laboratory module answers four core mathematical questions:

1. **The Theorem**: What exact partition identity or structural duality from Andrews is under examination?
2. **The Mechanism**: What combinatorial mapping, sign-reversing involution, or recurrence implements the result?
3. **The Deduction**: What do the computed invariants, parity cancellations, or coefficient limits establish mathematically?
4. **Scope & Limits**: What has been established by general mathematical proof, what is verified computationally over finite ranges, and what remains outside the current scope?

---

## 2. Integrated Laboratory Modules

### 📐 Module 1: Ferrers Graphs & Conjugation Duality (Andrews Ch. 1, §1.1–1.3)
- **Theorem 1.4 Duality**: Explores and proves through explicit bidirectional pairing that the number of partitions with $\le m$ parts equals the number of partitions with largest part $\le m$.
- **Transposition Dynamics**: Step-by-step visual reflection showing rows becoming columns with invariant preservation ($(\lambda')' = \lambda$ and $\sum \lambda'_i = \sum \lambda_i$).
- **Sylvester's Self-Conjugate Identity (Ch. 1, Ex. 8)**: Exact computational comparison establishing that self-conjugate partitions ($\lambda = \lambda'$) are equinumerous with partitions into distinct odd parts via hook unfolding.
- **Durfee Square Decomposition**: Visual and combinatorial decomposition of a partition into a $d \times d$ square, right partition $\lambda_R$ ($\le d$ parts), and bottom partition $\lambda_B$ (parts $\le d$), proving $|\lambda| = d^2 + |\lambda_R| + |\lambda_B|$.

### ⚡ Module 2: Franklin's Involution & Pentagonal Numbers (Andrews Ch. 1, §1.3, Thm 1.6)
- **Franklin's Sign-Reversing Involution (1881)**: Color-coded Ferrers diagram decomposition into Base $b$, Slope $s$, and Intersection points.
- **Exact Parity Cancellation**: Demonstrates why $p_e(D,n) - p_o(D,n) = 0$ for almost all $n$, and isolates the surviving residue $(-1)^k$ at generalized pentagonal numbers $\omega(\pm k) = \frac{3k^2 \mp k}{2}$.
- **Euler's Pentagonal Recurrence (Corollary 1.8)**: Evaluates $p(n) = \sum_{k \ge 1} (-1)^{k+1} [p(n - \omega(k)) + p(n - \omega(-k))]$, displaying arithmetic step-by-step breakdowns verified against exact values.
- **Computational Complexity Distinction**: Distinguishes the $O(\sqrt{n})$ cost of computing a single recurrence value when history is known from the $O(N\sqrt{N})$ cost of generating the full sequence up to $N$, contrasting with the intractable exponential search space of naive enumeration.

### 📜 Module 3: Series-Product Identities & Generating Functions (Andrews Ch. 2, §2.1–2.2)
- **Formal Power Series in $\mathbb{Z}[[q]]$**: Evaluates exact polynomial products and quotients without floating-point precision loss.
- **Polynomial Coefficient Stabilization (Section 2.1)**: Demonstrates that expanding $M \ge N$ factors of an infinite product guarantees exact coefficients up to degree $N$.
- **Andrews Theorem 2.1 ($q$-Binomial Theorem) Corollaries**:
  - *Euler's Corollary 2.2*: $\sum_{n=0}^\infty \frac{q^n}{(q; q)_n} = \frac{1}{(q; q)_\infty} = \sum p(n) q^n$ (decomposes partitions by largest part).
  - *Euler's Corollary 2.3*: $\sum_{n=0}^\infty \frac{q^{n(n+1)/2}}{(q; q)_n} = (-q; q)_\infty = \sum p(D, n) q^n$ (decomposes distinct partitions into triangular staircases $\Delta_n$).
- **Euler's Odd-Distinct Algebraic Identity**: Proves algebraically that $\prod_{k=1}^\infty (1 + q^k) = \prod_{k=1}^\infty \frac{1}{1 - q^{2k-1}}$ via telescoping cancellation of even factors.
- **Durfee Square Series Expansion (Andrews eq. 2.2.9)**: Evaluates the series $\sum_{d=0}^{d_{\max}} \frac{q^{d^2}}{(q; q)_d^2}$. Dynamically computes the completeness threshold $d_{\max} \ge \lfloor\sqrt{N}\rfloor$, proving completeness for $n < (d_{\max}+1)^2$ and isolating deficits for higher degrees.

---

## 3. Quickstart & Local Execution

The entire laboratory runs as a single unified application with one command:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 4. Automated Mathematical Test Suite

Every mathematical algorithm and invariant is validated by automated tests in `pytest`:

```bash
python -m pytest tests/ -v
```

### Verified Evidence Levels:
1. **Software Unit Tests**: 52 automated tests in `pytest` verifying integer arithmetic, recursive enumeration, and involution invariants.
2. **Finite-Range Empirical Matching**: Complete equality checks across verified ranges (e.g. $n \le 35$ for Franklin cancellation, $n \le 20, m \le 6$ for Theorem 1.4).
3. **Independent Algorithm Cross-Checks**: Agreement between recursive generation, dynamic programming tables, and formal power series polynomial division.
4. **General Theorems**: Distinguishes computational verification from the general mathematical proofs provided by Euler, Franklin, Sylvester, and Andrews.

---

## 5. Repository Architecture

```
theory_of_partitions/
├── app.py                          # Single unified Streamlit entry point
├── partition_core/                 # Presentation-agnostic computational engine
│   ├── __init__.py                 # Public mathematical API
│   ├── enumeration.py              # Lexicographic partition generator & DP recurrence
│   ├── conjugation.py              # Ferrers matrices, transposition involution, Theorem 1.4
│   ├── franklin.py                 # Franklin slope/base, exceptional points, Euler verifier
│   ├── generating_functions.py     # Formal power series arithmetic, q-binomial, Durfee series
│   └── asymptotics.py              # Hardy-Ramanujan approximation & error analysis
├── ui/                             # Modular research-grade UI components
│   ├── styles.py                   # Scholarly research theme, native LaTeX containers
│   ├── diagrams.py                 # Clean Ferrers and Franklin Plotly renderers
│   ├── home_page.py                # Academic framework & deliverable matrix
│   ├── module_1_conjugation.py     # Module 1 Laboratory & Findings Dossier
│   ├── module_2_franklin.py        # Module 2 Laboratory & Findings Dossier
│   ├── module_3_series_identities.py # Module 3 Laboratory & Findings Dossier
│   └── theory_dossier.py           # Andrews bibliography, theorem catalog, live pytest runner
├── tests/                          # Automated pytest suite (52 tests passing)
│   ├── test_enumeration.py
│   ├── test_conjugation.py
│   ├── test_franklin.py
│   ├── test_asymptotics.py
│   └── test_generating_functions.py
├── reports/
│   ├── IP_Progress_Report.md       # Comprehensive academic progress report
│   └── IP_Progress_Report.tex      # LaTeX research report
├── .streamlit/
│   └── config.toml                 # Scholarly dark theme configuration
├── README.md                       # Complete documentation & deployment guide
└── requirements.txt
```

---

## 6. Primary Academic References

- **Andrews, George E.** (1976/1998). *The Theory of Partitions*. Cambridge University Press.
- **Euler, Leonhard** (1748). *Introductio in Analysin Infinitorum*.
- **Franklin, Fabian** (1881). *Sur le développement du produit infini $(1-x)(1-x^2)\dots$*. *Comptes Rendus*, 92.
- **Sylvester, James Joseph** (1882). *A Constructive Theory of Partitions*. *Amer. J. Math.*, 5(1).
- **Heine, Eduard** (1847). *Untersuchungen über die Reihe...*. *J. Reine Angew. Math.*, 34.
- **Hardy, Godfrey H., & Ramanujan, Srinivasa** (1918). *Asymptotic Formulae in Combinatory Analysis*. *Proc. London Math. Soc.*
- **Rademacher, Hans** (1937). *On the Partition Function $p(n)$*. *Proc. London Math. Soc.*

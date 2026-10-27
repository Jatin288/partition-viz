# PartitionViz: Computational Laboratory for the Theory of Partitions

An interactive computational mathematics framework for investigating theorems, combinatorial bijections, and generating-function identities from George E. Andrews, *The Theory of Partitions* (Cambridge University Press).

---

## 1. Academic Purpose & Research Philosophy

**PartitionViz** turns foundational results in partition theory into rigorous, interactive computational investigations. Rather than presenting decorative visuals, every laboratory module answers four core mathematical questions:

1. **What mathematical theorem are we investigating?** (Exact formulation from Andrews)
2. **What algorithm implements the mathematical mechanism?** (Bijections, involutions, formal power series)
3. **What do the computations demonstrate, and what deductions follow?** (Empirical invariants, parity cancellations, limit distributions)
4. **What has actually been established, and what remains unproved or open?** (Rigorous proof vs. finite-range verification)

---

## 2. Integrated Laboratory Modules

### 📐 Module 1: Ferrers Diagrams and Conjugation Duality (Andrews Ch. 1, §1.1–1.3)
- **Theorem 1.4 Duality**: Explores and proves through explicit bidirectional pairing that the number of partitions with $\le m$ parts equals the number of partitions with largest part $\le m$.
- **Transposition Dynamics**: Step-by-step visual reflection showing rows becoming columns.
- **Sylvester's Self-Conjugate Identity (Ch. 1, Ex. 8)**: Exact computational comparison showing that the number of self-conjugate partitions ($\lambda = \lambda'$) equals the number of partitions into distinct odd parts.
- **Durfee Square Decomposition**: Visual and combinatorial decomposition of a partition into a $d \times d$ square, right partition $\lambda_R$ ($\le d$ parts), and bottom partition $\lambda_B$ (parts $\le d$), proving $\sum \lambda = d^2 + \sum \lambda_R + \sum \lambda_B$.
- **Chapter 1 Generating Function Connection**: Demonstrates how each factor $\frac{1}{1 - q^k} = 1 + q^k + q^{2k} + \dots$ encodes part multiplicities.

### ⚡ Module 2: Franklin's Involution & Pentagonal Numbers (Andrews Ch. 1, §1.3, Thm 1.6)
- **Franklin's Sign-Reversing Involution (1881)**: Color-coded Ferrers diagram decomposition into Base $b$, Slope $s$, and Intersection points.
- **Exact Parity Cancellation**: Demonstrates why $p_e(D,n) - p_o(D,n) = 0$ for almost all $n$, and isolates the surviving residue $(-1)^k$ at generalized pentagonal numbers $\omega(\pm k) = \frac{3k^2 \mp k}{2}$.
- **Euler's Pentagonal Recurrence (Corollary 1.8)**: Evaluates $p(n) = \sum_{k \ge 1} (-1)^{k+1} [p(n - \omega(k)) + p(n - \omega(-k))]$, displaying arithmetic step-by-step breakdowns verified against exact values.
- **Complexity Audit**: Clarifies the difference between calculating a single recurrence value in $O(\sqrt{n})$ terms versus generating the full table up to $N$ in $O(N\sqrt{N})$ operations, contrasting with the intractable exponential search space of naive enumeration.

### 📜 Module 3: Series-Product Identities & Generating Functions (Andrews Ch. 2, §2.1–2.2)
- **Formal Power Series in $\mathbb{Z}[[q]]$**: Evaluates exact polynomial products and quotients without floating-point precision loss.
- **Polynomial Coefficient Stabilization**: Demonstrates that expanding $M \ge N$ factors of an infinite product guarantees exact coefficients up to degree $N$.
- **Euler's Odd-Distinct Algebraic Identity**: Proves algebraically that $\prod_{k=1}^\infty (1 + q^k) = \prod_{k=1}^\infty \frac{1}{1 - q^{2k-1}}$ via telescoping cancellation of even factors.
- **Durfee Square Series Expansion (Andrews eq. 2.2.9)**: Evaluates the series $\sum_{d=0}^\infty \frac{q^{d^2}}{(q; q)_d^2}$ and proves coefficient equality with $p(n)$ for all $n \le N$.

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

## 4. Streamlit Community Cloud Deployment Guide

PartitionViz is 100% deployment-ready for Streamlit Community Cloud:

1. **Push to GitHub**:
   Ensure all repository files (`app.py`, `partition_core/`, `ui/`, `tests/`, `requirements.txt`) are committed and pushed to your GitHub repository:
   ```bash
   git add .
   git commit -m "PartitionViz: Chapters 1 & 2 Complete"
   git push origin main
   ```
2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
   - Click **"New app"**.
   - Select your repository: `<your-username>/theory_of_partitions`.
   - Branch: `main`.
   - Main file path: `app.py`.
   - Click **"Deploy!"**.
3. **Why Deployment Succeeds Instantly**:
   - Zero hardcoded local file paths (all imports and resources use relative paths).
   - Minimal standard dependencies (`streamlit`, `plotly`, `pandas`, `pytest`).
   - No external databases, binary drivers, or background services required.

---

## 5. Automated Mathematical Test Suite

Every mathematical algorithm and invariant is validated by 50 automated tests in `pytest`:

```bash
python -m pytest tests/ -v
```

### Verified Invariants:
- Sum preservation across conjugation, Franklin's involution, and Durfee square decomposition.
- Exact involution properties: $(\lambda')' = \lambda$ and $\phi(\phi(\lambda)) = \lambda$.
- Strict distinctness preservation under Franklin's map.
- Parity alternation: $\ell(\phi(\lambda)) = \ell(\lambda) \pm 1$.
- Agreement between Euler's recurrence and exact partition counts up to $n=100$.
- Sylvester's self-conjugate identity agreement across all tested ranges.
- Algebraic equivalence between distinct-part and odd-part generating functions.
- Exact coefficient match between Andrews's Durfee square series and $p(n)$.

---

## 6. Repository Architecture

```
theory_of_partitions/
├── app.py                          # Single unified Streamlit entry point
├── partition_core/                 # Presentation-agnostic computational engine
│   ├── __init__.py                 # Public mathematical API
│   ├── enumeration.py              # Lexicographic partition generator & DP recurrence
│   ├── conjugation.py              # Ferrers matrices, transposition involution, Theorem 1.4
│   ├── franklin.py                 # Franklin slope/base, exceptional points, Euler verifier
│   ├── generating_functions.py     # Formal power series arithmetic, Durfee series, GF expansions
│   └── asymptotics.py              # Hardy-Ramanujan approximation & error analysis
├── ui/                             # Modular research-grade UI components
│   ├── styles.py                   # Scholarly research theme, native LaTeX containers
│   ├── diagrams.py                 # Clean Ferrers and Franklin diagram renderer
│   ├── home_page.py                # Academic framework & multi-month roadmap
│   ├── module_1_conjugation.py     # Module 1 Laboratory & Defensible Findings Dossier
│   ├── module_2_franklin.py        # Module 2 Laboratory & Defensible Findings Dossier
│   ├── module_3_series_identities.py # Module 3 Laboratory & Defensible Findings Dossier
│   └── theory_dossier.py           # Andrews bibliography, theorem catalog, in-app test runner
├── tests/                          # Automated pytest suite (50/50 tests passing)
│   ├── test_enumeration.py
│   ├── test_conjugation.py
│   ├── test_franklin.py
│   ├── test_asymptotics.py
│   └── test_generating_functions.py
├── reports/
│   ├── IP_Milestone_Report_Month_1.md  # Comprehensive academic milestone report
│   └── IP_Milestone_Report_Month_1.tex # Overleaf/LaTeX printable research report
├── README.md                       # Complete documentation & deployment guide
└── requirements.txt
```

---

## 7. Primary Academic References

- **Andrews, George E.** (1976/1998). *The Theory of Partitions*. Cambridge University Press.
- **Euler, Leonhard** (1748). *Introductio in Analysin Infinitorum*.
- **Franklin, Fabian** (1881). *Sur le développement du produit infini $(1-x)(1-x^2)\dots$*. *Comptes Rendus*, 92.
- **Sylvester, James Joseph** (1882). *A Constructive Theory of Partitions*. *Amer. J. Math.*, 5(1).
- **Hardy, Godfrey H., & Ramanujan, Srinivasa** (1918). *Asymptotic Formulae in Combinatory Analysis*. *Proc. London Math. Soc.*

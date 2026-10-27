"""
ui/theory_dossier.py
Academic Reference Dossier, Coverage Matrix, and Dynamic Verification Dashboard for PartitionViz.
Primary Reference: George E. Andrews, The Theory of Partitions (1976/1998).
"""
from __future__ import annotations
import sys
import re
import subprocess
import streamlit as st
import pandas as pd


def parse_pytest_output(stdout: str) -> dict:
    """Extract real test counts and execution time from pytest stdout."""
    passed = 0
    failed = 0
    skipped = 0
    duration = 0.0

    m_passed = re.search(r"(\d+)\s+passed", stdout)
    if m_passed:
        passed = int(m_passed.group(1))

    m_failed = re.search(r"(\d+)\s+failed", stdout)
    if m_failed:
        failed = int(m_failed.group(1))

    m_skipped = re.search(r"(\d+)\s+skipped", stdout)
    if m_skipped:
        skipped = int(m_skipped.group(1))

    m_time = re.search(r"in\s+([\d\.]+)s", stdout)
    if m_time:
        duration = float(m_time.group(1))

    return {
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "duration": duration,
        "total": passed + failed + skipped,
    }


def render_theory_dossier():
    st.markdown("""
    <div class="academic-hero">
      <div style="margin-bottom:0.6rem">
        <span class="academic-badge badge-blue">Academic Dossier</span>
        <span class="academic-badge badge-green">Andrews References</span>
        <span class="academic-badge badge-amber">Mathematical Verification</span>
      </div>
      <div class="academic-hero-title">Theoretical Foundations & Coverage Matrix</div>
      <div class="academic-hero-subtitle">
        Formal mathematical references, rigorous theorem coverage matrix,
        and dynamic live test verification for the PartitionViz Independent Project.
      </div>
    </div>
    """, unsafe_allow_html=True)

    tab_coverage, tab_theorems, tab_bib, tab_test_dash = st.tabs([
        "📊 Mathematical Coverage Matrix",
        "📐 Theorem Catalog",
        "📚 Primary Bibliography",
        "🧪 Dynamic Test Dashboard",
    ])

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 1: MATHEMATICAL COVERAGE MATRIX (ANDREWS CH. 1–2)
    # ═════════════════════════════════════════════════════════════════════════
    with tab_coverage:
        st.markdown("### Andrews Chapters 1–2: Mathematical Coverage Matrix")
        st.markdown("""
        In accordance with academic standards, results in PartitionViz are explicitly categorized by their verification status:
        `Implemented`, `Tested`, `Mathematically verified over a stated range`, `Proof documented`, `Partially implemented`, or `Not yet covered`.
        No result is marked complete merely because its interface or statement exists.
        """)

        coverage_data = [
            {
                "Result": "Definition 1.1",
                "Andrews Reference": "Ch. 1, §1.1, p. 1",
                "Mathematical Statement": "Partition of n, part sequence λ, part count r, sum preservation",
                "Treatment": "Interactive generator & lexicographic descent",
                "Verification": "pytest (test_enumeration.py)",
                "Range / Scope": "Exact for all n ≤ 25 (interactive); table up to n=100",
                "Status": "Implemented & Tested",
            },
            {
                "Result": "Theorem 1.1",
                "Andrews Reference": "Ch. 1, §1.1, p. 3",
                "Mathematical Statement": "Unrestricted partition generating function sum p(n) qⁿ = ∏ 1/(1-qᵏ)",
                "Treatment": "Formal polynomial product expansion & stabilization",
                "Verification": "pytest (test_generating_functions.py)",
                "Range / Scope": "Verified for n ≤ 30 against recursive p(n)",
                "Status": "Mathematically verified over stated range",
            },
            {
                "Result": "Corollary 1.2",
                "Andrews Reference": "Ch. 1, §1.1, p. 5",
                "Mathematical Statement": "Euler's theorem: p(D, n) = p(O, n) (distinct equals odd)",
                "Treatment": "Formal product cancellation & independent enumeration",
                "Verification": "pytest (test_enumeration.py, test_generating_functions.py)",
                "Range / Scope": "Exact for all n ≤ 30 across 4 independent methods",
                "Status": "Proof documented & Tested",
            },
            {
                "Result": "Theorem 1.4",
                "Andrews Reference": "Ch. 1, §1.2, p. 7",
                "Mathematical Statement": "Duality: p(≤ m parts, n) = p(max part ≤ m, n) via conjugation",
                "Treatment": "Ferrers matrix transposition & animated bijection",
                "Verification": "pytest (test_conjugation.py)",
                "Range / Scope": "Complete grid n ≤ 20, m ≤ 6 verified",
                "Status": "Implemented & Tested",
            },
            {
                "Result": "Example 8",
                "Andrews Reference": "Ch. 1, Ex. 8, p. 15",
                "Mathematical Statement": "Sylvester's identity: self-conjugate partitions equinumerous to distinct odd parts",
                "Treatment": "Hook-unfolding inspection and direct count comparison",
                "Verification": "pytest (test_conjugation.py)",
                "Range / Scope": "Verified for all n ≤ 25",
                "Status": "Proof documented & Tested",
            },
            {
                "Result": "Theorem 1.5",
                "Andrews Reference": "Ch. 1, §1.3, p. 10",
                "Mathematical Statement": "Euler's Pentagonal Number Theorem: ∏ (1-qᵏ) = 1 + sum (-1)ᵏ [q^{ω(k)} + q^{ω(-k)}]",
                "Treatment": "Formal product expansion & pentagonal exponent matching",
                "Verification": "pytest (test_generating_functions.py)",
                "Range / Scope": "Verified for n ≤ 35",
                "Status": "Mathematically verified over stated range",
            },
            {
                "Result": "Theorem 1.6",
                "Andrews Reference": "Ch. 1, §1.3, p. 11",
                "Mathematical Statement": "Franklin's combinatorial proof using base b and slope s on D(n)",
                "Treatment": "Color-coded Ferrers diagram decomposition & sign-reversing involution",
                "Verification": "pytest (test_franklin.py)",
                "Range / Scope": "Verified involution φ(φ(λ))=λ on all distinct partitions n ≤ 30",
                "Status": "Implemented & Tested",
            },
            {
                "Result": "Corollary 1.8",
                "Andrews Reference": "Ch. 1, §1.3, p. 12",
                "Mathematical Statement": "Euler's Pentagonal Recurrence for p(n) in O(N√N) operations",
                "Treatment": "Step-by-step arithmetic trace & DP table evaluation",
                "Verification": "pytest (test_enumeration.py)",
                "Range / Scope": "Exact agreement up to n=100 verified",
                "Status": "Implemented & Tested",
            },
            {
                "Result": "Formal Topology",
                "Andrews Reference": "Ch. 2, §2.1, pp. 17–19",
                "Mathematical Statement": "Coefficient stabilization in Z[[q]]: ∏_{k=1}^M (1+c_k qᵏ) ≡ ∏^∞ mod q^{M+1}",
                "Treatment": "Dynamic degree-by-degree stabilization explorer",
                "Verification": "pytest (test_generating_functions.py)",
                "Range / Scope": "Verified for M ≥ N up to degree N=30",
                "Status": "Proof documented & Tested",
            },
            {
                "Result": "Theorem 2.1",
                "Andrews Reference": "Ch. 2, §2.2, p. 17",
                "Mathematical Statement": "The q-Binomial Theorem: sum (a; q)_n / (q; q)_n tⁿ = (at; q)_∞ / (t; q)_∞",
                "Treatment": "Corollaries 2.2 and 2.3 series expansion & partition interpretation",
                "Verification": "pytest (test_generating_functions.py)",
                "Range / Scope": "Verified mod q^{N+1} for N ≤ 25",
                "Status": "Implemented & Tested",
            },
            {
                "Result": "Equation (2.2.9)",
                "Andrews Reference": "Ch. 2, §2.2, p. 28",
                "Mathematical Statement": "Durfee square series: sum p(n) qⁿ = sum q^{d²} / (q; q)_d²",
                "Treatment": "Ferrers geometric decomposition (d², λ_R, λ_B) & dynamic completeness",
                "Verification": "pytest (test_generating_functions.py)",
                "Range / Scope": "Exact for n ≤ 30 when d_max ≥ ⌊√N⌋; deficits dynamically isolated",
                "Status": "Implemented & Tested",
            },
            {
                "Result": "Theorem 2.2",
                "Andrews Reference": "Ch. 2, §2.2, p. 21",
                "Mathematical Statement": "Jacobi's Triple Product Identity: ∏ (1-q²ⁿ)(1+z q²ⁿ⁻¹)(1+z⁻¹ q²ⁿ⁻¹) = sum zⁿ q^{n²}",
                "Treatment": "Formal derivation from q-binomial theorem",
                "Verification": "Unimplemented in current release",
                "Range / Scope": "Outside declared scope of current release",
                "Status": "Not yet covered",
            },
        ]

        df_cov = pd.DataFrame(coverage_data)
        st.dataframe(df_cov, use_container_width=True, height=440)

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 2: THEOREM CATALOG
    # ═════════════════════════════════════════════════════════════════════════
    with tab_theorems:
        st.markdown("### Formal Theorem Catalog: Andrews Chapters 1 & 2")
        st.markdown(r"""
        | Reference | Name | Mathematical Formulation | Implementation Module |
        |---|---|---|---|
        | **Definition 1.1** | Partition of $n$ | $\lambda_1 \ge \dots \ge \lambda_r > 0$, $\sum \lambda_i = n$. | `partition_core.enumeration` |
        | **Section 1.2** | Ferrers Graph | Array of dots with $\lambda_i$ dots in row $i$. | `ui.diagrams` |
        | **Definition 1.8** | Conjugate Partition | $\lambda'_i = \#\{j : \lambda_j \ge i\}$, reflection across main diagonal. | `partition_core.conjugation` |
        | **Theorem 1.4** | Bounded Partitions Duality | $p(\le m\text{ parts}, n) = p(\text{max part}\le m, n)$. | Module 1 (Tab 3) |
        | **Ch. 1, Ex. 8** | Sylvester's Identity | $\#\{\lambda : \lambda = \lambda'\} = \#\{\lambda : \lambda_i \text{ distinct and odd}\}$. | Module 1 (Tab 4) |
        | **Theorem 1.5** | Pentagonal Number Theorem | $\prod_{k=1}^\infty (1 - q^k) = 1 + \sum_{k=1}^\infty (-1)^k [q^{\omega(k)} + q^{\omega(-k)}]$. | Module 2 (Tab 4) |
        | **Theorem 1.6** | Franklin's Involution | Sign-reversing map $\phi$ on $D(n)$ with fixed points only at $\omega(\pm k)$. | Module 2 (Tabs 2–3) |
        | **Corollary 1.8** | Euler's Recurrence | $p(n) = \sum_{k \ge 1} (-1)^{k+1} [p(n - \omega(k)) + p(n - \omega(-k))]$. | Module 2 (Tab 5) |
        | **Ch. 2, §2.1** | Formal Power Series | Truncation $\prod_{k=1}^M (1+c_k q^k) \equiv \prod_{k=1}^\infty \pmod{q^{M+1}}$ in $\mathbb{Z}[[q]]$. | Module 3 (Tab 1) |
        | **Theorem 2.1** | $q$-Binomial Theorem | $\sum_{n=0}^\infty \frac{(a; q)_n}{(q; q)_n} t^n = \frac{(at; q)_\infty}{(t; q)_\infty}$. | Module 3 (Tab 2) |
        | **Corollary 2.2** | Euler's 1st Identity | $\sum_{n=0}^\infty \frac{q^n}{(q; q)_n} = \frac{1}{(q; q)_\infty} = \sum p(n) q^n$ (by largest part). | Module 3 (Tab 2) |
        | **Corollary 2.3** | Euler's 2nd Identity | $\sum_{n=0}^\infty \frac{q^{n(n+1)/2}}{(q; q)_n} = (-q; q)_\infty = \sum p(D, n) q^n$ (by staircase). | Module 3 (Tab 2) |
        | **Corollary 1.2** | Euler's Odd-Distinct | $\prod_{k=1}^\infty (1 + q^k) = \prod_{k=1}^\infty \frac{1}{1 - q^{2k-1}}$. | Module 3 (Tab 3) |
        | **Eq. (2.2.9)** | Durfee Square Series | $\sum_{n=0}^\infty p(n) q^n = \sum_{d=0}^\infty \frac{q^{d^2}}{(q; q)_d^2}$. | Module 3 (Tab 4) |
        """)

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 3: PRIMARY BIBLIOGRAPHY
    # ═════════════════════════════════════════════════════════════════════════
    with tab_bib:
        st.markdown("### Primary Academic References")
        st.markdown(r"""
        1. **Andrews, George E.** (1976). *The Theory of Partitions*. Encyclopedia of Mathematics and Its Applications, Vol. 2.
           Reading, Mass.: Addison-Wesley. (Reissued by Cambridge University Press, 1998, ISBN 0-521-63766-X).
           *Primary text for Chapters 1, 2, 5, 10, and 11.*

        2. **Euler, Leonhard** (1748). *Introductio in Analysin Infinitorum*, Vol. 1. Marcum-Michaelem Bousquet, Lausanne.
           *Introduction of the partition generating function and pentagonal number theorem.*

        3. **Franklin, Fabian** (1881). *Sur le développement du produit infini $(1-x)(1-x^2)(1-x^3)\dots$*.
           *Comptes Rendus de l'Académie des Sciences*, Paris, 92, pp. 448–450.
           *Original geometric and combinatorial proof of Euler's pentagonal theorem via slope and base transposition.*

        4. **Sylvester, James Joseph** (1882). *A Constructive Theory of Partitions, Arranged in Three Acts, an Interact and an Exodion*.
           *American Journal of Mathematics*, 5(1), pp. 251–330.
           *Combinatorial proof connecting self-conjugate partitions to partitions into distinct odd parts.*

        5. **Heine, Eduard** (1847). *Untersuchungen über die Reihe $1 + \frac{(1-q^\alpha)(1-q^\beta)}{(1-q)(1-q^\gamma)} x + \dots$*.
           *Journal für die reine und angewandte Mathematik*, 34, pp. 285–328.
           *Systematic development of basic hypergeometric series and the q-binomial theorem.*

        6. **Hardy, Godfrey H., & Ramanujan, Srinivasa** (1918). *Asymptotic Formulae in Combinatory Analysis*.
           *Proceedings of the London Mathematical Society*, (2) 17, pp. 75–115.
           *Discovery of the circle method and asymptotic partition expansion.*

        7. **Rademacher, Hans** (1937). *On the Partition Function $p(n)$*.
           *Proceedings of the London Mathematical Society*, (2) 43, pp. 241–254.
           *Convergent exact series representation for $p(n)$.*
        """)

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 4: DYNAMIC LIVE TEST DASHBOARD
    # ═════════════════════════════════════════════════════════════════════════
    with tab_test_dash:
        st.markdown("### Dynamic Mathematical Test Execution Dashboard")
        st.markdown("""
        PartitionViz features a live test runner that executes the automated test suite directly in the host environment.
        Results are parsed dynamically from the `pytest` output without hard-coded assumptions.
        """)

        with st.container(border=True):
            st.markdown("#### Four Levels of Mathematical Evidence")
            st.markdown("""
            1. **Software Unit Tests Passed:** Confirms algorithms produce expected values without runtime crashes or type regressions.
            2. **Finite-Range Empirical Matching:** Verifies equality over a bounded integer range (e.g., $n \\le 35$); does not constitute a proof for all $n$.
            3. **Independent Algorithm Cross-Check:** Two distinct algorithmic implementations (e.g. recursive generation vs dynamic programming vs formal power series) yield identical results.
            4. **Mathematical Theorem Proved Generally:** Rigorous deductive proof establishing universal validity for all $n \\in \\mathbb{N}$ (e.g. Andrews, Euler, Franklin).
            """)

        if st.button("Execute Live Test Suite Now (pytest)", type="primary"):
            with st.spinner("Running pytest test suite..."):
                try:
                    proc = subprocess.run(
                        [sys.executable, "-m", "pytest", "tests/", "-v"],
                        capture_output=True,
                        text=True,
                        timeout=45,
                    )
                    metrics = parse_pytest_output(proc.stdout)

                    c_m1, c_m2, c_m3, c_m4 = st.columns(4)
                    with c_m1:
                        st.metric("Total Tests Collected", metrics["total"])
                    with c_m2:
                        st.metric("Tests Passed", metrics["passed"])
                    with c_m3:
                        st.metric("Tests Failed", metrics["failed"])
                    with c_m4:
                        st.metric("Execution Time", f"{metrics['duration']:.2f}s")

                    if proc.returncode == 0 and metrics["failed"] == 0 and metrics["passed"] > 0:
                        st.success(f"✅ Verified: All {metrics['passed']} mathematical unit tests executed and passed in {metrics['duration']:.2f}s.")
                    else:
                        st.error(f"⚠️ Test suite returned exit code {proc.returncode} with {metrics['failed']} failure(s).")

                    with st.expander("Inspect Raw pytest Stdout & Details", expanded=False):
                        st.code(proc.stdout, language="text")

                except Exception as ex:
                    st.error(f"Unable to execute pytest subprocess: {ex}")
        else:
            st.info("Click the button above to run the live test suite in real time. The parsed summary and execution metrics will appear above.")

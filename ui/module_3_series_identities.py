"""
ui/module_3_series_identities.py
Module 3: Series-Product Identities, Formal Power Series, and the q-Binomial Theorem.
Reference: George E. Andrews, The Theory of Partitions (1976/1998), Chapter 2, Sections 2.1–2.2.
"""
from __future__ import annotations
import math
import streamlit as st
import pandas as pd

from partition_core import (
    partition_count,
    partitions_distinct,
    partitions_odd,
    expand_euler_product,
    expand_partition_gf,
    expand_distinct_partitions_gf,
    expand_odd_partitions_gf,
    expand_durfee_square_series,
    durfee_completeness_bound,
    expand_euler_first_identity,
    expand_euler_second_identity,
)
from ui.styles import render_theorem_box, render_defensible_findings


def render_module_3():
    st.markdown("""
    <div class="academic-hero">
      <div style="margin-bottom:0.6rem">
        <span class="academic-badge badge-blue">Module 3</span>
        <span class="academic-badge badge-purple">Andrews Chapter 2, §2.1–2.2</span>
        <span class="academic-badge badge-green">Exact Series Arithmetic</span>
      </div>
      <div class="academic-hero-title">Series-Product Identities & Generating Functions</div>
      <div class="academic-hero-subtitle">
        Investigating formal power series in ℤ[[q]], coefficient stabilization,
        the <em>q</em>-binomial theorem corollaries, Euler's odd-distinct identity, and the Durfee square series.
      </div>
    </div>
    """, unsafe_allow_html=True)

    tab_stabilization, tab_q_binomial, tab_odd_dist, tab_durfee_series, tab_findings = st.tabs([
        "📜 1. Formal Power Series & Stabilization",
        "⚡ 2. Andrews Thm 2.1: q-Binomial Corollaries",
        "⚖️ 3. Euler's Odd-Distinct Identity",
        "⬛ 4. Durfee Series Expansion",
        "📑 5. Defensible Findings",
    ])

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 1: FORMAL POWER SERIES STABILIZATION IN Z[[q]]
    # ═════════════════════════════════════════════════════════════════════════
    with tab_stabilization:
        st.markdown("### 1. Formal Power Series Stabilization Principle in $\\mathbb{Z}[[q]]$")

        render_theorem_box(
            title="Formal Power Series Stabilization Principle",
            reference="Andrews, The Theory of Partitions, Chapter 2, Section 2.1 (Formal Power Series, pp. 17–19)",
            statement_md=(
                "Let $\\mathbb{Z}[[q]]$ be the ring of formal power series equipped with the $(q)$-adic metric. "
                "An infinite product $\\prod_{k=1}^\\infty (1 + c_k q^k)$ converges formally if the sequence of degrees "
                "increases strictly without bound. For any target degree $N$, expanding $M \\ge N$ factors produces "
                "the **exact integer coefficient** of $q^n$ for all $0 \\le n \\le N$ with zero truncation error, "
                "because subsequent factors $k > M$ can only contribute to powers $q^k$ with $k \\ge M+1 > N$:"
            ),
            equation_latex=r"\prod_{k=1}^\infty (1 + c_k q^k) \equiv \prod_{k=1}^M (1 + c_k q^k) \pmod{q^{M+1}}",
            border_color="#58a6ff",
        )

        col_g1, col_g2 = st.columns([1, 2])
        with col_g1:
            gf_type = st.selectbox(
                "Select Generating Function:",
                [
                    "Euler Pentagonal Product: ∏ (1 - q^k)",
                    "Partition Function: ∏ 1/(1 - q^k)",
                    "Distinct Partitions: ∏ (1 + q^k)",
                    "Odd Partitions: ∏ 1/(1 - q^(2k-1))",
                ],
            )
            target_deg = st.slider("Target polynomial degree N:", 5, 30, 20, key="m3_deg")
            factor_count = st.slider("Truncation factor count M:", 1, target_deg + 5, min(target_deg, 15), key="m3_factors")

            is_fully_stabilized = factor_count >= target_deg
            if is_fully_stabilized:
                st.success(f"✅ Factor count $M = {factor_count} \\ge N = {target_deg}$: All coefficients up to $q^{{{target_deg}}}$ have mathematically stabilized.")
            else:
                st.warning(f"⚠️ Factor count $M = {factor_count} < N = {target_deg}$: Coefficients for $n > {factor_count}$ may still change as more factors are included.")

        with col_g2:
            if "Euler Pentagonal" in gf_type:
                coeffs = expand_euler_product(factor_count, target_deg)
                st.markdown(f"**Expanded Truncation:** $\\prod_{{k=1}}^{{{factor_count}}} (1 - q^k) \\pmod{{q^{{{target_deg+1}}}}}$")
            elif "Partition Function" in gf_type:
                coeffs = expand_partition_gf(factor_count, target_deg)
                st.markdown(f"**Expanded Truncation:** $\\prod_{{k=1}}^{{{factor_count}}} \\frac{{1}}{{1 - q^k}} \\pmod{{q^{{{target_deg+1}}}}}$")
            elif "Distinct Partitions" in gf_type:
                coeffs = expand_distinct_partitions_gf(factor_count, target_deg)
                st.markdown(f"**Expanded Truncation:** $\\prod_{{k=1}}^{{{factor_count}}} (1 + q^k) \\pmod{{q^{{{target_deg+1}}}}}$")
            else:
                coeffs = expand_odd_partitions_gf(factor_count, target_deg)
                st.markdown(f"**Expanded Truncation:** $\\prod_{{k=1}}^{{{factor_count}}} \\frac{{1}}{{1 - q^{{2k-1}}}} \\pmod{{q^{{{target_deg+1}}}}}$")

            gf_table = []
            for deg in range(target_deg + 1):
                c_val = coeffs[deg]
                if "Partition Function" in gf_type:
                    exact = partition_count(deg)
                    is_stab = deg <= factor_count
                elif "Distinct" in gf_type:
                    exact = len(partitions_distinct(deg))
                    is_stab = deg <= factor_count
                elif "Odd" in gf_type:
                    exact = len(partitions_odd(deg))
                    is_stab = deg <= 2 * factor_count - 1
                else:
                    wp_match = False
                    expected_c = 0
                    for k in range(1, deg + 2):
                        if k * (3 * k - 1) // 2 == deg:
                            expected_c = 1 if k % 2 == 0 else -1
                            break
                        if k * (3 * k + 1) // 2 == deg:
                            expected_c = 1 if k % 2 == 0 else -1
                            break
                    exact = 1 if deg == 0 else expected_c
                    is_stab = deg <= factor_count

                gf_table.append({
                    "Degree n": deg,
                    "Truncated Coeff [qⁿ]": c_val,
                    "Theoretical Limit": exact,
                    "Discrepancy": c_val - exact,
                    "Status": "✅ Stabilized" if is_stab and c_val == exact else ("⚠️ Pending factors" if not is_stab else "❌ Mismatch"),
                })

            st.dataframe(pd.DataFrame(gf_table), use_container_width=True, height=320)

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 2: ANDREWS THEOREM 2.1 (q-BINOMIAL THEOREM) & EULER COROLLARIES
    # ═════════════════════════════════════════════════════════════════════════
    with tab_q_binomial:
        st.markdown("### 2. Andrews Theorem 2.1: The $q$-Binomial Theorem & Euler's Partition Corollaries")

        render_theorem_box(
            title="Andrews Theorem 2.1 (The q-Binomial Theorem)",
            reference="Andrews, The Theory of Partitions, Chapter 2, Section 2.2, p. 17 (Cauchy 1843, Heine 1847)",
            statement_md=(
                "For complex numbers $|q| < 1$ and $|t| < 1$, the fundamental $q$-analog of the binomial theorem states:"
            ),
            equation_latex=r"\sum_{n=0}^\infty \frac{(a; q)_n}{(q; q)_n} t^n = \frac{(at; q)_\infty}{(t; q)_\infty}, \quad \text{where } (a; q)_n = \prod_{j=0}^{n-1} (1 - a q^j)",
            border_color="#7ee787",
        )

        st.markdown("""
        Andrews deduces two cornerstone partition-generating identities as limiting corollaries of Theorem 2.1:
        """)

        col_q1, col_q2 = st.columns(2)
        with col_q1:
            with st.container(border=True):
                st.markdown("#### Corollary 2.2 (Euler, 1748)")
                st.markdown("Set $a = 0$ in Theorem 2.1:")
                st.markdown(
                    "Setting $t = q$ yields:\n\n"
                    r"$$\sum_{n=0}^\infty \frac{q^n}{(q; q)_n} = \frac{1}{(q; q)_\infty} = \sum_{k=0}^\infty p(k) q^k$$"
                    "\n\n**Combinatorial Meaning:** Each term $\\frac{q^n}{(q; q)_n}$ generates partitions whose **largest part is equal to $n$**."
                )

        with col_q2:
            with st.container(border=True):
                st.markdown("#### Corollary 2.3 (Euler, 1748)")
                st.markdown("Replace $t \\to -t/a$ and take $a \\to \\infty$:")
                st.latex(r"\sum_{n=0}^\infty \frac{q^{n(n-1)/2} t^n}{(q; q)_n} = (-t; q)_\infty")
                st.markdown(
                    "Setting $t = q$ yields:\n\n"
                    r"$$\sum_{n=0}^\infty \frac{q^{n(n+1)/2}}{(q; q)_n} = (-q; q)_\infty = \sum_{k=0}^\infty p(D, k) q^k$$"
                    "\n\n**Combinatorial Meaning:** Partitions into $n$ distinct parts decompose into a triangular staircase $\\Delta_n = n(n+1)/2$ plus at most $n$ parts."
                )

        st.markdown("#### Interactive Verification of Corollaries 2.2 and 2.3")
        col_c_sel, col_c_view = st.columns([1, 2])
        with col_c_sel:
            selected_cor = st.radio(
                "Select Identity to Expand:",
                [
                    "Corollary 2.2: sum qⁿ / (q; q)ₙ  ⟶  p(n) (by largest part)",
                    "Corollary 2.3: sum q^{n(n+1)/2} / (q; q)ₙ  ⟶  p(D, n) (by staircase)",
                ],
            )
            c_deg = st.slider("Target degree N:", 5, 25, 15, key="m3_cor_deg")
            c_terms = st.slider("Max summation index n summed:", 1, c_deg, min(c_deg, 10), key="m3_cor_terms")

        with col_c_view:
            if "Corollary 2.2" in selected_cor:
                cor_poly = expand_euler_first_identity(c_terms, c_deg)
                cor_records = []
                for k in range(c_deg + 1):
                    exact_val = partition_count(k)
                    poly_val = cor_poly[k]
                    cor_records.append({
                        "Degree k": k,
                        "Series Coeff [q^k]": poly_val,
                        "Exact p(k)": exact_val,
                        "Difference": poly_val - exact_val,
                        "Status": "✅ Exact" if poly_val == exact_val else f"Missing parts n > {c_terms}",
                    })
                st.dataframe(pd.DataFrame(cor_records), use_container_width=True, height=280)
                st.caption(f"Note: Summing up to n = {c_terms} accounts for all partitions with largest part ≤ {c_terms}.")
            else:
                cor_poly = expand_euler_second_identity(c_terms, c_deg)
                cor_records = []
                for k in range(c_deg + 1):
                    exact_val = len(partitions_distinct(k))
                    poly_val = cor_poly[k]
                    cor_records.append({
                        "Degree k": k,
                        "Series Coeff [q^k]": poly_val,
                        "Exact |D(k)|": exact_val,
                        "Difference": poly_val - exact_val,
                        "Status": "✅ Exact" if poly_val == exact_val else f"Missing lengths n > {c_terms}",
                    })
                st.dataframe(pd.DataFrame(cor_records), use_container_width=True, height=280)
                st.caption(f"Note: Summing up to n = {c_terms} accounts for all distinct-part partitions with at most {c_terms} parts.")

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 3: EULER'S ODD-DISTINCT IDENTITY
    # ═════════════════════════════════════════════════════════════════════════
    with tab_odd_dist:
        st.markdown("### 3. Euler's Odd-Distinct Identity: Formal Product Factorization")

        render_theorem_box(
            title="Andrews Corollary 1.2 & Section 2.2",
            reference="The Theory of Partitions, pp. 5, 26",
            statement_md=(
                "**Euler's Theorem:** The number of partitions of $n$ into distinct parts equals the number "
                "of partitions of $n$ into odd parts. The formal power series proof follows by substituting $(1 + q^k) = \\frac{1 - q^{2k}}{1 - q^k}$ "
                "and cancelling all even factors:"
            ),
            equation_latex=r"\prod_{k=1}^\infty (1 + q^k) = \prod_{k=1}^\infty \frac{1 - q^{2k}}{1 - q^k} = \prod_{k=1}^\infty \frac{1}{1 - q^{2k-1}}",
            border_color="#7ee787",
        )

        n_range_e = st.slider("Verify algebraic coefficient agreement up to n =", 5, 30, 20, key="m3_euler_n")
        distinct_p = expand_distinct_partitions_gf(n_range_e, n_range_e)
        odd_p = expand_odd_partitions_gf(n_range_e, n_range_e)

        comp_rows = []
        all_passed = True
        for n in range(n_range_e + 1):
            c_dist = distinct_p[n]
            c_odd = odd_p[n]
            d_count = len(partitions_distinct(n))
            o_count = len(partitions_odd(n))
            match = (c_dist == c_odd == d_count == o_count)
            if not match:
                all_passed = False
            comp_rows.append({
                "n": n,
                "Distinct GF [qⁿ]": c_dist,
                "Odd GF [qⁿ]": c_odd,
                "|D(n)| Enumerated": d_count,
                "|O(n)| Enumerated": o_count,
                "Cross-Check Match": "✅ Identical" if match else "❌ Mismatch",
            })

        st.dataframe(pd.DataFrame(comp_rows), use_container_width=True, height=320)
        if all_passed:
            st.success(f"✅ Algebraic identity verified: All {n_range_e + 1} coefficients agree identically across both product expansions and independent combinatorial enumerations.")
        else:
            st.error("Discrepancy detected across the test range.")

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 4: DURFEE SQUARE SERIES EXPANSION & DYNAMIC COMPLETENESS
    # ═════════════════════════════════════════════════════════════════════════
    with tab_durfee_series:
        st.markdown("### 4. Durfee Square Series Expansion for $p(n)$")

        render_theorem_box(
            title="Andrews Section 2.2, eq. (2.2.9)",
            reference="The Theory of Partitions, p. 28",
            statement_md=(
                "Andrews derives the fundamental series-product partition identity by partitioning each Ferrers diagram "
                "by its Durfee square of side $d = 0, 1, 2, \\dots$:"
            ),
            equation_latex=r"\sum_{n=0}^\infty p(n) q^n = \sum_{d=0}^\infty \frac{q^{d^2}}{(q; q)_d^2} = 1 + \frac{q}{(1-q)^2} + \frac{q^4}{(1-q)^2(1-q^2)^2} + \dots",
            border_color="#f0883e",
        )

        col_d1, col_d2 = st.columns([1, 2])
        with col_d1:
            max_deg_d = st.slider("Polynomial degree N:", 5, 30, 20, key="m3_durfee_deg")
            max_d_terms = st.slider("Maximum Durfee side d summed:", 0, 6, 3, key="m3_durfee_d")

            poly_durfee = expand_durfee_square_series(max_d_terms, max_deg_d)
            bound_info = durfee_completeness_bound(max_d_terms, max_deg_d)

            st.markdown(f"""
            <div class="metric-box">
              <div class="metric-box-val">{max_d_terms}</div>
              <div class="metric-box-lbl">Max Durfee Side d Summed</div>
            </div>
            """, unsafe_allow_html=True)

            if bound_info["is_complete"]:
                st.success(
                    f"✅ **Complete Expansion**: Since $d_{{\\max}} = {max_d_terms} \\ge \\lfloor\\sqrt{{{max_deg_d}}}\\rfloor = {bound_info['min_required_d']}$, "
                    f"every partition of $n \\le {max_deg_d}$ has Durfee side $d \\le {max_d_terms}$. The coefficients are exact for all $0 \\le n \\le {max_deg_d}$."
                )
            else:
                st.warning(
                    f"⚠️ **Truncated Expansion (Incomplete)**: Since $d_{{\\max}} = {max_d_terms} < \\lfloor\\sqrt{{{max_deg_d}}}\\rfloor = {bound_info['min_required_d']}$, "
                    f"this summation is exact **only for $0 \\le n \\le {bound_info['exact_up_to_degree']}$**.\n\n"
                    f"For $n \\ge {bound_info['first_incomplete_degree']}$, partitions whose Durfee square has side $d \\ge {max_d_terms + 1}$ are omitted, resulting in strict deficits.",
                    icon="⚠️",
                )

        with col_d2:
            st.markdown("#### Comparison of Durfee Series Coefficients vs Exact $p(n)$")
            durfee_records = []
            for deg in range(max_deg_d + 1):
                c_durfee = poly_durfee[deg]
                exact_pn = partition_count(deg)
                diff = c_durfee - exact_pn
                is_exact = (diff == 0)

                durfee_records.append({
                    "Degree n": deg,
                    "Durfee Series [qⁿ]": c_durfee,
                    "Exact p(n)": exact_pn,
                    "Discrepancy": diff,
                    "Status": "✅ Exact" if is_exact else f"Deficit: {diff} (missing d ≥ {max_d_terms + 1})",
                })

            st.dataframe(pd.DataFrame(durfee_records), use_container_width=True, height=330)

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 5: DEFENSIBLE FINDINGS
    # ═════════════════════════════════════════════════════════════════════════
    with tab_findings:
        render_defensible_findings(
            module_title="Module 3 — Series-Product Identities (Andrews Chapter 2)",
            questions_md=(
                "1. How does the formal power series topology in $\\mathbb{Z}[[q]]$ establish that truncated products match exact partition counts up to degree $N$?\n\n"
                "2. How does Andrews's Theorem 2.1 (the $q$-binomial theorem) specialize into Euler's corollaries for partition generating functions?\n\n"
                "3. What exact completeness threshold guarantees that the Durfee square series $\\sum_{d=0}^{d_{\\max}} \\frac{q^{d^2}}{(q; q)_d^2}$ matches $p(n)$?"
            ),
            foundation_md=(
                "George E. Andrews, *The Theory of Partitions* (Cambridge University Press), Chapter 2, "
                "Section 2.1 (Formal Power Series Topology, pp. 17–19), "
                "Section 2.2, Theorem 2.1 ($q$-Binomial Theorem, p. 17), Corollaries 2.2 & 2.3 (Euler's identities, p. 19), "
                "and eq. (2.2.9) (Durfee Square Expansion, p. 28)."
            ),
            method_md=(
                "Evaluated using exact integer polynomial algebra in $\\mathbb{Z}[q] / (q^{N+1})$ via synthetic convolution and division. "
                "No floating-point approximations or rounding errors are present. "
                "Truncations are cross-checked against independent recursive partition counts and exact tables."
            ),
            deductions_md=(
                "- **Formal Power Series Stabilization:** In $\\mathbb{Z}[[q]]$, expanding $M \\ge N$ factors produces exact coefficients "
                "for all $0 \\le n \\le N$ because factors with index $k > M$ have valuation $v(q^k) = k > N$.\n\n"
                "- **q-Binomial Specializations:** Setting $a = 0, t = q$ in Theorem 2.1 recovers the partition generating function sorted by largest part. "
                "Taking $a \\to \\infty, t = q$ yields distinct partitions sorted by triangular staircase $\\Delta_n = n(n+1)/2$.\n\n"
                "- **Dynamic Durfee Completeness:** Because the Durfee square side satisfies $d^2 \\le n$, summing up to $d_{\\max}$ captures all partitions "
                "of $n$ whenever $(d_{\\max} + 1)^2 > n$. For $n \\ge (d_{\\max} + 1)^2$, coefficients exhibit strict deficits equal to the count of partitions with $d > d_{\\max}$."
            ),
            validation_md=(
                "Verified by automated unit tests in `tests/test_generating_functions.py`: "
                "formal power series stabilization, $q$-binomial Euler corollaries, Euler odd-distinct identity, and Durfee completeness bounds."
            ),
            limitations_md=(
                "Computations represent formal polynomial expansions in $\\mathbb{Z}[q] / (q^{N+1})$. "
                "They verify algebraic coefficient equalities over finite degree ranges, but do not replace analytic convergence proofs in $|q| < 1$."
            ),
        )

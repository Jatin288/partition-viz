"""
ui/module_1_conjugation.py
Module 1: Ferrers Diagrams, Conjugation Duality, Sylvester's Theorem, and Durfee Squares.
Reference: George E. Andrews, The Theory of Partitions (1976/1998), Chapter 1, Sections 1.1–1.3.
"""
from __future__ import annotations
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from partition_core import (
    generate_partitions,
    partition_count,
    partitions_distinct,
    conjugate,
    conjugation_animation_frames,
    verify_theorem_1_4,
    partitions_at_most_m_parts,
    partitions_max_part,
    durfee_decomposition,
    expand_partition_gf,
    Partition,
)
from ui.diagrams import render_ferrers_diagram, partition_to_str
from ui.styles import render_theorem_box, render_defensible_findings


def render_module_1():
    st.markdown("""
    <div class="academic-hero">
      <div style="margin-bottom:0.6rem">
        <span class="academic-badge badge-blue">Module 1</span>
        <span class="academic-badge badge-blue">Andrews Ch. 1, §1.1–1.3</span>
        <span class="academic-badge badge-green">Verified Duality</span>
      </div>
      <div class="academic-hero-title">Ferrers Diagrams & Conjugation Duality</div>
      <div class="academic-hero-subtitle">
        Investigating the geometric involution of Ferrers diagrams, Andrews's Theorem 1.4,
        Sylvester's self-conjugate identity, and Durfee square decompositions.
      </div>
    </div>
    """, unsafe_allow_html=True)

    tab_explore, tab_conj, tab_thm14, tab_sylvester, tab_durfee, tab_gf, tab_findings = st.tabs([
        "📐 1. Partition Explorer",
        "🔄 2. Conjugation Map",
        "⚖️ 3. Theorem 1.4 Duality",
        "🪞 4. Sylvester's Theorem",
        "⬛ 5. Durfee Decomposition",
        "📜 6. Generating Functions",
        "📑 7. Defensible Findings",
    ])

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 1: PARTITION EXPLORER
    # ═════════════════════════════════════════════════════════════════════════
    with tab_explore:
        st.markdown("### 1. Partition Enumeration & Lexicographic Inspection")

        render_theorem_box(
            title="Definition 1.1",
            reference="Andrews, The Theory of Partitions, p. 1",
            statement_md=(
                "A **partition** of a positive integer $n$ is a finite non-increasing sequence of positive integers "
                "$\\lambda = (\\lambda_1, \\lambda_2, \\dots, \\lambda_r)$ such that "
                "$\\sum_{i=1}^r \\lambda_i = n$. The $\\lambda_i$ are called the **parts**, and "
                "$r = \\ell(\\lambda)$ denotes the **number of parts** (length)."
            ),
            equation_latex=r"n = \lambda_1 + \lambda_2 + \dots + \lambda_r, \quad \lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_r > 0",
            border_color="#58a6ff",
        )

        col_n, col_stats = st.columns([1, 2])
        with col_n:
            n_in = st.slider("Select integer n:", min_value=1, max_value=25, value=7, key="m1_n")
            all_p = generate_partitions(n_in)
            total_pn = len(all_p)

            st.markdown(f"""
            <div class="metric-box">
              <div class="metric-box-val">{total_pn}</div>
              <div class="metric-box-lbl">Exact Partition Count p({n_in})</div>
            </div>
            """, unsafe_allow_html=True)

            p_labels = [partition_to_str(p) for p in all_p]
            sel_idx = st.selectbox("Select partition λ to inspect:", range(len(p_labels)), format_func=lambda i: p_labels[i])
            chosen_lam = all_p[sel_idx]

        with col_stats:
            fig_lam = render_ferrers_diagram(
                chosen_lam,
                title=f"Ferrers Graph of λ = {partition_to_str(chosen_lam)} (Sum = {sum(chosen_lam)})"
            )
            st.plotly_chart(fig_lam, use_container_width=True)

            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Total Sum n", sum(chosen_lam))
            with m2:
                st.metric("Number of Parts ℓ(λ)", len(chosen_lam))
            with m3:
                st.metric("Largest Part λ₁", chosen_lam[0])

        with st.expander(f"Inspect all {total_pn} partitions of {n_in} (Lexicographic Order)"):
            chips_html = "".join(
                f'<span class="partition-chip {"partition-chip-active" if p == chosen_lam else ""}">{partition_to_str(p)}</span>'
                for p in all_p
            )
            st.markdown(chips_html, unsafe_allow_html=True)

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 2: CONJUGATION MAP
    # ═════════════════════════════════════════════════════════════════════════
    with tab_conj:
        st.markdown("### 2. The Conjugation Involution: Rows into Columns")

        render_theorem_box(
            title="Definition 1.8",
            reference="Andrews, The Theory of Partitions, p. 7",
            statement_md=(
                "If $\\lambda = (\\lambda_1, \\dots, \\lambda_r)$ is a partition, the **conjugate partition** "
                "$\\lambda' = (\\lambda'_1, \\dots, \\lambda'_m)$ is defined by setting $\\lambda'_i$ equal to the "
                "number of parts of $\\lambda$ that are $\\ge i$. Geometrically, the Ferrers diagram of $\\lambda'$ "
                "is the reflection of the Ferrers diagram of $\\lambda$ across its main diagonal."
            ),
            equation_latex=r"\lambda'_i = \#\{ j : \lambda_j \ge i \}",
            border_color="#58a6ff",
        )

        col_c_in, col_c_fig = st.columns([1, 2])
        with col_c_in:
            user_raw = st.text_input("Enter partition (parts descending):", value="5, 3, 3, 1", key="m1_conj_in")
            try:
                lam_c = tuple(int(x.strip()) for x in user_raw.replace(",", " ").split() if x.strip())
                if any(lam_c[i] < lam_c[i+1] for i in range(len(lam_c)-1)) or any(p <= 0 for p in lam_c):
                    st.error("Parts must be positive integers in non-increasing order.")
                    st.stop()
            except ValueError:
                st.error("Invalid integer input.")
                st.stop()

            conj_c = conjugate(lam_c)
            double_conj = conjugate(conj_c)

            st.markdown("#### Mathematical Invariant Checks")
            sum_ok = sum(lam_c) == sum(conj_c)
            inv_ok = double_conj == lam_c
            dual_rows_ok = len(conj_c) == lam_c[0]
            dual_cols_ok = conj_c[0] == len(lam_c)

            st.markdown(f"- {'✅' if sum_ok else '❌'} **Sum Preserved**: $\\sum \\lambda = \\sum \\lambda' = {sum(lam_c)}$")
            st.markdown(f"- {'✅' if inv_ok else '❌'} **Exact Involution**: $(\\lambda')' = \\lambda$")
            st.markdown(f"- {'✅' if dual_rows_ok else '❌'} **Length Dual**: $\\ell(\\lambda') = \\lambda_1 = {lam_c[0]}$")
            st.markdown(f"- {'✅' if dual_cols_ok else '❌'} **Max Part Dual**: $\\lambda'_1 = \\ell(\\lambda) = {len(lam_c)}$")

        with col_c_fig:
            fc1, fc2 = st.columns(2)
            with fc1:
                st.plotly_chart(render_ferrers_diagram(lam_c, title=f"Original λ = {partition_to_str(lam_c)}"), use_container_width=True)
            with fc2:
                st.plotly_chart(render_ferrers_diagram(conj_c, title=f"Conjugate λ' = {partition_to_str(conj_c)}", color_dots="#7ee787"), use_container_width=True)

        st.markdown("#### Step-by-Step Transposition Animation")
        frames = conjugation_animation_frames(lam_c)
        step_idx = st.slider("Transposition step (reading columns as conjugate rows):", 0, len(frames)-1, 0, key="m1_step")
        cur_frame = frames[step_idx]

        st.caption(f"**Step {step_idx}/{len(frames)-1}**: {cur_frame['label']}")
        c_af1, c_af2 = st.columns(2)
        with c_af1:
            st.plotly_chart(
                render_ferrers_diagram(lam_c, title=f"Reading λ (Col {cur_frame['highlighted_col']})", highlight_col=cur_frame['highlighted_col']),
                use_container_width=True
            )
        with c_af2:
            st.plotly_chart(
                render_ferrers_diagram(cur_frame['conjugate_so_far'], title=f"Building λ' = {partition_to_str(cur_frame['conjugate_so_far'])}", color_dots="#7ee787"),
                use_container_width=True
            )

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 3: THEOREM 1.4 DUALITY
    # ═════════════════════════════════════════════════════════════════════════
    with tab_thm14:
        st.markdown("### 3. Andrews Theorem 1.4: Restricted Partition Bijection")

        render_theorem_box(
            title="Theorem 1.4",
            reference="Andrews, The Theory of Partitions, p. 8",
            statement_md=(
                "For any positive integers $n$ and $m$, the number of partitions of $n$ into **at most $m$ parts** "
                "equals the number of partitions of $n$ in which **no part exceeds $m$**."
            ),
            equation_latex=r"p(\le m\text{ parts}, n) = p(\text{largest part} \le m, n)",
            border_color="#58a6ff",
        )

        st.markdown("""
        > **Combinatorial Proof Insight:** Conjugation $\\lambda \\mapsto \\lambda'$ is an explicit bijection between the two sets.
        > If $\\ell(\\lambda) \\le m$, the Ferrers diagram has at most $m$ rows, so its reflection has at most $m$ columns,
        > which means $\\lambda'_1 \\le m$.
        """)

        t_c1, t_c2 = st.columns([1, 2])
        with t_c1:
            n_t = st.slider("Integer n:", 1, 25, 10, key="t14_n")
            m_t = st.slider("Bound m:", 1, n_t, min(4, n_t), key="t14_m")

            res_t = verify_theorem_1_4(n_t, m_t, partitions_at_most_m_parts, partitions_max_part)
            cnt_at_most = res_t["count_at_most_m_parts"]
            cnt_max_part = res_t["count_max_part_m"]

            st.markdown(f"""
            <div class="metric-box">
              <div class="metric-box-val">{cnt_at_most}</div>
              <div class="metric-box-lbl">Partitions of {n_t} with ≤ {m_t} parts</div>
            </div>
            <br>
            <div class="metric-box">
              <div class="metric-box-val">{cnt_max_part}</div>
              <div class="metric-box-lbl">Partitions of {n_t} with max part ≤ {m_t}</div>
            </div>
            """, unsafe_allow_html=True)

            if res_t["verified"]:
                st.success(f"✅ Verified: Both counts equal {cnt_at_most}. Difference = 0.")

        with t_c2:
            st.markdown("#### Explicit Bidirectional Pairing Table")
            p_left = res_t["partitions_at_most_m_parts"]
            p_right_set = set(res_t["partitions_max_part_m"])

            rows_table = []
            for lam in p_left:
                c_lam = conjugate(lam)
                rows_table.append({
                    "Partition λ (≤ m parts)": partition_to_str(lam),
                    "Length ℓ(λ)": len(lam),
                    "Conjugate λ'": partition_to_str(c_lam),
                    "Max Part of λ'": c_lam[0] if c_lam else 0,
                    "In Dual Set?": "✅ Yes" if c_lam in p_right_set else "❌ No",
                })
            st.dataframe(pd.DataFrame(rows_table), use_container_width=True, height=320)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown("#### Exhaustive Verification Grid (n = 1 .. 20, m = 1 .. 6)")
        matrix_data = []
        for nn in range(1, 21):
            row_dict = {"n": nn}
            for mm in range(1, 7):
                if mm <= nn:
                    r = verify_theorem_1_4(nn, mm, partitions_at_most_m_parts, partitions_max_part)
                    row_dict[f"m={mm}"] = f"{r['count_at_most_m_parts']} ✓" if r["verified"] else "FAIL"
                else:
                    row_dict[f"m={mm}"] = "—"
            matrix_data.append(row_dict)
        st.dataframe(pd.DataFrame(matrix_data).set_index("n"), use_container_width=True)

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 4: SYLVESTER'S THEOREM
    # ═════════════════════════════════════════════════════════════════════════
    with tab_sylvester:
        st.markdown("### 4. Sylvester's Theorem: Fixed Points of Conjugation")

        render_theorem_box(
            title="Sylvester's Theorem (1882)",
            reference="Andrews, The Theory of Partitions, Chapter 1, Example 8, p. 17",
            statement_md=(
                "A partition is **self-conjugate** if $\\lambda = \\lambda'$ (its Ferrers diagram is symmetric across "
                "the main diagonal).<br>"
                "**Theorem:** For every positive integer $n$, the number of self-conjugate partitions of $n$ "
                "equals the number of partitions of $n$ into **distinct odd parts**."
            ),
            equation_latex=r"\#\{\lambda \vdash n : \lambda = \lambda'\} = \#\{\mu \vdash n : \mu_1 > \mu_2 > \dots > 0, \; \mu_i \text{ odd}\}",
            border_color="#d2a8ff",
        )

        st.markdown("""
        > **Combinatorial Correspondence:** For each dot $(i, i)$ on the diagonal of a self-conjugate Ferrers diagram,
        > the $i$-th **hook** consists of the dot $(i, i)$, the dots in row $i$ to its right, and the dots in column $i$ below it.
        > Because $\\lambda = \\lambda'$, the right arm and bottom leg have equal length $h_i$, so the hook has length $2h_i + 1$ (odd).
        > Since parts strictly decrease, the hook lengths are strictly distinct odd numbers!
        """)

        sc_col1, sc_col2 = st.columns([1, 1])
        with sc_col1:
            st.markdown("#### Exact Computation: Self-Conjugate vs Distinct Odd")
            max_n_sc = st.slider("Compute range up to n:", 10, 40, 25, key="sc_slider")

            sc_records = []
            for nn in range(1, max_n_sc + 1):
                all_p = generate_partitions(nn)
                sc_parts = [p for p in all_p if conjugate(p) == p]
                dist_parts = partitions_distinct(nn)
                dist_odd_parts = [p for p in dist_parts if all(part % 2 == 1 for part in p)]

                sc_records.append({
                    "n": nn,
                    "Total p(n)": len(all_p),
                    "Self-Conjugate": len(sc_parts),
                    "Distinct Odd": len(dist_odd_parts),
                    "Equal?": "✅" if len(sc_parts) == len(dist_odd_parts) else "❌",
                    "SC Proportion": f"{(len(sc_parts)/len(all_p))*100:.1f}%",
                })
            df_sc = pd.DataFrame(sc_records)
            st.dataframe(df_sc[["n", "Total p(n)", "Self-Conjugate", "Distinct Odd", "Equal?", "SC Proportion"]], use_container_width=True, height=330)

        with sc_col2:
            st.markdown("#### Self-Conjugate Partition Hook Inspector")
            n_hook = st.slider("Inspect self-conjugate partitions for n:", 1, 30, 9, key="hook_n")
            all_p_hook = generate_partitions(n_hook)
            sc_list = [p for p in all_p_hook if conjugate(p) == p]

            if sc_list:
                sc_choice = st.selectbox("Select self-conjugate partition:", [partition_to_str(p) for p in sc_list])
                chosen_sc = sc_list[[partition_to_str(p) for p in sc_list].index(sc_choice)]

                # Compute hooks
                hooks = []
                for i in range(len(chosen_sc)):
                    if chosen_sc[i] > i:
                        arm = chosen_sc[i] - 1 - i
                        leg = sum(1 for p in chosen_sc if p > i) - 1 - i
                        hooks.append(1 + arm + leg)

                st.markdown(f"**Self-Conjugate Partition $\\lambda$**: `{partition_to_str(chosen_sc)}`")
                st.markdown(f"**Unfolded Distinct Odd Parts $\\mu$**: `{tuple(hooks)}` (Sum = {sum(hooks)})")
                st.plotly_chart(render_ferrers_diagram(chosen_sc, title=f"Self-Conjugate Ferrers Graph λ = {partition_to_str(chosen_sc)}"), use_container_width=True)
            else:
                st.info(f"No self-conjugate partitions exist for n = {n_hook}.")

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 5: DURFEE DECOMPOSITION
    # ═════════════════════════════════════════════════════════════════════════
    with tab_durfee:
        st.markdown("### 5. Durfee Square Decomposition & Chapter 2 Series Identity")

        render_theorem_box(
            title="Andrews Section 2.2, eq. (2.2.9)",
            reference="The Theory of Partitions, p. 28",
            statement_md=(
                "The **Durfee square** of a partition $\\lambda$ is the largest $d \\times d$ square of dots contained "
                "within its Ferrers diagram. Every partition can be uniquely decomposed into three disjoint components:<br>"
                "1. The $d \\times d$ Durfee square (containing $d^2$ dots).<br>"
                "2. A partition $\\lambda_R$ of dots to the right (having at most $d$ parts).<br>"
                "3. A partition $\\lambda_B$ of dots below (having parts at most $d$)."
            ),
            equation_latex=r"\sum_{n=0}^\infty p(n) q^n = \sum_{d=0}^\infty \frac{q^{d^2}}{(1-q)^2 (1-q^2)^2 \dots (1-q^d)^2}",
            border_color="#f0883e",
        )

        durfee_col1, durfee_col2 = st.columns([1, 1])
        with durfee_col1:
            st.markdown("#### Combinatorial Decomposition Tool")
            durfee_raw = st.text_input("Enter partition to decompose:", value="7, 6, 4, 3, 1", key="m1_durfee_decomp")
            try:
                lam_df = tuple(int(x.strip()) for x in durfee_raw.replace(",", " ").split() if x.strip())
                decomp = durfee_decomposition(lam_df)
                d_side = decomp["d"]

                st.markdown(f"""
                - **Durfee Square side $d$**: `{d_side}` (dots = $d^2 = {decomp['d_sq']}$)
                - **Right partition $\\lambda_R$**: `{partition_to_str(decomp['lambda_R'])}` (parts $\\le d$, sum = {decomp['sum_R']})
                - **Bottom partition $\\lambda_B$**: `{partition_to_str(decomp['lambda_B'])}` (largest part $\\le d$, sum = {decomp['sum_B']})
                - **Reconstructed sum**: ${decomp['d_sq']} + {decomp['sum_R']} + {decomp['sum_B']} = {sum(lam_df)}$ {'✅' if decomp['verified'] else '❌'}
                """)

                # Render diagram with Durfee boundary
                fig_df = render_ferrers_diagram(lam_df, title=f"Durfee Square d={d_side} of λ = {partition_to_str(lam_df)}")
                fig_df.add_shape(
                    type="rect",
                    x0=-0.4, y0=0.4,
                    x1=d_side - 0.6, y1=-(d_side - 1) - 0.4,
                    line=dict(color="#f0883e", width=2.5, dash="dash"),
                    fillcolor="rgba(240,136,62,0.12)",
                )
                st.plotly_chart(fig_df, use_container_width=True)
            except Exception as e:
                st.error(f"Invalid partition input: {e}")

        with durfee_col2:
            st.markdown("#### Combinatorial Proof of the Series Identity")
            st.markdown(r"""
            Why does the generating function equal $\sum_{d=0}^\infty \frac{q^{d^2}}{(q; q)_d^2}$?

            1. The $d \times d$ Durfee square contributes factor $q^{d^2}$.
            2. By Theorem 1.4, partitions $\lambda_R$ with at most $d$ parts have generating function:
               $$\frac{1}{(1-q)(1-q^2)\dots(1-q^d)}$$
            3. By Theorem 1.4, partitions $\lambda_B$ with largest part at most $d$ have conjugate partitions with at most $d$ parts, hence identical generating function:
               $$\frac{1}{(1-q)(1-q^2)\dots(1-q^d)}$$
            4. Because $\lambda_R$ and $\lambda_B$ can be chosen independently, their product is $\frac{1}{(q; q)_d^2}$.
            Summing over all possible Durfee square sizes $d \ge 0$ accounts for **every partition of $n$ exactly once**!
            """)

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 6: GENERATING FUNCTIONS
    # ═════════════════════════════════════════════════════════════════════════
    with tab_gf:
        st.markdown("### 6. Chapter 1 Generating Functions & Multiplicity Factors")

        render_theorem_box(
            title="Andrews Section 1.2, Theorem 1.1",
            reference="The Theory of Partitions, p. 3",
            statement_md=(
                "The generating function for unrestricted partitions is the infinite product of geometric series: "
                "each factor $1 / (1 - q^k) = 1 + q^k + q^{2k} + q^{3k} + \\dots$ represents the contribution of parts "
                "equal to $k$, where the exponent $m_k \\cdot k$ corresponds to choosing part $k$ with multiplicity $m_k$."
            ),
            equation_latex=r"\sum_{n=0}^\infty p(n) q^n = \prod_{k=1}^\infty \frac{1}{1 - q^k}",
            border_color="#58a6ff",
        )

        col_gf_ctrl, col_gf_table = st.columns([1, 2])
        with col_gf_ctrl:
            max_deg_gf = st.slider("Polynomial truncation degree N:", 5, 25, 15, key="gf_deg")
            factors_m = st.slider("Number of factors M:", 1, max_deg_gf, max_deg_gf, key="gf_factors")

            poly_coeffs = expand_partition_gf(factors_m, max_deg_gf)
            st.markdown(f"**Truncated Product:** $\\prod_{{k=1}}^{{{factors_m}}} \\frac{{1}}{{1 - q^k}} \\pmod{{q^{{{max_deg_gf+1}}}}}$")

        with col_gf_table:
            gf_comparison = []
            for deg in range(max_deg_gf + 1):
                exact_val = partition_count(deg)
                approx_val = poly_coeffs[deg]
                gf_comparison.append({
                    "Degree n": deg,
                    "Product Coeff [qⁿ]": approx_val,
                    "Exact p(n)": exact_val,
                    "Stabilized?": "✅ Exact" if approx_val == exact_val else f"Diff: {exact_val - approx_val}",
                })
            st.dataframe(pd.DataFrame(gf_comparison), use_container_width=True, height=320)
            st.caption("Note: When M ≥ n, the coefficient [qⁿ] has fully stabilized and equals p(n).")

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 7: DEFENSIBLE FINDINGS
    # ═════════════════════════════════════════════════════════════════════════
    with tab_findings:
        render_defensible_findings(
            module_title="Module 1 — Ferrers Diagrams & Conjugation Duality",
            questions_md=(
                "(a) How does Ferrers diagram reflection establish an exact bijection between row-bounded and column-bounded partition sets?<br>"
                "(b) What structural property characterizes the fixed points of conjugation ($\\lambda = \\lambda'$), and how does their proportion behave asymptotically as $n \\to \\infty$?<br>"
                "(c) How does the Durfee square decomposition provide an exact combinatorial proof of Andrews's Chapter 2 series-product identity?"
            ),
            foundation_md=(
                "George E. Andrews, *The Theory of Partitions* (Cambridge University Press), Chapter 1, Section 1.3, "
                "Definition 1.8 (Conjugation), Theorem 1.4 (Bounded Partitions Duality), Example 8 (Sylvester's self-conjugate identity), "
                "and Chapter 2, Section 2.2, eq. (2.2.9) (Durfee square partition identity)."
            ),
            method_md=(
                "Partitions are generated in strict lexicographic descending order via recursive integer descent. "
                "Conjugation is evaluated in $O(r)$ by column-height scanning. "
                "Exact polynomial algebra is computed in $\\mathbb{Z}[q]$ without floating-point precision loss. "
                "Durfee decomposition partitions each graph into $d^2$, $\\lambda_R$, and $\\lambda_B$ components."
            ),
            deductions_md=(
                "• **Geometric Duality:** The numerical equality $p(\\le m\\text{ parts}, n) = p(\\text{max part}\\le m, n)$ "
                "is proven to be a geometric identity: transposing the bounding rectangle $[r \\le m, c \\le n]$ yields $[r \\le n, c \\le m]$.<br>"
                "• **Exponential Decay of Symmetry:** While total partitions grow as $p(n) \\sim \\frac{1}{4n\\sqrt{3}}e^{\\pi\\sqrt{2n/3}}$, "
                "self-conjugate partitions grow at rate $e^{\\pi\\sqrt{n/3}}$. The proportion of symmetric partitions decays to zero "
                "at asymptotic rate $e^{-\\pi(\\sqrt{2}-1)\\sqrt{n/3}}$. A random large partition is almost never symmetric.<br>"
                "• **Durfee Limit Law:** The side length $d(\\lambda)$ satisfies $d(\\lambda) = d(\\lambda')$, and its expected value scales as "
                "$\\frac{\\sqrt{6}\\ln 2}{\\pi}\\sqrt{n} \\approx 0.5407\\sqrt{n}$, linking discrete Ferrers geometry to the Vershik-Kerov limit curve.<br>"
                "• **Chapter 2 Series Equivalence:** Every partition decomposes uniquely into a $d^2$ square, a partition with $\\le d$ parts, and a partition with parts $\\le d$, "
                "proving combinatorially that $\\sum_{n=0}^\\infty p(n) q^n = \\sum_{d=0}^\\infty \\frac{q^{d^2}}{(q; q)_d^2}$."
            ),
            validation_md=(
                "Verified by 50 automated tests in `tests/test_conjugation.py`, `tests/test_enumeration.py`, and `tests/test_generating_functions.py`, "
                "including sum preservation, involution symmetry, Sylvester hook unfolding, and Durfee square coefficient agreement."
            ),
            limitations_md=(
                "Exhaustive partition generation is computationally bounded to $n \\le 25$ in the interactive UI due to exponential partition growth. "
                "Universal identities are established by mathematical proofs; computational results serve as algorithmic verification."
            ),
        )

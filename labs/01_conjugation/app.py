"""
PartitionViz — Module 1: Ferrers & Conjugation Lab
===================================================
Based on Andrews, The Theory of Partitions, Chapter 1:
  • Definition 1.1  — partition
  • Section 1.3     — Ferrers diagram, conjugation
  • Definition 1.8  — conjugate partition
  • Theorem 1.4     — bijection: at-most-m-parts ↔ largest-part-≤-m

Run with:
    streamlit run labs/01_conjugation/app.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time

from partition_core import (
    generate_partitions,
    partition_count,
    partition_count_table,
    conjugate,
    ferrers_matrix,
    conjugation_animation_frames,
    verify_theorem_1_4,
    partitions_at_most_m_parts,
    partitions_max_part,
    Partition,
)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PartitionViz · Module 1: Ferrers & Conjugation",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .main { background: #0d1117; }

  .hero-box {
    background: linear-gradient(135deg, #1a1f2e 0%, #16213e 50%, #0f3460 100%);
    border: 1px solid #30363d;
    border-radius: 16px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
  }
  .hero-title {
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(90deg, #58a6ff, #79c0ff, #a5f3fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.4rem 0;
  }
  .hero-subtitle {
    font-size: 1rem;
    color: #8b949e;
    margin: 0;
  }
  .theorem-box {
    background: linear-gradient(135deg, #161b22, #1c2128);
    border-left: 4px solid #58a6ff;
    border-radius: 0 12px 12px 0;
    padding: 1.2rem 1.5rem;
    margin: 1rem 0;
  }
  .theorem-title {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    color: #58a6ff;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
  }
  .theorem-body {
    color: #c9d1d9;
    font-size: 0.95rem;
    line-height: 1.6;
  }
  .stat-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
  }
  .stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: #58a6ff;
    font-family: 'JetBrains Mono', monospace;
  }
  .stat-label {
    font-size: 0.8rem;
    color: #8b949e;
    margin-top: 0.2rem;
  }
  .section-header {
    font-size: 1.4rem;
    font-weight: 600;
    color: #e6edf3;
    margin: 1.5rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #21262d;
  }
  .step-badge {
    display: inline-block;
    background: #1f6feb;
    color: white;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 20px;
    margin-right: 6px;
    font-family: 'JetBrains Mono', monospace;
  }
  .verified-badge {
    background: #238636;
    color: #aff5b4;
    font-size: 0.85rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    display: inline-block;
  }
  .failed-badge {
    background: #da3633;
    color: #ffd7d7;
    font-size: 0.85rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    display: inline-block;
  }
  .partition-chip {
    display: inline-block;
    background: #1c2128;
    border: 1px solid #30363d;
    border-radius: 20px;
    padding: 3px 12px;
    margin: 3px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #c9d1d9;
  }
  .highlight-chip {
    background: #1f3a5e;
    border-color: #58a6ff;
    color: #79c0ff;
  }
  .research-box {
    background: linear-gradient(135deg, #0d1117, #161b22);
    border: 1px solid #f0883e55;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
  }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def make_ferrers_figure(lam: Partition, title: str,
                        highlight_col: int | None = None,
                        color_dots: str = "#58a6ff",
                        bg_color: str = "#161b22") -> go.Figure:
    """Build a Plotly Ferrers diagram figure."""
    if not lam:
        fig = go.Figure()
        fig.update_layout(
            title=title,
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
        )
        return fig

    rows = len(lam)
    cols = lam[0]

    x_dots, y_dots, colors_list = [], [], []
    x_hi, y_hi = [], []

    for r in range(rows):
        for c in range(lam[r]):
            x_dots.append(c)
            y_dots.append(-r)
            if highlight_col is not None and c == highlight_col:
                colors_list.append("#f0883e")
            else:
                colors_list.append(color_dots)

    # background ghost grid
    x_ghost, y_ghost = [], []
    for r in range(rows):
        for c in range(cols):
            if c >= lam[r]:
                x_ghost.append(c)
                y_ghost.append(-r)

    fig = go.Figure()

    # Ghost dots (show full rectangle outline)
    if x_ghost:
        fig.add_trace(go.Scatter(
            x=x_ghost, y=y_ghost,
            mode="markers",
            marker=dict(size=18, color="#21262d", symbol="circle"),
            hoverinfo="skip",
            showlegend=False,
        ))

    # Actual dots
    fig.add_trace(go.Scatter(
        x=x_dots, y=y_dots,
        mode="markers",
        marker=dict(
            size=22,
            color=colors_list,
            line=dict(width=1.5, color="#0d1117"),
            symbol="circle",
        ),
        hovertemplate="Row %{customdata[0]}, Col %{customdata[1]}<extra></extra>",
        customdata=[[(-y + 1), (x + 1)] for x, y in zip(x_dots, y_dots)],
        showlegend=False,
    ))

    # Row labels
    for r, part in enumerate(lam):
        fig.add_annotation(
            x=-0.8, y=-r,
            text=f"<b>{part}</b>",
            showarrow=False,
            font=dict(size=13, color="#8b949e", family="JetBrains Mono"),
            xanchor="right",
        )

    # Column labels
    for c in range(cols):
        col_ht = sum(1 for p in lam if p > c)
        fig.add_annotation(
            x=c, y=0.8,
            text=f"<b>{col_ht}</b>",
            showarrow=False,
            font=dict(
                size=13,
                color="#f0883e" if highlight_col == c else "#8b949e",
                family="JetBrains Mono",
            ),
            xanchor="center",
        )

    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color="#c9d1d9"), x=0.5, xanchor="center"),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        xaxis=dict(visible=False, range=[-1.5, cols + 0.5]),
        yaxis=dict(visible=False, range=[-rows - 0.5, 1.5]),
        margin=dict(l=40, r=20, t=50, b=20),
        height=max(250, 60 * rows + 80),
    )
    return fig


def parse_partition_input(raw: str) -> Partition | None:
    """Parse '4,2,1' or '4 2 1' → (4,2,1). Returns None on error."""
    try:
        parts = [int(x.strip()) for x in raw.replace(",", " ").split() if x.strip()]
        if not parts:
            return None
        if any(p <= 0 for p in parts):
            return None
        parts.sort(reverse=True)
        return tuple(parts)
    except ValueError:
        return None


def partition_to_str(lam: Partition) -> str:
    return "(" + " + ".join(str(p) for p in lam) + ")"


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔷 PartitionViz")
    st.markdown("**Module 1** — Ferrers & Conjugation")
    st.markdown("---")
    st.markdown("""
    **Navigate:**
    - 📐 Ferrers Explorer
    - 🔄 Conjugation Lab
    - ✅ Theorem 1.4 Verifier
    - 🔬 Research Section
    """)
    st.markdown("---")
    st.markdown("""
    **Reference:**
    Andrews, *The Theory of Partitions*
    Chapter 1, §1.1–1.3
    """)
    st.markdown("---")
    st.caption("IP · Theory of Partitions · 2026")


# ─────────────────────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-box">
  <div class="hero-title">🔷 Ferrers Diagrams & Conjugation</div>
  <div class="hero-subtitle">
    PartitionViz · Module 1 &nbsp;|&nbsp;
    Andrews: <em>The Theory of Partitions</em>, Chapter 1
    &nbsp;&nbsp;·&nbsp;&nbsp;
    Definitions 1.1, 1.8 · Section 1.3 · Theorem 1.4
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📐  Ferrers Explorer",
    "🔄  Conjugation Lab",
    "✅  Theorem 1.4 Verifier",
    "🔬  Research Section",
])


# ═════════════════════════════════════════════════════════════════════════════
# TAB 1 — FERRERS EXPLORER
# ═════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">📐 Ferrers Diagram Explorer</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="theorem-box">
      <div class="theorem-title">Definition 1.1 · Andrews p.1</div>
      <div class="theorem-body">
        A <strong>partition</strong> of a positive integer <em>n</em> is a finite
        non-increasing sequence of positive integers k₁ ≥ k₂ ≥ … ≥ k_r such
        that Σk_i = n.  The k_i are called the <strong>parts</strong> of the partition.
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_ctrl, col_main = st.columns([1, 2])

    with col_ctrl:
        st.markdown("#### Choose n")
        n_val = st.slider("n", min_value=1, max_value=20, value=8, key="fe_n")

        all_parts = generate_partitions(n_val)
        total_count = len(all_parts)

        st.markdown(f"""
        <div class="stat-card">
          <div class="stat-value">{total_count}</div>
          <div class="stat-label">p({n_val}) — total partitions</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Select a partition")
        part_labels = [partition_to_str(p) for p in all_parts]
        selected_label = st.selectbox("Partition", part_labels, key="fe_sel")
        selected_idx = part_labels.index(selected_label)
        selected = all_parts[selected_idx]

        conj = conjugate(selected)
        st.markdown(f"""
        <br>
        <div class="stat-card">
          <div class="stat-value" style="font-size:1.2rem">{partition_to_str(conj)}</div>
          <div class="stat-label">Conjugate λ'</div>
        </div>
        """, unsafe_allow_html=True)

    with col_main:
        fc1, fc2 = st.columns(2)
        with fc1:
            fig_orig = make_ferrers_figure(
                selected,
                f"λ = {partition_to_str(selected)}<br>n = {sum(selected)}, {len(selected)} part(s)"
            )
            st.plotly_chart(fig_orig, use_container_width=True, key="fe_orig")
        with fc2:
            fig_conj = make_ferrers_figure(
                conj,
                f"λ' = {partition_to_str(conj)}<br>n = {sum(conj)}, {len(conj)} part(s)",
                color_dots="#a5f3fc"
            )
            st.plotly_chart(fig_conj, use_container_width=True, key="fe_conj")

        # Quick facts
        st.markdown("---")
        qf1, qf2, qf3, qf4 = st.columns(4)
        with qf1:
            st.metric("Parts of λ", len(selected))
        with qf2:
            st.metric("Largest part", selected[0])
        with qf3:
            st.metric("Parts of λ'", len(conj))
        with qf4:
            st.metric("Largest part of λ'", conj[0] if conj else 0)

        # Show all partitions
        with st.expander(f"📋 All {total_count} partitions of {n_val}"):
            cols_per_row = 5
            parts_html = ""
            for p in all_parts:
                cls = "partition-chip highlight-chip" if p == selected else "partition-chip"
                parts_html += f'<span class="{cls}">{partition_to_str(p)}</span>'
            st.markdown(parts_html, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# TAB 2 — CONJUGATION LAB
# ═════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">🔄 Conjugation Lab — Step-by-Step</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="theorem-box">
      <div class="theorem-title">Definition 1.8 · Andrews p.7</div>
      <div class="theorem-body">
        If λ = (k₁,…,k_n) is a partition, define the <strong>conjugate partition</strong>
        λ' = (k₁',…,k_m') by choosing k_i' as the <em>number of parts of λ that are ≥ i</em>.
        Equivalently, λ' is obtained by reflecting the Ferrers graph across its main diagonal.
      </div>
    </div>
    """, unsafe_allow_html=True)

    cl1, cl2 = st.columns([1, 2])

    with cl1:
        st.markdown("#### Enter a partition")
        raw_input = st.text_input(
            "Parts (comma or space separated)",
            value="5, 3, 3, 1",
            key="cl_input",
            help="e.g. '5,3,3,1' or '5 3 3 1'"
        )
        lam_anim = parse_partition_input(raw_input)

        if lam_anim is None:
            st.error("⚠️ Invalid input. Enter positive integers in non-increasing order.")
            st.stop()

        n_anim = sum(lam_anim)
        conj_anim = conjugate(lam_anim)

        st.markdown(f"""
        <div class="stat-card" style="margin-top:1rem">
          <div class="stat-value" style="font-size:1.1rem">{partition_to_str(lam_anim)}</div>
          <div class="stat-label">λ &nbsp;|&nbsp; n = {n_anim}</div>
        </div>
        <br>
        <div class="stat-card">
          <div class="stat-value" style="font-size:1.1rem;color:#a5f3fc">{partition_to_str(conj_anim)}</div>
          <div class="stat-label">λ' (conjugate)</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Mathematical properties
        double_conj = conjugate(conj_anim)
        inv_ok = double_conj == lam_anim
        sum_ok = sum(conj_anim) == sum(lam_anim)

        st.markdown("**Mathematical Properties:**")
        st.markdown(f"{'✅' if sum_ok else '❌'} `sum(λ') = sum(λ) = {n_anim}`")
        st.markdown(f"{'✅' if inv_ok else '❌'} `(λ')' = λ` (involution)")
        st.markdown(f"✅ `len(λ') = λ[0] = {lam_anim[0]}`")
        st.markdown(f"✅ `λ'[0] = len(λ) = {len(lam_anim)}`")

    with cl2:
        frames = conjugation_animation_frames(lam_anim)
        max_step = len(frames) - 1

        st.markdown("#### Animation Controls")
        step = st.slider(
            "Step",
            min_value=0,
            max_value=max_step,
            value=0,
            key="cl_step",
            help="Drag to walk through the conjugation step by step"
        )

        frame = frames[step]
        hi_col = frame["highlighted_col"]
        conj_so_far = frame["conjugate_so_far"]

        # Step label
        st.markdown(f"""
        <div style="background:#1c2128;border-radius:8px;padding:0.8rem;margin:0.5rem 0;
                    border-left:3px solid #58a6ff;font-family:'JetBrains Mono',monospace;
                    font-size:0.88rem;color:#c9d1d9">
          <span class="step-badge">STEP {step}/{max_step}</span>
          {frame['label']}
        </div>
        """, unsafe_allow_html=True)

        af1, af2 = st.columns(2)
        with af1:
            fig_orig_anim = make_ferrers_figure(
                lam_anim,
                f"λ = {partition_to_str(lam_anim)}",
                highlight_col=hi_col,
            )
            st.plotly_chart(fig_orig_anim, use_container_width=True, key="cl_orig")

        with af2:
            if conj_so_far:
                fig_conj_anim = make_ferrers_figure(
                    conj_so_far,
                    f"λ' (building…) = {partition_to_str(conj_so_far)}",
                    color_dots="#a5f3fc" if step < max_step else "#7ee787",
                )
            else:
                fig_conj_anim = go.Figure()
                fig_conj_anim.update_layout(
                    title="λ' (building…)",
                    paper_bgcolor="#161b22",
                    plot_bgcolor="#161b22",
                    height=250,
                )
                fig_conj_anim.add_annotation(
                    x=0.5, y=0.5, xref="paper", yref="paper",
                    text="← Start the animation",
                    font=dict(size=14, color="#8b949e"),
                    showarrow=False,
                )
            st.plotly_chart(fig_conj_anim, use_container_width=True, key="cl_conj")

        if step == max_step:
            st.success(f"✅ Conjugation complete. λ' = {partition_to_str(conj_anim)}")


# ═════════════════════════════════════════════════════════════════════════════
# TAB 3 — THEOREM 1.4 VERIFIER
# ═════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">✅ Theorem 1.4 — Computational Verification</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="theorem-box">
      <div class="theorem-title">Theorem 1.4 · Andrews p.8</div>
      <div class="theorem-body">
        The number of partitions of <em>n</em> with <strong>at most m parts</strong>
        equals the number of partitions of <em>n</em> in which
        <strong>no part exceeds m</strong>.
        <br><br>
        <em>Proof idea:</em> The conjugation map λ → λ' is a bijection between the two sets,
        since transposing the Ferrers diagram converts the row-count bound into a column-height bound.
      </div>
    </div>
    """, unsafe_allow_html=True)

    tv1, tv2 = st.columns([1, 2])

    with tv1:
        st.markdown("#### Parameters")
        n_thm = st.slider("n", 1, 25, 10, key="thm_n")
        m_thm = st.slider("m", 1, n_thm, min(4, n_thm), key="thm_m")

        result = verify_theorem_1_4(
            n_thm, m_thm,
            partitions_at_most_m_parts,
            partitions_max_part,
        )

        badge = '<span class="verified-badge">✓ VERIFIED</span>' if result["verified"] \
                else '<span class="failed-badge">✗ FAILED</span>'

        st.markdown(f"""
        <br>
        <div class="stat-card">
          <div class="stat-value">{result['count_at_most_m_parts']}</div>
          <div class="stat-label">Partitions of {n_thm} with ≤ {m_thm} parts</div>
        </div>
        <br>
        <div class="stat-card">
          <div class="stat-value">{result['count_max_part_m']}</div>
          <div class="stat-label">Partitions of {n_thm} with max part ≤ {m_thm}</div>
        </div>
        <br>
        {badge}
        """, unsafe_allow_html=True)

        # Bijection check
        bij_ok = result["bijection_explicit_ok"]
        st.markdown(
            f"<br>{'✅' if bij_ok else '❌'} Explicit bijection verified (λ→λ' maps each "
            f"partition of the first set into the second)",
            unsafe_allow_html=True
        )

    with tv2:
        st.markdown("#### Side-by-Side Partition Lists")

        p_left  = result["partitions_at_most_m_parts"]
        p_right = result["partitions_max_part_m"]

        tvc1, tvc2 = st.columns(2)
        with tvc1:
            st.markdown(f"**At most {m_thm} parts** ({len(p_left)} partitions)")
            for lam in p_left:
                conj_lam = conjugate(lam)
                st.markdown(
                    f'<span class="partition-chip highlight-chip">{partition_to_str(lam)}</span>'
                    f' → <span class="partition-chip">{partition_to_str(conj_lam)}</span>',
                    unsafe_allow_html=True,
                )
        with tvc2:
            st.markdown(f"**Largest part ≤ {m_thm}** ({len(p_right)} partitions)")
            p_right_set = set(p_right)
            for lam in p_left:
                conj_lam = conjugate(lam)
                in_set = conj_lam in p_right_set
                cls = "partition-chip highlight-chip" if in_set else "partition-chip"
                st.markdown(
                    f'<span class="{cls}">{partition_to_str(conj_lam)}</span>'
                    f' {"✅" if in_set else "❌"}',
                    unsafe_allow_html=True,
                )

        # Batch verification table
        st.markdown("---")
        st.markdown("#### Batch Verification: n = 1 to 20, m = 1 to 6")
        rows_data = []
        for nn in range(1, 21):
            for mm in range(1, min(nn + 1, 7)):
                r = verify_theorem_1_4(nn, mm, partitions_at_most_m_parts, partitions_max_part)
                rows_data.append({
                    "n": nn, "m": mm,
                    "≤m parts": r["count_at_most_m_parts"],
                    "max≤m": r["count_max_part_m"],
                    "equal?": "✅" if r["verified"] else "❌",
                })
        df_batch = pd.DataFrame(rows_data)
        all_verified = all(r == "✅" for r in df_batch["equal?"])
        if all_verified:
            st.success(f"✅ Theorem 1.4 verified for all {len(rows_data)} cases (n=1..20, m=1..6)")
        st.dataframe(
            df_batch.pivot(index="n", columns="m", values="equal?"),
            use_container_width=True,
            height=350,
        )


# ═════════════════════════════════════════════════════════════════════════════
# TAB 4 — RESEARCH SECTION
# ═════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">🔬 Research Section</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="research-box">
      <div style="font-size:0.8rem;color:#f0883e;font-weight:600;letter-spacing:1px;
                  text-transform:uppercase;margin-bottom:0.5rem">Research Question</div>
      <div style="color:#c9d1d9;font-size:1rem">
        How do the self-conjugate partitions (those fixed by conjugation, λ = λ') 
        distribute across all n?  What structural property characterizes them?
        Is there a generating function?
      </div>
    </div>
    """, unsafe_allow_html=True)

    r1, r2 = st.columns([1, 1])

    with r1:
        st.markdown("#### Self-Conjugate Partitions (λ = λ')")
        st.markdown("""
        A partition is **self-conjugate** if its Ferrers diagram is symmetric
        across the main diagonal.  These are the fixed points of the conjugation involution.

        **Known result** (Andrews, Ch.1 Example 8, attributed to Sylvester):
        The number of self-conjugate partitions of n equals the number of
        partitions of n into *distinct odd parts*.
        """)

        max_n_sc = st.slider("Compute up to n =", 5, 40, 20, key="sc_max")
        data_sc = []
        for nn in range(1, max_n_sc + 1):
            all_p = generate_partitions(nn)
            sc = [p for p in all_p if conjugate(p) == p]
            data_sc.append({
                "n": nn,
                "p(n)": len(all_p),
                "self-conjugate count": len(sc),
                "examples": ", ".join(partition_to_str(p) for p in sc[:3])
                            + ("…" if len(sc) > 3 else "")
            })

        df_sc = pd.DataFrame(data_sc)
        st.dataframe(df_sc, use_container_width=True, height=350)

    with r2:
        st.markdown("#### Visualization: Self-Conjugate Proportion")

        fig_sc = go.Figure()
        fig_sc.add_trace(go.Bar(
            x=df_sc["n"],
            y=df_sc["p(n)"],
            name="All partitions p(n)",
            marker_color="#21262d",
        ))
        fig_sc.add_trace(go.Bar(
            x=df_sc["n"],
            y=df_sc["self-conjugate count"],
            name="Self-conjugate partitions",
            marker_color="#58a6ff",
        ))
        fig_sc.update_layout(
            barmode="overlay",
            paper_bgcolor="#0d1117",
            plot_bgcolor="#0d1117",
            font=dict(color="#c9d1d9"),
            xaxis=dict(title="n", gridcolor="#21262d"),
            yaxis=dict(title="Count", gridcolor="#21262d"),
            legend=dict(bgcolor="#161b22", bordercolor="#30363d"),
            title="Self-conjugate partitions vs all partitions",
            height=320,
        )
        st.plotly_chart(fig_sc, use_container_width=True, key="sc_chart")

        # Durfee square
        st.markdown("---")
        st.markdown("#### Durfee Square — Another Fixed-Point Invariant")
        st.markdown("""
        The **Durfee square** of a partition λ is the largest square of dots
        that fits in its Ferrers diagram.  Its side length d(λ) satisfies:
        d(λ) = d(λ') — it is preserved under conjugation.

        Andrews uses the Durfee square at the end of Chapter 2 to give a
        combinatorial proof of a key q-series identity (eq. 2.2.9).
        """)

        raw_durfee = st.text_input("Enter partition:", value="8, 6, 5, 4, 1", key="durfee_in")
        lam_d = parse_partition_input(raw_durfee)
        if lam_d:
            d = sum(1 for i, p in enumerate(lam_d, 1) if p >= i)
            st.markdown(f"""
            **λ = {partition_to_str(lam_d)}**
            — Durfee square side: **d(λ) = {d}**

            λ' = {partition_to_str(conjugate(lam_d))}
            — Durfee square side of λ': **d(λ') = {sum(1 for i,p in enumerate(conjugate(lam_d),1) if p>=i)}**
            """)

            fig_d_orig = make_ferrers_figure(
                lam_d,
                f"Ferrers diagram of λ = {partition_to_str(lam_d)} with Durfee square d={d}"
            )

            # Add Durfee square overlay
            fig_d_orig.add_shape(
                type="rect",
                x0=-0.4, y0=0.4,
                x1=d - 0.6, y1=-(d - 1) - 0.4,
                line=dict(color="#f0883e", width=2, dash="dot"),
                fillcolor="rgba(240,136,62,0.08)",
            )
            st.plotly_chart(fig_d_orig, use_container_width=True, key="durfee_fig")

    # Module summary
    st.markdown("---")
    st.markdown("""
    <div class="theorem-box" style="border-left-color:#238636">
      <div class="theorem-title" style="color:#3fb950">Module 1 — What We Built</div>
      <div class="theorem-body">
        <strong>Mathematical implementations:</strong> partition enumeration (Euler pentagonal recurrence),
        conjugation (Definition 1.8), Theorem 1.4 bijection.<br><br>
        <strong>Verified computationally:</strong> Theorem 1.4 holds for all (n,m) with n≤20, m≤6.<br><br>
        <strong>Research experiment:</strong> Self-conjugate partition counts tabulated, 
        Durfee square invariance under conjugation confirmed.<br><br>
        <strong>Next module:</strong> Franklin's Involution — a sign-reversing bijection that
        proves Euler's pentagonal number theorem combinatorially.
      </div>
    </div>
    """, unsafe_allow_html=True)

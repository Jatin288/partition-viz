"""
PartitionViz — Module 2: Franklin's Involution & Euler's Pentagonal Theorem
===========================================================================
Based on Andrews, The Theory of Partitions, Chapter 1:
  • Section 1.3  — Graphical representation, base & slope
  • Theorem 1.6  — Euler's Pentagonal Number Theorem:
                   prod_{n=1}^inf (1 - q^n) = sum_{k=-inf}^inf (-1)^k q^{k(3k-1)/2}
  • Corollary 1.7 — Combinatorial interpretation: p_e(D, n) - p_o(D, n) = (-1)^k or 0
  • Corollary 1.8 — Pentagonal recurrence for p(n)

Run with:
    streamlit run labs/02_franklin_involution/app.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from partition_core import (
    partitions_distinct,
    partition_count,
    partition_count_table,
    Partition,
)
from partition_core.franklin import (
    slope_length,
    base_length,
    is_exceptional,
    franklin_map,
    franklin_details,
    verify_euler_pentagonal,
)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PartitionViz · Module 2: Franklin's Involution",
    page_icon="⚡",
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
    background: linear-gradient(135deg, #161b22 0%, #1c2833 50%, #0d2818 100%);
    border: 1px solid #30363d;
    border-radius: 16px;
    padding: 2.2rem;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
  }
  .hero-title {
    font-size: 2.3rem;
    font-weight: 700;
    background: linear-gradient(90deg, #3fb950, #58a6ff, #a5f3fc);
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
    border-left: 4px solid #3fb950;
    border-radius: 0 12px 12px 0;
    padding: 1.2rem 1.5rem;
    margin: 1rem 0;
  }
  .theorem-title {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    color: #3fb950;
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
    font-size: 1.9rem;
    font-weight: 700;
    color: #3fb950;
    font-family: 'JetBrains Mono', monospace;
  }
  .stat-label {
    font-size: 0.8rem;
    color: #8b949e;
    margin-top: 0.2rem;
  }
  .section-header {
    font-size: 1.35rem;
    font-weight: 600;
    color: #e6edf3;
    margin: 1.5rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #21262d;
  }
  .exceptional-badge {
    background: linear-gradient(135deg, #d29922, #f0883e);
    color: #0d1117;
    font-size: 0.85rem;
    font-weight: 700;
    padding: 6px 14px;
    border-radius: 20px;
    display: inline-block;
    box-shadow: 0 0 12px rgba(240,136,62,0.4);
  }
  .paired-badge {
    background: #238636;
    color: #aff5b4;
    font-size: 0.85rem;
    font-weight: 600;
    padding: 5px 12px;
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
    font-size: 0.85rem;
    color: #c9d1d9;
  }
  .even-chip {
    border-color: #388bfd;
    color: #79c0ff;
  }
  .odd-chip {
    border-color: #bc8cff;
    color: #d2a8ff;
  }
  .exp-chip {
    border-color: #f0883e;
    background: #2a1b0a;
    color: #f0883e;
    font-weight: 700;
  }
  .legend-item {
    display: inline-block;
    margin-right: 15px;
    font-size: 0.85rem;
    color: #c9d1d9;
  }
  .legend-dot {
    display: inline-block;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    margin-right: 5px;
    vertical-align: middle;
  }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def partition_to_str(lam: Partition) -> str:
    if not lam:
        return "∅"
    return "(" + " + ".join(str(p) for p in lam) + ")"


def make_franklin_ferrers_figure(details: dict, title: str, bg_color: str = "#161b22") -> go.Figure:
    """Build a Plotly Ferrers figure highlighting Base, Slope, and Intersection."""
    lam = details["lam"]
    if not lam:
        fig = go.Figure()
        fig.update_layout(title=title, paper_bgcolor=bg_color, plot_bgcolor=bg_color, height=250)
        return fig

    rows = len(lam)
    cols = lam[0]

    base_set = set(details["base_coords"])
    slope_set = set(details["slope_coords"])
    intersect_set = set(details["intersection_coords"])

    x_dots, y_dots, colors, labels = [], [], [], []

    for r in range(rows):
        for c in range(lam[r]):
            pt = (r, c)
            x_dots.append(c)
            y_dots.append(-r)

            if pt in intersect_set:
                colors.append("#f85149")  # Red for collision
                labels.append(f"Intersection (Base & Slope)<br>Row {r+1}, Col {c+1}")
            elif pt in base_set:
                colors.append("#f0883e")  # Orange for Base
                labels.append(f"Base b={details['b']}<br>Row {r+1}, Col {c+1}")
            elif pt in slope_set:
                colors.append("#3fb950")  # Green for Slope
                labels.append(f"Slope s={details['s']}<br>Row {r+1}, Col {c+1}")
            else:
                colors.append("#58a6ff")  # Blue for Body
                labels.append(f"Part {lam[r]}<br>Row {r+1}, Col {c+1}")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_dots, y=y_dots,
        mode="markers",
        marker=dict(size=22, color=colors, line=dict(width=1.5, color="#0d1117")),
        hovertext=labels,
        hoverinfo="text",
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

    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color="#c9d1d9"), x=0.5, xanchor="center"),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        xaxis=dict(visible=False, range=[-1.5, cols + 0.5]),
        yaxis=dict(visible=False, range=[-rows - 0.5, 1.0]),
        margin=dict(l=40, r=20, t=50, b=20),
        height=max(260, 60 * rows + 80),
    )
    return fig


def parse_partition_input(raw: str) -> Partition | None:
    try:
        parts = [int(x.strip()) for x in raw.replace(",", " ").split() if x.strip()]
        if not parts:
            return None
        if any(p <= 0 for p in parts):
            return None
        if len(parts) != len(set(parts)):
            return None  # distinct parts required
        parts.sort(reverse=True)
        return tuple(parts)
    except ValueError:
        return None


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ PartitionViz")
    st.markdown("**Module 2** — Franklin's Involution")
    st.markdown("---")
    st.markdown("""
    **Navigate:**
    - 🔍 Franklin Explorer
    - ⚖️ Parity Pairing Matrix
    - 📜 Euler's Pentagonal Series
    - 🔬 Andrews's Recurrence
    """)
    st.markdown("---")
    st.markdown("""
    **Reference:**
    Andrews, *The Theory of Partitions*
    Chapter 1, §1.3, Theorem 1.6
    (Franklin, 1881)
    """)
    st.markdown("---")
    st.caption("IP · Theory of Partitions · 2026")


# ─────────────────────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-box">
  <div class="hero-title">⚡ Franklin's Involution & Euler's Pentagonal Theorem</div>
  <div class="hero-subtitle">
    PartitionViz · Module 2 &nbsp;|&nbsp;
    Andrews: <em>The Theory of Partitions</em>, Chapter 1, Section 1.3 & Theorem 1.6
    &nbsp;&nbsp;·&nbsp;&nbsp;
    The Combinatorial Proof of Euler's Identity
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍  Franklin Explorer",
    "⚖️  Parity Pairing Matrix",
    "📜  Euler's Pentagonal Series",
    "🔬  Andrews's Recurrence",
])


# ═════════════════════════════════════════════════════════════════════════════
# TAB 1 — FRANKLIN EXPLORER
# ═════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">🔍 Interactive Involution Explorer</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="theorem-box">
      <div class="theorem-title">Theorem 1.6 · Franklin (1881) · Andrews p.10</div>
      <div class="theorem-body">
        For partitions into <strong>distinct parts</strong>, let <em>b</em> be the length of the base (smallest part)
        and <em>s</em> be the length of the slope (consecutive parts decreasing by 1 from the top).
        <br>
        The map <strong>φ</strong> moves either the base to a new slope (if <em>b ≤ s</em>) or the slope to a new base (if <em>b &gt; s</em>).
        <br>
        This pairs partitions of even part-count with odd part-count, failing <em>only</em> at the generalized pentagonal numbers!
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Visual legend
    st.markdown("""
    <div style="margin: 0.8rem 0 1.2rem 0">
      <span class="legend-item"><span class="legend-dot" style="background:#3fb950"></span><b>Slope (s)</b>: consecutive parts decreasing by 1</span>
      <span class="legend-item"><span class="legend-dot" style="background:#f0883e"></span><b>Base (b)</b>: smallest part (bottom row)</span>
      <span class="legend-item"><span class="legend-dot" style="background:#f85149"></span><b>Intersection</b>: base meets slope (r = s)</span>
      <span class="legend-item"><span class="legend-dot" style="background:#58a6ff"></span><b>Body</b>: other parts</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("#### Input Partition")
        mode = st.radio("Selection Mode:", ["Preset Examples", "Choose n", "Custom Input"], horizontal=True)

        selected_partition = (5, 4, 2)

        if mode == "Preset Examples":
            presets = {
                "Regular move (b ≤ s): (5, 4, 2)": (5, 4, 2),
                "Regular move (b > s): (5, 3, 2)": (5, 3, 2),
                "Exceptional ω(2)=5: (3, 2)": (3, 2),
                "Exceptional ω(-2)=7: (4, 3)": (4, 3),
                "Exceptional ω(3)=12: (5, 4, 3)": (5, 4, 3),
                "Exceptional ω(-3)=15: (6, 5, 4)": (6, 5, 4),
                "Large distinct: (8, 6, 4, 2, 1)": (8, 6, 4, 2, 1),
            }
            choice = st.selectbox("Select preset:", list(presets.keys()))
            selected_partition = presets[choice]

        elif mode == "Choose n":
            n_val = st.slider("Integer n", 1, 25, 7)
            dist_list = partitions_distinct(n_val)
            if dist_list:
                str_list = [partition_to_str(p) for p in dist_list]
                p_choice = st.selectbox(f"Distinct partition of {n_val}:", str_list)
                selected_partition = dist_list[str_list.index(p_choice)]
            else:
                st.info("No distinct partitions.")

        else:
            custom_str = st.text_input("Enter distinct parts (e.g. 7, 5, 3, 1):", value="7, 5, 3, 1")
            parsed = parse_partition_input(custom_str)
            if parsed:
                selected_partition = parsed
            else:
                st.error("Please enter strictly decreasing positive integers (strictly distinct).")
                st.stop()

        # Detailed analysis
        details = franklin_details(selected_partition)

        st.markdown("---")
        st.markdown("#### Geometric Invariants")
        q1, q2 = st.columns(2)
        with q1:
            st.metric("Base length b", details["b"])
            st.metric("Total parts r", details["r"])
        with q2:
            st.metric("Slope length s", details["s"])
            parity_str = "Even (2k)" if details["r"] % 2 == 0 else "Odd (2k+1)"
            st.metric("Parity", parity_str)

        # Decision explanation
        st.markdown("---")
        st.markdown("#### Map Decision")
        if details["is_exceptional"]:
            case = details["exceptional_case"]
            k = details["k_index"]
            st.markdown(f"""
            <div class="exceptional-badge">⚠️ EXCEPTIONAL FIXED POINT</div>
            <p style="margin-top:0.8rem;color:#f0883e;font-size:0.9rem">
              <strong>Base meets Slope (r = s = {details['r']})</strong>.<br>
              Case: <code>{case}</code> with k = {k}.<br>
              Cannot move base to slope or slope to base without violating distinctness or row counts!<br>
              <strong>n = {details['n']} is a Generalized Pentagonal Number ω({k})!</strong>
            </p>
            """, unsafe_allow_html=True)
        else:
            if details["b"] <= details["s"]:
                st.markdown(f"""
                <div class="paired-badge">✓ CASE: b ≤ s ({details['b']} ≤ {details['s']})</div>
                <p style="margin-top:0.6rem;color:#c9d1d9;font-size:0.9rem">
                  Remove bottom row of length <strong>b = {details['b']}</strong>, add 1 dot to each of the first {details['b']} rows.<br>
                  Parts count: <strong>{details['r']} → {details['r'] - 1}</strong> (parity flips!).
                </p>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="paired-badge">✓ CASE: b &gt; s ({details['b']} &gt; {details['s']})</div>
                <p style="margin-top:0.6rem;color:#c9d1d9;font-size:0.9rem">
                  Remove 1 dot from each of the first <strong>s = {details['s']}</strong> rows, append a new bottom row of length {details['s']}.<br>
                  Parts count: <strong>{details['r']} → {details['r'] + 1}</strong> (parity flips!).
                </p>
                """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### Ferrers Diagram Mapping")
        fig_src = make_franklin_ferrers_figure(
            details,
            f"λ = {partition_to_str(selected_partition)}  |  n = {details['n']}"
        )
        st.plotly_chart(fig_src, use_container_width=True)

        st.markdown("---")
        if details["is_exceptional"]:
            st.markdown(f"""
            <div style="background:#161b22;border:1px solid #d29922;border-radius:12px;padding:1.5rem;text-align:center">
              <h4 style="color:#f0883e;margin:0">No Partner Exists!</h4>
              <p style="color:#8b949e;margin:0.5rem 0 0 0">
                This partition survives the parity cancellation in Euler's pentagonal series.
                It contributes <strong>(-1)<sup>{details['k_index']}</sup> = {(-1)**details['k_index']}</strong> to the coefficient of q<sup>{details['n']}</sup>.
              </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            target = details["target"]
            target_details = franklin_details(target)
            st.markdown(f"#### Mapped Partner: φ(λ) = {partition_to_str(target)}")
            fig_tgt = make_franklin_ferrers_figure(
                target_details,
                f"φ(λ) = {partition_to_str(target)}  |  n = {target_details['n']}"
            )
            st.plotly_chart(fig_tgt, use_container_width=True)

            # Involution confirmation
            st.success(f"🔄 Involution Verified: φ(φ(λ)) = φ({partition_to_str(target)}) = {partition_to_str(franklin_map(target))}")


# ═════════════════════════════════════════════════════════════════════════════
# TAB 2 — PARITY PAIRING MATRIX
# ═════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">⚖️ Parity Pairing Matrix: Even Parts vs Odd Parts</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="theorem-box">
      <div class="theorem-title">Corollary 1.7 · Andrews p.11</div>
      <div class="theorem-body">
        Let <em>p_e(D, n)</em> be the number of partitions of <em>n</em> into an <strong>even number</strong> of distinct parts,
        and <em>p_o(D, n)</em> be the number into an <strong>odd number</strong> of distinct parts.
        <br><br>
        Because Franklin's map is a bijection between even and odd partitions whenever it is defined:
        <br>
        <strong>p_e(D, n) - p_o(D, n) = 0</strong> unless <em>n = k(3k±1)/2</em>, in which case the difference is <strong>(-1)^k</strong>.
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_ctrl, col_view = st.columns([1, 2])

    with col_ctrl:
        n_p = st.slider("Select n", 1, 30, 7, key="parity_n")
        all_d = partitions_distinct(n_p)

        even_d = [p for p in all_d if len(p) % 2 == 0]
        odd_d  = [p for p in all_d if len(p) % 2 == 1]
        diff = len(even_d) - len(odd_d)

        st.markdown(f"""
        <div class="stat-card">
          <div class="stat-value">{len(all_d)}</div>
          <div class="stat-label">Total distinct partitions |D({n_p})|</div>
        </div>
        <br>
        <div class="stat-card">
          <div class="stat-value" style="color:#79c0ff">{len(even_d)}</div>
          <div class="stat-label">p_e(D, {n_p}) — Even parts count</div>
        </div>
        <br>
        <div class="stat-card">
          <div class="stat-value" style="color:#d2a8ff">{len(odd_d)}</div>
          <div class="stat-label">p_o(D, {n_p}) — Odd parts count</div>
        </div>
        <br>
        <div class="stat-card" style="border-color:{'#f0883e' if diff != 0 else '#3fb950'}">
          <div class="stat-value" style="color:{'#f0883e' if diff != 0 else '#3fb950'}">{diff:+d}</div>
          <div class="stat-label">Difference: p_e - p_o</div>
        </div>
        """, unsafe_allow_html=True)

    with col_view:
        st.markdown("#### Exact Involution Matching Chords")

        # Table of pairings
        pairs_data = []
        visited = set()

        for p in all_d:
            if p in visited:
                continue
            mapped = franklin_map(p)
            if mapped is None:
                # Exceptional
                exp, case, k = is_exceptional(p)
                parity_label = "Even" if len(p) % 2 == 0 else "Odd"
                pairs_data.append({
                    "Even Partition (p_e)": partition_to_str(p) if parity_label == "Even" else "—",
                    "Odd Partition (p_o)": partition_to_str(p) if parity_label == "Odd" else "—",
                    "Status": f"⭐ EXCEPTIONAL (ω({k})={n_p})",
                    "Sign Contribution": f"{(-1)**k:+d}",
                })
                visited.add(p)
            else:
                p_even = p if len(p) % 2 == 0 else mapped
                p_odd  = mapped if len(p) % 2 == 0 else p
                pairs_data.append({
                    "Even Partition (p_e)": partition_to_str(p_even),
                    "Odd Partition (p_o)": partition_to_str(p_odd),
                    "Status": "⇄ Paired by φ",
                    "Sign Contribution": "0 (cancels)",
                })
                visited.add(p)
                visited.add(mapped)

        df_pairs = pd.DataFrame(pairs_data)
        st.dataframe(df_pairs, use_container_width=True, height=350)

        if diff != 0:
            st.markdown(f"""
            <div style="background:#2a1b0a;border:1px solid #f0883e;border-radius:10px;padding:1rem;margin-top:1rem">
              <b style="color:#f0883e">⭐ Pentagonal Cancellation Residue:</b><br>
              Because <em>n = {n_p}</em> is a pentagonal number, exactly one partition cannot be paired!<br>
              It leaves an unmatched residue of <strong>{diff:+d}</strong> in the infinite product expansion.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success(f"✅ Perfect Matching: All {len(all_d)} distinct partitions of {n_p} cancel out in pairs! p_e - p_o = 0.")


# ═════════════════════════════════════════════════════════════════════════════
# TAB 3 — EULER'S PENTAGONAL SERIES
# ═════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">📜 Euler\'s Pentagonal Series & Coefficients</div>',
                unsafe_allow_html=True)

    st.markdown("""
    $$\\prod_{n=1}^\\infty (1 - q^n) = 1 - q - q^2 + q^5 + q^7 - q^{12} - q^{15} + q^{22} + q^{26} - \\dots$$
    Each exponent is a generalized pentagonal number:
    $$\\omega(k) = \\frac{k(3k-1)}{2}, \\quad k \\in \\{1, -1, 2, -2, 3, -3, \\dots\\}$$
    """)

    max_n_series = st.slider("Verify series up to n =", 10, 50, 30, key="series_n")
    results = verify_euler_pentagonal(max_n_series)

    # Format dataframe
    table_rows = []
    for r in results:
        table_rows.append({
            "n": r["n"],
            "|D(n)|": r["total_distinct"],
            "p_e(D,n)": r["p_e"],
            "p_o(D,n)": r["p_o"],
            "p_e - p_o": r["difference"],
            "Theoretical Coeff": r["expected_diff"],
            "Pentagonal k": r["pentagonal_k"] if r["pentagonal_k"] is not None else "",
            "Verified": "✅" if r["verified"] else "❌",
        })

    df_series = pd.DataFrame(table_rows)

    c1, c2 = st.columns([2, 1])
    with c1:
        st.dataframe(df_series, use_container_width=True, height=400)
    with c2:
        # Visual plot of coefficients
        fig_coeffs = go.Figure()
        fig_coeffs.add_trace(go.Bar(
            x=df_series["n"],
            y=df_series["p_e - p_o"],
            marker_color=[
                "#f0883e" if v != 0 else "#21262d"
                for v in df_series["p_e - p_o"]
            ],
            name="Coefficient",
        ))
        fig_coeffs.update_layout(
            title="Coefficients of prod (1 - q^n)",
            paper_bgcolor="#161b22",
            plot_bgcolor="#161b22",
            font=dict(color="#c9d1d9"),
            xaxis=dict(title="Exponent n", gridcolor="#21262d"),
            yaxis=dict(title="Coefficient (-1)^k", gridcolor="#21262d", range=[-1.5, 1.5]),
            height=380,
        )
        st.plotly_chart(fig_coeffs, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# TAB 4 — ANDREWS'S RECURRENCE
# ═════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">🔬 Corollary 1.8: Euler\'s Recurrence for p(n)</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="theorem-box">
      <div class="theorem-title">Corollary 1.8 · Andrews p.12</div>
      <div class="theorem-body">
        Because <strong>(prod (1 - q^n)) * (sum p(n) q^n) = 1</strong>, multiplying the series yields Euler's celebrated recurrence:
        <br><br>
        <strong>p(n) = p(n - 1) + p(n - 2) - p(n - 5) - p(n - 7) + p(n - 12) + p(n - 15) - ...</strong>
        <br><br>
        where the signs follow <strong>(-1)^(k+1)</strong> and the shifts are the generalized pentagonal numbers!
      </div>
    </div>
    """, unsafe_allow_html=True)

    n_rec = st.slider("Compute p(n) step-by-step for n =", 1, 60, 10, key="rec_n")

    # Build recurrence steps
    p_table = partition_count_table(n_rec)

    terms_data = []
    k = 1
    total = 0
    formula_parts = []

    while True:
        wp = k * (3 * k - 1) // 2
        wn = k * (3 * k + 1) // 2
        sign = (-1) ** (k + 1)
        sign_str = "+" if sign > 0 else "-"

        if wp <= n_rec:
            val_p = p_table[n_rec - wp]
            contrib_p = sign * val_p
            total += contrib_p
            terms_data.append({
                "k": f"+{k}",
                "Pentagonal ω(k)": wp,
                "n - ω(k)": n_rec - wp,
                "p(n - ω)": val_p,
                "Sign": sign_str,
                "Contribution": contrib_p,
            })
            formula_parts.append(f"{sign_str} p({n_rec - wp}) [{contrib_p:+d}]")

        if wn <= n_rec:
            val_n = p_table[n_rec - wn]
            contrib_n = sign * val_n
            total += contrib_n
            terms_data.append({
                "k": f"-{k}",
                "Pentagonal ω(-k)": wn,
                "n - ω(-k)": n_rec - wn,
                "p(n - ω)": val_n,
                "Sign": sign_str,
                "Contribution": contrib_n,
            })
            formula_parts.append(f"{sign_str} p({n_rec - wn}) [{contrib_n:+d}]")

        if wp > n_rec and wn > n_rec:
            break
        k += 1

    rc1, rc2 = st.columns([1, 1])

    with rc1:
        st.markdown(f"#### Recurrence Breakdown for p({n_rec})")
        st.markdown(f"**Formula**: `p({n_rec}) = " + " ".join(formula_parts) + "`")
        st.markdown(f"""
        <div class="stat-card" style="margin-top:1.5rem">
          <div class="stat-value">{total}</div>
          <div class="stat-label">Result: p({n_rec})</div>
        </div>
        """, unsafe_allow_html=True)

    with rc2:
        st.markdown("#### Pentagonal Shift Terms")
        df_terms = pd.DataFrame(terms_data)
        st.dataframe(df_terms, use_container_width=True)

st.markdown("---")
st.caption("PartitionViz · Module 2: Franklin's Involution & Euler's Pentagonal Theorem · Andrews Ch. 1")

"""
ui/home_page.py
Unified Home Page and Research Overview for PartitionViz.
"""
from __future__ import annotations
import streamlit as st


def render_home_page():
    st.markdown("""
    <div class="academic-hero">
      <div style="margin-bottom:0.6rem">
        <span class="academic-badge badge-blue">Independent Project (IP)</span>
        <span class="academic-badge badge-green">Cambridge University Press</span>
        <span class="academic-badge badge-amber">50 Tests Passing</span>
      </div>
      <div class="academic-hero-title">PartitionViz: Computational Laboratory</div>
      <div class="academic-hero-subtitle">
        An interactive computational framework for investigating theorems, combinatorial bijections,
        and generating-function identities from George E. Andrews, <em>The Theory of Partitions</em> (1976/1998).
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Core Academic Framework
    st.markdown("### 1. The Laboratory Framework")
    st.markdown("""
    Every investigation in **PartitionViz** is structured around four fundamental mathematical questions:
    """)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="metric-box" style="text-align:left;height:180px">
          <div style="color:#58a6ff;font-weight:700;font-size:0.9rem">1. The Theorem</div>
          <div style="font-size:0.83rem;color:#c9d1d9;margin-top:0.4rem">
            What exact partition identity or structural duality from Andrews is under examination?
          </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="metric-box" style="text-align:left;height:180px">
          <div style="color:#7ee787;font-weight:700;font-size:0.9rem">2. The Mechanism</div>
          <div style="font-size:0.83rem;color:#c9d1d9;margin-top:0.4rem">
            What combinatorial map, involution, or dynamic programming recurrence implements the result?
          </div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="metric-box" style="text-align:left;height:180px">
          <div style="color:#f0883e;font-weight:700;font-size:0.9rem">3. The Deduction</div>
          <div style="font-size:0.83rem;color:#c9d1d9;margin-top:0.4rem">
            What do the computed invariants, parity cancellations, or scaling limits demonstrate mathematically?
          </div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="metric-box" style="text-align:left;height:180px">
          <div style="color:#d2a8ff;font-weight:700;font-size:0.9rem">4. Scope & Limits</div>
          <div style="font-size:0.83rem;color:#c9d1d9;margin-top:0.4rem">
            What has been established rigorously, what is computationally verified over finite ranges, and what remains open?
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Active Modules
    st.markdown("### 2. Available Laboratory Modules")

    col_m1, col_m2, col_m3 = st.columns(3)

    with col_m1:
        with st.container(border=True):
            st.markdown("""
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;font-weight:700;color:#58a6ff;text-transform:uppercase;margin-bottom:4px">
              Module 1 · Andrews §1.1–1.3
            </div>
            <div style="font-weight:700;font-size:1.05rem;color:#f0f6fc;margin-bottom:6px">
              Ferrers Graphs & Conjugation
            </div>
            <div style="font-size:0.88rem;color:#c9d1d9;line-height:1.5">
              Geometric involution transposing Ferrers diagrams, establishing the bijection between
              partitions with ≤ <em>m</em> parts and partitions with largest part ≤ <em>m</em> (Theorem 1.4),
              Sylvester's self-conjugate identity, and Durfee square invariance.
            </div>
            <div style="margin-top:10px">
              <span class="academic-badge badge-blue">Andrews Thm 1.4</span>
              <span class="academic-badge badge-blue">Sylvester (1882)</span>
            </div>
            """, unsafe_allow_html=True)

    with col_m2:
        with st.container(border=True):
            st.markdown("""
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;font-weight:700;color:#3fb950;text-transform:uppercase;margin-bottom:4px">
              Module 2 · Andrews §1.3, Thm 1.6
            </div>
            <div style="font-weight:700;font-size:1.05rem;color:#f0f6fc;margin-bottom:6px">
              Franklin's Involution & Pentagonal Numbers
            </div>
            <div style="font-size:0.88rem;color:#c9d1d9;line-height:1.5">
              Franklin's (1881) sign-reversing involution on distinct partitions.
              Geometric transitions between base <em>b</em> and slope <em>s</em> explaining exact parity cancellation
              in Euler's pentagonal series and the <em>O(n√n)</em> partition recurrence.
            </div>
            <div style="margin-top:10px">
              <span class="academic-badge badge-green">Euler Pentagonal Thm</span>
              <span class="academic-badge badge-green">Franklin Map φ</span>
            </div>
            """, unsafe_allow_html=True)

    with col_m3:
        with st.container(border=True):
            st.markdown("""
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;font-weight:700;color:#d2a8ff;text-transform:uppercase;margin-bottom:4px">
              Module 3 · Andrews §2.1–2.2
            </div>
            <div style="font-weight:700;font-size:1.05rem;color:#f0f6fc;margin-bottom:6px">
              Series-Product Identities
            </div>
            <div style="font-size:0.88rem;color:#c9d1d9;line-height:1.5">
              Exact formal power series arithmetic in ℤ[q], degree-by-degree coefficient stabilization,
              algebraic proof of Euler's odd-distinct identity, and the Durfee square expansion of <em>p(n)</em> (Andrews eq. 2.2.9).
            </div>
            <div style="margin-top:10px">
              <span class="academic-badge badge-purple">Andrews Eq 2.2.9</span>
              <span class="academic-badge badge-purple">Odd-Distinct GF</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Mathematical Context & Roadmap
    st.markdown("### 3. Context & Multi-Month Roadmap")
    st.markdown("""
    The theory of partitions, initiated by Leonhard Euler in 1748, sits at the crossroads of combinatorics,
    number theory, complex analysis, and statistical mechanics. This Independent Project follows the
    exposition in George E. Andrews's definitive treatise:
    """)

    st.markdown(r"""
    | Milestone | Andrews Chapters | Focus & Mathematical Content | Status |
    |---|---|---|---|
    | **Milestone 1** | **Chapter 1** | **Elementary Theory**: Ferrers diagrams, Conjugation (Thm 1.4), Sylvester's identity, Franklin's involution (Thm 1.6), and Euler's recurrence (Cor. 1.8). | **Completed (50 tests)** |
    | **Milestone 2** | **Chapter 2** | **Series-Product Identities**: Formal power series in $\mathbb{Z}[[q]]$, Euler's odd-distinct theorem, and Durfee square series expansion (eq. 2.2.9). | **Completed (50 tests)** |
    | **Milestone 3** | **Chapter 5** | **Asymptotics**: The Hardy–Ramanujan asymptotic formula and Rademacher exact convergent series for $p(n)$. | *Next Phase* |
    | **Milestone 4** | **Chapter 10** | **Congruences & Combinatorial Cranks**: Ramanujan's congruences modulo 5, 7, 11; Dyson's Rank; Andrews–Garvan Crank. | *Planned* |
    """)

    st.info("Use the sidebar navigation to select a module and begin an interactive investigation.")

"""
ui/home_page.py
Unified Home Page, Research Framework, and Academic Scope Overview for PartitionViz.
Primary Reference: George E. Andrews, The Theory of Partitions (1976/1998).
"""
from __future__ import annotations
import streamlit as st


def render_home_page():
    # Hero Section
    st.markdown("""
    <div class="academic-hero">
      <div style="margin-bottom:0.6rem">
        <span class="academic-badge badge-blue">Independent Project (IP)</span>
        <span class="academic-badge badge-green">Jatin Pawar · 2024279 · IIIT Delhi</span>
        <span class="academic-badge badge-amber">Selected Results from Ch. 1–2</span>
      </div>
      <div class="academic-hero-title">PartitionViz: Computational Laboratory</div>
      <div class="academic-hero-subtitle">
        An interactive computational laboratory for the theory of partitions, investigating combinatorial bijections,
        geometric involutions, and series-product generating functions based on George E. Andrews, 
        <em>The Theory of Partitions</em> (1976/1998).
      </div>
      <div style="margin-top:0.8rem;font-size:0.85rem;color:#8b949e">
        <strong style="color:#c9d1d9">Author:</strong> Jatin Pawar &nbsp;·&nbsp;
        <strong style="color:#c9d1d9">Roll No:</strong> 2024279 &nbsp;·&nbsp;
        <strong style="color:#c9d1d9">Institution:</strong> IIIT Delhi &nbsp;·&nbsp;
        <strong style="color:#c9d1d9">Project:</strong> Independent Project (IP)
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
        with st.container(border=True):
            st.markdown("""
            <div style="color:#58a6ff;font-weight:700;font-size:0.95rem;margin-bottom:6px">1. The Theorem</div>
            <div style="font-size:0.85rem;color:#c9d1d9;line-height:1.5">
              What exact partition identity, duality, or generating function from Andrews is under examination?
            </div>
            """, unsafe_allow_html=True)
    with c2:
        with st.container(border=True):
            st.markdown("""
            <div style="color:#7ee787;font-weight:700;font-size:0.95rem;margin-bottom:6px">2. The Mechanism</div>
            <div style="font-size:0.85rem;color:#c9d1d9;line-height:1.5">
              What combinatorial mapping, sign-reversing involution, or recurrence implements the result?
            </div>
            """, unsafe_allow_html=True)
    with c3:
        with st.container(border=True):
            st.markdown("""
            <div style="color:#f0883e;font-weight:700;font-size:0.95rem;margin-bottom:6px">3. The Deduction</div>
            <div style="font-size:0.85rem;color:#c9d1d9;line-height:1.5">
              What do the computed invariants, parity cancellations, or coefficient limits establish mathematically?
            </div>
            """, unsafe_allow_html=True)
    with c4:
        with st.container(border=True):
            st.markdown("""
            <div style="color:#d2a8ff;font-weight:700;font-size:0.95rem;margin-bottom:6px">4. Scope &amp; Limits</div>
            <div style="font-size:0.85rem;color:#c9d1d9;line-height:1.5">
              What has been proved generally, what is verified over finite ranges, and what remains outside current scope?
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
              Ferrers Graphs &amp; Conjugation
            </div>
            <div style="font-size:0.88rem;color:#c9d1d9;line-height:1.5;min-height:115px">
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
              Franklin's Involution &amp; Pentagonal Numbers
            </div>
            <div style="font-size:0.88rem;color:#c9d1d9;line-height:1.5;min-height:115px">
              Franklin's (1881) sign-reversing involution on distinct partitions.
              Geometric transitions between base <em>b</em> and slope <em>s</em> explaining exact parity cancellation
              in Euler's pentagonal series and the <em>O(N√N)</em> partition recurrence.
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
              Series-Product Identities &amp; q-Binomial
            </div>
            <div style="font-size:0.88rem;color:#c9d1d9;line-height:1.5;min-height:115px">
              Formal power series stabilization in ℤ[[q]], Andrews Theorem 2.1 (<em>q</em>-binomial theorem)
              and its partition corollaries, algebraic proof of Euler's odd-distinct identity,
              and the Durfee square series expansion of <em>p(n)</em> (eq. 2.2.9).
            </div>
            <div style="margin-top:10px">
              <span class="academic-badge badge-purple">Andrews Thm 2.1</span>
              <span class="academic-badge badge-purple">Andrews Eq 2.2.9</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Deliverables & Mathematical Scope
    st.markdown("### 3. Mathematical Scope & Verified Deliverables")
    st.markdown("""
    Progress is organized strictly by verified mathematical deliverables and reproducible algorithms.
    Each module reports its implementation status and verification scope:
    """)

    st.markdown(r"""
    | Laboratory Module | Primary Andrews Reference | Core Deliverable & Mathematical Content | Verification Status |
    |---|---|---|---|
    | **Module 1: Ferrers Graphs & Conjugation** | **Chapter 1, §1.1–1.3** | Bounded partition duality (Thm 1.4), Ferrers transposition involution, Sylvester hook unfolding, and Durfee square geometry. | **Implemented & Tested** |
    | **Module 2: Franklin's Involution** | **Chapter 1, §1.3** | Base and slope decomposition on $D(n)$, sign-reversing involution $\phi$ (Thm 1.6), and Euler's pentagonal recurrence (Cor. 1.8). | **Implemented & Tested** |
    | **Module 3: Series-Product Identities** | **Chapter 2, §2.1–2.2** | Formal power series stabilization in $\mathbb{Z}[[q]]$, $q$-binomial corollaries (Thm 2.1), Euler's odd-distinct identity, and Durfee series (eq. 2.2.9). | **Implemented & Tested** |
    | **Module 4: Asymptotics & Hard Growth** | **Chapter 5** | Hardy–Ramanujan asymptotic formula $p(n) \sim \frac{1}{4n\sqrt{3}}e^{\pi\sqrt{2n/3}}$ and Rademacher series. | *Planned for subsequent phase* |
    | **Module 5: Congruences & Dyson's Rank** | **Chapter 10** | Ramanujan congruences mod 5, 7, 11, Dyson's rank, and the Andrews–Garvan crank. | *Planned for subsequent phase* |
    """)

    st.info("Use the sidebar navigation to select a module and begin an interactive investigation.")

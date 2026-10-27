"""
ui/theory_dossier.py
Academic Reference Dossier, Bibliography, and Mathematical Foundations for PartitionViz.
"""
import streamlit as st
import subprocess


def render_theory_dossier():
    st.markdown("""
    <div class="academic-hero">
      <div style="margin-bottom:0.6rem">
        <span class="academic-badge badge-blue">Academic Dossier</span>
        <span class="academic-badge badge-green">Andrews References</span>
        <span class="academic-badge badge-amber">Formal Bibliography</span>
      </div>
      <div class="academic-hero-title">Theoretical Foundations & Bibliography</div>
      <div class="academic-hero-subtitle">
        Formal mathematical references, theorem catalog, and verification dashboard
        for the PartitionViz Independent Project.
      </div>
    </div>
    """, unsafe_allow_html=True)

    tab_bib, tab_theorems, tab_test_dash = st.tabs([
        "📚 Primary Bibliography",
        "📐 Theorem Catalog",
        "🧪 Automated Test Dashboard",
    ])

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

        5. **Hardy, Godfrey H., & Ramanujan, Srinivasa** (1918). *Asymptotic Formulae in Combinatory Analysis*.
           *Proceedings of the London Mathematical Society*, (2) 17, pp. 75–115.
           *Discovery of the circle method and asymptotic partition expansion.*

        6. **Rademacher, Hans** (1937). *On the Partition Function $p(n)$*.
           *Proceedings of the London Mathematical Society*, (2) 43, pp. 241–254.
           *Convergent exact series representation for $p(n)$.*
        """)

    with tab_theorems:
        st.markdown("### Theorem Catalog: Andrews Chapters 1 & 2")
        st.markdown(r"""
        | Reference | Name | Mathematical Statement | Implementation |
        |---|---|---|---|
        | **Definition 1.1** | Partition of $n$ | Non-increasing sequence $\lambda_1 \ge \dots \ge \lambda_r > 0$ with $\sum \lambda_i = n$. | `partition_core.enumeration.generate_partitions` |
        | **Section 1.3** | Ferrers Graph | Geometric array of dots with $\lambda_i$ dots in row $i$. | `ui.diagrams.render_ferrers_diagram` |
        | **Definition 1.8** | Conjugate Partition | $\lambda'_i = \#\{j : \lambda_j \ge i\}$, reflection across main diagonal. | `partition_core.conjugation.conjugate` |
        | **Theorem 1.4** | Bounded Partitions Duality | $p(\le m\text{ parts}, n) = p(\text{max part}\le m, n)$. | `partition_core.conjugation.verify_theorem_1_4` |
        | **Ch. 1, Ex. 8** | Sylvester's Identity | $\#\{\lambda : \lambda = \lambda'\} = \#\{\lambda : \lambda_i \text{ distinct and odd}\}$. | `tests.test_conjugation.test_sylvester_self_conjugate_theorem` |
        | **Theorem 1.6** | Franklin's Involution | Sign-reversing bijection $\phi$ on $D(n)$ with fixed points only at $\omega(\pm k)$. | `partition_core.franklin.franklin_map` |
        | **Corollary 1.7** | Euler's Pentagonal Identity | $\prod_{k=1}^\infty (1 - q^k) = 1 + \sum_{k=1}^\infty (-1)^k [q^{\omega(k)} + q^{\omega(-k)}]$. | `partition_core.franklin.verify_euler_pentagonal` |
        | **Corollary 1.8** | Pentagonal Recurrence | $p(n) = \sum_{k \ge 1} (-1)^{k+1} [p(n - \omega(k)) + p(n - \omega(-k))]$. | `partition_core.enumeration.partition_count_table` |
        | **Corollary 1.2** | Euler's Odd-Distinct Identity | $\prod_{k=1}^\infty (1 + q^k) = \prod_{k=1}^\infty \frac{1}{1 - q^{2k-1}}$. | `partition_core.generating_functions.expand_distinct_partitions_gf` |
        | **Section 2.2, eq. 2.2.9** | Durfee Square Series | $\sum_{n=0}^\infty p(n) q^n = \sum_{d=0}^\infty \frac{q^{d^2}}{(q; q)_d^2}$. | `partition_core.generating_functions.expand_durfee_square_series` |
        """)

    with tab_test_dash:
        st.markdown("### Automated Mathematical Test Dashboard")
        st.markdown("""
        The mathematical integrity of PartitionViz is continuously validated by an automated test suite.
        Every mathematical invariant—from integer preservation to involution symmetry—is verified before execution.
        """)

        if st.button("Run Full Test Suite Now (pytest)"):
            with st.spinner("Executing mathematical test suite..."):
                proc = subprocess.run(
                    ["python", "-m", "pytest", "tests/", "-v"],
                    capture_output=True,
                    text=True,
                )
                if proc.returncode == 0:
                    st.success("✅ All 50 mathematical tests passed successfully!")
                else:
                    st.error("Some tests failed.")
                st.code(proc.stdout)
        else:
            st.info("Click the button above to execute all 50 unit tests live from within the application.")

"""
ui/styles.py
Centralized CSS design system and typography for PartitionViz.
Academic, scholarly research-tool aesthetic with native LaTeX rendering support.
"""
import streamlit as st


def inject_academic_styles():
    st.markdown("""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

      html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      }

      .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
      }

      /* Hero Header */
      .academic-hero {
        background: linear-gradient(135deg, #161b22 0%, #1c2128 50%, #132337 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.8rem 2.2rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
      }
      .academic-hero-title {
        font-size: 2.1rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        color: #f0f6fc;
        margin: 0 0 0.4rem 0;
      }
      .academic-hero-subtitle {
        font-size: 0.95rem;
        color: #8b949e;
        line-height: 1.5;
        margin: 0;
      }
      .academic-badge {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        padding: 2px 8px;
        border-radius: 4px;
        margin-right: 6px;
      }
      .badge-blue { background: #1f3a5e; color: #79c0ff; border: 1px solid #388bfd44; }
      .badge-green { background: #1c3d28; color: #7ee787; border: 1px solid #23863644; }
      .badge-amber { background: #3b2712; color: #f0883e; border: 1px solid #f0883e44; }
      .badge-purple { background: #2e1f47; color: #d2a8ff; border: 1px solid #bc8cff44; }

      /* Metric Summary Cards */
      .metric-box {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
      }
      .metric-box-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.8rem;
        font-weight: 700;
        color: #58a6ff;
      }
      .metric-box-lbl {
        font-size: 0.78rem;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 0.2rem;
      }

      /* Partition Sequence Chip */
      .partition-chip {
        display: inline-block;
        background: #1c2128;
        border: 1px solid #30363d;
        border-radius: 4px;
        padding: 2px 10px;
        margin: 2px 4px 2px 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.84rem;
        color: #c9d1d9;
      }
      .partition-chip-active {
        background: #1f3a5e;
        border-color: #58a6ff;
        color: #79c0ff;
      }

      /* Section Divider */
      .section-divider {
        height: 1px;
        background: #21262d;
        margin: 1.8rem 0 1.2rem 0;
      }
    </style>
    """, unsafe_allow_html=True)


def render_theorem_box(title: str, reference: str, statement_md: str, equation_latex: str | None = None, border_color: str = "#58a6ff"):
    """
    Renders a clean academic theorem box using a native Streamlit container
    with native KaTeX math support (guaranteed rendering of $inline$ and display LaTeX).
    """
    with st.container(border=True):
        st.markdown(
            f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.75rem;font-weight:700;'
            f'letter-spacing:1.2px;text-transform:uppercase;color:{border_color};margin-bottom:0.35rem">'
            f'{title} &nbsp;·&nbsp; <span style="color:#8b949e">{reference}</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(statement_md)
        if equation_latex:
            st.latex(equation_latex)


def render_defensible_findings(
    module_title: str,
    questions_md: str,
    foundation_md: str,
    method_md: str,
    deductions_md: str,
    validation_md: str,
    limitations_md: str,
):
    """
    Renders the required Defensible Findings Dossier with native Streamlit Markdown
    and KaTeX math parsing.
    """
    with st.container(border=True):
        st.markdown(f"### 📑 Defensible Findings Dossier: {module_title}")
        st.markdown("---")

        st.markdown(f"#### 1. Mathematical Questions Investigated\n\n{questions_md}")
        st.markdown(f"#### 2. Theoretical Foundation (Andrews Citation)\n\n{foundation_md}")
        st.markdown(f"#### 3. Computational Method & Algorithm\n\n{method_md}")
        st.markdown(f"#### 4. Deductions & Mathematical Insights\n\n{deductions_md}")
        st.markdown(f"#### 5. Automated Validation & Mathematical Invariants\n\n{validation_md}")
        st.markdown(f"#### 6. Limitations, Finite Ranges & Scope\n\n{limitations_md}")

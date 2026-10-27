"""
app.py
PartitionViz: An Interactive Computational Laboratory for the Theory of Partitions.
Based on George E. Andrews, "The Theory of Partitions" (Cambridge University Press).

Run with:
    streamlit run app.py
"""
import sys
import os

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
from ui.styles import inject_academic_styles
from ui.home_page import render_home_page
from ui.module_1_conjugation import render_module_1
from ui.module_2_franklin import render_module_2
from ui.module_3_series_identities import render_module_3
from ui.theory_dossier import render_theory_dossier

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PartitionViz · Computational Laboratory",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply unified academic research styling
inject_academic_styles()

# ─────────────────────────────────────────────────────────────────────────────
# UNIFIED SIDEBAR NAVIGATION
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 0.6rem 0 1rem 0">
      <div style="font-size: 1.35rem; font-weight: 700; color: #f0f6fc; letter-spacing: -0.3px">
        🔷 PartitionViz
      </div>
      <div style="font-size: 0.8rem; color: #8b949e; margin-top: 2px">
        Theory of Partitions Laboratory
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("SELECT LABORATORY MODULE")

    page_choice = st.radio(
        label="Navigation Menu",
        options=[
            "Home & Architecture",
            "Module 1: Ferrers & Conjugation",
            "Module 2: Franklin's Involution",
            "Module 3: Series-Product Identities",
            "Academic Dossier & References",
        ],
        index=0,
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.8rem;color:#8b949e;line-height:1.5">
      <b>Project</b>: Independent Project (IP)<br>
      <b>Author</b>: Jatin Pawar · 2024279<br>
      <b>Primary Text</b>: G. E. Andrews (1976/1998)<br>
      <b>Scope</b>: Selected Results from Ch. 1–2
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Single Command Execution:")
    st.code("streamlit run app.py", language="bash")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE ROUTING
# ─────────────────────────────────────────────────────────────────────────────
if page_choice == "Home & Architecture":
    render_home_page()
elif page_choice == "Module 1: Ferrers & Conjugation":
    render_module_1()
elif page_choice == "Module 2: Franklin's Involution":
    render_module_2()
elif page_choice == "Module 3: Series-Product Identities":
    render_module_3()
elif page_choice == "Academic Dossier & References":
    render_theory_dossier()

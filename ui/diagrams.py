"""
ui/diagrams.py
Mathematical diagram rendering for Ferrers graphs, transposition reflection,
and Franklin's slope-and-base decompositions using Plotly.
"""
from __future__ import annotations
import plotly.graph_objects as go
from partition_core.enumeration import Partition


def partition_to_latex(lam: Partition) -> str:
    if not lam:
        return r"\emptyset"
    return "(" + " + ".join(str(p) for p in lam) + ")"


def partition_to_str(lam: Partition) -> str:
    if not lam:
        return "∅"
    return "(" + " + ".join(str(p) for p in lam) + ")"


def render_ferrers_diagram(
    lam: Partition,
    title: str = "",
    highlight_col: int | None = None,
    color_dots: str = "#58a6ff",
    bg_color: str = "#161b22",
) -> go.Figure:
    """
    Render a clean Ferrers diagram of partition lam.
    Row 0 is top row (largest part, Andrews convention).
    """
    if not lam:
        fig = go.Figure()
        fig.update_layout(
            title=dict(text=title, font=dict(size=14, color="#8b949e")),
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            height=200,
        )
        return fig

    rows = len(lam)
    cols = lam[0]

    x_dots, y_dots, colors_list = [], [], []

    for r in range(rows):
        for c in range(lam[r]):
            x_dots.append(c)
            y_dots.append(-r)
            if highlight_col is not None and c == highlight_col:
                colors_list.append("#f0883e")
            else:
                colors_list.append(color_dots)

    # Ghost bounding rectangle dots to visualize ambient grid
    x_ghost, y_ghost = [], []
    for r in range(rows):
        for c in range(cols):
            if c >= lam[r]:
                x_ghost.append(c)
                y_ghost.append(-r)

    fig = go.Figure()

    if x_ghost:
        fig.add_trace(go.Scatter(
            x=x_ghost, y=y_ghost,
            mode="markers",
            marker=dict(size=16, color="#21262d", symbol="circle"),
            hoverinfo="skip",
            showlegend=False,
        ))

    fig.add_trace(go.Scatter(
        x=x_dots, y=y_dots,
        mode="markers",
        marker=dict(
            size=20,
            color=colors_list,
            line=dict(width=1.5, color="#0d1117"),
            symbol="circle",
        ),
        hovertemplate="Part %{customdata[0]} (Row %{customdata[0]}): Col %{customdata[1]}<extra></extra>",
        customdata=[[(-y + 1), (x + 1)] for x, y in zip(x_dots, y_dots)],
        showlegend=False,
    ))

    # Row headers (part sizes)
    for r, part in enumerate(lam):
        fig.add_annotation(
            x=-0.7, y=-r,
            text=f"<b>{part}</b>",
            showarrow=False,
            font=dict(size=12, color="#8b949e", family="JetBrains Mono"),
            xanchor="right",
        )

    # Column headers (conjugate part heights)
    for c in range(cols):
        col_ht = sum(1 for p in lam if p > c)
        fig.add_annotation(
            x=c, y=0.75,
            text=f"<b>{col_ht}</b>",
            showarrow=False,
            font=dict(
                size=12,
                color="#f0883e" if highlight_col == c else "#8b949e",
                family="JetBrains Mono",
            ),
            xanchor="center",
        )

    fig.update_layout(
        title=dict(text=title, font=dict(size=13, color="#c9d1d9"), x=0.5, xanchor="center"),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        xaxis=dict(visible=False, range=[-1.4, max(cols, 1) + 0.5]),
        yaxis=dict(visible=False, range=[-rows - 0.5, 1.3]),
        margin=dict(l=35, r=20, t=45, b=20),
        height=max(240, 50 * rows + 70),
    )
    return fig


def render_franklin_diagram(
    details: dict,
    title: str = "",
    bg_color: str = "#161b22",
) -> go.Figure:
    """
    Render a Ferrers diagram with explicit geometric highlighting of:
    - Base b: amber (#f0883e)
    - Slope s: emerald (#3fb950)
    - Intersection: crimson (#f85149)
    - Body cells: blue (#58a6ff)
    """
    lam = details.get("lam", ())
    if not lam:
        fig = go.Figure()
        fig.update_layout(
            title=dict(text=title, font=dict(size=13, color="#8b949e")),
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            height=200,
        )
        return fig

    rows = len(lam)
    cols = lam[0]

    base_set = set(details.get("base_coords", []))
    slope_set = set(details.get("slope_coords", []))
    intersect_set = set(details.get("intersection_coords", []))

    x_dots, y_dots, colors, labels = [], [], [], []

    for r in range(rows):
        for c in range(lam[r]):
            pt = (r, c)
            x_dots.append(c)
            y_dots.append(-r)

            if pt in intersect_set:
                colors.append("#f85149")
                labels.append(f"Intersection (Base & Slope)<br>Row {r+1}, Col {c+1}")
            elif pt in base_set:
                colors.append("#f0883e")
                labels.append(f"Base b={details.get('b', 0)}<br>Row {r+1}, Col {c+1}")
            elif pt in slope_set:
                colors.append("#3fb950")
                labels.append(f"Slope s={details.get('s', 0)}<br>Row {r+1}, Col {c+1}")
            else:
                colors.append("#58a6ff")
                labels.append(f"Part {lam[r]}<br>Row {r+1}, Col {c+1}")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_dots, y=y_dots,
        mode="markers",
        marker=dict(size=20, color=colors, line=dict(width=1.5, color="#0d1117")),
        hovertext=labels,
        hoverinfo="text",
        showlegend=False,
    ))

    # Row labels
    for r, part in enumerate(lam):
        fig.add_annotation(
            x=-0.7, y=-r,
            text=f"<b>{part}</b>",
            showarrow=False,
            font=dict(size=12, color="#8b949e", family="JetBrains Mono"),
            xanchor="right",
        )

    fig.update_layout(
        title=dict(text=title, font=dict(size=13, color="#c9d1d9"), x=0.5, xanchor="center"),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        xaxis=dict(visible=False, range=[-1.4, cols + 0.5]),
        yaxis=dict(visible=False, range=[-rows - 0.5, 0.9]),
        margin=dict(l=35, r=20, t=45, b=20),
        height=max(240, 50 * rows + 70),
    )
    return fig

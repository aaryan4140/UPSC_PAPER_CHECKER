"""Analytics dashboard page - charts and performance tracking."""

from __future__ import annotations

import streamlit as st

from app.state.session import SessionStateManager


def render_analytics_page(session: SessionStateManager):
    """Render the analytics dashboard."""
    st.markdown('<p class="page-header">Analytics Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Track your progress and identify areas for improvement</p>', unsafe_allow_html=True)

    from app.services.analytics_service import AnalyticsService
    svc = AnalyticsService()

    stats = svc.get_overall_stats()

    if stats["total"] == 0:
        st.info("📊 No evaluations yet. Complete your first evaluation to see analytics here.")
        return

    # Top metrics
    cols = st.columns(4)
    with cols[0]:
        st.metric("Total Attempts", stats["total"])
    with cols[1]:
        st.metric("Average Score", f"{stats['average']}%")
    with cols[2]:
        st.metric("Highest Score", f"{stats['highest']}%")
    with cols[3]:
        st.metric("Lowest Score", f"{stats['lowest']}%")

    st.markdown("---")

    # Charts section
    tab_overview, tab_subjects, tab_progress = st.tabs(["📈 Overview", "📚 Subject Analysis", "📅 Progress"])

    with tab_overview:
        _render_overview_charts(svc)

    with tab_subjects:
        _render_subject_charts(svc)

    with tab_progress:
        _render_progress_charts(svc)


def _render_overview_charts(svc):
    """Render overview analytics charts."""
    import plotly.graph_objects as go
    import plotly.express as px

    history = svc.get_recent_attempts(limit=50)
    if not history:
        st.info("Not enough data for charts.")
        return

    # Score distribution
    percentages = [h.get("percentage", 0) for h in history if h.get("percentage")]
    if percentages:
        col1, col2 = st.columns(2)

        with col1:
            fig = go.Figure(data=[go.Histogram(
                x=percentages,
                nbinsx=10,
                marker_color="#1565c0",
                opacity=0.8,
            )])
            fig.update_layout(
                title="Score Distribution",
                xaxis_title="Percentage",
                yaxis_title="Count",
                height=350,
                margin=dict(l=40, r=20, t=50, b=40),
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Strictness vs Score
            strictness_data = {}
            for h in history:
                s = h.get("strictness", 6)
                p = h.get("percentage", 0)
                if s not in strictness_data:
                    strictness_data[s] = []
                strictness_data[s].append(p)

            avg_by_strictness = {k: sum(v)/len(v) for k, v in strictness_data.items()}
            if avg_by_strictness:
                fig = go.Figure(data=[go.Bar(
                    x=list(avg_by_strictness.keys()),
                    y=list(avg_by_strictness.values()),
                    marker_color="#1a237e",
                )])
                fig.update_layout(
                    title="Average Score by Strictness",
                    xaxis_title="Strictness Level",
                    yaxis_title="Avg %",
                    height=350,
                    margin=dict(l=40, r=20, t=50, b=40),
                )
                st.plotly_chart(fig, use_container_width=True)


def _render_subject_charts(svc):
    """Render subject-wise analytics."""
    import plotly.graph_objects as go

    averages = svc.get_subject_averages()
    if not averages:
        st.info("Not enough subject data for charts.")
        return

    col1, col2 = st.columns(2)

    with col1:
        # Bar chart of subject averages
        subjects = list(averages.keys())
        scores = list(averages.values())

        colors = ["#10b981" if s >= 70 else "#f59e0b" if s >= 50 else "#ef4444" for s in scores]

        fig = go.Figure(data=[go.Bar(
            x=subjects,
            y=scores,
            marker_color=colors,
        )])
        fig.update_layout(
            title="Average Score by Subject",
            xaxis_title="Subject",
            yaxis_title="Average %",
            height=400,
            margin=dict(l=40, r=20, t=50, b=80),
        )
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Radar chart if enough subjects
        if len(subjects) >= 3:
            fig = go.Figure(data=go.Scatterpolar(
                r=scores + [scores[0]],
                theta=subjects + [subjects[0]],
                fill="toself",
                fillcolor="rgba(21, 101, 192, 0.2)",
                line_color="#1565c0",
            ))
            fig.update_layout(
                title="Subject Performance Radar",
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                height=400,
                margin=dict(l=40, r=40, t=50, b=40),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least 3 subjects for radar chart.")

    # Subject table
    st.markdown("### Subject Summary")
    table_md = "| Subject | Average % | Status |\n|---------|-----------|--------|\n"
    for k, v in averages.items():
        status = "✓ Good" if v >= 60 else "⚠ Needs Work"
        table_md += f"| {k} | {v} | {status} |\n"
    st.markdown(table_md)


def _render_progress_charts(svc):
    """Render progress over time."""
    import plotly.graph_objects as go

    history = svc.get_recent_attempts(limit=30)
    if len(history) < 2:
        st.info("Need at least 2 attempts to show progress.")
        return

    # Reverse to chronological order
    history = list(reversed(history))

    dates = [h.get("created_at", "")[:10] for h in history]
    scores = [h.get("percentage", 0) for h in history]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(1, len(scores) + 1)),
        y=scores,
        mode="lines+markers",
        line=dict(color="#1565c0", width=3),
        marker=dict(size=8, color="#1a237e"),
        fill="tozeroy",
        fillcolor="rgba(21, 101, 192, 0.1)",
    ))
    fig.update_layout(
        title="Score Trend Over Attempts",
        xaxis_title="Attempt #",
        yaxis_title="Score %",
        height=400,
        yaxis=dict(range=[0, 100]),
        margin=dict(l=40, r=20, t=50, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Moving average
    if len(scores) >= 5:
        ma = [sum(scores[max(0,i-4):i+1])/min(5, i+1) for i in range(len(scores))]
        improvement = ma[-1] - ma[0] if ma else 0
        st.markdown(f"**Trend:** {'📈 Improving' if improvement > 0 else '📉 Declining'} ({improvement:+.1f}% over period)")

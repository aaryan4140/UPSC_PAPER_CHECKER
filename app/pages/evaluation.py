"""Evaluation page - upload, evaluate, and display results."""

from __future__ import annotations

import streamlit as st

from app.state.session import SessionStateManager
from core.enums import Subject, StrictnessLevel


def render_evaluation_page(session: SessionStateManager):
    """Render the complete evaluation page."""
    st.markdown('<p class="page-header">Answer Evaluation</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Upload your handwritten UPSC answer sheet for AI-powered evaluation</p>', unsafe_allow_html=True)

    # Check API key
    from app.services.evaluation_service import EvaluationService
    svc = EvaluationService()
    if not svc.validate_api_key():
        st.error("⚠️ Gemini API key not configured. Please add GEMINI_API_KEY to your .env file.")
        return

    # Show results if available
    if session.get("evaluation_result"):
        _render_results(session)
        st.markdown("---")
        if st.button("📄 New Evaluation", use_container_width=True):
            session.set("evaluation_result", None)
            session.set("ocr_result", None)
            session.set("paper_data", None)
            st.rerun()
        return

    # Upload section
    _render_upload_section(session, svc)


def _render_upload_section(session: SessionStateManager, svc):
    """Render the PDF upload and evaluation trigger."""
    col_upload, col_thumb = st.columns([3, 1])

    with col_upload:
        uploaded_file = st.file_uploader(
            "Upload Answer Sheet (PDF)",
            type=["pdf"],
            help="Upload a handwritten UPSC answer sheet in PDF format (max 50 MB)",
            key="pdf_uploader",
        )

        if uploaded_file:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            st.success(f"✓ **{uploaded_file.name}** uploaded ({file_size_mb:.1f} MB)")

            if st.button("🚀 Evaluate Answer Sheet", type="primary"):
                _run_evaluation(session, svc, uploaded_file)

    if uploaded_file:
        with col_thumb:
            _render_pdf_preview(uploaded_file, session)


def _render_pdf_preview(uploaded_file, session: SessionStateManager):
    """Render a single-page preview with navigation arrows."""
    try:
        from pdf2image import convert_from_bytes
        import PyPDF2
        import io

        file_bytes = uploaded_file.getvalue()

        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        total_pages = len(reader.pages)

        current_page = session.get("preview_page", 1)
        current_page = max(1, min(current_page, total_pages))

        images = convert_from_bytes(
            file_bytes, dpi=72, first_page=current_page, last_page=current_page
        )
        if images:
            st.image(images[0], use_container_width=True)

        col_prev, col_info, col_next = st.columns([1, 2, 1])
        with col_prev:
            if st.button("◀", key="prev_page", disabled=(current_page <= 1)):
                session.set("preview_page", current_page - 1)
                st.rerun()
        with col_info:
            st.caption(f"{current_page} / {total_pages}")
        with col_next:
            if st.button("▶", key="next_page", disabled=(current_page >= total_pages)):
                session.set("preview_page", current_page + 1)
                st.rerun()

    except Exception:
        st.caption("Preview unavailable")


def _run_evaluation(session: SessionStateManager, svc, uploaded_file):
    """Execute the evaluation pipeline with progress display."""
    subject_str = session.get("selected_subject", "Polity")
    strictness_val = session.get("strictness", 6)

    try:
        subject = Subject(subject_str)
    except ValueError:
        subject = Subject.POLITY

    strictness = StrictnessLevel(strictness_val)

    progress_bar = st.progress(0, text="Starting evaluation...")
    status_text = st.empty()

    def update_progress(message: str, progress: float):
        progress_bar.progress(min(progress, 1.0), text=message)
        status_text.markdown(f"*{message}*")

    with st.spinner("Processing your answer sheet..."):
        output = svc.evaluate(
            file_bytes=uploaded_file.getvalue(),
            filename=uploaded_file.name,
            subject=subject,
            strictness=strictness,
            progress_callback=update_progress,
        )

    progress_bar.empty()
    status_text.empty()

    if output.status.value == "failed":
        st.error(f"❌ Evaluation failed: {output.error_message}")
        return

    # Store results in session
    session.set("evaluation_result", output.evaluation_result)
    session.set("paper_data", output.paper)
    session.set("eval_time", output.processing_time)

    # Save to history
    from app.services.history_service import HistoryService
    history_svc = HistoryService()
    if output.evaluation_result:
        history_svc.save_attempt({
            "paper_id": output.paper.id if output.paper else "",
            "subject": subject_str,
            "strictness": strictness_val,
            "total_awarded": output.evaluation_result.total_marks_awarded,
            "total_possible": output.evaluation_result.total_marks_possible,
            "percentage": output.evaluation_result.overall_percentage,
        })

    st.rerun()


def _render_results(session: SessionStateManager):
    """Render evaluation results."""
    result = session.get("evaluation_result")
    paper = session.get("paper_data")
    eval_time = session.get("eval_time", 0)

    if not result:
        return

    # Summary hero
    st.markdown(f"""
    <div class="score-hero">
        <div class="label">Total Score</div>
        <div class="big">{result.total_marks_awarded}/{result.total_marks_possible}</div>
        <div class="label">{result.overall_percentage:.1f}% | {len(result.question_evaluations)} Questions | {eval_time:.0f}s</div>
    </div>
    """, unsafe_allow_html=True)

    # Metrics row
    cols = st.columns(4)
    with cols[0]:
        st.metric("Questions", len(result.question_evaluations))
    with cols[1]:
        st.metric("Marks Obtained", f"{result.total_marks_awarded}")
    with cols[2]:
        st.metric("Percentage", f"{result.overall_percentage:.1f}%")
    with cols[3]:
        st.metric("Strictness", f"{result.strictness_used}/10")

    st.markdown("---")

    # Tabs for different views
    tab_results, tab_report, tab_download = st.tabs(
        ["📊 Question Analysis", "📋 Full Report", "⬇️ Download"]
    )

    with tab_results:
        _render_question_cards(result, paper)

    with tab_report:
        _render_html_report(result, session)

    with tab_download:
        _render_downloads(result, session)


def _render_question_cards(result, paper):
    """Render individual question evaluation cards."""
    for qe in result.question_evaluations:
        with st.expander(f"**Q{qe.question_number}** — {qe.awarded_marks}/{qe.max_marks} marks ({qe.percentage:.0f}%)", expanded=False):
            # Score and rubric
            col_score, col_rubric = st.columns([1, 2])

            with col_score:
                pct = qe.percentage
                color = "#10b981" if pct >= 70 else "#f59e0b" if pct >= 50 else "#ef4444"
                st.markdown(f"""
                <div style="text-align:center; padding:1rem;">
                    <div style="font-size:2.5rem; font-weight:700; color:{color};">{qe.awarded_marks}</div>
                    <div style="font-size:0.9rem; color:#90a4ae;">out of {qe.max_marks}</div>
                </div>
                """, unsafe_allow_html=True)

            with col_rubric:
                st.markdown("**Rubric Breakdown**")
                for rs in qe.rubric_scores:
                    pct_val = (rs.score / rs.max_score * 100) if rs.max_score > 0 else 0
                    name = rs.component.replace("_", " ").title()
                    st.markdown(f"""
                    <div class="rubric-bar">
                        <span class="name">{name}</span>
                        <div class="bar-bg"><div class="bar-fill" style="width:{pct_val}%"></div></div>
                        <span class="score">{rs.score:.1f}/{rs.max_score:.0f}</span>
                    </div>
                    """, unsafe_allow_html=True)

            # Strengths & Weaknesses
            if qe.strengths or qe.weaknesses:
                st.markdown("---")
                c1, c2 = st.columns(2)
                with c1:
                    if qe.strengths:
                        st.markdown("**✓ Strengths**")
                        for s in qe.strengths[:4]:
                            st.markdown(f"- {s}")
                with c2:
                    if qe.weaknesses:
                        st.markdown("**✗ Weaknesses**")
                        for w in qe.weaknesses[:4]:
                            st.markdown(f"- {w}")

            # Missing Content
            if qe.missing_content:
                st.markdown("---")
                st.markdown("**Missing Content**")
                for i, item in enumerate(qe.missing_content[:6]):
                    priority_class = "missing-high" if i < 2 else "missing-medium" if i < 4 else "missing-low"
                    st.markdown(f'<span class="{priority_class}">{item}</span>', unsafe_allow_html=True)

            # UPSC Feedback
            if qe.upsc_style_feedback:
                st.markdown("---")
                st.markdown(f'<div class="feedback-box"><strong>Examiner Note:</strong> {qe.upsc_style_feedback}</div>', unsafe_allow_html=True)

            # Model Answer & Improvement (side-by-side)
            if qe.model_answer:
                st.markdown("---")
                st.markdown("**Model Answer vs Candidate Answer**")
                ma_col, ca_col = st.columns(2)
                with ca_col:
                    st.markdown("*Candidate Answer*")
                    answer_text = ""
                    if paper and paper.answers:
                        for ans in paper.answers:
                            if ans.question_number == qe.question_number:
                                answer_text = ans.text
                                break
                    st.text_area("", value=answer_text[:1000] if answer_text else "N/A", height=200, disabled=True, key=f"ca_{qe.question_number}")
                with ma_col:
                    st.markdown("*Model Answer*")
                    st.text_area("", value=qe.model_answer[:1000], height=200, disabled=True, key=f"ma_{qe.question_number}")

            # Improvement Suggestions
            if qe.improvement_suggestions:
                st.markdown("---")
                st.markdown("**Improvement Suggestions**")
                for suggestion in qe.improvement_suggestions[:4]:
                    st.info(suggestion)


def _render_html_report(result, session):
    """Render the full HTML report inline."""
    from app.services.report_service import ReportService
    report_svc = ReportService()

    subject = session.get("selected_subject", "")
    strictness = session.get("strictness", 6)
    html = report_svc.generate_html_report(result, subject, strictness)
    import streamlit.components.v1 as components
    components.html(html, height=800, scrolling=True)



def _render_downloads(result, session):
    """Render download buttons for reports."""
    from app.services.report_service import ReportService
    report_svc = ReportService()

    subject = session.get("selected_subject", "")
    strictness = session.get("strictness", 6)

    st.markdown("### Download Reports")

    col1, col2 = st.columns(2)

    with col1:
        html_report = report_svc.generate_html_report(result, subject, strictness)
        st.download_button(
            label="📄 Download HTML Report",
            data=html_report,
            file_name="upsc_evaluation_report.html",
            mime="text/html",
            use_container_width=True,
        )

    with col2:
        pdf_bytes = report_svc.generate_pdf_bytes(result, subject, strictness)
        st.download_button(
            label="📑 Download PDF Report",
            data=pdf_bytes,
            file_name="upsc_evaluation_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    st.markdown("---")
    st.markdown("### Export Data")
    import json
    export_data = {
        "total_marks": result.total_marks_awarded,
        "total_possible": result.total_marks_possible,
        "percentage": result.overall_percentage,
        "questions": [
            {
                "number": qe.question_number,
                "marks": qe.awarded_marks,
                "max": qe.max_marks,
                "strengths": qe.strengths,
                "weaknesses": qe.weaknesses,
                "missing": qe.missing_content[:5],
            }
            for qe in result.question_evaluations
        ],
    }
    st.download_button(
        label="💾 Export JSON Data",
        data=json.dumps(export_data, indent=2),
        file_name="evaluation_data.json",
        mime="application/json",
        use_container_width=True,
    )

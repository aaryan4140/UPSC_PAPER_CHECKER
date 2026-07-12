"""Settings page - application configuration."""

from __future__ import annotations

import streamlit as st

from app.state.session import SessionStateManager


def render_settings_page(session: SessionStateManager):
    """Render the application settings page."""
    st.markdown('<p class="page-header">⚙️ Settings</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Configure application behavior and integrations</p>', unsafe_allow_html=True)

    from app.services.config_service import ConfigurationService
    svc = ConfigurationService()

    config = svc.get_current_config()
    issues = svc.validate_configuration()

    if issues:
        for issue in issues:
            st.warning(f"⚠️ {issue}")

    # Evaluation Settings (moved from sidebar)
    st.markdown("### 📝 Evaluation Settings")
    col_subj, col_strict = st.columns(2)
    with col_subj:
        from core.enums import Subject
        subjects = [s.value for s in Subject.ordered_list()]
        default_subject = session.get("selected_subject", "Polity")
        idx = subjects.index(default_subject) if default_subject in subjects else 0
        selected = st.selectbox("Default Subject", subjects, index=idx, key="settings_subject_select")
        session.set("selected_subject", selected)
    with col_strict:
        from core.enums import StrictnessLevel
        default_strictness = session.get("strictness", 6)
        strictness = st.slider("Default Strictness", 1, 10, default_strictness, key="settings_strictness_slider")
        session.set("strictness", strictness)
        level = StrictnessLevel(strictness)
        st.caption(f"**{level.label}**")

    st.markdown("---")

    # API Configuration
    st.markdown("### 🔑 API Configuration")
    col1, col2 = st.columns(2)
    with col1:
        api_status = "✅ Configured" if config["api_key_configured"] else "❌ Not Configured"
        st.markdown(f"**Gemini API Key:** {api_status}")
        st.markdown(f"**Model:** `{config['gemini_model']}`")
    with col2:
        st.markdown(f"**Temperature:** {config['gemini_temperature']}")
        st.markdown(f"**Max Tokens:** {config['gemini_max_tokens']}")

    st.markdown("---")

    # Model Selection
    st.markdown("### 🤖 Model Settings")
    available_models = svc.get_available_models()
    current_idx = available_models.index(config["gemini_model"]) if config["gemini_model"] in available_models else 0
    st.selectbox("Gemini Model", available_models, index=current_idx, key="settings_model", disabled=True, help="Change in .env file")
    st.caption("Model selection is configured via the .env file (GEMINI_MODEL)")

    st.markdown("---")

    # OCR Configuration
    st.markdown("### 📷 OCR Configuration")
    col1, col2 = st.columns(2)
    with col1:
        providers = svc.get_available_ocr_providers()
        current_provider_idx = providers.index(config["ocr_provider"]) if config["ocr_provider"] in providers else 0
        st.selectbox("OCR Provider", providers, index=current_provider_idx, key="settings_ocr", disabled=True, help="Change in .env file")
    with col2:
        st.number_input("Confidence Threshold", value=config["ocr_confidence_threshold"], min_value=0.1, max_value=1.0, step=0.05, disabled=True, key="settings_threshold")
    st.caption("OCR settings are configured via the .env file")

    st.markdown("---")

    # System Info
    st.markdown("### ℹ️ System Information")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Storage:** {config['storage_engine']}")
        st.markdown(f"**Log Level:** {config['log_level']}")
    with col2:
        st.markdown(f"**Debug Mode:** {'On' if config['debug'] else 'Off'}")
        st.markdown(f"**OCR Language:** {config['ocr_language']}")

    st.markdown("---")
    st.markdown("### 📂 Configuration File")
    st.code("""
# .env file location: project root
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.0-flash
GEMINI_TEMPERATURE=0.3
OCR_PROVIDER=paddleocr
OCR_CONFIDENCE_THRESHOLD=0.6
LOG_LEVEL=INFO
    """, language="bash")

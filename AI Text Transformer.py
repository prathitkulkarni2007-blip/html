import html
import streamlit as st


def inject_css():
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                max-width: 900px;
            }

            .hero-card {
                background: linear-gradient(135deg, #111827, #1f2937);
                color: white;
                padding: 24px;
                border-radius: 20px;
                margin-bottom: 18px;
                box-shadow: 0 12px 30px rgba(0,0,0,0.18);
            }

            .hero-title {
                font-size: 2rem;
                font-weight: 800;
                margin-bottom: 6px;
            }

            .hero-subtitle {
                font-size: 0.98rem;
                color: #d1d5db;
                line-height: 1.6;
            }

            .output-card {
                background: #f8fafc !important;
                color: #111827 !important;
                border: 1px solid #e5e7eb;
                border-radius: 18px;
                padding: 18px;
                margin-top: 14px;
                box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
            }

            .output-label {
                font-size: 0.82rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: #475569 !important;
                margin-bottom: 10px;
            }

            .output-text {
                color: #111827 !important;
                font-size: 1rem;
                line-height: 1.8;
                white-space: pre-wrap;
                word-wrap: break-word;
            }

            .mini-note {
                color: #94a3b8;
                font-size: 0.9rem;
                margin-top: 8px;
            }

            /* Keep input readable on dark textarea background */
            div[data-testid="stTextArea"] textarea {
                color: #f8fafc !important;
                background: transparent !important;
            }

            div[data-testid="stTextArea"] textarea::placeholder {
                color: #94a3b8 !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">AI Text Transformer</div>
            <div class="hero-subtitle">
                Rewrite plain text in a new style while keeping the meaning the same.
                Pick a style, paste your text, and let the transformer do the polish.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_output(text: str):
    safe_text = html.escape(text).replace("\n", "<br>")
    st.markdown(
        f"""
        <div class="output-card">
            <div class="output-label">Transformed Output</div>
            <div class="output-text">{safe_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state():
    st.markdown(
        """
        <div class="output-card">
            <div class="output-label">Transformed Output</div>
            <div class="output-text">
                Your rewritten text will appear here once you click <b>Transform Text</b>.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
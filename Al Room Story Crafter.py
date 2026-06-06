import base64
import html
import streamlit as st


def inject_css():
    st.markdown(
        """
        <style>
            .block-container {
                max-width: 900px;
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
            .hero {
                background: linear-gradient(135deg, #1e1b4b, #312e81);
                color: white;
                padding: 24px;
                border-radius: 20px;
                margin-bottom: 20px;
            }
            .hero-title {
                font-size: 2rem;
                font-weight: 800;
                margin-bottom: 6px;
            }
            .hero-subtitle {
                color: #dbeafe;
                line-height: 1.6;
            }
            .card {
                background: #f8fafc;
                color: #111827;
                border: 1px solid #e5e7eb;
                border-radius: 18px;
                padding: 18px;
                margin-top: 18px;
            }
            .label {
                font-size: 0.8rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: #475569;
                margin-bottom: 8px;
            }
            .title {
                font-size: 1.6rem;
                font-weight: 800;
                color: #1e293b;
                margin-bottom: 10px;
            }
            .text {
                font-size: 1rem;
                line-height: 1.75;
                color: #111827;
                white-space: pre-wrap;
            }
            .room-image {
                width: 100%;
                border-radius: 16px;
                margin-bottom: 16px;
            }
            .error-box {
                margin-bottom: 16px;
                padding: 12px;
                border-radius: 10px;
                background: #fee2e2;
                color: #7f1d1d;
                border: 1px solid #fca5a5;
                font-size: 0.9rem;
                line-height: 1.5;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">AI Room Story Crafter</div>
            <div class="hero-subtitle">
                Generate fantasy room descriptions in structured JSON, validate them,
                and bring the room to life with artwork.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_room_output(room_data: dict):
    image_base64 = base64.b64encode(room_data["image_bytes"]).decode("utf-8")

    title = html.escape(room_data["title"])
    description = html.escape(room_data["description"]).replace("\n", "<br>")
    clue = html.escape(room_data["clue"]).replace("\n", "<br>")
    art_prompt = html.escape(room_data["art_prompt"]).replace("\n", "<br>")

    error_html = ""
    if room_data.get("image_error"):
        error_html = f"""
        <div class="error-box">
            ⚠️ {html.escape(room_data["image_error"])}
        </div>
        """

    st.markdown(
        f"""
        <div class="card">
            <img class="room-image" src="data:image/png;base64,{image_base64}" />
            {error_html}

            <div class="label">Room Title</div>
            <div class="title">{title}</div>

            <div class="label">Description</div>
            <div class="text">{description}</div>

            <br>
            <div class="label">Clue</div>
            <div class="text">{clue}</div>

            <br>
            <div class="label">Art Prompt</div>
            <div class="text">{art_prompt}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state():
    st.markdown(
        """
        <div class="card">
            <div class="label">No Room Yet</div>
            <div class="text">
                Enter a room name and theme, then click <b>Craft Room Story</b>.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
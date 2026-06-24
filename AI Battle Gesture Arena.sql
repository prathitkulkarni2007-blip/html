from __future__ import annotations

import streamlit as st
from PIL import Image

import config
from ai_helpers import build_image_prompt, generate_battle_image, generate_battle_text, get_move_profile
from gesture_utils import load_local_teachable_machine_model, predict_gesture_from_image

st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

LABEL_MAP = {
    "palm": "Palm",
    "Palm": "Palm",
    "open palm": "Palm",
    "Open Palm": "Palm",
    "peace": "Peace",
    "Peace": "Peace",
    "pointer": "Pointer",
    "Pointer": "Pointer",
    "point": "Pointer",
    "Point": "Pointer",
    "thumbs up": "Thumbs Up",
    "Thumbs Up": "Thumbs Up",
    "thumbsup": "Thumbs Up",
    "Thumbsup": "Thumbs Up",
    "no gesture": "No Gesture",
    "No Gesture": "No Gesture",
}

for key in ["prediction", "move_name", "move_text", "move_image", "input_source", "last_key"]:
    if key not in st.session_state:
        st.session_state[key] = None if key in ("prediction", "move_image") else ""


def render_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at 15% 15%, rgba(99,102,241,.20), transparent 20%),
                radial-gradient(circle at 85% 8%, rgba(239,68,68,.18), transparent 20%),
                radial-gradient(circle at 85% 80%, rgba(249,115,22,.15), transparent 22%),
                linear-gradient(180deg, #080b16 0%, #0e1325 100%);
        }
        .block-container {max-width: 1200px; padding-top: 1.5rem; padding-bottom: 2rem;}
        .hero, .panel, .info-card, .move-card {
            background: rgba(13, 19, 38, .78);
            border: 1px solid rgba(255,255,255,.10);
            box-shadow: 0 20px 50px rgba(0,0,0,.25);
            backdrop-filter: blur(10px);
        }
        .hero {
            border-radius: 28px;
            padding: 1.35rem 1.4rem;
            margin-bottom: 1rem;
        }
        .hero h1 {margin: 0 0 .35rem 0; font-size: 2.1rem; line-height: 1.05;}
        .hero p {margin: 0; color: #dbe4ff; font-size: 1rem;}
        .hero-strip {
            margin-top: .9rem;
            display: flex;
            flex-wrap: wrap;
            gap: .55rem;
        }
        .chip {
            display: inline-block;
            padding: .45rem .75rem;
            border-radius: 999px;
            color: #eef2ff;
            font-size: .83rem;
            border: 1px solid rgba(255,255,255,.10);
            background: linear-gradient(90deg, rgba(99,102,241,.22), rgba(236,72,153,.18));
        }
        .panel {
            border-radius: 24px;
            padding: 1rem;
        }
        .pill {
            display: inline-block;
            margin: .45rem 0 .85rem 0;
            padding: .35rem .72rem;
            border-radius: 999px;
            font-size: .84rem;
            color: #eef2ff;
            background: linear-gradient(90deg, rgba(14,165,233,.22), rgba(99,102,241,.22));
            border: 1px solid rgba(255,255,255,.10);
        }
        .info-grid {display: grid; grid-template-columns: repeat(2, 1fr); gap: .8rem; margin-top: .85rem;}
        .info-card, .move-card {border-radius: 20px; padding: 1rem; min-height: 140px;}
        .eyebrow {font-size: .78rem; text-transform: uppercase; letter-spacing: .08em; color: #a5b4fc; margin-bottom: .35rem;}
        .title {font-size: 1.22rem; font-weight: 700; color: #fff; line-height: 1.15;}
        .copy {font-size: .96rem; color: #dbe4ff; line-height: 1.5; margin-top: .45rem;}
        .move-card {margin-bottom: .8rem;}
        .empty-box {
            border: 1px dashed rgba(255,255,255,.18);
            border-radius: 22px;
            padding: 1.2rem;
            color: #dbe4ff;
            background: rgba(255,255,255,.03);
        }
        @media (max-width: 900px) {
            .info-grid {grid-template-columns: 1fr;}
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource(show_spinner=False)
def get_model():
    return load_local_teachable_machine_model(str(config.MODEL_PATH), str(config.LABELS_PATH))


def normalize(label: str) -> str:
    clean = label.strip()
    return LABEL_MAP.get(clean, clean)


def generate_battle_magic(label: str, move_name: str, source: str) -> None:
    with st.spinner("Entering the arena and charging your AI battle move..."):
        st.session_state.move_text = generate_battle_text(label, move_name, source)
        img, err = generate_battle_image(build_image_prompt(move_name, label, source))
        if img is not None:
            st.session_state.move_image = img
        else:
            st.session_state.move_image = None
            st.error(err or "Could not generate the battle action image.")


def prediction_panel(image: Image.Image, source: str) -> None:
    st.session_state.input_source = source
    st.image(image, caption="Battle gesture input", use_container_width=True)
    st.markdown(f"<div class='pill'>Input source: {source.title()}</div>", unsafe_allow_html=True)

    try:
        model, labels = get_model()
        pred = predict_gesture_from_image(model, labels, image, label_map=LABEL_MAP)
        pred["label"] = normalize(pred["label"])
        for item in pred["top_predictions"]:
            item["label"] = normalize(item["label"])
        st.session_state.prediction = pred

        profile = get_move_profile(pred["label"])
        move_name = profile["move"]
        st.session_state.move_name = move_name

        st.success(f"Detected battle gesture: **{pred['label']}**")
        st.progress(float(pred["confidence"]), text=f"Confidence: {pred['confidence']:.1%}")

        st.markdown(
            f"""
            <div class="info-grid">
                <div class="info-card">
                    <div class="eyebrow">Recognised Gesture</div>
                    <div class="title">{pred['label']}</div>
                    <div class="copy">The arena camera matched your pose with this trained gesture class.</div>
                </div>
                <div class="info-card">
                    <div class="eyebrow">Battle Move Unlocked</div>
                    <div class="title">⚔️ {move_name}</div>
                    <div class="copy">Element: {profile['element']}<br>Impact: {profile['impact'].capitalize()}.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        key = f"{source}:{pred['label']}:{pred['confidence']:.4f}"
        if st.session_state.last_key != key:
            if st.button("🔥 Generate Battle Move", use_container_width=True):
                generate_battle_magic(pred["label"], move_name, source)
                st.session_state.last_key = key

        with st.expander("See all battle prediction scores"):
            for item in pred["top_predictions"]:
                st.progress(float(item["confidence"]), text=f"{item['label']} — {item['confidence']:.1%}")
    except Exception as exc:
        st.error(
            f"Model error: {exc}\n\n"
            "Tip: place keras_model.h5 and labels.txt inside models/, and use Python 3.10 or 3.11."
        )


def show_output() -> None:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.subheader("🏟️ Arena Output")

    if st.session_state.move_name:
        st.markdown(
            f"""
            <div class="move-card">
                <div class="eyebrow">Selected Move</div>
                <div class="title">{st.session_state.move_name}</div>
                <div class="copy">Your detected gesture has now been converted into a battle-ready special move.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.session_state.move_text:
        st.markdown(
            f"""
            <div class="move-card">
                <div class="eyebrow">AI Move Description</div>
                <div class="copy">{st.session_state.move_text.replace(chr(10), '<br>')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.session_state.move_image is not None:
        st.image(st.session_state.move_image, caption="AI-generated battle action image", use_container_width=True)
    elif not st.session_state.move_name:
        st.markdown(
            """
            <div class="empty-box">
                <b>No battle move yet.</b><br><br>
                Detect a gesture on the left, then click <b>Generate Battle Move</b> to create the move description and action image.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    render_styles()
    st.markdown(
        f"""
        <div class="hero">
            <h1>{config.APP_ICON} {config.APP_TITLE}</h1>
            <p>{config.APP_SUBTITLE}</p>
            <div class="hero-strip">
                <span class="chip">Gesture Recognition</span>
                <span class="chip">AI Battle Text</span>
                <span class="chip">AI Action Image</span>
                <span class="chip">Arena-Style UI</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("ℹ️ Supported battle gestures"):
        st.markdown(
            """
            Train your Teachable Machine model with four gesture classes such as <b>palm</b>, <b>thumbs up</b>,
            <b>pointer</b>, and <b>peace</b>. These are mapped to arena moves inside <code>ai_helpers.py</code>.
            """,
            unsafe_allow_html=True,
        )

    left, right = st.columns([1, 1], gap="large")
    with left:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.subheader("📷 Battle Input")
        tabs = st.tabs(["Webcam Capture", "Upload Image"])
        with tabs[0]:
            cam = st.camera_input("Capture battle gesture", help=config.CAMERA_HELP)
            if cam:
                prediction_panel(Image.open(cam).convert("RGB"), "webcam")
            else:
                st.info("Take a photo with your webcam to detect a battle gesture.")
        with tabs[1]:
            up = st.file_uploader("Upload a battle gesture image", type=["png", "jpg", "jpeg"])
            if up:
                prediction_panel(Image.open(up).convert("RGB"), "upload")
            else:
                st.info("Upload a hand gesture image to unlock an arena move.")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        show_output()


if __name__ == "__main__":
    main()
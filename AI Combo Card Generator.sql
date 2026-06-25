from __future__ import annotations

import streamlit as st
from PIL import Image

import config
from ai_helpers import (
    build_hidden_prompt,
    create_combo_card,
    generate_magic_response,
    generate_magic_visual,
    get_combo_name_for_gesture,
)
from gesture_utils import load_local_teachable_machine_model, predict_gesture_from_image

st.set_page_config(page_title=config.APP_TITLE, page_icon=config.APP_ICON, layout="wide", initial_sidebar_state="collapsed")

LABEL_MAP = {
    "palm": "Palm", "Palm": "Palm", "open palm": "Palm", "Open Palm": "Palm",
    "peace": "Peace", "Peace": "Peace",
    "pointer": "Pointer", "Pointer": "Pointer", "point": "Pointer", "Point": "Pointer",
    "thumbs up": "Thumbs Up", "Thumbs Up": "Thumbs Up", "thumbsup": "Thumbs Up", "Thumbsup": "Thumbs Up",
}

_DEFAULTS = {
    "prediction": None,
    "captured_image": None,
    "spell_name": "",
    "spell_text": "",
    "spell_prompt": "",
    "spell_scene_image": None,
    "spell_card_image": None,
    "input_source": "",
    "last_generated_key": "",
    "spell_log": [],
    "gesture_mapping": {
        "Palm": "Aegis Burst",
        "Peace": "Nova Split",
        "Pointer": "Volt Pierce",
        "Thumbs Up": "Inferno Rush",
    },
}
for key, value in _DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


def render_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at 15% 12%, rgba(99,102,241,.20), transparent 20%),
                radial-gradient(circle at 85% 10%, rgba(236,72,153,.16), transparent 18%),
                radial-gradient(circle at 82% 78%, rgba(56,189,248,.16), transparent 22%),
                linear-gradient(180deg, #090b16 0%, #0d1225 100%);
        }
        .block-container {max-width: 1240px; padding-top: 1.2rem; padding-bottom: 2rem;}
        .hero,.panel,.status-card,.detect-card,.spell-box {
            background: rgba(13,19,38,.80);
            border: 1px solid rgba(255,255,255,.10);
            box-shadow: 0 18px 45px rgba(0,0,0,.25);
            backdrop-filter: blur(10px);
        }
        .hero {border-radius: 28px; padding: 1.35rem 1.5rem; margin-bottom: 1rem;}
        .hero p {margin: .25rem 0 0 0; color: #dbe4ff; font-size: 1rem;}
        .hero-strip {display:flex; gap:.55rem; flex-wrap:wrap; margin-top:.85rem;}
        .chip,.source-pill {
            display:inline-block; border-radius:999px; padding:.4rem .74rem; font-size:.83rem;
            color:#eef2ff; border:1px solid rgba(255,255,255,.10);
        }
        .chip {background: linear-gradient(90deg, rgba(99,102,241,.22), rgba(236,72,153,.18));}
        .source-pill {margin:.45rem 0 .85rem 0; background: linear-gradient(90deg, rgba(14,165,233,.22), rgba(99,102,241,.22));}
        .panel {border-radius: 24px; padding: 1rem;}
        .status-card,.detect-card,.spell-box {border-radius: 18px; padding: .95rem; min-height: 98px;}
        .kicker {font-size:.78rem; text-transform:uppercase; letter-spacing:.08em; color:#a5b4fc; margin-bottom:.3rem;}
        .big {font-size:1.18rem; font-weight:700; color:#fff; line-height:1.15;}
        .copy {font-size:.95rem; color:#dbe4ff; line-height:1.45; margin-top:.38rem;}
        .empty-state {
            border:1px dashed rgba(255,255,255,.18); border-radius:20px; padding:1.1rem;
            background: rgba(255,255,255,.03); color:#dbe4ff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource(show_spinner=False)
def get_model_and_labels():
    return load_local_teachable_machine_model(str(config.MODEL_PATH), str(config.LABELS_PATH))


def normalize_label(label: str) -> str:
    return LABEL_MAP.get(label.strip(), label.strip())


def reset_magic_session() -> None:
    for key, value in _DEFAULTS.items():
        st.session_state[key] = value.copy() if isinstance(value, dict) else value.copy() if isinstance(value, list) else value


def generate_magic_bundle() -> None:
    if not st.session_state.prediction:
        st.warning("Capture or upload an image first.")
        return

    label = st.session_state.prediction["label"]
    combo_name = st.session_state.spell_name
    st.session_state.spell_prompt = build_hidden_prompt(label, combo_name, st.session_state.input_source)

    with st.spinner("Chaining your combo outputs into one final premium card..."):
        st.session_state.spell_text = generate_magic_response(
            label,
            combo_name,
            f"This combo came from a {st.session_state.input_source} hand-gesture image.",
        )
        img, err = generate_magic_visual(st.session_state.spell_prompt)
        if img:
            st.session_state.spell_scene_image = img
            st.session_state.spell_card_image = create_combo_card(combo_name, label, st.session_state.spell_text, img)
        else:
            st.session_state.spell_scene_image = None
            st.session_state.spell_card_image = None
            st.error(err or "Could not generate the combo scene image.")

        st.session_state.spell_log = (
            [{
                "gesture": label,
                "spell": combo_name,
                "text": st.session_state.spell_text,
                "source": st.session_state.input_source,
            }] + st.session_state.spell_log
        )[: config.MAX_CARD_LOG]


def show_hud() -> None:
    c1, c2, c3, c4 = st.columns(4)
    gesture = st.session_state.prediction["label"] if st.session_state.prediction else "Waiting"
    spell = st.session_state.spell_name or "No Combo Yet"
    log_count = len(st.session_state.spell_log)
    items = [
        (c1, "Supported Gestures", "Palm · Peace · Pointer · Thumbs Up"),
        (c2, "Detected Gesture", gesture),
        (c3, "Active Combo", spell),
        (c4, "Combo Log", log_count),
    ]
    for col, label, value in items:
        col.markdown(
            f"<div class='status-card'><div class='kicker'>{label}</div><div class='big'>{value}</div></div>",
            unsafe_allow_html=True,
        )


def show_output() -> None:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.subheader("🪄 Chained Output")

    if st.session_state.spell_name:
        st.markdown(
            f"<div class='spell-box'><div class='kicker'>Combo Name</div><div class='big'>{st.session_state.spell_name}</div></div>",
            unsafe_allow_html=True,
        )
    if st.session_state.spell_text:
        st.markdown(
            f"<div class='spell-box' style='margin-top:.75rem;'><div class='kicker'>AI Narration</div><div class='copy'>{st.session_state.spell_text.replace(chr(10), '<br>')}</div></div>",
            unsafe_allow_html=True,
        )
    if st.session_state.spell_scene_image is not None or st.session_state.spell_card_image is not None:
        a, b = st.columns(2)
        if st.session_state.spell_scene_image is not None:
            a.image(st.session_state.spell_scene_image, caption="AI-generated combo scene", use_container_width=True)
        if st.session_state.spell_card_image is not None:
            b.image(st.session_state.spell_card_image, caption="Final combo card", use_container_width=True)
    elif not st.session_state.spell_name:
        st.markdown(
            "<div class='empty-state'>Detect a gesture and click <b>Generate Combo Card</b> to see the chained narration, scene image, and final combo card.</div>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


def show_spell_log() -> None:
    left, right = st.columns([4, 1])
    left.subheader("📚 Combo Log")
    if right.button("Reset Studio", use_container_width=True):
        reset_magic_session()
        st.rerun()

    if st.session_state.spell_log:
        for i, item in enumerate(st.session_state.spell_log, 1):
            with st.expander(f"Combo {i}: {item['spell']} ({item['gesture']})"):
                st.write(f"Source: {item['source']}")
                st.write(item["text"])
    else:
        st.caption("Your combo history will appear here after you generate cards.")


def prediction_panel(current_image: Image.Image, source_name: str) -> None:
    st.session_state.captured_image = current_image
    st.session_state.input_source = source_name
    st.image(current_image, caption="Gesture image used for combo generation", use_container_width=True)
    st.markdown(f"<div class='source-pill'>Input source: {source_name.title()}</div>", unsafe_allow_html=True)
    try:
        model, labels = get_model_and_labels()
        pred = predict_gesture_from_image(model, labels, current_image, label_map=LABEL_MAP)
        pred["label"] = normalize_label(pred["label"])
        for item in pred["top_predictions"]:
            item["label"] = normalize_label(item["label"])
        st.session_state.prediction = pred
        combo_name = get_combo_name_for_gesture(pred["label"], st.session_state.gesture_mapping)
        st.session_state.spell_name = combo_name
        st.success(f"Detected gesture: **{pred['label']}**")
        st.progress(float(pred["confidence"]), text=f"Confidence: {pred['confidence']:.1%}")
        c1, c2 = st.columns(2)
        c1.markdown(
            f"<div class='detect-card'><div class='kicker'>Detected</div><div class='big'>{pred['label']}</div><div class='copy'>This is the highest-confidence class from your local gesture model.</div></div>",
            unsafe_allow_html=True,
        )
        c2.markdown(
            f"<div class='detect-card'><div class='kicker'>Mapped Combo</div><div class='big'>{combo_name}</div><div class='copy'>The combo name is pulled from a runtime-configurable gesture mapping.</div></div>",
            unsafe_allow_html=True,
        )
        with st.expander("See all prediction scores"):
            for item in pred["top_predictions"]:
                st.progress(float(item["confidence"]), text=f"{item['label']} — {item['confidence']:.1%}")
        key = f"{source_name}:{pred['label']}:{pred['confidence']:.4f}"
        if st.session_state.last_generated_key != key:
            if st.button("Generate Combo Card ✨", use_container_width=True):
                generate_magic_bundle()
                st.session_state.last_generated_key = key
    except Exception as exc:
        st.error(f"Could not load or run the local model: {exc}")


def main() -> None:
    render_styles()
    st.markdown(
        f"""
        <div class='hero'>
            <h1 style='margin:0 0 6px 0;'>{config.APP_ICON} {config.APP_TITLE}</h1>
            <p>{config.APP_SUBTITLE}</p>
            <div class='hero-strip'>
                <span class='chip'>Gesture Label</span>
                <span class='chip'>AI Narration</span>
                <span class='chip'>Scene Image</span>
                <span class='chip'>Final Combo Card</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    show_hud()
    left, right = st.columns([1, 1], gap="large")
    with left:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.subheader("📷 Input")
        tabs = st.tabs(["Webcam Capture", "Upload Image"])
        with tabs[0]:
            cam = st.camera_input("Capture gesture from webcam", help=config.CAMERA_HELP)
            if cam:
                prediction_panel(Image.open(cam).convert("RGB"), "webcam")
            else:
                st.info("Take a photo with your webcam to detect a gesture.")
        with tabs[1]:
            up = st.file_uploader("Upload a gesture image", type=["png", "jpg", "jpeg"])
            if up:
                prediction_panel(Image.open(up).convert("RGB"), "upload")
            else:
                st.info("Upload a hand gesture image to detect a combo gesture.")
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        show_output()
    st.divider()
    show_spell_log()


if __name__ == "__main__":
    main()  
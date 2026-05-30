import base64
import json
from io import BytesIO

import streamlit as st
from PIL import Image, ImageDraw
from groq import Groq
from config import (
    APP_TITLE,
    APP_SUBTITLE,
    GROQ_API_KEY,
    MODEL_NAME,
    SYSTEM_PROMPT,
    USER_PROMPT,
)

st.set_page_config(page_title=APP_TITLE, page_icon="🧾", layout="wide")

def image_to_base64(image: Image.Image) -> str:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def extract_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```json"):
        text = text.replace("```json", "", 1).rsplit("```", 1)[0].strip()
    elif text.startswith("```"):
        text = text.replace("```", "", 1).rsplit("```", 1)[0].strip()
    return json.loads(text)

def analyze_image(image: Image.Image) -> dict:
    client = Groq(api_key=GROQ_API_KEY)
    image_base64 = image_to_base64(image)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": USER_PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{image_base64}"},
                    },
                ],
            },
        ],
        temperature=0.2,
        max_tokens=700,
    )
    content = response.choices[0].message.content
    return extract_json(content)

def draw_overlay(image: Image.Image, report: dict) -> Image.Image:
    base = image.convert("RGBA")
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    width, height = base.size
    for item in report.get("objects", []):
        box = item.get("box", {})
        x1 = int(box.get("x1", 0) * width)
        y1 = int(box.get("y1", 0) * height)
        x2 = int(box.get("x2", 0) * width)
        y2 = int(box.get("y2", 0) * height)
        label = item.get("label", "Object")

        draw.rectangle([x1, y1, x2, y2], outline=(0, 255, 180, 255), width=4)
        draw.rectangle([x1, max(0, y1 - 28), min(width, x1 + 180), y1], fill=(0, 255, 180, 170))
        draw.text((x1 + 8, max(0, y1 - 22)), label, fill=(10, 20, 25, 255))

    return Image.alpha_composite(base, overlay)

def build_summary(report: dict) -> str:
    scene = report.get("scene_type", "Unknown")
    mood = report.get("mood", "Unknown")
    safety = report.get("safety_note", "No safety note available.")
    count = len(report.get("objects", []))
    return (
        f"This image appears to show a **{scene}** scene with a **{mood}** mood. "
        f"The AI identified **{count} key visual elements**. "
        f"Responsible AI note: {safety}"
    )

st.title(APP_TITLE)
st.caption(APP_SUBTITLE)

with st.container(border=True):
    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["png", "jpg", "jpeg", "webp"],
    )

if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
    st.warning("Add your Groq API key in the .env file before generating the report.")

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded image", use_container_width=True)

    if st.button("Generate visual report", type="primary", use_container_width=True):
        if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
            st.error("Groq API key is missing. Update the .env file and try again.")
        else:
            with st.spinner("Analyzing image and building report..."):
                try:
                    report = analyze_image(image)
                    annotated = draw_overlay(image, report)
                    summary = build_summary(report)

                    tab1, tab2, tab3, tab4 = st.tabs(
                        ["Annotated Image", "Summary", "Parsed JSON", "Object Table"]
                    )

                    with tab1:
                        st.image(annotated, caption="Visual report overlay", use_container_width=True)

                    with tab2:
                        st.subheader("AI Visual Summary")
                        st.markdown(summary)
                        st.markdown("### Scene Type")
                        st.write(report.get("scene_type", "Unknown"))
                        st.markdown("### Mood")
                        st.write(report.get("mood", "Unknown"))
                        st.markdown("### Responsible AI Note")
                        st.write(report.get("safety_note", "No note provided."))

                    with tab3:
                        st.subheader("Structured JSON Output")
                        st.json(report)

                    with tab4:
                        st.subheader("Detected Objects")
                        rows = []
                        for item in report.get("objects", []):
                            rows.append({
                                "Label": item.get("label", ""),
                                "Confidence": item.get("confidence", ""),
                                "Reason": item.get("reason", ""),
                            })
                        if rows:
                            st.dataframe(rows, use_container_width=True)
                        else:
                            st.info("No objects were returned.")

                except Exception as error:
                    st.error(f"Could not generate the report right now. {error}")

st.markdown("---")
st.markdown(
    "**What this project teaches:** Responsible AI design, drawing on images with PIL, "
    "RGBA transparency and image compositing, structured AI output, parsing JSON, "
    "and displaying multiple outputs."
)

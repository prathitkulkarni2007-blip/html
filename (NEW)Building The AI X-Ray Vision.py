import base64, io, json
from io import BytesIO
import streamlit as st 
from PIL import Image, ImageDraw, ImageFont
from greq import Groq
import config

st.set_page_config(page_title="The AI X-Ray Vision", page_icon="🧪", layout="centered")

client = Groq(api_key=config.GROQ_API_KEY)
st.session_state.setdefault("xray_outputs", [])

PROMPT = """Analyze this image and return ONLY valid JSON.
Identify all clearly visible important objects in the image.
For each object, return: name, short_label, fun_metadata, confidence, box
The "box" must use percentages 0 to 100 with x, y, w, h.
Rules:
- Include all clearly visible important objects
- Do not guess hidden or unclear objects
- if unsure, skip the object
- Keep labels short and kid-friendly
- Confidence must be one of: high, medium, low
- Never identify a real person by name
- Return JSON only
Format:
{"scence_title":"title","objects":[{"name"...","short_label":"...","fun_metadata":"...","confidence":"high","box":{"x":20,"y":10,"w":25,"h":60}}]}"""

PERSON_WORDS = {"person", "adult", "child", "woman", "man", "girl", "boy", "human","people"}
SAFE_LABELS = {"person", "smiling adult", "child", "seated person"}

st.title("🧪 The AI X-Ray Vision")
st.write("Upload a real photo and turn it into AI scanner images.")
st.markdown(
    "This app scans your image, finds important objects, "
    "and creates clean scanner-style images in smaller groups."
)

def analyze_image(file):
    encoded = base64.b64encode(file.getvalue()).decade()
    response = client.chat.completions.create(
        model=config.GROQ_ VISION_MODEL,
        messages=[{
            "role": "user",
            "content": [
                {"type":"text", "text": PROMPT},
                {"type": "image_url", "image_url": {"url": f"data:{file.type};base64,{encoded}"}}
            ],
        }],
        temperature=0.2,
        max_completion_tokens=1200,
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)

def px(box, w,h):
    values = 
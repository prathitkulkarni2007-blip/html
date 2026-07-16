Create the main project folder first. Then create the templates folder and the static/css plus static/js folders inside it.


Windows / macOS / Linux 


mkdir ai-car-concept-lab 
cd ai-car-concept-lab 
mkdir templates
mkdir static
mkdir static\css 
mkdir static\js
Inside the project folder, create these names:


app.py
config.py
requirements.txt
.env

README.md

templates/base.html

templates/index.html

templates/studio.html

templates/history.html

templates/car_svg.html

static/css/style.css

static/js/studio.js
flask==3.1.3
groq==1.0.0
requests==2.32.5
python-dotenv==1.2.1
GROQ_API_KEY=
HF_API_KEY=
HCAPTCHA_SITE_KEY=
HCAPTCHA_SECRET=
FLASK_SECRET_KEY=car-lab-dev-secret
import os
from dotenv import load_dotenv

load_dotenv()

APP_TITLE = "AI Car Concept Lab"
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "car-lab-dev-secret")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

HF_API_KEY = os.getenv("HF_API_KEY", "")
HF_IMAGE_URL = os.getenv(
    "HF_IMAGE_URL",
    "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell",
)

HCAPTCHA_SITE_KEY = os.getenv("HCAPTCHA_SITE_KEY", "10000000-ffff-ffff-ffff-000000000001")
HCAPTCHA_SECRET = os.getenv("HCAPTCHA_SECRET", "0x0000000000000000000000000000000000000000")
HCAPTCHA_VERIFY_URL = "https://api.hcaptcha.com/siteverify"

MAX_HISTORY = int(os.getenv("MAX_HISTORY", "20"))
import base64, json, uuid
from datetime import datetime

import requests
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from groq import Groq

import config

app = Flask(__name__)
app.secret_key = config.FLASK_SECRET_KEY

groq_client = Groq(api_key=config.GROQ_API_KEY) if config.GROQ_API_KEY else None

DESIGN_PROMPT = """You are an expert futuristic car designer.
Generate a detailed concept based on:
Style: {style}
Primary Color: {primary_color}
Accent Color: {accent_color}
Material: {material}
Occasion: {occasion}
Inspiration: {inspiration}

Respond with raw JSON only - no markdown, no explanation.
{{
  "name":"2-4 word creative car name",
  "tagline":"punchy tagline max 10 words",
  "description":"2-3 sentence concept description",
  "materials":["mat1","mat2","mat3"],
  "colorways":[
    {{"name":"variant 1","body":"#hex","roof":"#hex","accent":"#hex","glass":"#hex","wheel":"#hex"}},
    {{"name":"variant 2","body":"#hex","roof":"#hex","accent":"#hex","glass":"#hex","wheel":"#hex"}},
    {{"name":"variant 3","body":"#hex","roof":"#hex","accent":"#hex","glass":"#hex","wheel":"#hex"}}
  ],
  "features":["feat1","feat2","feat3","feat4"],
  "powertrain":"short powertrain line",
  "target_audience":"who this is for",
  "retail_price":"$XXX,XXX",
  "style_tags":["tag1","tag2","tag3"]
}}
Generate exactly 3 colorways. All hex codes must be valid #RRGGBB."""

def get_prefs(data):
    defaults = {
        "style": "futuristic",
        "primary_color": "#1a1a2e",
        "accent_color": "#e2b714",
        "material": "carbon fiber",
        "occasion": "city launch",
        "inspiration": "",
    }
    return {k: (data.get(k) or v) for k, v in defaults.items()}

def strip_json_fences(raw):
    raw = (raw or "").strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return raw.strip().rstrip("```").strip()

def fallback_concept(prefs):
    p = prefs["primary_color"]
    a = prefs["accent_color"]
    style = prefs["style"].title()
    theme = prefs["inspiration"] or "future motion"
    return {
        "name": f"{style} Vector X",
        "tagline": "Charge the road ahead.",
        "description": f"A {prefs['style']} concept car shaped for {prefs['occasion']}, mixing {prefs['material']} detailing with a bold {theme} influence.",
        "materials": [prefs["material"].title(), "Recycled interior trim", "Performance composite shell"],
        "colorways": [
            {"name": "Launch Spec", "body": p, "roof": "#101317", "accent": a, "glass": "#7aa7c7", "wheel": "#d9d9d9"},
            {"name": "Night Pulse", "body": "#101317", "roof": p, "accent": a, "glass": "#87b7d9", "wheel": "#f0f0f0"},
            {"name": "Solar Drift", "body": a, "roof": "#ffffff", "accent": p, "glass": "#9bc8ea", "wheel": "#222222"},
        ],
        "features": ["Active aero front blade", "Adaptive ambient cabin", "Panoramic canopy roof", "AI driving assistance"],
        "powertrain": "Dual-motor electric drivetrain",
        "target_audience": "Drivers who want bold futuristic design",
        "retail_price": "$148,000",
        "style_tags": [prefs["style"], prefs["occasion"], "concept"],
    }

def generate_concept(prefs):
    if not groq_client:
        return fallback_concept(prefs)
    chat = groq_client.chat.completions.create(
        model=config.GROQ_MODEL,
        messages=[
            {"role": "system", "content": "Car design expert. Pure JSON only."},
            {"role": "user", "content": DESIGN_PROMPT.format(**prefs)},
        ],
        temperature=0.85,
        max_tokens=1200,
    )
    return json.loads(strip_json_fences(chat.choices[0].message.content))

def verify_hcaptcha(token):
    if not token:
        return False
    try:
        r = requests.post(
            config.HCAPTCHA_VERIFY_URL,
            data={"secret": config.HCAPTCHA_SECRET, "response": token},
            timeout=5,
        )
        return r.json().get("success", False)
    except Exception:
        return False

def hex_to_color_name(h):
    h = (h or "").lstrip("#").lower()
    try:
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    except Exception:
        return "colorful"
    mx, mn = max(r, g, b), min(r, g, b)
    br, sat = mx / 255, ((mx - mn) / mx if mx else 0)
    if br < 0.15:
        return "black"
    if br > 0.88 and sat < 0.15:
        return "white"
    if sat < 0.18:
        return "dark gray" if br < 0.4 else "gray" if br < 0.65 else "light gray"
    if mx == r:
        return ("orange" if g > 120 else "dark orange") if g > b + 60 else ("magenta" if b > g + 40 else "red")
    if mx == g:
        return "yellow-green" if r > b + 60 else ("cyan-green" if b > r + 40 else "green")
    return "purple" if r > g + 60 else ("cyan" if g > r + 40 else "blue")

def build_image_prompt(prefs):
    p = hex_to_color_name(prefs["primary_color"])
    a = hex_to_color_name(prefs["accent_color"])
    prompt = (
        f"Professional product photography of a futuristic concept car, {prefs['style']} styling, "
        f"{p} body, {a} accents, {prefs['material']} details, side three-quarter view, white studio background, "
        f"sharp focus, premium automotive render, car only"
    )
    if prefs.get("inspiration"):
        prompt += f", {prefs['inspiration']} theme"
    return prompt

def generate_car_image(prompt):
    if not config.HF_API_KEY:
        return None
    try:
        r = requests.post(
            config.HF_IMAGE_URL,
            headers={
                "Authorization": f"Bearer {config.HF_API_KEY}",
                "Content-Type": "application/json",
            },
            json={"inputs": prompt},
            timeout=60,
        )
        if r.status_code == 200 and r.headers.get("content-type", "").startswith("image"):
            mime = r.headers["content-type"].split(";")[0].strip()
            return f"data:{mime};base64,{base64.b64encode(r.content).decode()}"
    except Exception:
        pass
    return None

def save_to_history(concept, prefs, image_url=None):
    session.setdefault("history", [])
    entry = {
        "id": str(uuid.uuid4())[:8],
        "timestamp": datetime.now().strftime("%b %d, %Y | %I:%M %p"),
        "concept": concept,
        "prefs": prefs,
        "image_url": image_url,
    }
    session["history"] = ([entry] + session["history"])[: config.MAX_HISTORY]
    return entry["id"]

@app.route("/")
def index():
    return render_template("index.html", hcaptcha_site_key=config.HCAPTCHA_SITE_KEY)

@app.route("/studio")
def studio():
    return render_template("studio.html", hcaptcha_site_key=config.HCAPTCHA_SITE_KEY)

@app.route("/history")
def history():
    return render_template("history.html", designs=session.get("history", []))

@app.route("/clear-history", methods=["POST"])
def clear_history():
    session.pop("history", None)
    return redirect(url_for("history"))

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or request.form
    token = data.get("h-captcha-response", "")
    if not token:
        return jsonify({"error": "Please complete the CAPTCHA."}), 400
    if not verify_hcaptcha(token):
        return jsonify({"error": "CAPTCHA verification failed."}), 400

    prefs = get_prefs(data)
    try:
        concept = generate_concept(prefs)
        concept["image_prompt"] = build_image_prompt(prefs)
        history_id = save_to_history(concept, prefs)
        return jsonify({"success": True, "concept": concept, "prefs": prefs, "history_id": history_id})
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Malformed AI response: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Concept generation failed: {e}"}), 500

@app.route("/generate-image", methods=["POST"])
def generate_image():
    data = request.get_json(silent=True) or {}
    prompt = data.get("image_prompt", "")
    history_id = data.get("history_id", "")
    if not prompt:
        return jsonify({"error": "No image prompt."}), 400
    if not config.HF_API_KEY:
        return jsonify({"error": "HF_API_KEY not configured."}), 503
    image_url = generate_car_image(prompt)
    if not image_url:
        return jsonify({"error": "Image generation failed. Try again."}), 500

    if history_id and "history" in session:
        for entry in session["history"]:
            if entry["id"] == history_id:
                entry["image_url"] = image_url
                break
        session.modified = True

    return jsonify({"success": True, "image_url": image_url})

if __name__ == "__main__":
    app.run(debug=True, port=5000)

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{{ title or "AI Car Concept Lab" }}</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
  <script>window.HCAPTCHA_SITE_KEY = "{{ hcaptcha_site_key or '' }}";</script>
  <script src="https://js.hcaptcha.com/1/api.js?render=explicit&onload=hcaptchaReady" async defer></script>
</head>
<body>
  <header class="topbar">
    <a class="brand" href="{{ url_for('index') }}">AI Car Concept Lab</a>
    <nav>
      <a href="{{ url_for('index') }}">Home</a>
      <a href="{{ url_for('studio') }}">Studio</a>
      <a href="{{ url_for('history') }}">History</a>
    </nav>
  </header>
  <main class="page">{% block content %}{% endblock %}</main>
</body>
</html>

{% extends "base.html" %}
{% block content %}
<section class="hero">
  <div>
    <h1>Design futuristic cars with AI</h1>
    <p>Build a concept, explore three live colorways, render a hero image, and save every design to your session garage.</p>
    <div class="hero-actions">
      <a class="btn primary" href="{{ url_for('studio') }}">Start Designing</a>
      <a class="btn" href="{{ url_for('history') }}">View Garage</a>
    </div>
  </div>
  <div class="hero-car card-visual">
    {% include "car_svg.html" %}
  </div>
</section>
{% endblock %}

{% extends "base.html" %}
{% block content %}
<section class="studio-grid">
  <form id="designForm" class="panel">
    <h2>Design Brief</h2>
    <label>Style
      <select id="style">
        <option>futuristic</option><option>luxury</option><option>off-road</option>
        <option>track-focused</option><option>minimalist</option><option>retro-future</option>
      </select>
    </label>
    <label>Material
      <select id="material">
        <option>carbon fiber</option><option>aluminium</option><option>forged composite</option>
        <option>brushed metal</option><option>recycled polymer</option>
      </select>
    </label>
    <label>Occasion
      <select id="occasion">
        <option>city launch</option><option>track day</option><option>concept showcase</option>
        <option>luxury commute</option><option>desert run</option>
      </select>
    </label>
    <div class="colors">
      <label>Primary color <input type="color" id="primary_color" value="#1a1a2e"></label>
      <label>Accent color <input type="color" id="accent_color" value="#e2b714"></label>
    </div>
    <label>Inspiration
      <textarea id="inspiration" rows="3" placeholder="Tokyo neon nights, desert solar racer, stealth jet..."></textarea>
    </label>
    <button id="generateBtn" class="btn primary" type="submit">Verify & Generate Car Concept</button>
    <p id="formError" class="error"></p>
  </form>

  <section class="panel">
    <h2>Output</h2>
    <div id="emptyState" class="empty">No concept yet. Fill the brief and generate one.</div>

    <div id="resultWrap" class="hidden">
      <div class="result-head">
        <div>
          <h3 id="resultName"></h3>
          <p id="resultTagline" class="muted"></p>
        </div>
        <div class="price-box" id="resultPrice"></div>
      </div>

      <div class="colorway-tabs" id="colorwayTabs"></div>

      <div class="viewer-grid">
        <div>
          <div id="sneakerStage" class="card-visual">{% include "car_svg.html" %}</div>
          <div id="colorwayInfo" class="cw-info"></div>
        </div>
        <div>
          <div id="imageBox" class="image-box hidden">
            <p id="loaderText" class="muted">Rendering image...</p>
            <div class="loader-line"></div>
            <img id="resultImage" class="hidden" alt="AI generated car render">
            <button id="regenerateImageBtn" class="btn small hidden" type="button">Regenerate Image ↺</button>
          </div>
          <p id="resultDesc"></p>
          <h4>Materials</h4><ul id="materialsList"></ul>
          <h4>Features</h4><ul id="featuresList"></ul>
          <h4>Powertrain</h4><p id="resultPowertrain"></p>
          <h4>Audience</h4><p id="resultAudience"></p>
        </div>
      </div>
    </div>
  </section>
</section>

<div id="captchaModal" class="modal hidden">
  <div class="modal-card">
    <h3>Verify you're human</h3>
    <div id="hcaptchaWidget"></div>
    <button id="captchaCancel" class="btn" type="button">Cancel</button>
  </div>
</div>

<script src="{{ url_for('static', filename='js/studio.js') }}"></script>
{% endblock %}
{% extends "base.html" %}
{% block content %}
<section class="history-head">
  <div>
    <h1>Your Garage</h1>
    <p class="muted">Session-based history for this browser visit.</p>
  </div>
  {% if designs %}
  <form method="POST" action="{{ url_for('clear_history') }}" class="clear-form">
    <button type="submit" class="btn" onclick="return confirm('Clear all car history?')">Clear All ✕</button>
  </form>
  {% endif %}
</section>

{% if not designs %}
  <div class="empty history-empty">No car concepts yet. Generate one from the Studio.</div>
{% else %}
  <div class="history-grid">
    {% for entry in designs %}
      <article class="history-card">
        <div class="card-meta">
          <span>#{{ entry.id }}</span>
          <span>{{ entry.timestamp }}</span>
        </div>
        <div class="card-visual" style="
          --body-color: {{ entry.concept.colorways[0].body if entry.concept.colorways else '#1a1a2e' }};
          --roof-color: {{ entry.concept.colorways[0].roof if entry.concept.colorways else '#101317' }};
          --accent-color: {{ entry.concept.colorways[0].accent if entry.concept.colorways else '#e2b714' }};
          --glass-color: {{ entry.concept.colorways[0].glass if entry.concept.colorways else '#7aa7c7' }};
          --wheel-color: {{ entry.concept.colorways[0].wheel if entry.concept.colorways else '#d9d9d9' }};
        ">
          {% if entry.image_url %}
            <img src="{{ entry.image_url }}" alt="{{ entry.concept.name }}">
            <span class="card-ai-badge">AI</span>
          {% else %}
            {% include "car_svg.html" %}
          {% endif %}
        </div>
        <h3>{{ entry.concept.name }}</h3>
        <p class="muted">{{ entry.concept.tagline }}</p>
        <p>{{ entry.concept.description }}</p>
        <div class="tags">
          {% for tag in entry.concept.style_tags %}
            <span class="tag">{{ tag }}</span>
          {% endfor %}
        </div>
      </article>
    {% endfor %}
  </div>
{% endif %}
{% endblock %}
<svg class="car-svg" viewBox="0 0 520 220" xmlns="http://www.w3.org/2000/svg" aria-label="Car preview">
  <rect x="0" y="0" width="520" height="220" rx="18" fill="#0d1118"/>
  <g>
    <path d="M95 138 C110 100, 150 82, 218 78 L310 74 C350 74, 392 92, 430 122 L454 138 L452 162 L72 162 L72 146 C72 141, 78 138, 95 138Z"
      fill="var(--body-color, #1a1a2e)"/>
    <path d="M200 86 L318 83 C350 84, 382 98, 408 122 L338 122 C322 104, 294 94, 256 94 C236 94, 220 92, 200 86Z"
      fill="var(--roof-color, #101317)"/>
    <path d="M220 92 L250 120 L346 120 C329 103, 304 95, 270 95 C250 95, 235 94, 220 92Z"
      fill="var(--glass-color, #7aa7c7)" opacity="0.9"/>
    <path d="M110 136 H166 L144 154 H98 Z" fill="var(--accent-color, #e2b714)"/>
    <path d="M390 132 H430 L416 152 H380 Z" fill="var(--accent-color, #e2b714)"/>
    <circle cx="165" cy="163" r="28" fill="#101317"/>
    <circle cx="165" cy="163" r="16" fill="var(--wheel-color, #d9d9d9)"/>
    <circle cx="375" cy="163" r="28" fill="#101317"/>
    <circle cx="375" cy="163" r="16" fill="var(--wheel-color, #d9d9d9)"/>
  </g>
</svg>
:root { color-scheme: dark; }
*{box-sizing:border-box} body{margin:0;font-family:Inter,Arial,sans-serif;background:#0a0e14;color:#edf1f7}
a{text-decoration:none;color:inherit} .page{max-width:1180px;margin:0 auto;padding:28px}
.topbar{display:flex;justify-content:space-between;align-items:center;padding:18px 28px;border-bottom:1px solid #1c2430;background:#0f1520;position:sticky;top:0;z-index:5}
.topbar nav{display:flex;gap:16px}.brand{font-weight:700}.topbar a{color:#d4d9e4}
.hero{display:grid;grid-template-columns:1.2fr 1fr;gap:24px;align-items:center}.hero h1{font-size:48px;line-height:1.05;margin:0 0 12px}
.hero-actions,.history-head{display:flex;gap:12px;align-items:center;justify-content:space-between}
.panel{background:#101722;border:1px solid #202b39;border-radius:20px;padding:20px}
.studio-grid{display:grid;grid-template-columns:380px 1fr;gap:20px}.viewer-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}
label{display:block;margin-bottom:14px;font-size:14px;color:#c4ccdb} select,textarea,input[type=color]{width:100%;margin-top:8px;background:#0c1118;color:#edf1f7;border:1px solid #273140;border-radius:12px;padding:12px}
.colors{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.btn{display:inline-flex;align-items:center;justify-content:center;padding:12px 16px;border-radius:12px;border:1px solid #334257;background:#131c29;color:#edf1f7;cursor:pointer}
.btn.primary{background:#e2b714;color:#14181d;border-color:#e2b714;font-weight:700}.btn.small{padding:9px 12px;font-size:13px}
.error{color:#ff8d8d;min-height:20px}.muted{color:#aab4c5}.hidden{display:none!important}.empty{padding:40px;border:1px dashed #334257;border-radius:16px;color:#9ea9ba;text-align:center}
.result-head{display:flex;justify-content:space-between;gap:16px;align-items:flex-start}.price-box{padding:10px 14px;border-radius:12px;background:#0b1118;border:1px solid #273140}
.card-visual{background:linear-gradient(180deg,#131b29,#0b1118);border:1px solid #273140;border-radius:18px;padding:10px;min-height:250px;display:flex;align-items:center;justify-content:center;position:relative}
.car-svg{width:100%;height:auto;max-width:480px}
.colorway-tabs{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0}.cw-tab{padding:10px 12px;border-radius:999px;border:1px solid #2c384a;background:#0c1118;color:#edf1f7;cursor:pointer}
.cw-tab.active{border-color:#e2b714;box-shadow:0 0 0 1px #e2b714 inset}.cw-swatch{display:inline-block;width:12px;height:12px;border-radius:999px;margin-right:6px;vertical-align:middle}
.cw-info{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}.cw-color-item{padding:10px;border-radius:12px;background:#0b1118;border:1px solid #273140;font-size:14px}
.cw-dot{display:inline-block;width:12px;height:12px;border-radius:50%;margin-right:8px;vertical-align:middle}
.image-box{padding:14px;border-radius:16px;background:#0b1118;border:1px solid #273140}.image-box img{width:100%;border-radius:14px;margin-top:10px}
.loader-line{height:6px;background:linear-gradient(90deg,#e2b714,#ffd95d);border-radius:999px;animation:load 1.1s infinite alternate}.tags{display:flex;gap:8px;flex-wrap:wrap}.tag{padding:6px 10px;border-radius:999px;background:#0b1118;border:1px solid #273140;color:#cfd7e4;font-size:12px}
.history-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:18px;margin-top:20px}.history-card{background:#101722;border:1px solid #202b39;border-radius:20px;padding:16px}
.history-card img{width:100%;border-radius:14px}.card-meta{display:flex;justify-content:space-between;color:#9ea9ba;font-size:12px;margin-bottom:10px}.card-ai-badge{position:absolute;top:18px;right:18px;background:#e2b714;color:#111;padding:6px 8px;border-radius:999px;font-size:12px;font-weight:700}
.modal{position:fixed;inset:0;background:rgba(4,8,14,.68);display:grid;place-items:center;padding:20px}.modal-card{width:min(420px,100%);background:#101722;border:1px solid #202b39;border-radius:18px;padding:20px}
@keyframes load{from{transform:scaleX(.35);opacity:.4}to{transform:scaleX(1);opacity:1}}
@media (max-width: 900px){.studio-grid,.viewer-grid,.hero{grid-template-columns:1fr}.topbar{padding:16px}.page{padding:20px}}
# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py

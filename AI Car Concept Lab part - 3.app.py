flask==3.1.3
groq==1.0.0
python-dotenv==1.2.1
FLASK_SECRET_KEY=replace_with_any_long_random_string
GROQ_API_KEY=your_groq_key_here
GROQ_MODEL=llama-3.3-70b-versatile
HCAPTCHA_SITE_KEY=your_hcaptcha_site_key_here
HCAPTCHA_SECRET=your_hcaptcha_secret_here

from __future__ import annotations

import hashlib
import json
import os
import random
import re
from datetime import datetime
from typing import Any
from urllib.parse import quote_plus

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, session
from groq import Groq

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "ai-car-concept-lab-dev-key")
app.config["SESSION_PERMANENT"] = False

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
HCAPTCHA_SITE_KEY = os.environ.get("HCAPTCHA_SITE_KEY", "10000000-ffff-ffff-ffff-000000000001")
HCAPTCHA_SECRET = os.environ.get("HCAPTCHA_SECRET", "0x0000000000000000000000000000000000000000")
HCAPTCHA_VERIFY_URL = "https://api.hcaptcha.com/siteverify"
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
MAX_HISTORY = 12

STYLE_TAGS = {
    "Hypercar": ["aggressive aero", "track-born drama", "hero stance"],
    "Luxury": ["quiet prestige", "clean surfacing", "executive cabin"],
    "Off-Road": ["all-terrain muscle", "raised stance", "rugged utility"],
    "EV": ["clean tech", "silent thrust", "future cockpit"],
    "Retro-Future": ["heritage remix", "neo-classic curves", "concept nostalgia"],
    "Street": ["night-run energy", "urban custom", "after-dark attitude"],
}

MATERIAL_NOTES = {
    "Carbon Fiber": ["carbon composite shell", "forged aero fins", "lightweight chassis"],
    "Aluminum": ["aluminum body frame", "precision-machined trim", "satin shell panels"],
    "Titanium": ["titanium highlights", "heat-blued metal details", "ultra-premium structural spine"],
    "Recycled Composite": ["recycled composite shell", "eco-performance weave", "sustainable cabin accents"],
    "Glass & Metal": ["glass canopy roof", "brushed alloy bodywork", "framed light signature"],
    "Mixed Performance": ["hybrid material shell", "performance mesh venting", "contrasting aero textures"],
}

PRICE_BANDS = {
    "Daily Drive": "$58,000",
    "Track Day": "$210,000",
    "Adventure": "$96,000",
    "Collector Reveal": "$320,000",
    "City Tech": "$74,000",
    "Luxury Tourer": "$168,000",
}

DESIGN_PROMPT = """You are a visionary automotive concept designer.
Generate a complete futuristic car concept based on:
Style: {style}
Primary Color: {primary_color}
Accent Color: {accent_color}
Material: {material}
Occasion: {occasion}
Inspiration: {inspiration}

Respond with raw JSON only — no markdown, no explanation.
{{
  "name": "2-4 word creative car name",
  "tagline": "punchy tagline max 10 words",
  "description": "2-3 sentence cinematic concept description",
  "materials": ["mat1", "mat2", "mat3"],
  "colorways": [
    {{"name": "launch spec", "body": "#hex", "accent": "#hex", "wheels": "#hex", "cabin": "#hex"}}
  ],
  "features": ["feat1", "feat2", "feat3", "feat4"],
  "powertrain": "power system description",
  "cockpit_theme": "cockpit mood and interface idea",
  "target_driver": "who this concept is for",
  "retail_price": "$XXX,XXX",
  "style_tags": ["tag1", "tag2", "tag3"]
}}
Generate exactly 3 colorways. All hex codes must be valid #RRGGBB."""


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/studio")
def studio() -> str:
    return render_template("studio.html", hcaptcha_site_key=HCAPTCHA_SITE_KEY)


@app.route("/history")
def history() -> str:
    return render_template("history.html", designs=get_history())


@app.route("/generate", methods=["POST"])
def generate() -> Any:
    data = request.get_json(silent=True) or request.form
    token = str(data.get("h-captcha-response", "")).strip()
    if not token:
        return jsonify({"error": "Please complete the CAPTCHA."}), 400
    if not verify_hcaptcha(token):
        return jsonify({"error": "CAPTCHA verification failed."}), 400

    prefs = get_prefs(data)
    if any(not v for v in prefs.values()):
        return jsonify({"error": "Please complete every field in the design brief."}), 400

    try:
        concept = generate_concept(prefs)
    except json.JSONDecodeError as exc:
        return jsonify({"error": f"Malformed AI response: {exc}"}), 500
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": f"Concept generation failed: {exc}"}), 500


    concept["image_url"] = build_image_url(concept, prefs)
    concept["brief"] = prefs
    concept["timestamp"] = datetime.now().strftime("%d %b %Y, %I:%M %p")
    concept["fingerprint"] = fingerprint(prefs, concept["name"])
    add_to_history(concept)
    return jsonify({"success": True, "concept": concept, "prefs": prefs})


@app.route("/clear-history", methods=["POST"])
def clear_history() -> Any:
    session["designs"] = []
    session.modified = True
    return jsonify({"success": True})


def verify_hcaptcha(token: str) -> bool:
    try:
        response = requests.post(
            HCAPTCHA_VERIFY_URL,
            data={"secret": HCAPTCHA_SECRET, "response": token},
            timeout=5,
        )
        return response.json().get("success", False)
    except Exception:
        return False


def get_prefs(data: Any) -> dict[str, str]:
    fields = [
        ("style", "Hypercar"),
        ("primary_color", "#1d4ed8"),
        ("accent_color", "#f97316"),
        ("material", "Carbon Fiber"),
        ("occasion", "City Tech"),
        ("inspiration", "Tokyo neon rain"),
    ]
    getter = getattr(data, "get", None)
    return {k: str(getter(k, d) if getter else d).strip() for k, d in fields}


def get_history() -> list[dict[str, Any]]:
    return session.get("designs", [])


def add_to_history(concept: dict[str, Any]) -> None:
    current = session.get("designs", [])
    deduped = [d for d in current if d.get("fingerprint") != concept["fingerprint"]]
    session["designs"] = [concept] + deduped[: MAX_HISTORY - 1]
    session.modified = True


def fingerprint(prefs: dict[str, str], name: str) -> str:
    raw = "|".join([*prefs.values(), name])
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:14]


def generate_concept(prefs: dict[str, str]) -> dict[str, Any]:
    if groq_client:
        concept = generate_via_groq(prefs)
        if concept:
            return concept
    return generate_local_concept(prefs)


def generate_via_groq(prefs: dict[str, str]) -> dict[str, Any] | None:
    raw = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": "Automotive concept design expert. Pure JSON only."},
            {"role": "user", "content": DESIGN_PROMPT.format(**prefs)},
        ],
        temperature=0.85,
        max_tokens=1200,
    ).choices[0].message.content.strip()

    cleaned = clean_ai_json_text(raw)
    concept = json.loads(cleaned)
    if not is_valid_concept(concept):
        return None
    return sanitize_concept(concept, prefs)


def clean_ai_json_text(raw: str) -> str:
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip().rstrip("```").strip()
    match = re.search(r"\{[\s\S]*\}", raw)
    return match.group(0) if match else raw


def is_valid_concept(concept: dict[str, Any]) -> bool:
    required = {
        "name", "tagline", "description", "materials", "features", "powertrain",
        "cockpit_theme", "target_driver", "retail_price", "style_tags", "colorways",
    }
    return required.issubset(concept.keys()) and isinstance(concept.get("colorways"), list)


def sanitize_concept(concept: dict[str, Any], brief: dict[str, str]) -> dict[str, Any]:
    return {
        "name": str(concept.get("name", "Concept X")).strip(),
        "tagline": str(concept.get("tagline", "Future in motion.")).strip(),
        "description": str(concept.get("description", "")).strip(),
        "materials": [str(x).strip() for x in concept.get("materials", [])][:5] or MATERIAL_NOTES.get(brief["material"], [])[:3],
        "features": [str(x).strip() for x in concept.get("features", [])][:6] or [
            "Adaptive aero body surfaces", "Panoramic digital cockpit", "Active rear light blade", "Predictive drive intelligence"
        ],
        "powertrain": str(concept.get("powertrain", "Quad-motor electric performance")).strip(),
        "cockpit_theme": str(concept.get("cockpit_theme", "Minimal driver-first cockpit")).strip(),
        "target_driver": str(concept.get("target_driver", "Design-forward performance drivers")).strip(),
        "retail_price": str(concept.get("retail_price", PRICE_BANDS.get(brief["occasion"], "$120,000"))).strip(),
        "style_tags": [str(x).strip() for x in concept.get("style_tags", [])][:3] or STYLE_TAGS.get(brief["style"], [])[:3],
        "colorways": normalize_colorways(concept.get("colorways", []), brief),
    }


def normalize_colorways(colorways: list[dict[str, Any]], brief: dict[str, str]) -> list[dict[str, str]]:
    fallback = [

        {"name": "Launch Spec", "body": brief["primary_color"], "accent": brief["accent_color"], "wheels": "#1b1e28", "cabin": "#d9dce5"},
        {"name": "Midnight Pulse", "body": shift_hex(brief["primary_color"], -18), "accent": brief["accent_color"], "wheels": "#0f1218", "cabin": "#c7d2e2"},
        {"name": "Solar Echo", "body": shift_hex(brief["primary_color"], 18), "accent": shift_hex(brief["accent_color"], 20), "wheels": "#2b2f3e", "cabin": "#f4f1eb"},
    ]
    cleaned: list[dict[str, str]] = []
    for idx, item in enumerate(colorways[:3]):
        cleaned.append({
            "name": str(item.get("name", fallback[idx]["name"])).strip(),
            "body": normalize_hex(str(item.get("body", fallback[idx]["body"])).strip(), fallback[idx]["body"]),
            "accent": normalize_hex(str(item.get("accent", fallback[idx]["accent"])).strip(), fallback[idx]["accent"]),
            "wheels": normalize_hex(str(item.get("wheels", fallback[idx]["wheels"])).strip(), fallback[idx]["wheels"]),
            "cabin": normalize_hex(str(item.get("cabin", fallback[idx]["cabin"])).strip(), fallback[idx]["cabin"]),
        })
    while len(cleaned) < 3:
        cleaned.append(fallback[len(cleaned)])
    return cleaned


def normalize_hex(value: str, fallback: str) -> str:
    value = value if value.startswith("#") else f"#{value}"
    return value if re.fullmatch(r"#[0-9a-fA-F]{6}", value) else fallback


def shift_hex(hex_color: str, amount: int) -> str:
    hex_color = normalize_hex(hex_color, "#667eea")
    parts = [int(hex_color[i : i + 2], 16) for i in (1, 3, 5)]
    shifted = [max(0, min(255, p + amount)) for p in parts]
    return "#" + "".join(f"{p:02x}" for p in shifted)


def generate_local_concept(brief: dict[str, str]) -> dict[str, Any]:
    seed = int(hashlib.sha1(json.dumps(brief, sort_keys=True).encode("utf-8")).hexdigest(), 16)
    rng = random.Random(seed + random.randint(1, 9999))
    first = ["Nova", "Aero", "Volt", "Phantom", "Zenith", "Pulse", "Halo", "Rift"]
    second = ["GT", "Flux", "One", "Racer", "Drive", "Arc", "XR", "Vision"]
    name = f"{rng.choice(first)} {rng.choice(second)}"
    return {
        "name": name,
        "tagline": rng.choice([
            "Built for tomorrow's roads.",
            "Where concept meets velocity.",
            "Electric drama. Precision control.",
            "Designed to steal the skyline.",
        ]),
        "description": (
            f"{name} is a {brief['style'].lower()} concept shaped for {brief['occasion'].lower()} moments. "
            f"It pairs {brief['material'].lower()} surfaces with {brief['primary_color']} as the hero tone and "
            f"{brief['accent_color']} as the visual pulse. The whole build channels {brief['inspiration']} into a cinematic road presence."
        ),
        "materials": MATERIAL_NOTES.get(brief["material"], MATERIAL_NOTES["Mixed Performance"])[:3],
        "features": [
            f"{brief['style']} silhouette with active aero channels",
            f"{brief['occasion']} tuned suspension package",
            "Full-width reactive light blade",
            "Augmented HUD with route intelligence",
            f"Cabin accents inspired by {brief['inspiration']}",
        ],
        "powertrain": rng.choice([
            "Tri-motor electric vector drive",
            "Hydrogen-electric hybrid thrust system",
            "Dual-motor grand touring EV platform",
        ]),
        "cockpit_theme": rng.choice([
            "Wraparound holo-dash with floating controls",
            "Pilot-inspired cabin with layered ambient light",
            "Minimal glass cockpit with tactile drive spine",
        ]),
        "target_driver": rng.choice([
            "Trend-forward urban performance drivers",
            "Collectors chasing a cinematic concept feel",
            "Drivers who want tech presence with everyday usability",
        ]),
        "retail_price": PRICE_BANDS.get(brief["occasion"], "$120,000"),
        "style_tags": STYLE_TAGS.get(brief["style"], ["future-ready", "bold stance", "concept energy"]),
        "colorways": normalize_colorways([], brief),
    }


def build_image_url(concept: dict[str, Any], brief: dict[str, str]) -> str:
    prompt = (
        f"futuristic concept car studio render, {concept['name']}, {brief['style']} design, "
        f"{brief['material']} body details, primary {brief['primary_color']}, accent {brief['accent_color']}, "
        f"inspired by {brief['inspiration']}, front three quarter angle, premium automotive product photography, "
        f"clean background, ultra detailed"
    )
    return f"https://image.pollinations.ai/prompt/{quote_plus(prompt)}?width=1024&height=640&seed=7&model=flux"


if __name__ == "__main__":
    app.run(debug=True, port=5000)

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}AI Car Concept Lab{% endblock %}</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
  <script>
    window.HCAPTCHA_SITE_KEY = {{ hcaptcha_site_key|default('', true)|tojson }};
  </script>
  <script src="https://js.hcaptcha.com/1/api.js?render=explicit&onload=hcaptchaReady" async defer></script>
</head>
<body>
  <div class="noise"></div>
  <header class="site-header">
    <a href="{{ url_for('index') }}" class="brand">AI Car Concept Lab</a>
    <nav class="nav-links">
      <a class="{% if request.endpoint == 'index' %}active{% endif %}" href="{{ url_for('index') }}">Home</a>
      <a class="{% if request.endpoint == 'studio' %}active{% endif %}" href="{{ url_for('studio') }}">Studio</a>
      <a class="{% if request.endpoint == 'history' %}active{% endif %}" href="{{ url_for('history') }}">History</a>
    </nav>
    <a href="{{ url_for('studio') }}" class="btn btn-primary small">Design Now</a>
  </header>

  <main>
    {% block content %}{% endblock %}
  </main>

  <footer class="site-footer">
    <p>Built with Flask, structured prompts, session history, secure CAPTCHA gating, and a futuristic product workflow.</p>
  </footer>
  {% block scripts %}{% endblock %}
</body>
</html>


{% extends 'base.html' %}
{% block title %}Home · AI Car Concept Lab{% endblock %}
{% block content %}
<section class="hero shell">
  <div class="hero-copy">
    <span class="eyebrow">Product Studio · AI Workflow</span>
    <h1>Turn a sharp brief into a futuristic car concept.</h1>
    <p>Create complete vehicle ideas with a name, tagline, materials, colorways, audience, pricing, and a cinematic concept render.</p>
    <div class="cta-row">
      <a href="{{ url_for('studio') }}" class="btn btn-primary">Start Designing</a>
      <a href="{{ url_for('history') }}" class="btn btn-secondary">View History</a>
    </div>
    <div class="stats-row">
      <div class="stat-card"><strong>3 Pages</strong><span>Home, Studio, History</span></div>
      <div class="stat-card"><strong>1 Brief</strong><span>Style, material, colour, inspiration</span></div>
      <div class="stat-card"><strong>Instant Concepts</strong><span>Text output + concept visuals</span></div>
    </div>
  </div>
  <div class="hero-visual">
    <div class="car-card glow-card">
      <div class="car-lines"></div>
      <div class="floating-chip chip-a">EV Aura</div>
      <div class="floating-chip chip-b">Neo Luxury</div>
      <svg viewBox="0 0 760 360" class="hero-car" aria-hidden="true">
        <defs>
          <linearGradient id="bodyGrad" x1="0" x2="1">
            <stop offset="0%" stop-color="#7c5cff"/>
            <stop offset="100%" stop-color="#31e1ff"/>
          </linearGradient>
        </defs>
        <ellipse cx="380" cy="295" rx="250" ry="24" fill="rgba(31,225,255,.18)"/>
        <path d="M140 230 Q190 155 310 145 L470 130 Q555 132 615 190 L662 232 L635 255 L580 255 Q565 211 520 208 Q478 209 456 255 L273 255 Q255 210 208 208 Q163 211 145 255 L106 255 Q87 254 92 236 Z" fill="url(#bodyGrad)" stroke="#d8f7ff" stroke-width="4"/>
        <path d="M275 150 L355 120 Q430 105 510 118 L568 183 L355 183 Z" fill="#b8f5ff" opacity=".76"/>
        <circle cx="210" cy="254" r="39" fill="#111827"/><circle cx="210" cy="254" r="20" fill="#94a3b8"/>
        <circle cx="520" cy="254" r="39" fill="#111827"/><circle cx="520" cy="254" r="20" fill="#94a3b8"/>
        <path d="M595 210 L643 219" stroke="#fff19c" stroke-width="7" stroke-linecap="round"/>
        <path d="M150 212 L104 221" stroke="#ff8ebf" stroke-width="6" stroke-linecap="round"/>
      </svg>
    </div>
  </div>
</section>

<section class="shell how-grid">
  <article class="info-card"><h3>1 · Discover</h3><p>Understand the concept lab and how a product journey moves from landing page to creation to review.</p></article>
  <article class="info-card"><h3>2 · Create</h3><p>Use a structured brief with style, material, colour, occasion, and inspiration to direct the AI clearly.</p></article>
  <article class="info-card"><h3>3 · Generate</h3><p>The back-end turns the brief into a rich concept object with specs, positioning, and polished colorways.</p></article>
  <article class="info-card"><h3>4 · Review</h3><p>Every design is saved into session history so you can compare ideas and build faster creative iterations.</p></article>
</section>
{% endblock %}


{% extends 'base.html' %}
{% block title %}Studio · AI Car Concept Lab{% endblock %}
{% block content %}
<section class="shell studio-shell" id="studioApp">
  <div class="panel brief-panel">
    <div class="panel-head">
      <span class="eyebrow">Design Brief</span>
      <h2>Shape the concept.</h2>
      <p>Pick strong inputs. The more precise the brief, the more focused the concept.</p>
    </div>

    <form id="conceptForm" class="brief-form">
      <div>
        <label for="style">Style</label>
        <select id="style" name="style" required>
          <option value="">Choose a style</option>
          <option>Hypercar</option>
          <option>Luxury</option>
          <option>Off-Road</option>
          <option>EV</option>
          <option>Retro-Future</option>
          <option>Street</option>
        </select>
      </div>
      <div>
        <label for="material">Primary Material</label>
        <select id="material" name="material" required>
          <option value="">Choose a material</option>
          <option>Carbon Fiber</option>
          <option>Aluminum</option>
          <option>Titanium</option>
          <option>Recycled Composite</option>
          <option>Glass &amp; Metal</option>
          <option>Mixed Performance</option>
        </select>
      </div>
      <div>
        <label for="occasion">Occasion</label>
        <select id="occasion" name="occasion" required>
          <option value="">Choose a use case</option>
          <option>Daily Drive</option>
          <option>Track Day</option>
          <option>Adventure</option>
          <option>Collector Reveal</option>
          <option>City Tech</option>
          <option>Luxury Tourer</option>
        </select>
      </div>
      <div class="color-grid">
        <label>Primary Colour
          <input type="color" id="primaryColor" name="primary_color" value="#1d4ed8">
        </label>
        <label>Accent Colour
          <input type="color" id="accentColor" name="accent_color" value="#f97316">
        </label>
      </div>
      <div>
        <label for="inspiration">Inspiration</label>
        <textarea id="inspiration" name="inspiration" rows="4" placeholder="Example: Tokyo neon rain, desert eclipse, aurora over ice highways" required></textarea>
      </div>
      <button type="submit" class="btn btn-primary full" id="generateBtn">Verify &amp; Generate Car Concept</button>
      <p id="formError" class="form-error" aria-live="polite"></p>
      <p class="form-note">This version adds hCaptcha before the AI call, so the brief only reaches generation after a human check passes.</p>
    </form>
  </div>

  <div class="panel result-panel" id="resultPanel">
    <div class="empty-state" id="emptyState">
      <span class="eyebrow">Output Panel</span>
      <h2>Your concept will appear here.</h2>

      <p>Generate once to see the car name, positioning, concept render, specs, and colorway system.</p>
    </div>

    <div class="loading-state hidden" id="loadingState">
      <span class="eyebrow">Generating</span>
      <h2>Assembling your future vehicle...</h2>
      <p id="loaderText" class="loader-text">Querying AI…</p>
      <div class="loader-bar"><span></span></div>
    </div>

    <div class="hidden" id="resultState">
      <div class="result-header">
        <div>
          <span class="eyebrow">AI Car Concept</span>
          <h2 id="carName"></h2>
          <p id="tagline" class="lead"></p>
        </div>
        <div class="price-pill" id="retailPrice"></div>
      </div>

      <div class="media-grid">
        <div class="render-card">
          <img id="conceptImage" alt="AI car concept render">
        </div>
        <div class="svg-card">
          <div class="svg-toolbar">
            <strong>Live Colorway Explorer</strong>
            <div id="swatchButtons" class="swatch-buttons"></div>
          </div>
          <div id="carSvgMount"></div>
        </div>
      </div>

      <p id="description" class="description"></p>

      <div class="spec-grid">
        <div class="spec-card"><h3>Materials</h3><ul id="materials"></ul></div>
        <div class="spec-card"><h3>Features</h3><ul id="features"></ul></div>
        <div class="spec-card"><h3>Powertrain</h3><p id="powertrain"></p></div>
        <div class="spec-card"><h3>Cockpit</h3><p id="cockpitTheme"></p></div>
        <div class="spec-card"><h3>Target Driver</h3><p id="targetDriver"></p></div>
        <div class="spec-card"><h3>Style Tags</h3><div id="styleTags" class="tags"></div></div>
      </div>
    </div>
  </div>
</section>

<div class="captcha-modal hidden" id="captchaModal" aria-hidden="true">
  <div class="captcha-card">
    <div class="captcha-head">
      <div>
        <span class="eyebrow">Security Check</span>
        <h3>Verify you're human</h3>
      </div>
      <button type="button" class="ghost-btn" id="cancelCaptcha">Cancel</button>
    </div>
    <p class="captcha-copy">The AI call is protected so free usage stays available for real people.</p>
    <div id="hcaptchaWidget"></div>
  </div>
</div>
{% endblock %}
{% block scripts %}
<script src="{{ url_for('static', filename='js/studio.js') }}"></script>
{% endblock %}

{% extends 'base.html' %}
{% block title %}History · AI Car Concept Lab{% endblock %}
{% block content %}
<section class="shell history-shell">
  <div class="history-head">
    <div>
      <span class="eyebrow">Session Gallery</span>
      <h1>Review your generated car concepts.</h1>
      <p>Compare naming, positioning, colorways, and design direction across all concepts in this session.</p>
    </div>
    {% if designs %}
      <button class="btn btn-secondary" id="clearHistoryBtn">Clear History</button>
    {% endif %}
  </div>

  {% if designs %}
    <div class="history-grid">
      {% for item in designs %}
      <article class="history-card">
        <img src="{{ item.image_url }}" alt="{{ item.name }} concept image">
        <div class="history-content">
          <div class="row-space">
            <h3>{{ item.name }}</h3>
            <span class="history-time">{{ item.timestamp }}</span>
          </div>
          <p class="lead small-lead">{{ item.tagline }}</p>
          <p class="history-desc">{{ item.description }}</p>
          <div class="tags">
            {% for tag in item.style_tags %}<span class="tag">{{ tag }}</span>{% endfor %}
          </div>
          <div class="swatch-row">
            {% for cw in item.colorways %}
            <div class="swatch-card">
              <strong>{{ cw.name }}</strong>
              <div class="mini-swatches">
                <span style="background:{{ cw.body }}"></span>
                <span style="background:{{ cw.accent }}"></span>
                <span style="background:{{ cw.wheels }}"></span>
              </div>
            </div>
            {% endfor %}
          </div>
          <div class="brief-summary">{{ item.brief.style }} · {{ item.brief.material }} · {{ item.brief.occasion }}</div>
        </div>
      </article>
      {% endfor %}
    </div>
  {% else %}
    <div class="empty-history glow-card">
      <div class="emoji">🚗</div>
      <h2>No concepts yet</h2>
      <p>Generate your first futuristic car in the studio and it will appear here automatically.</p>
      <a href="{{ url_for('studio') }}" class="btn btn-primary">Open Studio</a>
    </div>
  {% endif %}
</section>
<script>
const clearBtn = document.getElementById('clearHistoryBtn');
if (clearBtn) {
  clearBtn.addEventListener('click', async () => {
    await fetch('/clear-history', { method: 'POST' });
    location.reload();
  });
}
</script>
{% endblock %}


:root {
  --bg: #090b11;
  --panel: rgba(16, 20, 33, 0.78);
  --panel-solid: #111625;
  --line: rgba(255,255,255,0.08);
  --text: #eef2ff;
  --muted: #98a2c4;
  --primary: #7c5cff;
  --accent: #31e1ff;
  --gold: #ffd369;
  --shadow: 0 20px 70px rgba(0,0,0,.35);
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; font-family: Inter, Arial, sans-serif; background:
  radial-gradient(circle at top left, rgba(124,92,255,.16), transparent 30%),
  radial-gradient(circle at top right, rgba(49,225,255,.12), transparent 26%),
  linear-gradient(180deg, #090b11, #07090e 60%, #090b11);
  color: var(--text);
}
a { color: inherit; text-decoration: none; }
body { min-height: 100vh; position: relative; }
.noise { pointer-events:none; position: fixed; inset: 0; opacity: .08; background-image: radial-gradient(#fff 0.5px, transparent 0.5px); background-size: 18px 18px; }
.shell { width: min(1180px, calc(100% - 32px)); margin: 0 auto; }
.site-header, .site-footer { width: min(1180px, calc(100% - 32px)); margin: 0 auto; }
.site-header { display:flex; align-items:center; justify-content:space-between; padding: 22px 0; position: sticky; top: 0; z-index: 20; backdrop-filter: blur(18px); }
.brand { font-weight: 800; letter-spacing: .03em; }
.nav-links { display:flex; gap: 18px; align-items:center; }
.nav-links a { color: var(--muted); padding: 8px 10px; border-radius: 999px; }
.nav-links a.active, .nav-links a:hover { color: var(--text); background: rgba(255,255,255,.06); }
.site-footer { padding: 28px 0 38px; color: var(--muted); font-size: 14px; }
.btn { display:inline-flex; align-items:center; justify-content:center; gap: 8px; border: 1px solid var(--line); border-radius: 14px; padding: 13px 20px; font-weight: 700; cursor: pointer; transition: .2s ease; }
.btn:hover { transform: translateY(-1px); }
.btn.small { padding: 10px 16px; }
.btn.full { width: 100%; }
.btn-primary { background: linear-gradient(90deg, var(--primary), var(--accent)); color: #07090f; border: none; box-shadow: 0 10px 30px rgba(124,92,255,.28); }
.btn-secondary { background: rgba(255,255,255,.03); color: var(--text); }
.hero { display:grid; grid-template-columns: 1.1fr .9fr; gap: 28px; align-items: center; padding: 40px 0 28px; }
.hero h1 { font-size: clamp(40px, 5vw, 72px); line-height: .98; margin: 12px 0; }
.hero-copy p { color: var(--muted); max-width: 620px; font-size: 18px; }
.eyebrow { display:inline-block; color: var(--gold); text-transform: uppercase; letter-spacing: .14em; font-size: 12px; font-weight: 800; }
.cta-row { display:flex; gap: 14px; margin: 24px 0 30px; }
.stats-row { display:grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
.stat-card, .info-card, .panel, .history-card, .empty-history, .glow-card, .spec-card { background: var(--panel); border: 1px solid var(--line); backdrop-filter: blur(16px); box-shadow: var(--shadow); }
.stat-card { border-radius: 22px; padding: 18px; }
.stat-card strong { display:block; margin-bottom: 7px; font-size: 20px; }
.stat-card span, .info-card p, .panel-head p, .form-note, .description, .lead, .history-desc, .small-lead { color: var(--muted); }
.car-card { position: relative; border-radius: 28px; min-height: 420px; overflow: hidden; padding: 24px; }
.car-lines { position:absolute; inset:0; background: radial-gradient(circle at 25% 15%, rgba(124,92,255,.35), transparent 22%), radial-gradient(circle at 75% 22%, rgba(49,225,255,.22), transparent 18%); }
.hero-car { width: 100%; position: absolute; inset: auto 0 0 0; }
.floating-chip { position:absolute; padding: 10px 14px; border-radius: 999px; background: rgba(255,255,255,.08); border: 1px solid var(--line); font-size: 12px; font-weight: 700; }
.chip-a { left: 24px; top: 26px; }
.chip-b { right: 24px; top: 68px; }
.how-grid { display:grid; grid-template-columns: repeat(4, 1fr); gap: 14px; padding: 10px 0 48px; }
.info-card { border-radius: 22px; padding: 22px; }
.info-card h3 { margin-top: 0; }
.studio-shell { display:grid; grid-template-columns: 430px minmax(0, 1fr); gap: 18px; padding: 26px 0 36px; }
.panel { border-radius: 28px; padding: 24px; }
.panel-head h2, .history-head h1 { margin: 10px 0 8px; }
.brief-form { display:grid; gap: 16px; }
label { display:grid; gap: 9px; font-size: 14px; font-weight: 700; }
select, textarea, input[type="color"] { width: 100%; border-radius: 16px; border: 1px solid var(--line); background: rgba(255,255,255,.04); color: var(--text); padding: 14px 16px; }

select:focus, textarea:focus { outline: 2px solid rgba(49,225,255,.35); }
textarea { resize: vertical; min-height: 120px; }
input[type="color"] { height: 54px; padding: 8px; }
.color-grid { display:grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.result-panel { min-height: 760px; }
.empty-state, .loading-state { display:grid; align-content:center; justify-items:start; min-height: 680px; }
.hidden { display:none !important; }
.loader-bar { width: min(420px, 100%); height: 14px; border-radius: 999px; overflow:hidden; background: rgba(255,255,255,.06); margin-top: 16px; }
.loader-bar span { display:block; height:100%; width:40%; background: linear-gradient(90deg, var(--primary), var(--accent)); animation: load 1.15s infinite alternate ease-in-out; }
@keyframes load { from { transform: translateX(-40%);} to { transform: translateX(170%);} }
.result-header { display:flex; justify-content:space-between; gap: 16px; align-items:flex-start; margin-bottom: 18px; }
.result-header h2 { margin: 8px 0 6px; font-size: 40px; }
.lead { font-size: 18px; }
.price-pill { border-radius: 999px; padding: 12px 14px; background: rgba(49,225,255,.1); color: #dffcff; border: 1px solid rgba(49,225,255,.22); font-weight: 800; }
.media-grid { display:grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 18px; }
.render-card, .svg-card { border-radius: 24px; overflow: hidden; border: 1px solid var(--line); background: var(--panel-solid); }
.render-card img { width:100%; height:100%; min-height: 310px; object-fit: cover; display:block; }
.svg-card { padding: 18px; }
#carSvgMount svg { width:100%; height:auto; display:block; }
.svg-toolbar { display:flex; justify-content:space-between; gap: 10px; align-items:center; margin-bottom: 10px; }
.swatch-buttons { display:flex; flex-wrap:wrap; gap: 8px; }
.swatch-btn { border: 1px solid var(--line); background: rgba(255,255,255,.04); color: var(--text); padding: 8px 10px; border-radius: 999px; font-size: 12px; font-weight: 700; cursor:pointer; }
.swatch-btn.active { background: rgba(124,92,255,.2); border-color: rgba(124,92,255,.42); }
.description { font-size: 16px; line-height: 1.7; }
.spec-grid { display:grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: 18px; }
.spec-card { border-radius: 22px; padding: 18px; }
.spec-card h3 { margin-top: 0; }
.spec-card ul { padding-left: 18px; margin: 0; }
.tags { display:flex; flex-wrap: wrap; gap: 8px; }
.tag { padding: 7px 11px; border-radius: 999px; background: rgba(255,255,255,.06); border: 1px solid var(--line); color: #dbe4ff; font-size: 12px; font-weight: 700; }
.history-shell { padding: 26px 0 42px; }
.history-head { display:flex; justify-content:space-between; gap: 18px; align-items:flex-start; margin-bottom: 18px; }
.history-grid { display:grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
.history-card { overflow:hidden; border-radius: 24px; }
.history-card img { width:100%; height: 260px; object-fit: cover; display:block; }
.history-content { padding: 18px; }
.row-space { display:flex; justify-content:space-between; gap: 12px; align-items:flex-start; }
.history-time, .brief-summary { color: var(--muted); font-size: 13px; }
.swatch-row { display:grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 14px 0; }
.swatch-card { padding: 12px; border: 1px solid var(--line); border-radius: 16px; background: rgba(255,255,255,.03); }
.mini-swatches { display:flex; gap: 8px; margin-top: 10px; }
.mini-swatches span { width: 22px; height: 22px; border-radius: 50%; border: 1px solid rgba(255,255,255,.2); }
.empty-history { border-radius: 30px; min-height: 420px; display:grid; justify-items:center; align-content:center; text-align:center; padding: 24px; }
.emoji { font-size: 58px; }
@media (max-width: 980px) {
  .hero, .studio-shell, .media-grid, .history-grid, .how-grid, .spec-grid, .stats-row { grid-template-columns: 1fr; }
  .site-header { gap: 12px; flex-wrap: wrap; }
  .nav-links { order: 3; width: 100%; justify-content: center; }
  .result-header, .history-head, .svg-toolbar, .row-space { flex-direction: column; }
}

.form-error{min-height:1.25rem;color:#fca5a5;font-size:.94rem;margin:.5rem 0 0;}


.loader-text{color:#9fb0d7;margin:0 0 14px;font-size:.95rem}
.captcha-modal{position:fixed;inset:0;background:rgba(4,8,18,.72);display:grid;place-items:center;padding:20px;z-index:40}
.captcha-card{width:min(100%,420px);background:rgba(12,18,34,.96);border:1px solid rgba(255,255,255,.09);border-radius:24px;padding:24px;box-shadow:0 24px 80px rgba(0,0,0,.45)}
.captcha-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-bottom:8px}
.captcha-copy{margin:0 0 18px;color:#9fb0d7;line-height:1.55}
.ghost-btn{background:transparent;border:1px solid rgba(255,255,255,.15);color:#dbeafe;border-radius:999px;padding:10px 14px;cursor:pointer}
#hcaptchaWidget{min-height:86px;display:flex;align-items:center;justify-content:center}

(() => {
  const form = document.getElementById('conceptForm')
  const emptyState = document.getElementById('emptyState')
  const loadingState = document.getElementById('loadingState')
  const resultState = document.getElementById('resultState')
  const formError = document.getElementById('formError')
  const loaderText = document.getElementById('loaderText')
  const generateBtn = document.getElementById('generateBtn')
  const captchaModal = document.getElementById('captchaModal')
  const cancelCaptcha = document.getElementById('cancelCaptcha')

  const LOADER_MSGS = [
    'Querying AI…',
    'Sketching body lines…',
    'Balancing materials…',
    'Dialing the cockpit mood…',
    'Finalizing launch specs…',
  ]

  let loaderInterval = null
  let captchaWidgetId = null

  const bindText = (id, value) => { document.getElementById(id).textContent = value || '' }
  const escHtml = (value) => String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')

  const listInto = (id, items) => {
    document.getElementById(id).innerHTML = (items || []).map(item => `<li>${escHtml(item)}</li>`).join('')
  }

  const tagsInto = (id, items) => {
    document.getElementById(id).innerHTML = (items || []).map(item => `<span class="tag">${escHtml(item)}</span>`).join('')
  }

  window.hcaptchaReady = () => {
    if (!window.hcaptcha || !document.getElementById('hcaptchaWidget') || captchaWidgetId !== null) return
    captchaWidgetId = window.hcaptcha.render('hcaptchaWidget', {
      sitekey: window.HCAPTCHA_SITE_KEY,
      theme: 'dark',
      size: 'compact',
      callback: token => {
        hideCaptcha()
        runGeneration(token)
      },
      'expired-callback': () => {
        hideCaptcha()
        generateBtn.disabled = false
        formError.textContent = 'CAPTCHA expired. Please try again.'
      },
      'error-callback': () => {
        hideCaptcha()
        generateBtn.disabled = false
        formError.textContent = 'CAPTCHA could not load. Refresh and try again.'
      },
    })
  }

  form?.addEventListener('submit', (event) => {
    event.preventDefault()
    formError.textContent = ''
    generateBtn.disabled = true
    if (window.hcaptcha && captchaWidgetId !== null) {
      window.hcaptcha.reset(captchaWidgetId)
      showCaptcha()
      return
    }
    generateBtn.disabled = false
    formError.textContent = 'CAPTCHA is still loading. Please wait a moment and try again.'
  })

  cancelCaptcha?.addEventListener('click', () => {
    hideCaptcha()
    generateBtn.disabled = false
  })

  async function runGeneration(token) {
    formError.textContent = ''
    toggleStates('loading')
    startLoader()
    try {
      const prefs = Object.fromEntries(new FormData(form).entries())
      prefs['h-captcha-response'] = token
      const resp = await fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(prefs),
      })
      const data = await resp.json()
      if (!resp.ok || !data.success) throw new Error(data.error || 'Something went wrong.')
      renderConcept(data.concept)
      toggleStates('result')
    } catch (error) {
      toggleStates('empty')
      formError.textContent = error.message || 'Could not generate the concept.'
    } finally {
      stopLoader()
      generateBtn.disabled = false
      if (window.hcaptcha && captchaWidgetId !== null) window.hcaptcha.reset(captchaWidgetId)
    }
  }

  function startLoader() {
    let i = 0
    loaderText.textContent = LOADER_MSGS[0]
    loaderInterval = window.setInterval(() => {

      i = (i + 1) % LOADER_MSGS.length
      loaderText.textContent = LOADER_MSGS[i]
    }, 1400)
  }

  function stopLoader() {
    if (loaderInterval) window.clearInterval(loaderInterval)
    loaderInterval = null
  }

  function showCaptcha() {
    captchaModal.classList.remove('hidden')
  }

  function hideCaptcha() {
    captchaModal.classList.add('hidden')
  }

  function toggleStates(mode) {
    emptyState.classList.toggle('hidden', mode !== 'empty')
    loadingState.classList.toggle('hidden', mode !== 'loading')
    resultState.classList.toggle('hidden', mode !== 'result')
  }

  function renderConcept(concept) {
    const c = concept
    bindText('carName', c.name)
    bindText('tagline', c.tagline)
    bindText('retailPrice', c.retail_price)
    bindText('description', c.description)
    bindText('powertrain', c.powertrain)
    bindText('cockpitTheme', c.cockpit_theme)
    bindText('targetDriver', c.target_driver)
    listInto('materials', c.materials)
    listInto('features', c.features)
    tagsInto('styleTags', c.style_tags)
    const img = document.getElementById('conceptImage')
    img.src = c.image_url
    img.alt = `${c.name} concept render`
    renderColorwayButtons(c.colorways, c.name)
    renderCarSvg(c.colorways?.[0] || {}, c.name)
  }

  function renderColorwayButtons(colorways, name) {
    const mount = document.getElementById('swatchButtons')
    mount.innerHTML = ''
    ;(colorways || []).forEach((cw, index) => {
      const btn = document.createElement('button')
      btn.type = 'button'
      btn.className = `swatch-btn ${index === 0 ? 'active' : ''}`
      btn.textContent = cw.name
      btn.addEventListener('click', () => {
        document.querySelectorAll('.swatch-btn').forEach(node => node.classList.remove('active'))
        btn.classList.add('active')
        renderCarSvg(cw, name)
      })
      mount.appendChild(btn)
    })
  }

  function renderCarSvg(cw, name = '') {
    const mount = document.getElementById('carSvgMount')
    mount.innerHTML = `
    <svg viewBox="0 0 780 420" role="img" aria-label="${escHtml(name || cw.name || 'Car concept')} colorway preview">
      <defs>
        <linearGradient id="bodyFill" x1="0" x2="1">
          <stop offset="0%" stop-color="${cw.body || '#1d4ed8'}"/>
          <stop offset="100%" stop-color="${shade(cw.body || '#1d4ed8', 32)}"/>
        </linearGradient>
        <linearGradient id="accentFill" x1="0" x2="1">
          <stop offset="0%" stop-color="${cw.accent || '#f97316'}"/>
          <stop offset="100%" stop-color="${shade(cw.accent || '#f97316', 18)}"/>
        </linearGradient>
      </defs>
      <rect width="780" height="420" rx="28" fill="#0d1220"/>
      <ellipse cx="390" cy="336" rx="250" ry="24" fill="${alpha(cw.accent || '#f97316', .18)}"/>
      <path d="M128 264 Q176 176 314 160 L468 146 Q576 147 642 223 L684 263 L660 292 L598 292 Q582 239 530 236 Q480 238 458 292 L276 292 Q254 238 204 236 Q151 239 132 292 L98 292 Q75 292 83 270 Z" fill="url(#bodyFill)" stroke="${shade(cw.body || '#1d4ed8', 52)}" stroke-width="4"/>
      <path d="M285 168 L362 132 Q437 118 516 128 L582 214 L352 214 Z" fill="${alpha(cw.cabin || '#d9dce5', .86)}"/>
      <path d="M170 248 L102 260" stroke="url(#accentFill)" stroke-width="8" stroke-linecap="round"/>
      <path d="M614 247 L674 256" stroke="#fff2b0" stroke-width="8" stroke-linecap="round"/>
      <path d="M323 158 Q416 135 526 146" stroke="${alpha(cw.accent || '#f97316', .95)}" stroke-width="6" stroke-linecap="round"/>
      <circle cx="208" cy="290" r="43" fill="${cw.wheels || '#1b1e28'}"/>
      <circle cx="208" cy="290" r="22" fill="${shade(cw.wheels || '#1b1e28', 70)}"/>
      <circle cx="528" cy="290" r="43" fill="${cw.wheels || '#1b1e28'}"/>
      <circle cx="528" cy="290" r="22" fill="${shade(cw.wheels || '#1b1e28', 70)}"/>
      <text x="40" y="52" fill="#dbeafe" font-size="24" font-family="Inter, Arial" font-weight="700">${escHtml(cw.name || 'Launch Spec')}</text>
      <text x="40" y="82" fill="#95a4c6" font-size="14" font-family="Inter, Arial">Body · ${escHtml(cw.body || '#1d4ed8')} · Accent · ${escHtml(cw.accent || '#f97316')}</text>
    </svg>`
  }

  function shade(hex, amount) {
    const clean = (hex || '#000000').replace('#', '')
    const num = parseInt(clean, 16)
    const r = Math.min(255, Math.max(0, (num >> 16) + amount))
    const g = Math.min(255, Math.max(0, ((num >> 8) & 255) + amount))
    const b = Math.min(255, Math.max(0, (num & 255) + amount))
    return `#${[r, g, b].map(v => v.toString(16).padStart(2, '0')).join('')}`
  }

  function alpha(hex, opacity) {
    const clean = (hex || '#000000').replace('#', '')
    const num = parseInt(clean, 16)
    const r = num >> 16
    const g = (num >> 8) & 255
    const b = num & 255
    return `rgba(${r}, ${g}, ${b}, ${opacity})`
  }
})()

# 1. Open terminal inside the project folder
cd ai-car-concept-lab-protected

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Flask app
python app.py

# 4. Open in browser
http://localhost:5000


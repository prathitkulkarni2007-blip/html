pip install -r requirements.txt
flask==3.1.3
requests==2.32.5
python-dotenv==1.2.1
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
 
load_dotenv()
 
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "ai-car-concept-lab-dev-key")
app.config["SESSION_PERMANENT"] = False
 
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
MAX_HISTORY = 12
 
 
STYLE_TAGS = {
    "Hypercar": ["aggressive aero", "track-ready stance", "dramatic lighting"],
    "Luxury": ["executive comfort", "clean surfacing", "premium cabin"],
    "Off-Road": ["raised ride height", "rugged utility", "all-terrain confidence"],
    "EV": ["clean tech aesthetic", "silent performance", "futuristic cockpit"],
    "Retro-Future": ["classic proportions", "neo-futurist detailing", "heritage remix"],
    "Street": ["urban stance", "after-dark energy", "custom performance"],
}
 
MATERIAL_NOTES = {
    "Carbon Fiber": ["carbon composite body panels", "forged aero fins", "lightweight frame"],
    "Aluminum": ["aluminum monocoque", "satin body surfaces", "precision-machined trim"],
    "Titanium": ["titanium highlights", "heat-blued accents", "ultra-premium shell"],
    "Recycled Composite": ["sustainable composite shell", "eco-performance interior", "recycled weave trim"],
    "Glass & Metal": ["panoramic glass canopy", "brushed alloy bodywork", "sculpted metallic spine"],
    "Mixed Performance": ["hybrid material shell", "performance mesh vents", "contrasting aero textures"],
}
 
PRICE_BANDS = {
    "Daily Drive": "$58,000",
    "Track Day": "$210,000",
    "Adventure": "$96,000",
    "Collector Reveal": "$320,000",
    "City Tech": "$74,000",
    "Luxury Tourer": "$168,000",
}
 
 
@app.route("/")
def index() -> str:
    return render_template("index.html")
 
 
@app.route("/studio")
def studio() -> str:
    return render_template("studio.html")
 
 
@app.route("/history")
def history() -> str:
    return render_template("history.html", designs=get_history())
 
 
@app.post("/api/generate")
def generate() -> Any:
    payload = request.get_json(silent=True) or {}
    brief = normalize_brief(payload)
    missing = [k for k, v in brief.items() if not v]
    if missing:
        return jsonify({"ok": False, "error": "Please complete all design brief fields."}), 400
 
    concept = generate_concept(brief)
    image_url = build_image_url(concept, brief)
    concept["image_url"] = image_url
    concept["brief"] = brief
    concept["timestamp"] = datetime.now().strftime("%d %b %Y, %I:%M %p")
    concept["fingerprint"] = fingerprint(brief, concept["name"])
 
    add_to_history(concept)
    return jsonify({"ok": True, "concept": concept})
 
 
@app.post("/clear-history")
def clear_history() -> Any:
    session["designs"] = []
    return jsonify({"ok": True})
 
 
def normalize_brief(payload: dict[str, Any]) -> dict[str, str]:
    return {
        "style": str(payload.get("style", "")).strip(),
        "material": str(payload.get("material", "")).strip(),
        "occasion": str(payload.get("occasion", "")).strip(),
        "primary_color": str(payload.get("primary_color", "")).strip(),
        "accent_color": str(payload.get("accent_color", "")).strip(),
        "inspiration": str(payload.get("inspiration", "")).strip(),
    }
 
 
def get_history() -> list[dict[str, Any]]:
    return session.get("designs", [])
 
 
def add_to_history(concept: dict[str, Any]) -> None:
    current = session.get("designs", [])
    deduped = [d for d in current if d.get("fingerprint") != concept["fingerprint"]]
    session["designs"] = [concept] + deduped[: MAX_HISTORY - 1]
    session.modified = True
 
 
def fingerprint(brief: dict[str, str], name: str) -> str:
    raw = "|".join([brief["style"], brief["material"], brief["occasion"], brief["primary_color"], brief["accent_color"], brief["inspiration"], name])
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:14]
 
 
def generate_concept(brief: dict[str, str]) -> dict[str, Any]:
    if GROQ_API_KEY:
        concept = generate_via_groq(brief)
        if concept:
            return concept
    return generate_local_concept(brief)
 
 
def generate_via_groq(brief: dict[str, str]) -> dict[str, Any] | None:
    system_prompt = (
        "You are a senior futuristic car concept designer. "
        "Return ONLY valid JSON. No markdown, no explanation."
    )
    user_prompt = f'''
Create one futuristic car concept from this structured brief.
 
Brief:
- Style: {brief['style']}
- Material: {brief['material']}
- Occasion: {brief['occasion']}
- Primary colour: {brief['primary_color']}
- Accent colour: {brief['accent_color']}
- Inspiration: {brief['inspiration']}
 
Return JSON with exactly these keys:
name, tagline, description, materials, features, powertrain, cockpit_theme,
target_driver, retail_price, style_tags, colorways
 
Rules:
- materials: array of 3 to 5 strings
- features: array of 4 to 6 strings
- style_tags: array of 3 short strings
- colorways: array of exactly 3 objects
- each colorway object must contain: name, body, accent, wheels, cabin
- keep retail_price as a string like "$120,000"
- make the result vivid, premium, and product-like
'''
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": GROQ_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.9,
            },
            timeout=45,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"].strip()
        match = re.search(r"\{[\s\S]*\}", content)
        if not match:
            return None
        concept = json.loads(match.group(0))
        if not is_valid_concept(concept):
            return None
        return sanitize_concept(concept, brief)
    except Exception:
        return None
 
 
def is_valid_concept(concept: dict[str, Any]) -> bool:
    required = [
        "name",
        "tagline",
        "description",
        "materials",
        "features",
        "powertrain",
        "cockpit_theme",
        "target_driver",
        "retail_price",
        "style_tags",
        "colorways",
    ]
    return all(k in concept for k in required) and isinstance(concept.get("colorways"), list)
 
 
def sanitize_concept(concept: dict[str, Any], brief: dict[str, str]) -> dict[str, Any]:
    clean = {
        "name": str(concept.get("name", "Concept X")).strip(),
        "tagline": str(concept.get("tagline", "Future in motion.")).strip(),
        "description": str(concept.get("description", "")).strip(),
        "materials": [str(x).strip() for x in concept.get("materials", [])][:5] or MATERIAL_NOTES.get(brief["material"], [])[:3],
        "features": [str(x).strip() for x in concept.get("features", [])][:6] or ["Adaptive aero body", "Panoramic digital cockpit", "Active rear light blade", "Performance-tuned handling"],
        "powertrain": str(concept.get("powertrain", "Quad-motor electric performance")).strip(),
        "cockpit_theme": str(concept.get("cockpit_theme", "Minimal driver-first cockpit")).strip(),
        "target_driver": str(concept.get("target_driver", "Design-forward performance enthusiasts")).strip(),
        "retail_price": str(concept.get("retail_price", PRICE_BANDS.get(brief["occasion"], "$120,000"))).strip(),
        "style_tags": [str(x).strip() for x in concept.get("style_tags", [])][:3] or STYLE_TAGS.get(brief["style"], [])[:3],
        "colorways": normalize_colorways(concept.get("colorways", []), brief),
    }
    return clean
 
 
def normalize_colorways(colorways: list[dict[str, Any]], brief: dict[str, str]) -> list[dict[str, str]]:
    fallback = [
        {
            "name": "Launch Spec",
            "body": brief["primary_color"],
            "accent": brief["accent_color"],
            "wheels": "#1b1e28",
            "cabin": "#d9dce5",
        },
        {
            "name": "Midnight Signal",
            "body": shift_hex(brief["primary_color"], -18),
            "accent": brief["accent_color"],
            "wheels": "#0f1218",
            "cabin": "#c7d2e2",
        },
        {
            "name": "Volt Mirage",
            "body": shift_hex(brief["primary_color"], 18),
            "accent": shift_hex(brief["accent_color"], 20),
            "wheels": "#2b2f3e",
            "cabin": "#f4f1eb",
        },
    ]
    cleaned: list[dict[str, str]] = []
    for idx, item in enumerate(colorways[:3]):
        cleaned.append(
            {
                "name": str(item.get("name", fallback[idx]["name"])).strip(),
                "body": normalize_hex(str(item.get("body", fallback[idx]["body"])).strip(), fallback[idx]["body"]),
                "accent": normalize_hex(str(item.get("accent", fallback[idx]["accent"])).strip(), fallback[idx]["accent"]),
                "wheels": normalize_hex(str(item.get("wheels", fallback[idx]["wheels"])).strip(), fallback[idx]["wheels"]),
                "cabin": normalize_hex(str(item.get("cabin", fallback[idx]["cabin"])).strip(), fallback[idx]["cabin"]),
            }
        )
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
    rng = random.Random(seed)
    first = ["Nova", "Aero", "Volt", "Phantom", "Zenith", "Pulse", "Halo", "Rift"]
    second = ["GT", "Flux", "One", "Racer", "Drive", "Arc", "XR", "Vision"]
    name = f"{rng.choice(first)} {rng.choice(second)}"
    taglines = [
        "Built for tomorrow's roads.",
        "Where concept meets velocity.",
        "Electric drama. Precision control.",
        "Designed to steal the skyline.",
    ]
    materials = MATERIAL_NOTES.get(brief["material"], MATERIAL_NOTES["Mixed Performance"])
    features = [
        f"{brief['style']} silhouette with active aero channels",
        f"{brief['occasion']} tuned suspension package",
        "Full-width reactive light blade",
        "Augmented HUD with route intelligence",
        f"Cabin accents inspired by {brief['inspiration']}",
    ]
    description = (
        f"{name} is a {brief['style'].lower()} future concept shaped for {brief['occasion'].lower()} moments. "
        f"It pairs a {brief['material'].lower()}-driven body language with {brief['primary_color']} as the hero tone and "
        f"{brief['accent_color']} as the electric punch. The entire build channels {brief['inspiration']} into a sleek, cinematic road presence."
    )
    return {
        "name": name,
        "tagline": rng.choice(taglines),
        "description": description,
        "materials": materials[:3],
        "features": features[:5],
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
    <p>Built with Flask, structured prompts, session history, and a futuristic product workflow.</p>
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
          <option>Glass & Metal</option>
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
      <button type="submit" class="btn btn-primary full">Generate Car Concept</button>
      <p class="form-note">Tip: bold imagery and a clear design mood usually create more memorable results.</p>
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
const form = document.getElementById('conceptForm')
const emptyState = document.getElementById('emptyState')
const loadingState = document.getElementById('loadingState')
const resultState = document.getElementById('resultState')
 
const bindText = (id, value) => { document.getElementById(id).textContent = value }
const listInto = (id, items) => {
  document.getElementById(id).innerHTML = items.map(item => `<li>${escapeHtml(item)}</li>`).join('')
}
const tagsInto = (id, items) => {
  document.getElementById(id).innerHTML = items.map(item => `<span class="tag">${escapeHtml(item)}</span>`).join('')
}
const escapeHtml = (value) => String(value)
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;')
 
form?.addEventListener('submit', async (event) => {
  event.preventDefault()
  toggleStates('loading')
  const payload = Object.fromEntries(new FormData(form).entries())
  try {
    const response = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
    const data = await response.json()
    if (!response.ok || !data.ok) throw new Error(data.error || 'Something went wrong.')
    renderConcept(data.concept)
    toggleStates('result')
  } catch (error) {
    toggleStates('empty')
    alert(error.message)
  }
})
 
function toggleStates(mode) {
  emptyState.classList.toggle('hidden', mode !== 'empty')
  loadingState.classList.toggle('hidden', mode !== 'loading')
  resultState.classList.toggle('hidden', mode !== 'result')
}
 
function renderConcept(concept) {
  bindText('carName', concept.name)
  bindText('tagline', concept.tagline)
  bindText('retailPrice', concept.retail_price)
  bindText('description', concept.description)
  bindText('powertrain', concept.powertrain)
  bindText('cockpitTheme', concept.cockpit_theme)
  bindText('targetDriver', concept.target_driver)
  listInto('materials', concept.materials)
  listInto('features', concept.features)
  tagsInto('styleTags', concept.style_tags)
  document.getElementById('conceptImage').src = concept.image_url
  renderColorwayButtons(concept.colorways)
  renderCarSvg(concept.colorways[0], concept.name)
}
 
function renderColorwayButtons(colorways) {
  const mount = document.getElementById('swatchButtons')
  mount.innerHTML = ''
  colorways.forEach((cw, index) => {
    const btn = document.createElement('button')
    btn.type = 'button'
    btn.className = `swatch-btn ${index === 0 ? 'active' : ''}`
    btn.textContent = cw.name
    btn.addEventListener('click', () => {
      document.querySelectorAll('.swatch-btn').forEach(node => node.classList.remove('active'))
      btn.classList.add('active')
      renderCarSvg(cw)
    })
    mount.appendChild(btn)
  })
}
 
function renderCarSvg(cw, name = '') {
  const mount = document.getElementById('carSvgMount')
  mount.innerHTML = `
  <svg viewBox="0 0 780 420" role="img" aria-label="${escapeHtml(name || cw.name)} colorway preview">
    <defs>
      <linearGradient id="bodyFill" x1="0" x2="1">
        <stop offset="0%" stop-color="${cw.body}"/>
        <stop offset="100%" stop-color="${shade(cw.body, 32)}"/>
      </linearGradient>
      <linearGradient id="accentFill" x1="0" x2="1">
        <stop offset="0%" stop-color="${cw.accent}"/>
        <stop offset="100%" stop-color="${shade(cw.accent, 18)}"/>
      </linearGradient>
    </defs>
    <rect width="780" height="420" rx="28" fill="#0d1220"/>
    <ellipse cx="390" cy="336" rx="250" ry="24" fill="${alpha(cw.accent, .18)}"/>
    <path d="M128 264 Q176 176 314 160 L468 146 Q576 147 642 223 L684 263 L660 292 L598 292 Q582 239 530 236 Q480 238 458 292 L276 292 Q254 238 204 236 Q151 239 132 292 L98 292 Q75 292 83 270 Z" fill="url(#bodyFill)" stroke="${shade(cw.body, 52)}" stroke-width="4"/>
    <path d="M285 168 L362 132 Q437 118 516 128 L582 214 L352 214 Z" fill="${alpha(cw.cabin, .86)}"/>
    <path d="M170 248 L102 260" stroke="url(#accentFill)" stroke-width="8" stroke-linecap="round"/>
    <path d="M614 247 L674 256" stroke="#fff2b0" stroke-width="8" stroke-linecap="round"/>
    <path d="M323 158 Q416 135 526 146" stroke="${alpha(cw.accent, .95)}" stroke-width="6" stroke-linecap="round"/>
    <circle cx="208" cy="290" r="43" fill="${cw.wheels}"/>
    <circle cx="208" cy="290" r="22" fill="${shade(cw.wheels, 70)}"/>
    <circle cx="528" cy="290" r="43" fill="${cw.wheels}"/>
    <circle cx="528" cy="290" r="22" fill="${shade(cw.wheels, 70)}"/>
    <text x="40" y="52" fill="#dbeafe" font-size="24" font-family="Inter, Arial" font-weight="700">${escapeHtml(cw.name)}</text>
    <text x="40" y="82" fill="#95a4c6" font-size="14" font-family="Inter, Arial">Body · ${cw.body} · Accent · ${cw.accent}</text>
  </svg>`
}
 
function shade(hex, amount) {
  const clean = hex.replace('#', '')
  const num = parseInt(clean, 16)
  const r = Math.min(255, Math.max(0, (num >> 16) + amount))
  const g = Math.min(255, Math.max(0, ((num >> 8) & 255) + amount))
  const b = Math.min(255, Math.max(0, (num & 255) + amount))
  return `#${[r,g,b].map(v => v.toString(16).padStart(2, '0')).join('')}`
}
 
function alpha(hex, opacity) {
  const clean = hex.replace('#', '')
  const num = parseInt(clean, 16)
  const r = num >> 16
  const g = (num >> 8) & 255
  const b = num & 255
  return `rgba(${r}, ${g}, ${b}, ${opacity})`
}
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
python app.py
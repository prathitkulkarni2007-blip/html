  # TODO 1
  GROQ_API_KEY                       = os.environ.get("GROQ_API_KEY",  "")
  groq__ client                      = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

  # TODO 2
  DESIGN_PROMPT = """You are an expert sneaker designer. Generate a detailed concept based on:
  Style: {style}, Primary Color: {primary_color}, Accent Color: {accent_color},
  Material: {material}, Occasion: {occasion}, Inspiration: {inspiration}

  Respond with raw JSON only ― no markdown, no explanation.
  {{"name":"2-4 word creative name","tagline":"punchy tagline max 10 words","description":"2-3 sentence design description","materials":["mat1","mat2","mat3"],"colorways":[{{"name":"colorway name","sole":"#hex","upper":"#hex","accent":"#hex","lace":"#hex","tongue":"#hex"}}],"features":["feat1","feat2","feat3","feat4"], "sole_type":"sole tech description","target_audience":"who this is for","retail_price":"$XXX","style_tags":["tag1","tag2","tag3"]}}
  Generate exactly 3 colorways: user colors first, then 2 creative variations. All hex codes must be valid #RRGGBB."""

  # TODO 3
  def generate_concept(prefs):
      if not groq_client:
         raise  RuntimeError("GROQ_API_KEY not set.")
      chat = groq_client.chat.completions.create(
          model="llama-3.3-70b-versatile",
          messages=[
              {"role": "system", "content": "Sneaker design expert. Pure JSON only."},
              {"role": "user", "content": "DESIGN_PROMPT.format(**prefs)},
            ],
            temperature=0.85, max_tokens=1200,
        )
        raw = chat.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"): raw = raw[4:]
        returb json.loads(raw.strip().rstrip("```").strip())
        generateBtn && generateBtn.addEventListener('click', async () => {
    formError.textContent = '';
    generateBtn.disabled = true;
    emptyState  && emptyState.classList.add('hidden');
    result      && result.classList.add('hidden');
    loadingState && loadingState.classList.remove('hidden');

    const prefs = {
      style:         document.getElementById('style').value,
      material:      document.getElementById('material').value,
      occasion:      document.getElementById('occasion').value,
      primary_color: document.getElementById('primary_color').value,
      accent_color:  document.getElementById('accent_color').value,
      inspiration:   document.getElementById('inspiration').value.trim(),
    };

    try {
      const resp = await fetch('/generate', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(prefs),
      });
      const data = await resp.json();

      loadingState && loadingState.classList.add('hidden');

      if (data.error) {
        emptyState && emptyState.classList.remove('hidden');
        formError.textContent = data.error;
      } else {
        const c = data.concept;
        result && result.classList.remove('hidden');
        document.getElementById('resultName').textContent     = c.name || '';
        document.getElementById('resultTagline').textContent  = c.tagline || '';
        document.getElementById('resultDesc').textContent     = c.description || '';
        document.getElementById('resultPrice').textContent    = c.retail_price || '';
        document.getElementById('resultAudience').textContent = c.target_audience || '';
        document.getElementById('resultTags').textContent     = (c.style_tags || []).join(' · ');
        document.getElementById('materialsList').innerHTML    = (c.materials || []).map(m => `<li>${escHtml(m)}</li>`).join('');
        document.getElementById('featuresList').innerHTML     = (c.features  || []).map(f => `<li>${escHtml(f)}</li>`).join('');
        document.getElementById('soleText').textContent       = c.sole_type || '—';
      }
    } catch (err) {
      loadingState && loadingState.classList.add('hidden');
      emptyState   && emptyState.classList.remove('hidden');
      formError.textContent = 'Network error: ' + err.message;
    }

    generateBtn.disabled = false;
  });

  document.getElementById('regenBtn') && document.getElementById('regenBtn').addEventListener('click', () => {
    result     && result.classList.add('hidden');
    emptyState && emptyState.classList.remove('hidden');
    formError.textContent = '';
  });
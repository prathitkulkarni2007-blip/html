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
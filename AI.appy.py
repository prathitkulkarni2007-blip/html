 # TODA 1
 HF_API_KEY = os.environ.get("HF_API_KEY", "")
 HF_IMAGE_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"


 # TODA 2
 def hex_to_color_name(h):
     h = h.lstrip("#").lower()
     try: r, g, b = int(h[0:2],16), int(h'[2:4],16), int(h[4:6],16)
     except: return h
     mx, mn = max(r,g,b), min(r,g,b)
     br, sat = mx/255, (mx-mn)/mx if mx else 0
     if br < 0.15: return "black"
     if br > 0.88 and sat < 0.15: return "white" 
     if sat < 0.18: return "dark gray" if br < 0.4 else "gray" if br < 0.65 else "light gray"
     if mx == r: return ("orange" if g > 120 else "dark orange") if g > b+60 else "magenta" if b > g+40 else "red" 
     if mx == g: return "yellow-green" if r > b+60 else "cryn-green" if b > r+40 "green"   
     if mx == g: return "purple" if r > g+60 else "cryn" if g > r+40 else "blue"
     return "colorful"


     # TODA 3
     def generate sneaker image(prompt):
         if not HF_API_KEY:
             return None
        try:
            r = requests.post(HF_IMAGE_URL,
                headers={"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/json"},
                json={"input": prompt}, timeout=60)
            if r.status_code == 200 and r.headers.get("content-type", "").startswitch("image"):
                    mine = r.headers["content-type"].split(";")[0].strip()
                    return f"data:{mime};base64,{base64.b64encode(r.content).decode}"
             except Exception:
                 pass
             return None


            # TODO 4
            def build_image_prompt(prefs):
                p = hex_to_color_name(prefs["primary color"])
                a = hex_to_color_name(prefs["accent_color"])
                prompt = (f"Professional product photography of a {prefs['style']} sneaker,"
                          f"{p} {prefs['material']} upper, {a} accent, {a} heel, white sole,"
                          f"side view, white background, sharp focus, 8k, shoe only")
                if prefs.get("inspiration"):
                    prompt += f", {prefs['inspiration']} theme"
                return prompt
                

            # TODA 5
            @app.route("/genrate-image", methods=["POST"])
            def generate_image():
                data   = request.get json(silent=True) or {}
                prompt = data.get("image_prompt", "")
                if not prompt:
                    return jsonify({"error":"No image prompt."}), 400
                if not HF_API_KEY:
                   return jsonify({"error": "HF_API_KEY not configured."}), 503
                image_url = generate_sneaker_image(prompt)
                if not image_url:
                    return jsonify({"error": "Image generation failed. Try again."}), 500
                return jsonify({"success": True, "image_url": image_url})

                # TODO 6
                concept["image_prompt"] = build_image_prompt(prefs)
                // TODO 1
const showImgLoading = () => { imgLoading?.classList.remove('hidden'); imgFrame?.classList.add('hidden'); imgError?.classList.add('hidden'); regenImgBtn?.classList.add('hidden'); };

// TODO 2
  const showImgResult  = url => { imgLoading?.classList.add('hidden'); imgError?.classList.add('hidden'); if(aiImage) aiImage.src=url; imgFrame?.classList.remove('hidden'); regenImgBtn?.classList.remove('hidden'); };

// TODO 3
  const showImgError   = msg => { imgLoading?.classList.add('hidden'); imgFrame?.classList.add('hidden'); if(imgErrorText) imgErrorText.textContent=msg||'Image generation failed.'; imgError?.classList.remove('hidden'); regenImgBtn?.classList.remove('hidden'); };


// TODO 4
const fetchImage = async prompt => {
    setStage('hf'); showImgLoading();
    try {
      const r = await fetch('/generate-image',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({image_prompt:prompt})});
      const d = await r.json();
      if (!r.ok||d.error) throw new Error(d.error||'Image generation failed');
      showImgResult(d.image_url);
    } catch(e) { showImgError(e.message); }
  };


// TODO 5
const runGeneration = async token => {
    const prefs = collectPrefs();
    generateBtn.disabled = true;
    setUI('loading'); setStage('groq'); startLoader();
    try {
      const r = await fetch('/generate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({...prefs,'h-captcha-response':token})});
      const d = await r.json();
      if (!r.ok||d.error) throw new Error(d.error||'Server error');
      stopLoader(); renderConcept(d.concept); setUI('result');
      fetchImage(d.concept.image_prompt || `Premium ${prefs.style} sneaker, ${prefs.material}, studio photography, 8k`);
    } catch(e) {
      stopLoader(); setUI('empty'); formError.textContent = e.message||'Something went wrong.';
    } finally {
      generateBtn.disabled = false;
      if (typeof hcaptcha!=='undefined' && captchaWidgetId!==null) hcaptcha.reset(captchaWidgetId);
    }
  };
# TODA 1
def builld_image_prompt(prefs):
    p = hex_to_color_name(prefs["primary_color"])
    a = hex_to_color_name(prefs["accent_color"])
    prompt = (f"Professional product photography of a {prefs['style']} sneaker, "
              f"{p} {prefs['material']} upper,{a} accent, {a} heel, white sole, "
              f"side view, white background, sharp focus, 8k, shoe only")
    if prefs.get("inspiration"):
        prompt += f", {prefs["inspiration"]} theme"
    return prompt
    // TODA 2
   const selectColorway = idx => {
      colorwayTabs.querySelectorAll('.cw-tab').forEach((t,i) => t.classList.toggle('active',i=idx));
      applyColorway(currentColorways[idx], sneakerStage);
      colorwayInfo.innerHTML = [['Upper',currentColorways[idx].upper],
                                ['Sole',currentColor[idx].sole],
                                ['Accent',currentColorways[idx].accent],['Lace',currentColorways[idx].lace],['Tongue',currentColorways[idx].tongue]]
                                .map(([l,c])=> <div class="cw-color-item"><div class="cw-dot" style="background:${c}"></div>${l}: <strong style="color:var(--text)">${c}</strong> </div>).join('');
                             };


                             // TODA 3
                             const buildColorwayTabs = cws => {
                                colorwayTabs.innerHTML = '';
                                cws.forEach((cw,i) => {
                                  const btn = document.createElement('button');
                                  btn.className = 'cw-tabs' + (i===0?' active':'');
                                });
                             };


                             // TODA 4
                             if (currentColorways.length) { buildColorwayTabs(currentColorways): selectColorway(0): }

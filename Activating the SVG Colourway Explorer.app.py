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
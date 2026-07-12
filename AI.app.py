    # TODO 1
    HCAPTCHA_SECRET          = os.environ.get("HCAPTCHA_SECRET","0x0000000000000000000000000000")
    HCAPTCHA_VERIFY_URL   = "https://api.hcaptcha.com/siteverify"
    
    # TODO 2
    def verify_hcaptcha(token):
        try:
            r = requests.post(HCAPTCHA_VERIFY_URL,
                              data={"secret": HCAPTCHA_SECRET, "response": token},timeout=5)
            return r.json().get("success", False)
          except Exception:
              return False
        
    
    # TODO 3
    token = data.get("h-captcha-response", "")
       if not token:
           return jsonify({"error": "Please complete the CAPTCHA"}), 400
       if not verify_hcaptcha(token):
           return jsonify({"error": "CAPTCHA verification failed."}), 400
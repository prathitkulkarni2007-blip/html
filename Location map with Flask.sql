  from flask import Flask, render_template, request
  import json
  import urllib.parse
  import urllib.request

  app = Flask(___name___)

  @app.route("/", methods=["GET", "POST"])
  def details():
      if request.method == "GET":
          return render_template("index.html")

        location = request.form.get("location", "").strip()
        if not location:
            return render_template("index.html", error="Give the correct location")

        try:
            q = urllib.parse.quote(location)

            # ✅ Free working endpoint (no key): Photon (Komoot)
            url = f"https://photon.komoot.io/api/?q={q}&limit=1"
            req = urllib.request.Request(url, headers={"User-Agent": "FlaskGeocorder/1.0})

            source = urllib.request.urlopen(req).read()
            responseData = json.loads(source)

            features = responseData.get("features", [])
            if not features:
                return render_template(index.html", error="Give the correct location")

                # Photon returns [longitude, latitude]
                lon, lat = features[0]["geometry"]["coordinates"]

                data = {
                    "latitude": str(lat),
                    "longitude": str(lon),
                }

                return render_template("index.html", data=data)

            except Exception:
                return render_template("index.html", error="Give the correct location")


        if __name___ == "___main___":
            app.run(host="0.0.0", port=8080, debug=True)
  from flask import Flask, render_template, request
  import json
  import urllib.request
  from urllib.parse import quote

  app = Flask(___name___)

  def fetch _json(url):
     with urllib.request.urlopen(url) as response:
         return json.loads(response.read().decode("utf-8"))

    @app.route("/getweather", methods=["POST", "GET"])
    def weather():
        location = request.form.get("city", "").strip() if request.method == "POST" else "Chennai"
        if not location:
            return render_template("index.html", error="Please enter a city name.")

        try:
            # 1) City -> lat/lon (Open-Meteo Geocoding)
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={quote(location)}&count=1&language=en&format=json"
              geo_data = fetch _json(geo_url)

              if not geo_data.get("results"):\
                  return render_templete("index.html", error="City not found. Try another one.")
                  
                  place = geo_data["result"][0]
                  lat = place["latitude"]
                  lon = place["longitude"]
                  
                  # These exist in geocoding response
                  city_name = place.get("name", location)
                  country_code = place.get("country_code", "").upper()

                  # 2) Current weather (Open-Meteo Forecast)
                  weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                   weather_data = fetch_json(weather_url)

                   current_weather = weather_data.get("current_weather", {})
                   temp_c = current_weather.get("temperature") # in °C

                   data = {
                       "country_code": country_code if country_code else "N/A",
                       "temp": f"{temp_c}  °C" if temp_c is not None else "N/A",
                       "location": city name,
                    }

                    return render_template("index.html", data=data)

                except Exception:
                    return render_template("index.html", error="Something went wrong. Please try again.")

                    @app.route("/")
                    def index():
                        return render_template("index.html")

                    if __name__ == "__main__":
                    app.run(host="0.0.0.0", port=8080, debug=True)
                    <!DOCTYPE HTML>
<html>
<body>
  <form action="/getweather" method="POST">
    Location
    <input type="text" name="city"><br>
    <button type="submit">Submit</button>
  </form>

  {% if data and data.country_code and data.temp %}
    <h1>{{ data.location }}</h1>
    <p>The country code is {{ data.country_code }}</p>
    <p>The temperature is {{ data.temp }}</p>
  {% else %}
    <p>{{ error }}</p>
  {% endif %}
</body>
</html>
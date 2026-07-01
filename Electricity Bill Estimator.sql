   from flask import Flask, render_template, request

   app = Flask(___name___)

   @app.route("/")
   def home():
       return render_template("index.html")

    @app.route("/calculate", methods=["POST"])
    def calculate():
        units = int(request.form["units"])
        bill = units * 5

        if units <= 100:
            message = "Great! You are an energy saver! 🌱"
      elif units <= 200:
        message = "Not bad! Try saving a little more! 👍"
      else:
        message = "Whoa! Time to switch off some lights! 💡"

    return render_template("index.html", units=units, bill=bill, message=message)

  if  __name__  == " __main___ ":
       app.run(debug=True) 
<!DOCTYPE html>
 <html lang="en">
 <head>
    <meta charset="UTF-8">
    <title>⚡ Electricity Bill Estimator</title>
    <link rel="stylesheet" href="/static/style.css">
  </head>
  <body>

  <h1>⚡ Electricity Bill Estimator</h1>
  <p>Enter your monthly units to find out your bill!</p>

  <form action="/calculate" method="POST">
      <label>🔌 Units Consumed:</label>
        <input type="number" name="units" placeholder="e.g. 150" required>
        <button type="submit">Calculate 💡</button>
    </form>

    {% if bill %}
    <div class="result">
        <h2>Units Used: {{ units }} kWh</h2>
        <h2>Total Bill: ₹ {{ bill }}</h2>
        <p>{{ message }}</p>
    </div>
    {% endif %}

</body>
</html>

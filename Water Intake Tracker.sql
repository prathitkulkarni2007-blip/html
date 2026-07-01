from flask import Flask, render_template, request
 
app = Flask(__name__)
 
 
@app.route("/")
def home():
    return render_template("index.html")
 
 
@app.route("/track", methods=["POST"])
def track_water():
    # Handling form data with request
    name = request.form["name"]
    goal = int(request.form["goal"])
    glasses = int(request.form["glasses"])
 
    remaining = goal - glasses
 
    if glasses >= goal:
        message = "Great job! You reached your water intake goal today."
        status = "Goal completed"
        remaining = 0
    else:
        message = "Keep going! You still need to drink more water."
        status = "Goal not completed"
 
    # Passing data to the HTML template using Jinja2
    return render_template(
        "index.html",
        name=name,
        goal=goal,
        glasses=glasses,
        remaining=remaining,
        message=message,
        status=status
    )
 
 
if __name__ == "__main__":
    app.run(debug=True)
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Water Intake Tracker</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
 
  <div class="container">
 
    <h1>Water Intake Tracker</h1>
 
    <p>
      Enter your daily water goal and check whether you drank enough water today.
    </p>
 
    <form action="/track" method="POST">
 
      <label>Your Name:</label>
      <input type="text" name="name" placeholder="Enter your name" required>
 
      <label>Daily Goal:</label>
      <input type="number" name="goal" placeholder="Number of glasses" required>
 
      <label>Glasses Drunk:</label>
      <input type="number" name="glasses" placeholder="Glasses you drank" required>
 
      <button type="submit">Check Water Intake</button>
 
    </form>
 
    {% if name %}
    <div class="result">
 
      <h2>Hello, {{ name }}!</h2>
 
      <p><strong>Daily Goal:</strong> {{ goal }} glasses</p>
      <p><strong>Glasses Drunk:</strong> {{ glasses }} glasses</p>
      <p><strong>Status:</strong> {{ status }}</p>
 
      {% if remaining > 0 %}
        <p><strong>Remaining:</strong> {{ remaining }} more glasses to go.</p>
      {% else %}
        <p><strong>Remaining:</strong> 0 glasses. You completed your goal!</p>
      {% endif %}
 
      <h3>{{ message }}</h3>
 
    </div>
    {% endif %}
 
  </div>
 
</body>
</html>
body {
  font-family: Arial, sans-serif;
  background-color: #e0f7fa;
  color: #003344;
  text-align: center;
}
 
.container {
  width: 500px;
  background-color: white;
  border: 3px solid #00acc1;
  border-radius: 18px;
  margin: 40px auto;
  padding: 25px;
}
 
h1 {
  color: #00838f;
}
 
form {
  text-align: left;
}
 
label {
  display: block;
  font-weight: bold;
  margin-top: 15px;
}
 
input {
  width: 95%;
  padding: 10px;
  margin-top: 6px;
  border: 2px solid #80deea;
  border-radius: 8px;
}
 
button {
  background-color: #00acc1;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 12px 22px;
  font-size: 16px;
  font-weight: bold;
  margin-top: 20px;
  cursor: pointer;
}
 
button:hover {
  background-color: #00838f;
}
 
.result {
  background-color: #e0f2f1;
  border: 2px dashed #00acc1;
  border-radius: 12px;
  margin-top: 25px;
  padding: 15px;
  text-align: left;
}
 
.result h2,
.result h3 {
  color: #006064;
}   
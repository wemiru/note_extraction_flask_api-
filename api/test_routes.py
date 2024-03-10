from __main__ import app

# Greeting route
@app.route("/greet")
def greet():
    return "Hello"
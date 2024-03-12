from __main__ import app
from flask import render_template

# Render Template 
@app.route("/")
def index_page():
    return render_template('index.html')

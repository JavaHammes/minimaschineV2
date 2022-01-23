from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

code_input = ""

@app.route("/")
def home():
    return render_template(
        "index.html"
    )

@app.route("/submit", methods=["POST"])
def submit():
    code_input = request.form['text']
    return 'You entered: {}'.format(code_input)


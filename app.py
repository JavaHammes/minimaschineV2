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
    global code_input 
    code_input = request.form['text']
    code_input += "hallo"
    print(code_input)
    return 'You entered: {}'.format(code_input)


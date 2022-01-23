from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

# +++++ VARIABLES +++++

code_input = ""

# +++++ METHODS +++++

def ConvertListToDict(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

# +++++ FLASK METHODS +++++

@app.route("/")
def home():
    return render_template(
        "index.html"
    )

@app.route("/submit", methods=["POST"])
def submit():
    code_input = ConvertListToDict(request.form['text'].split())
    print(code_input)
    return render_template(
        "index.html"
    )


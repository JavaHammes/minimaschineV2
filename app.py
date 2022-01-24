from flask import Flask
from flask import render_template
from flask import request

from ilex import Ilex

app = Flask(__name__)

# +++++ VARIABLES +++++

code_input = ""
ilex = Ilex()

# +++++ METHODS +++++



# +++++ FLASK METHODS +++++

@app.route("/")
def home():
    return render_template(
        "index.html"
    )

@app.route("/submit", methods=["POST"])
def submit():

    commands = ilex.convert_list_to_commands(request.form['text'].split())

    ilex.init_commands(commands)

    value = ilex.return_commands_readable()
    value.append(ilex.check_valid())

    return render_template(
        "index.html",
        value = value
    )

from atexit import register
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

    reg_1 = 0000000000000000
    reg_2 = 0000000000000000
    reg_3 = 0000000000000000
    reg_4 = 0000000000000000
    reg_5 = 0000000000000000
    reg_6 = 0000000000000000
    reg_7 = 0000000000000000
    reg_8 = 0000000000000000

    ov = 0
    zr = 0
    sf = 0
    pf = 0


    return render_template(
        "index.html",
        value = value,
        reg_1 = reg_1,
        reg_2 = reg_2,
        reg_3 = reg_3,
        reg_4 = reg_4,
        reg_5 = reg_5,
        reg_6 = reg_6,
        reg_7 = reg_7,
        reg_8 = reg_8,
        ov = ov,
        zr = zr,
        sf = sf,
        pf = pf
    )

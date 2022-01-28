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

    programmcounter = ilex.get_programmzähler()
    akkumulator = ilex.get_akkumulator()
    befehleregister_key = ilex.get_befehlsregister_key()
    befehleregister_value = ilex.get_befehlsregister_value()
    
    reg_1 = ilex.get_reg_1()
    reg_2 = ilex.get_reg_2()
    reg_3 = ilex.get_reg_3()
    reg_4 = ilex.get_reg_4()
    reg_5 = ilex.get_reg_5()
    reg_6 = ilex.get_reg_6()
    reg_7 = ilex.get_reg_7()
    reg_8 = ilex.get_reg_8()

    ov = ilex.get_ov()
    zr = ilex.get_zr()
    sf = ilex.get_sf()
    pf = ilex.get_pf()


    return render_template(
        "index.html",
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

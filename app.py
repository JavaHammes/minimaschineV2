import os
from flask import Flask
from flask import render_template
from flask import request

from ilex import Ilex

app = Flask(__name__)

# +++++ VARIABLES +++++

code_input = ""
ilex = Ilex()

# +++++ FLASK METHODS +++++

@app.route("/")
def home():
    return render_template(
        "index.html"
    )

@app.route("/submit", methods=["POST"])
def submit():

    code_input = os.linesep.join([s for s in request.form['text'].splitlines() if s]).lstrip()

    commands = ilex.convert_list_to_commands(request.form['text'].split())
    ilex.init_commands(commands)

    try:
        ilex.run_code(False)
    except Exception:
        ilex.set_every_value(500)

    regs = ilex.get_regs()

    programmzähler = ilex.get_programmzähler() + 1
    akkumulator = ilex.get_akkumulator()
    befehlsregister_key = ilex.get_befehlsregister_key()
    befehlsregister_value = ilex.get_befehlsregister_value()

    ov = ilex.get_ov()
    zr = ilex.get_zr()
    sf = ilex.get_sf()
    pf = ilex.get_pf()

    return render_template(
        "index.html",
        code_input = code_input,
        reg_1 = regs[0],
        reg_2 = regs[1],
        reg_3 = regs[2],
        reg_4 = regs[3],
        reg_5 = regs[4],
        reg_6 = regs[5],
        reg_7 = regs[6],
        reg_8 = regs[7],
        ov = ov,
        zr = zr,
        sf = sf,
        pf = pf,
        programmzähler = programmzähler,
        akkumulator = akkumulator,
        befehlsregister_key = befehlsregister_key,
        befehlsregister_value = befehlsregister_value
    )

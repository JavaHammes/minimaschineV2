import os
from flask import Flask
from flask import render_template
from flask import request

from ilex import Ilex

app = Flask(__name__)

# +++++ VARIABLES +++++

code_input = ""
ilex = Ilex()

# +++++ METHODS +++++

def to_number(bin16):
    if str(bin16)[0] == "0":
        try:
            return int(str(bin16)[str(bin16).find("1"):], 2)
        except ValueError:
            return bin16
    else:
        try:
            bin16_pos = str(bin16)[1:]
            return -int(bin16_pos[bin16_pos.find("1"):], 2)
        except:
            return bin16


# +++++ FLASK METHODS +++++

@app.route("/")
def home():
    return render_template(
        "index.html"
    )

@app.route("/submit", methods=["POST"])
def submit():
    #try:
    code_input = os.linesep.join([s for s in request.form['text'].splitlines() if s]).lstrip()

    if not code_input:
        return render_template(
            "index.html"
        )
    
    commands = ilex.convert_list_to_commands(request.form['text'].split())

    if request.form['submit_button'] == "Ausführen":
        #try:
            ilex.init_commands(commands, False)
            ilex.run_code(False)
        #except Exception:
            #ilex.set_every_value(500)
    elif request.form['submit_button'] == "Einzelschritt":
        #try:
            ilex.init_commands(commands, True)
            ilex.run_code(True)
        #except Exception:
            #ilex.set_every_value(500)
    elif request.form['submit_button'] == "Reset":
            ilex.set_every_value(0)

    regs = ilex.get_regs()

    programmzähler = ilex.get_programmzähler()
    akkumulator = ilex.get_akkumulator()
    befehlsregister_key = ilex.get_befehlsregister_key()
    befehlsregister_value = ilex.get_befehlsregister_value()

    ov = ilex.get_ov()
    zr = ilex.get_zr()
    sf = ilex.get_sf()
    pf = ilex.get_pf()

    reg_1_numeric = to_number(regs[0])
    reg_2_numeric = to_number(regs[1])
    reg_3_numeric = to_number(regs[2])
    reg_4_numeric = to_number(regs[3])
    reg_5_numeric = to_number(regs[4])
    reg_6_numeric = to_number(regs[5])
    reg_7_numeric = to_number(regs[6])
    reg_8_numeric = to_number(regs[7])
    #except Exception:
        #ilex.set_every_value(500)

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
        reg_1_numeric = reg_1_numeric,
        reg_2_numeric = reg_2_numeric,
        reg_3_numeric = reg_3_numeric,
        reg_4_numeric = reg_4_numeric,
        reg_5_numeric = reg_5_numeric,
        reg_6_numeric = reg_6_numeric,
        reg_7_numeric = reg_7_numeric,
        reg_8_numeric = reg_8_numeric,
        ov = ov,
        zr = zr,
        sf = sf,
        pf = pf,
        programmzähler = programmzähler,
        akkumulator = akkumulator,
        befehlsregister_key = befehlsregister_key,
        befehlsregister_value = befehlsregister_value
    )

@app.route("/befehle")
def befehle():
    return render_template (
        "befehle.html"
    )

@app.route("/errors")
def errors():
    return render_template (
        "errors.html"
    )

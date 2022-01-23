from flask import Flask
from flask import render_template
from flask import request
from command import Command

app = Flask(__name__)

# +++++ VARIABLES +++++

code_input = ""

# +++++ METHODS +++++

def ConvertListToCommands(lst):
    res_lst = list()
    
    if len(lst) < 2:
        res_lst.append(Command("ERROR", "403"))
        return res_lst

    i = 0
    while i < len(lst):
        if ":" in lst[i]:
            res_lst.append(Command(lst[i], "METHOD"))
            i += 1
        elif "HOLD" in lst[i]:
            res_lst.append(Command(lst[i], "END"))
            if i is not len(lst)-1:
                res_lst.append(Command("ERROR", "404"))
            return res_lst
        elif "#" in lst[i]:
            while i < len(lst):
                i += 1
                if "#" in lst[i]:
                    i += 1
                    break
        else:
            res_lst.append(Command(lst[i], lst[i+1]))        
            i += 2
    
    return res_lst


# +++++ FLASK METHODS +++++

@app.route("/")
def home():
    return render_template(
        "index.html"
    )

@app.route("/submit", methods=["POST"])
def submit():
    code_input = ConvertListToCommands(request.form['text'].split())



    readable_out = list(i.get() for i in code_input)


    return render_template(
        "index.html",
        value = readable_out
    )

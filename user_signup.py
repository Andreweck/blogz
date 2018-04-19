from flask import Flask, request, redirect, render_template
import cgi
app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/fll", methods=["POST"])
def frmfrm():
    un = request.form['usrnme']
    pw = request.form['psswd']
    cpw = request.form['confm_psswd']
    emm = request.form['eml']
    gg = ""
    if len(subject) == 0:
        gg = gg + "U"
    if len(content) == 0:
        gg = gg + "P" 
    if len(gg) > 0:
        rgb = str(gg)
        nam = ['','']
        if 'U' in rgb:
            nam[0] = "Please title this blogpost."

        if 'P' in rgb:
            nam[1] = "Please give us content."

        return render_template('newpost.html', str(nam[0]), str(nam[1]))
        
        
        
        #return redirect("/error")
    else:
        return redirect("/scss?usrnme={u}".format(u = un))
    

@app.route("/scss")
def scss():
    usrnme = request.args.get('usrnme')
    return render_template('welcome.html', usrnme=str(usrnme))

@app.route("/")
def index():
   # template = jinja_env.get_template('index.html')
    usrnme = request.args.get('usrnme')
    email = request.args.get('eml')
    return render_template('home.html', f="", s="", t="", sm="", ufld="", efld="")


app.run()

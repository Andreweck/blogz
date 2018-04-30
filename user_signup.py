
@app.route("/fll", methods=["POST"])
def frmfrm():
    un = request.form['usrnme']
    pw = request.form['psswd']
    cpw = request.form['confm_psswd']
    emm = request.form['eml']
    gg = ""
    if len(un) >= 3 and len(un) <= 20:
        for j in un:
            if j == " ":
                gg = gg + "U"
    else: 
        gg = gg + "U"
    if len(pw) >= 3 and len(pw) <= 20:
        for u in pw:
            if u == " ":
                break
                gg = gg + "P" 
        
        if pw != cpw:
            gg = gg + "C"
    else:
        gg = gg + "CP"
    if len(emm) > 0:
        if "@" in emm and "." in emm and len(emm) >= 3 and len(emm) <= 20:
            gg = gg
        else: #"@" not in emm:
            gg = gg + "E"
    else:
        gg = gg + "E"
   
    
    if len(gg) > 0:
        rgb = str(gg)
        nam = ['','','','']
        if 'U' in rgb:
            nam[0] = "This is not a valid username."

        if 'P' in rgb:
            nam[1] = "This is not a valid password."

        if 'C' in rgb:
            nam[2] = "These passwords do NOT match!"
        if 'E' in rgb:
            nam[3] = "That is not a valid email" 

        return render_template('register.html', f=str(nam[0]), s=str(nam[1]), t=str(nam[2]), sm=str(nam[3]), ufld=un, efld=emm)
        
        
        
        #return redirect("/error")
    else:
        emailcount = User.query.filter_by(email = emm).count()
        usercount = User.query.filter_by(name = un).count()
        if emailcount + usercount > 0:
            err_list = ['', '']
            if emailcount > 0:
                err_list[0]= "This email address already exists."
            if usercount > 0:
                err_list[1] = "This username already exists."
            return render_template('register.html', f= str(err_list[0]), sm=str(err_list[1]), ufld=un, efld=emm)
        else:
            new_user = User(name = un, password = pw, email = emm)
            db.session.add(new_user)
            db.sessopn.commit()
            session['user'] = user.email
            return redirect("/newpost?usrnme={u}".format(u = un))
@app.route("/login")
    def login():
        usrnme = request.args.get('usrnme')
        return render_template('login.html')
@app.route("/login_confirmation", methods = ["GET", "POST"])
def login_confirmation():
    un = request.form['usrnme']
    pw = request.form['psswd']
    emm = request.form['eml']
    name = User.query.filter_by(name = un)
    if name.count() == 0:
        return render_template('login.html', error = "Invalid username or password") 
    else:
        user = name.first()
        if pw =! user.password:
            return render_template('login.html', error = "Invalid username or password")
        else:
            session['user'] = user.name
            return redirect("/newpost")

@app.route("/logout", methods=['POST'])
def logout():
    del session['user']
    return redirect("/")

@app.route("/register")
def index():
    usrnme = request.args.get('usrnme')
    email = request.args.get('eml')
    return render_template('register.html', f="", s="", t="", sm="", ufld="", efld="")




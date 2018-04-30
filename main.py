from flask import Flask, request, render_template, session, flash, redirect
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'Drxwy_jdg25543'

class entry(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    post_entry = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, post_entry):
        self.name = name
        self.post_entry = post_entry
        self.user = user 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    password = db.Column(db.String(120))
    email = db.Column(db.String(120))
    
    blogs = db.relationship('entry', backref='user')#, lazy=True)
    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email
        
   # def __repr__(self):
@app.before_request
def require_login():
    routes = ['index', 'register', 'blog_posts', 'login', 'login_confirmation']
    if 'name' not in session:
        if request.endpoint not in routes:
            return redirect("/login")   #    return '<User %r>' % self.name
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
            db.session.commit()
            session['name'] = new_user.name
            return redirect("/newpost?usrnme={u}".format(u = un))
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        un = request.form['usrnme']
        pw = request.form['psswd']
        name = User.query.filter_by(name = un).all()
        if name == None:
            return render_template('login.html', error = "Invalid username or password") 
        else:
            user = name
            if pw != user[0].password:
                return render_template('login.html', error = "Invalid username or password")
            else:
                
                session['name'] = user[0].name
                return redirect("/newpost")
    return render_template("login.html")
@app.route("/logout", methods=['GET'])
def logout():
    del session['name']
    return redirect("/")

@app.route("/register")
def register():
    usrnme = request.args.get('usrnme')
    email = request.args.get('eml')
    return render_template('register.html', f="", s="", t="", sm="", ufld="", efld="")
@app.route("/newpost")
def newpost():
    post_name = request.args.get('post_name')
    entry = request.args.get('entry')
    return render_template('newpost.html', c = '', o = '')
@app.route("/submitted_form", methods=['POST'])
def submitted_form():
    subject = request.form['post_name']
    content = request.form['entry']
    error_string = ""
    #error_string = gg
    if len(subject) == 0:
        error_string = error_string + "U"
    if len(content) == 0:
        error_string = error_string + "P" 
    if len(gg) > 0:
        error_string_2 = str(error_string)
        #error_string_2 = rgb
        nam = ['','']
        if 'U' in error_string_2:
            nam[0] = "Please title this blogpost."

        if 'P' in error_string_2:
            nam[1] = "Please give us content."

        return render_template('newpost.html', c = str(nam[0]), o = str(nam[1]))
    elif len(error_string) == 0:
        new_blog = entry(name = subject, post_entry = content)#, user = )
        db.session.add(new_blog)
        db.session.commit()
        dd = entry.query.filter_by(name=subject).first()
        da = dd.id
           # dbs = dd[-1].id()
        return redirect("/blog?id={i}".format(i = da))



@app.route("/blog")
def blog():
    title = request.args.get('id')
    id_num = int(title)
    post = entry.query.get(id_num)
    return render_template('viewpost.html', post_heading=post.name, post_content=post.post_entry)


@app.route("/blogposts", methods=["POST", "GET"])
def blogposts():
    tbl_qry = entry.query.all()
    #if len(tbl_qry) == 0:
     #   return render_template('home.html', posts = "There are no posts as of yet")

   
    return render_template('blogposts.html', tbl_qry = tbl_qry)
@app.route("/")
def index():
    usr_qry = User.query.all()
    return render_template('index.html', usr_qry = usr_qry)


if __name__ == "__main__":
    app.run()

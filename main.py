from flask import Flask, request, render_template, session, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import hashlib



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

    def __init__(self, name, post_entry, user_id):
        self.name = name
        self.post_entry = post_entry
        self.user = user_id 
        
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    password = db.Column(db.String(120))
    email = db.Column(db.String(120))
    
    blogs = db.relationship('entry', backref='user', lazy="select")
    def __init__(self, name, password, email, blogs):
        self.name = name
        self.password = hash(password)
        self.email = email
        self.blogs = blogs
   # def __repr__(self):

def hash(pw):
    return hashlib.sha256(str.encode(pw)).hexdigest()

@app.before_request
def require_login():
    routes = ['index', 'register', 'blogposts', 'login', 'login_confirmation', 'profile']
    if 'name' not in session:
        if request.endpoint not in routes:
            return redirect("/login")   #    return '<User %r>' % self.name
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        un = request.form['usrnme']
        pw = request.form['psswd']
        name = User.query.filter_by(name = un).all()
        if len(name) == 0:
            return render_template('login.html', error = "Invalid username or password") 
        else:
            user = name
            if hash(pw) != user[0].password:
                return render_template('login.html', error = "Invalid username or password")
            else:
                
                session['name'] = user[0].name
                return redirect("/newpost")
    return render_template("login.html")
@app.route("/logout", methods=['GET'])
def logout():
    del session['name']
    return redirect("/")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        un = request.form['usrnme']
        pw = request.form['psswd']
        cpw = request.form['confm_psswd']
        emm = request.form['eml']
        error_string = ""
        if len(un) >= 3 and len(un) <= 20:
            for j in un:
                if j == " ":
                    error_string = error_string + "U"
        else: 
            error_string = error_string + "U"
        if len(pw) >= 3 and len(pw) <= 20:
            for u in pw:
                if u == " ":
                    break
                    error_string = error_string + "P" 

            if pw != cpw:
                error_string = error_string + "C"
        else:
            error_string = error_string + "CP"
        if len(emm) > 0:
            if "@" in emm and "." in emm and len(emm) >= 3 and len(emm) <= 20:
                error_string = error_string
            else: #"@" not in emm:
                error_string = error_string + "E"
        else:
            error_string = error_string + "E"
    
    
        if len(error_string) > 0:
            rgb = str(error_string)
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
            emailcount = User.query.filter_by(email = emm).all()
            usercount = User.query.filter_by(name = un).all()
            if len(emailcount) != 0 or len(usercount) != 0:
                err_list = ['', '']
                if usercount != None:
                    err_list[0] = "This username already exists."
                if emailcount != None:
                    err_list[1]= "This email address already exists."
                return render_template('register.html', f= str(err_list[0]), sm=str(err_list[1]), ufld=un, efld=emm)
            else:
                new_user = User(name = un, password = pw, email = emm, blogs = [])
                db.session.add(new_user)
                db.session.commit()
                session['name'] = new_user.name
                return redirect("/newpost?usrnme={u}".format(u = un))
    return render_template('register.html', f="", s="", t="", sm="", ufld="", efld="")
@app.route("/newpost")
def newpost():
    post_name = request.args.get('post_name')
    entry = request.args.get('entry')
    return render_template('newpost.html', c = '', o = '')
@app.route("/submitted_form", methods=['POST'])
def submitted_form():
    print()
    print(session['name'])
    print()
    subject = request.form['post_name']
    content = request.form['entry']
    error_string = ""
        #error_string = error_string
    if len(subject) == 0:
        error_string = error_string + "U"
    if len(content) == 0:
        error_string = error_string + "P" 
    if len(error_string) > 0:
        error_string_2 = str(error_string)
        #error_string_2 = rgb
        nam = ['','']
        if 'U' in error_string_2:
            nam[0] = "Please title this blogpost."

        if 'P' in error_string_2:
            nam[1] = "Please give us content."

        return render_template('newpost.html', c = str(nam[0]), o = str(nam[1]))
    elif len(error_string) == 0:
        user = User.query.filter_by(name = session['name']).first()
        new_blog = entry(name = subject, post_entry = content, user_id = user)#, user = )
        db.session.add(new_blog)
        db.session.commit()
        dd = entry.query.filter_by(name=subject).first()
        da = dd.id
               # dbs = dd[-1].id()
        return redirect("/blog?id={i}".format(i = da))

@app.route("/profile")
def profile():
    title = request.args.get('id')
    id_num = int(title)
    user = User.query.get(id_num)
    tbl_qry = entry.query.filter_by(user_id = id_num).all()
    return render_template('profile.html', name = user.name, tbl_qry = tbl_qry, usr = user.name) 
@app.route("/blog")
def blog():
    use = User.query.all()
    user = User.query.filter_by(name = session['name']).first()
    plc_hldr = user.id - 1
    user_2 = use[plc_hldr].name
    user_3 = use[plc_hldr].id
    title = request.args.get('id')
    id_num = int(title)
    post = entry.query.get(id_num)
    return render_template('viewpost.html', post_heading=post.name, post_content=post.post_entry, user=user_2, id = user_3)


@app.route("/blog_posts")
def blogposts():
    tbl_qry = entry.query.all()
    #user_querry = []
    #ph = 0
    #for i in range(len(tbl_qry)):
    #    pq = tbl_qry[ph].user.name
    #    user_querry.append(pq)
    #    ph += 1

    return render_template('blogposts.html', tbl_qry = tbl_qry)#, usr_qry = user_querry)
@app.route("/")
def index():
    usr_qry = User.query.all()
    return render_template('index.html', usr_qry = usr_qry)


if __name__ == "__main__":
    app.run()

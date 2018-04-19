from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class entry(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    post_entry = db.Column(db.String(120))

    def __init__(self, name, post_entry):
        self.name = name
        self.post_entry = post_entry
@app.route("/newpost", methods=["POST"])
def newpost():
    subject = request.form['post_name']
    content = request.form['entry']
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
    elif len(gg) == 0:
        subject = request.form['post_name']
        content = request.form['entry']
        if len(subject) > 0:
            new_blog = entry(name = subject, post_entry = content)
            db.session.add(new_blog)
            db.session.commit()
            dd = build-a-blog.query.get_id(subject)
            return redirect("/blog?id={0}".format(dd))


#@app.route("/newpost")
#def newpost():
#    subject = request.args.get('post_name')
#    content = request.args.get('entry')
#    return render_template('newpost.html', '')
#    if request.method =='POST':
#        subject = request.form['post_name']
#        content = request.form['entry']
#        if len(subject) > 0:
#            new_blog = entry(name = subject, post_entry = content)
#            db.session.add(new_blog)
#            db.session.commit()
#            dd = build-a-blog.query.get(subject)
#            return redirect("/blog?id={0}".format(dd))
#        else:
#            return redirect

@app.route("/blog", methods=["POST"])
def viewpost():
    title = request.args.get['post_id']
    return render_template('viewpost.html', title = title, entry = entry)


@app.route("/", methods=["POST", "GET"])
def index():
    posts = []
    
    if request.method == 'POST':
        post = request.form['blogpost']
        if len(posts) < 10:
            posts.append(post)
        elif len(posts) >= 10:
            posts.append(post)
            first_post = posts[0]
            posts.remove(first_post)

    
    return render_template('home.html', posts = posts)

if __name__ == "__main__":
    app.run()

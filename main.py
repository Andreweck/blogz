from flask import Flask, request, render_template, session, flash, redirect
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
            

@app.route("/newpost")
def newpost():
    post_name = request.args.get('post_name')
    entry = request.args.get('entry')
    return render_template('newpost.html', c = '', o = '')
@app.route("/submitted_form", methods=['POST'])
def all_filled_out():
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

        return render_template('newpost.html', c = str(nam[0]), o = str(nam[1]))
    elif len(gg) == 0:
#        if len(subject) > 0:
        new_blog = entry(name = subject, post_entry = content)
        db.session.add(new_blog)
        db.session.commit()
        dd = entry.query.filter_by(name=subject).first()
        da = dd.id
           # dbs = dd[-1].id()
        return redirect("/blog?id={i}".format(i = da))



@app.route("/blog")
def viewpost():
    title = request.args.get('id')
    id_num = int(title)
    post = entry.query.get(id_num)
    return render_template('viewpost.html', post_heading=post.name, post_content=post.post_entry)


@app.route("/", methods=["POST", "GET"])
def index():
    tbl_qry = entry.query.all()
    #if len(tbl_qry) == 0:
     #   return render_template('home.html', posts = "There are no posts as of yet")
#    else:
 #       plc_lst = []
  #      posts = ['', '', '', '', '', '', '', '', '', '']
   #     links =['', '', '', '', '', '', '', '', '', '']
    #    plc_hldr = 0
     #   for i in range(len(tbl_qry)):
      #      posts[plc_hldr] = tbl_qry[plc_hldr].name
       #     links[plc_hldr] = tbl_qry[plc_hldr].id
        #    plc_hldr += 1
    
   
    return render_template('home.html', tbl_qry = tbl_qry)
            

if __name__ == "__main__":
    app.run()

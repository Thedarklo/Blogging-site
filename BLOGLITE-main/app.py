from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Rishabh_db.sqlite3'
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()


class Post(db.Model):
    __tablename__='post'
    post_id = db.Column(db.Integer, nullable = False, autoincrement = True, unique= True, primary_key = True)
    posttitle = db.Column(db.String, nullable = False)
    postdesc = db.Column(db.String, nullable = False)
    links = db.Column(db.String)
    username = db.Column(db.String, db.ForeignKey("user.username"),nullable=False)
    timestamp = db.Column(db.String)


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    username = db.Column(db.String, unique = True, nullable = False)
    email = db.Column(db.String, unique = True, nullable = False)
    fname = db.Column(db.String, nullable = False)
    lname = db.Column(db.String)
    password = db.Column(db.String, nullable = False)
    dob = db.Column(db.String, nullable = False)


class Following(db.Model):
    __tablename__='following'
    follow_id=db.Column(db.Integer, nullable = False, autoincrement = True, unique= True, primary_key = True)
    following = db.Column(db.String, db.ForeignKey("user.username"), nullable = False)
    follower = db.Column(db.String, db.ForeignKey("user.username"),nullable = False)


@app.route('/',methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username=request.form["username"]
        password=request.form["password"]
        #user = User.query.first()
        user = User.query.filter_by(username=username,password=password).first()
        if user is None:
            return render_template("auth_error.html") 
        else:
            return redirect("/"+username+"/home")



@app.route('/registration',methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    else:
        user=User(username=request.form["uname"],fname=request.form["fname"],lname=request.form["lname"],password=request.form["pass"],email=request.form["email"],dob=request.form["dob"])
        db.create_all()
        db.session.add(user)
        db.session.commit()
        return redirect("/")



@app.route('/<username>/home',methods=['GET'])
def home(username):
    if request.method == "GET":
        user = User.query.filter_by(username=username).first()
        post=Post.query.all()
        follow=[]
        follows=Following.query.filter_by(follower=username).all()
        for i in follows:
            follow+=[i.following]
        if len(post)==0:
            return render_template("no_post.html",users=user)
        else : 
            return render_template("feed.html",users=user,posts=post,follow=follow)



@app.route('/<username>/my_profile',methods=['GET','POST'])
def summary(username):
    if request.method=='GET':
        user = User.query.filter_by(username=username).first()
        posts = Post.query.filter_by(username=username).all()
        total_posts=len(posts)
        followers = Following.query.filter_by(follower=username).all()
        following = Following.query.filter_by(following=username).all()
        total_followers=len(followers)
        total_following=len(following)
        return render_template("profile.html",users=user,total_posts=total_posts,posts=posts,total_followers=total_followers,total_following=total_following)


@app.route('/<username>/update',methods=['GET','POST'])
def update_user(username):
    if request.method=='GET':
        user = User.query.filter_by(username=username).first()
        return render_template("update_user.html",users=user)
    elif request.method=='POST':
        user=User.query.filter_by(username=username).first()
        if request.form.get("fname")!='':
            user.fname=request.form.get("fname")
        if request.form.get("lname")!='':
            user.lname=request.form.get("lname")
        if request.form.get("email")!='':
            user.email=request.form.get("email")
        if request.form.get("pass")!='':
            user.password=request.form.get("pass")
        if request.form.get("dob")!='':
            user.dob=request.form.get("dob")
        db.session.commit()
        return redirect("/"+username+"/my_profile")



@app.route('/<username>/search',methods=['GET','POST'])
def search(username):
    if request.method=='GET':
        user = User.query.filter_by(username=username).first()
        return render_template("find.html",users=user)
    else:
        user = User.query.filter_by(username=username).first()
        search=request.form.get("search")
        result=User.query.filter(or_(User.username.like(search),User.fname.like(search),User.lname.like(search),User.username.like(search.capitalize()),User.fname.like(search.capitalize()),User.lname.like(search.capitalize()))).all()
        if user in result:
            result.remove(user)
        if len(result)==0:
            search=search.capitalize()
            return render_template("not_found.html",users=user,search=search)
        results,follow=[],[]
        for i in result:
            results+=[i.username]
        follows=Following.query.filter_by(follower=username).all()
        for i in follows:
            follow+=[i.following]
        return render_template("result.html",users=user,results=results,follow=follow)



@app.route('/<username>/new_post',methods=['GET','POST'])
def new_post(username):
    if request.method=='GET':
        user = User.query.filter_by(username=username).first()
        return render_template("create.html",users=user)
    if request.method=='POST':
        user = User.query.filter_by(username=username).first()
        post=Post(posttitle=request.form.get("pname"),postdesc=request.form.get("pdescription"),username=username,timestamp=str(datetime.datetime.now()).split()[0])
        db.session.add(post)
        db.session.commit()
        return redirect("/"+username+"/my_profile")




@app.route('/<username>/profile/<other_username>',methods=['GET','POST'])
def other_profile(username,other_username):
    if request.method=='GET':
        user=User.query.filter_by(username=username).first()
        posts = Post.query.filter_by(username=other_username).all()
        total_posts=len(posts)
        followers = Following.query.filter_by(follower=other_username).all()
        following = Following.query.filter_by(following=other_username).all()
        total_followers=len(followers)
        total_following=len(following)
        return render_template("friend.html",users=user,total_posts=total_posts,posts=posts,other_user_name=other_username,total_followers=total_followers,total_following=total_following)




@app.route('/<username>/delete/<post_id>',methods=['GET','POST'])
def delete(username,post_id):
    if request.method=='GET':
        post=Post.query.filter_by(post_id=post_id).first()
        db.session.delete(post)
        db.session.commit()
        return redirect("/"+username+"/my_profile")



@app.route('/<username>/update/<post_id>',methods=['GET','POST'])
def update(username,post_id):
    if request.method=='GET':
        user = User.query.filter_by(username=username).first()
        post=Post.query.filter_by(post_id=post_id).first()
        return render_template("change.html",users=user,post=post)
    elif request.method=='POST':
        post=Post.query.filter_by(post_id=post_id).first()
        if request.form.get("pname")!='':
            post.posttitle=request.form.get("pname")
        if request.form.get("pdescription")!='':
            post.postdesc=request.form.get("pdescription")
        post.timestamp=str(datetime.datetime.now()).split()[0]
        db.session.commit()
        return redirect("/"+username+"/my_profile")



@app.route('/<follower>/follow/<following>',methods=['GET','POST'])
def follow(following,follower):
    if request.method=='GET':
        follow=Following(following=following,follower=follower)
        db.session.add(follow)
        db.session.commit()
        return redirect('/'+follower+'/my_profile')



@app.route('/<follower>/unfollow/<following>',methods=['GET','POST'])
def unfollow(following,follower):
    if request.method=='GET':
        follow=Following.query.filter_by(following=following,follower=follower).first()
        db.session.delete(follow)
        db.session.commit()
        return redirect('/'+follower+'/my_profile')



#Entry Point
if __name__ == "__main__":
    app.debug=True
    app.run()

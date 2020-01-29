from flask import render_template, url_for, flash, redirect, request

from flaskblog import app, db, bcrypt

from flaskblog.forms import RegistrationForm, LoginForm , PostForm , AboutForm 

from flaskblog.models import User, Post , Intro

from flask_login import login_user, current_user, logout_user, login_required

from sqlalchemy import desc



@app.route("/")
def blog():
    posts=Post.query.filter_by(author=current_user)
    
    return render_template('home.html', posts=posts)

@app.route("/home")

def home():
    posts=Post.query.order_by(Post.date_posted.desc()).all()
   # Post.date_posted.desc()
#posts = session.query(Post).order_by(Post.date_posted).all()
    return render_template('home.html', posts=posts)





@app.route("/about")

def about():
    posts=Intro.query.filter_by(author=current_user)
    return render_template('about.html',posts=posts)



@app.route("/register", methods=['GET', 'POST'])

def register():

    if current_user.is_authenticated:

        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validated_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        db.session.add(user)

        db.session.commit()

        flash('Your account has been created! You are now able to log in', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)





@app.route("/login", methods=['GET', 'POST'])

def login():

    if current_user.is_authenticated:

        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):

            login_user(user, remember=form.remember.data)

            return redirect(url_for('home'))

        else:

            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)





@app.route("/logout")

def logout():

    logout_user()

    return redirect(url_for('home'))





@app.route("/account")

@login_required

def account():

    return render_template('account.html', title='Account')


@app.route("/post/new", methods=['GET', 'POST'])

@login_required

def new_post():

    form = PostForm()

    if form.validate_on_submit():
        post=Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')

        return redirect(url_for('home'))

    return render_template('create_post.html', title='New Post',form=form)


@app.route("/intro", methods=['GET', 'POST'])

@login_required

def describe():

    form = AboutForm()

    if form.validate_on_submit():
        post=Intro(name=form.name.data,description=form.description.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Information added!', 'success')

        return redirect(url_for('home'))

    return render_template('introduction.html', title='Introduction',form=form)

@app.route("/post/<int:post_id>")

def post(post_id):

    post = Post.query.get_or_404(post_id)

    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])

@login_required

def update_post(post_id):

    post = Post.query.get_or_404(post_id)

    if post.author != current_user:

        abort(403)

    form = PostForm()

    if form.validate_on_submit():

        post.title = form.title.data

        post.content = form.content.data

        db.session.commit()

        flash('Your post has been updated!', 'success')

        return redirect(url_for('post', post_id=post.id))

    elif request.method == 'GET':

        form.title.data = post.title

        form.content.data = post.content

    return render_template('create_post.html', title='Update Post',form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])

@login_required

def delete_post(post_id):

    post = Post.query.get_or_404(post_id)

    if post.author != current_user:

        abort(403)

    db.session.delete(post)

    db.session.commit()

    flash('Your post has been deleted!', 'success')

    return redirect(url_for('home'))

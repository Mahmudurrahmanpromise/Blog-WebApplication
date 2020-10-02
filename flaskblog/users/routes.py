from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route('/register', methods=["Get", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Account created!', "success")
        return redirect(url_for("users.login"))

    return render_template("register.html", title='register', form=form)


@users.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            print('login : next_page', next_page)
            # ternary conditon applied here. if true then left stat will execute neither right stat will be executed
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Login Unsuccessful! please check email and password", "danger")
    print("GET")
    return render_template("login.html", title='login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@users.route('/account', methods=["POST", "GET"])
# login_required decorator hosche ami jokon ai route a jabo tokon login required hoite hobe naile dukte dibena
# and amake __init__ file theke bole dite hobe login_required hole kon page a jaite hobe
# so oikhane theke ami login route a chole jabo jate login kore access korte pare account route a.
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your information has been updated", 'success')
        return redirect(url_for('users.account'))
    elif request.method == "GET":
        print("accountroute : get")
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    print("image_file: ", image_file)
    # print("accountroute :", image_file)
    return render_template("account.html", title="account", image_file=image_file, form=form)


@users.route('/user/<string:username>')
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    print(page)
    posts = Post.query.filter_by(author=user) \
        .order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=2)
    return render_template("user_posts.html", posts=posts, user=user)


@users.route('/reset_password', methods=["POST", "GET"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # print("reset_request: ", user)
        send_reset_email(user)
        flash("An email has been send with instructions to reset your password", 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='reset_password', form=form)


@users.route('/reset_password/<token>', methods=["POST", "GET"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_code(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash('Your password has been created! You are now able to log in', "success")
        return redirect(url_for("users.login"))
    return render_template('reset_token.html', title='reset_password', form=form)
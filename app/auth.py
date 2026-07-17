from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models import User
from app.forms import RegistrationForm, LoginForm


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("tasks.home"))

    form = RegistrationForm()

    if form.validate_on_submit():

        existing_user = User.query.filter(
            (User.username == form.username.data) |
            (User.email == form.email.data)
        ).first()

        if existing_user:
            flash("Username or email already exists.", "danger")
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(form.password.data)

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully!", "success")

        return redirect(url_for("auth.login"))

    return render_template(
        "register.html",
        form=form
    )


@auth.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("tasks.home"))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user and check_password_hash(
            user.password,
            form.password.data
        ):

            login_user(user)

            flash("Logged in successfully!", "success")

            return redirect(url_for("tasks.home"))

        flash("Invalid email or password.", "danger")

    return render_template(
        "login.html",
        form=form
    )


@auth.route("/logout")
def logout():

    logout_user()

    flash("You have been logged out.", "info")

    return redirect(url_for("auth.login"))
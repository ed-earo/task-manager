from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.extensions import db
from app.models import Task, User


main = Blueprint("main", __name__)


@main.route("/")
@login_required
def home():
    tasks = Task.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "index.html",
        tasks=tasks
    )


@main.route("/add", methods=["POST"])
@login_required
def add_task():
    title = request.form.get("title")

    if title:
        task = Task(
            title=title,
            user_id=current_user.id
        )

        db.session.add(task)
        db.session.commit()

        flash("Task added successfully!", "success")

    return redirect(url_for("main.home"))


@main.route("/complete/<int:id>")
@login_required
def complete_task(id):
    task = Task.query.get_or_404(id)

    task.completed = not task.completed

    db.session.commit()

    flash("Task updated.", "success")

    return redirect(url_for("main.home"))


@main.route("/delete/<int:id>")
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    flash("Task deleted.", "danger")

    return redirect(url_for("main.home"))


@main.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully!", "success")

        return redirect(url_for("main.login"))

    return render_template("register.html")


@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            flash("Logged in successfully!", "success")

            return redirect(url_for("main.home"))

        else:

            flash("Invalid email or password.", "danger")


    return render_template("login.html")


@main.route("/logout")
def logout():

    logout_user()

    flash("You have been logged out.", "info")

    return redirect(url_for("main.login"))
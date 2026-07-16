from flask import Blueprint, render_template, request, redirect, url_for
from app.extensions import db
from app.models import Task


main = Blueprint("main", __name__)


@main.route("/")
def home():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)


@main.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")

    if title:
        task = Task(title=title)
        db.session.add(task)
        db.session.commit()

    return redirect(url_for("main.home"))
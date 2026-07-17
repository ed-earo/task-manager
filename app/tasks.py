from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Task

tasks = Blueprint("tasks", __name__)


@tasks.route("/")
@login_required
def home():
    tasks_list = Task.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "index.html",
        tasks=tasks_list
    )


@tasks.route("/add", methods=["POST"])
@login_required
def add_task():

    title = request.form.get("title", "").strip()

    if title:

        task = Task(
            title=title,
            user_id=current_user.id
        )

        db.session.add(task)
        db.session.commit()

        flash("Task added successfully!", "success")

    else:

        flash("Task cannot be empty.", "warning")

    return redirect(url_for("tasks.home"))


@tasks.route("/complete/<int:id>")
@login_required
def complete_task(id):

    task = Task.query.get_or_404(id)

    if task.user_id != current_user.id:
        flash("You are not allowed to modify this task.", "danger")
        return redirect(url_for("tasks.home"))

    task.completed = not task.completed

    db.session.commit()

    flash("Task updated.", "success")

    return redirect(url_for("tasks.home"))


@tasks.route("/delete/<int:id>")
@login_required
def delete_task(id):

    task = Task.query.get_or_404(id)

    if task.user_id != current_user.id:
        flash("You are not allowed to delete this task.", "danger")
        return redirect(url_for("tasks.home"))

    db.session.delete(task)
    db.session.commit()

    flash("Task deleted.", "info")

    return redirect(url_for("tasks.home"))
from flask import render_template, redirect, url_for, Blueprint, request, session, flash
from .models import Users
from . import db
from datetime import  datetime


login_blueprint = Blueprint("login", __name__)
dashboard_blueprint = Blueprint("dashboard", __name__)
logout_blueprint = Blueprint("logout", __name__)


@login_blueprint.route('/', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        joining_date = datetime.now()
        nickname = request.form['nickname']
        found_user = Users.query.filter_by(name=nickname).first()

        if not found_user:
            new_user = Users(name=nickname, join_date=joining_date)
            db.session.add(new_user)
            db.session.commit()
            session.update({"nick" : nickname, 'join_date': joining_date})

            flash("You've been successfully registered.", "success")
        else:
            right_now = datetime.now()
            registration_date = found_user.join_date
            time_difference_in_days = (right_now - registration_date).days
            session.update({"nick": nickname, "join_date": found_user.join_date})
            flash(f"Hello, {nickname}. You’re with us for {time_difference_in_days} days.", "success")

    elif request.method == "GET" and "nick" not in session:
        return render_template("login.html")
    elif request.method == "GET" and "nick" in session:
        flash("Already logged in!", "warning")

    return redirect(url_for("dashboard.dashboard"))


@logout_blueprint.route('/logout')
def logout():
    if "nick" in session:
        session.pop("nick", None)
        session.pop("join_date", None)
        flash("You have been logged out!", "success")
    else:
        flash("You are not logged in!", "warning")

    return redirect(url_for("login.login"))


@dashboard_blueprint.route('/dashboard', methods=["POST", "GET"])
def dashboard():
    if "nick" in session:
        nickname = session["nick"]
        join_date = session["join_date"]

        if request.method == "POST":
            join_date = datetime.datetime.now()
            db.session.commit()

        return render_template("dashboard.html", nickname=nickname, join_date=join_date)
    else:
        flash("You are not logged in!", "warning")

    return redirect(url_for("login.login"))

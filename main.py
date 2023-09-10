from flask import render_template, redirect, url_for, Blueprint, request, session, flash
from .models import Users, Notes, NotesSchema
from . import db
from datetime import  datetime


login_blueprint = Blueprint("login", __name__)
dashboard_blueprint = Blueprint("dashboard", __name__)
logout_blueprint = Blueprint("logout", __name__)
notes_blueprint = Blueprint("notes", __name__)

add_note_blueprint = Blueprint('add_note', __name__)
get_notes_blueprint = Blueprint('get_notes', __name__)
get_note_blueprint = Blueprint('get_note', __name__)
update_note_blueprint = Blueprint('update_note', __name__)
delete_note_blueprint = Blueprint('delete_note', __name__)
adding_note_blueprint = Blueprint('adding_note', __name__)
add_note_from_form_blueprint = Blueprint('add_note_from_form', __name__)



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
            date_format = "%Y-%m-%d %H:%M:%S.%f"
            parsed_date = datetime.strptime(registration_date, date_format)
            time_difference_in_days = (right_now - parsed_date).days
            session.update({"nick": nickname, "join_date": found_user.join_date})
            flash(f"Hello, {nickname}. You’re with us for {time_difference_in_days} days.", "success")

    elif request.method == "GET" and "nick" not in session:
        return render_template("login.html")
    elif request.method == "GET" and "nick" in session:
        flash("Already logged in!", "warning")

    return redirect(url_for("dashboard.dashboard"))


@add_note_from_form_blueprint.route('/adding-note', methods=['GET', 'POST'])
def add_note_from_form():
    if request.method == 'GET':
        return render_template('adding_note.html')

    if request.method == 'POST':
        content = request.form['content']
        note = Notes(content=content)
        db.session.add(note)
        db.session.commit()
        return redirect('/notes')


# @adding_note_blueprint.route('/note', method=['POST'])
# def adding_note():
#     return render_template("adding_note.html")


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


note_schema = NotesSchema()
notes_schema = NotesSchema(many=True)


def add_to_db(new_note: Notes) -> None:
    db.session.add(new_note)
    db.session.commit()


def delete_from_db(note_to_delete: Notes) -> None:
    db.session.delete(note_to_delete)
    db.session.commit()


# @add_note_blueprint.route('/note', methods=['POST'])
# def add_note() -> str:
#     body = request.json
#
#     new_note = Notes.create_from_json(json_body=body)
#
#     add_to_db(new_note)
#
#     return note_schema.jsonify(new_note)


@get_notes_blueprint.route('/notes', methods=['GET'])
def get_notes() -> str:
    all_notes = Notes.query.all()
    return notes_schema.jsonify(all_notes)


@get_note_blueprint.route('/note/<int:id>', methods=['GET'])
def get_note_by_id(id: int) -> str:
    found_note = Notes.query.get(id)
    return note_schema.jsonify(found_note)


@update_note_blueprint.route('/note/<int:id>', methods=['PUT'])
def update_note(id: int) -> str:
    found_note = Notes.query.get(id)

    body = request.json
    found_note.update(Notes.create_from_json(json_body=body))

    db.session.commit()

    return note_schema.jsonify(found_note)


@delete_note_blueprint.route('/note/<int:id>', methods=['DELETE'])
def delete_note(id: int) -> str:
    note_to_delete = Notes.query.get(id)
    delete_from_db(note_to_delete)

    return note_schema.jsonify(note_to_delete)
from flask import Blueprint, flash, request, render_template, session, redirect, url_for

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@admin.route("/")
def index():
    if "admin" not in session or not session["admin"]:
        return redirect(url_for(".login"))
    return "admin"

@admin.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and ("admin" not in session or not session["admin"]):
        if request.form["login"] == "admin" and request.form["password"] == "admin":
            session["admin"] = True
            return redirect(url_for(".index"))
        else:
            flash("Неверный логин", "error")
    if "admin" in session and session["admin"]:
        return redirect(url_for(".index"))
    return render_template("admin/login.html", title="Админ-панель")

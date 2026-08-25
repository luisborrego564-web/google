import os
import re

from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_wtf import CSRFProtect
from werkzeug.security import check_password_hash, generate_password_hash

import database as db
from config import DevelopmentConfig, ProductionConfig

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_registration(username, email, password):
    errors = []
    if not username or len(username) < 3:
        errors.append("El usuario debe tener al menos 3 caracteres.")
    if not email or not EMAIL_RE.match(email):
        errors.append("El correo electrónico no es válido.")
    if not password or len(password) < 8:
        errors.append("La contraseña debe tener al menos 8 caracteres.")
    return errors


def create_app():
    app = Flask(__name__)
    env = os.environ.get("FLASK_ENV", "development")
    app.config.from_object(ProductionConfig if env == "production" else DevelopmentConfig)

    CSRFProtect(app)

    with app.app_context():
        db.init_db()

    @app.route("/")
    def index():
        if session.get("user_id"):
            return redirect(url_for("dashboard"))
        return render_template("login.html")

    @app.route("/login")
    def login_page():
        return render_template("login.html")

    @app.route("/register")
    def register_page():
        return render_template("register.html")

    @app.route("/dashboard")
    def dashboard():
        if not session.get("user_id"):
            return redirect(url_for("login_page"))
        return render_template("dashboard.html", username=session.get("username"))

    @app.route("/api/register", methods=["POST"])
    def api_register():
        data = request.get_json(silent=True) or {}
        username = (data.get("username") or "").strip()
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""

        errors = validate_registration(username, email, password)
        if errors:
            return jsonify({"success": False, "errors": errors}), 400

        if db.get_user_by_username(username):
            return jsonify({"success": False, "errors": ["El usuario ya existe."]}), 409
        if db.get_user_by_email(email):
            return jsonify({"success": False, "errors": ["El correo ya está registrado."]}), 409

        password_hash = generate_password_hash(password)
        if not db.create_user(username, email, password_hash):
            return jsonify({"success": False, "errors": ["No se pudo crear el usuario."]}), 500

        return jsonify({"success": True, "message": "Usuario registrado correctamente."}), 201

    @app.route("/api/login", methods=["POST"])
    def api_login():
        data = request.get_json(silent=True) or {}
        username = (data.get("username") or "").strip()
        password = data.get("password") or ""

        if not username or not password:
            return jsonify({"success": False, "errors": ["Usuario y contraseña son obligatorios."]}), 400

        user = db.get_user_by_username(username)
        if not user or not check_password_hash(user["password_hash"], password):
            return jsonify({"success": False, "errors": ["Usuario o contraseña incorrectos."]}), 401

        session.clear()
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return jsonify({"success": True, "redirect": url_for("dashboard")}), 200

    @app.route("/api/logout", methods=["POST"])
    def api_logout():
        session.clear()
        return jsonify({"success": True, "redirect": url_for("login_page")}), 200

    return app


app = create_app()

if __name__ == "__main__":
    # HTTPS local para pruebas: FLASK_HTTPS=1 python app.py (certificado autofirmado).
    # En producción, usa un certificado real (p. ej. Let's Encrypt) detrás de un proxy (ver README.md).
    ssl_context = "adhoc" if os.environ.get("FLASK_HTTPS") == "1" else None
    app.run(debug=app.config.get("DEBUG", True), ssl_context=ssl_context)

import os

from dotenv import load_dotenv

load_dotenv()

from flask import Flask, jsonify, render_template, request, session
from flask_wtf import CSRFProtect
from werkzeug.security import check_password_hash, generate_password_hash

import database as db
from config import DevelopmentConfig, ProductionConfig


def create_app():
    app = Flask(__name__)
    env = os.environ.get("FLASK_ENV", "development")
    app.config.from_object(ProductionConfig if env == "production" else DevelopmentConfig)

    CSRFProtect(app)

    with app.app_context():
        db.init_db()

    @app.route("/")
    def index():
        return render_template("login.html")

    @app.route("/login")
    def login_page():
        return render_template("login.html")

    @app.route("/api/login", methods=["POST"])
    def api_login():
        data = request.get_json(silent=True) or {}
        username = (data.get("username") or "").strip()
        password = data.get("password") or ""

        if not username or not password:
            return jsonify({"success": False, "errors": ["Correo y contraseña son obligatorios."]}), 400

        user = db.get_user_by_username(username)
        if user is None:
            # Primer inicio de sesión con este correo: crea la cuenta automáticamente.
            db.create_user(username, username, generate_password_hash(password))
            user = db.get_user_by_username(username)
        elif not check_password_hash(user["password_hash"], password):
            return jsonify({"success": False, "errors": ["Usuario o contraseña incorrectos."]}), 401

        session.clear()
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return jsonify({"success": True, "message": "Sesión iniciada correctamente."}), 200

    @app.route("/api/logout", methods=["POST"])
    def api_logout():
        session.clear()
        return jsonify({"success": True}), 200

    return app


app = create_app()

if __name__ == "__main__":
    # HTTPS local para pruebas: FLASK_HTTPS=1 python app.py (certificado autofirmado).
    # En producción, usa un certificado real (p. ej. Let's Encrypt) detrás de un proxy (ver README.md).
    ssl_context = "adhoc" if os.environ.get("FLASK_HTTPS") == "1" else None
    app.run(debug=app.config.get("DEBUG", True), ssl_context=ssl_context)

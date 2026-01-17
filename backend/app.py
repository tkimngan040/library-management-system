from flask import Flask, request, jsonify
from config import DevelopmentConfig
from auth_service import authenticate, login_user, logout_user
from auth_service import login_required, role_required, guest_allowed


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    @app.route("/")
    @guest_allowed
    def index():
        return jsonify({"message": "Library Management Backend is running"})

    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        user = authenticate(username, password)
        if not user:
            return jsonify({"error": "Invalid username or password"}), 401

        login_user(user)
        return jsonify({"message": "Login successful"})

    @app.route("/logout", methods=["POST"])
    @login_required
    def logout():
        logout_user()
        return jsonify({"message": "Logout successful"})

    @app.route("/admin")
    @role_required("Admin")
    def admin_only():
        return jsonify({"message": "Welcome Admin"})

    @app.route("/member")
    @role_required("Member")
    def member_only():
        return jsonify({"message": "Welcome Member"})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

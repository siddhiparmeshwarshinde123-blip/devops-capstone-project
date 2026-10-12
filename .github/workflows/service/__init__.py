from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS

from service.routes import accounts_bp


def create_app():
    app = Flask(__name__)

    CORS(app)
    Talisman(
        app,
        force_https=False,
        content_security_policy={
            "default-src": "'self'",
            "style-src": ["'self'", "'unsafe-inline'"],
            "script-src": ["'self'"],
        },
    )

    app.register_blueprint(accounts_bp)

    @app.route("/")
    def index():
        return {
            "name": "Account REST API Service",
            "version": "1.0",
        }

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

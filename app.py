import os
from flask import Flask
from config import Config
import db
from routes_public import public_bp
from routes_admin import admin_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)

    @app.context_processor
    def inject_settings():
        from routes_public import get_settings
        try:
            return {"settings": get_settings()}
        except Exception:
            return {"settings": {}}

    @app.template_filter("dateformat")
    def dateformat(value, fmt="%d %b %Y"):
        if not value:
            return ""
        try:
            return value.strftime(fmt)
        except AttributeError:
            return value

    return app


app = create_app()

if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    app.run(debug=True, host="0.0.0.0", port=5000)

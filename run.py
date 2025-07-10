from dotenv import load_dotenv

load_dotenv()

from flask import Flask
from app.models import db
from app.admin import init_admin
from app import create_app
import os

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    debug = os.environ.get("FLASK_ENV", "production") == "development"
    app.run(host="0.0.0.0", port=5000, debug=debug)

"""
app.py
Main Flask application entry point.
"""
import atexit
from flask import Flask
from config import Config
from extensions import db, login_manager, mail
from auth import auth
from subscriptions import main
from analytics import analytics_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialise extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(analytics_bp)

    # Create DB tables on first run
    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == '__main__':
    from models import Subscription, User
    from scheduler import start_scheduler

    scheduler = start_scheduler(app, mail, db, Subscription, User)

    # Graceful shutdown of scheduler when the app exits
    atexit.register(lambda: scheduler.shutdown(wait=False))

    app.run(debug=True, use_reloader=False)

import os

class Config:
    # App secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sub-tracker-ultra-secret-key-2024!'

    # SQLite database stored as subscriptions.db in the project root
    SQLALCHEMY_DATABASE_URI = 'sqlite:///subscriptions.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── Email / Gmail SMTP ──────────────────────────────────────────────────
    # To enable emails:
    #   1. Go to Google Account → Security → 2-Step Verification → App Passwords
    #   2. Generate a password for "Mail"
    #   3. Set MAIL_USERNAME and MAIL_PASSWORD below (or use environment vars)
    MAIL_SERVER   = 'smtp.gmail.com'
    MAIL_PORT     = 587
    MAIL_USE_TLS  = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your-email@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your-app-password-here'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME') or 'your-email@gmail.com'

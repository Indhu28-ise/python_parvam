"""
models.py
SQLAlchemy models: User & Subscription
"""
from datetime import date
from dateutil.relativedelta import relativedelta
from extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ── User ──────────────────────────────────────────────────────────────────────
class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80),  unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at    = db.Column(db.DateTime, default=db.func.current_timestamp())

    subscriptions = db.relationship('Subscription', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


# ── Subscription ──────────────────────────────────────────────────────────────
class Subscription(db.Model):
    __tablename__ = 'subscription'

    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service      = db.Column(db.String(100), nullable=False)
    cost         = db.Column(db.Float,       nullable=False)
    period       = db.Column(db.String(20),  nullable=False)   # 'Monthly' | 'Annual'
    renewal_date = db.Column(db.Date,        nullable=False)
    category     = db.Column(db.String(50),  default='Other')
    is_active    = db.Column(db.Boolean,     default=True)
    created_at   = db.Column(db.DateTime,    default=db.func.current_timestamp())

    # ── Computed properties ────────────────────────────────────────────────

    @property
    def days_left(self) -> int:
        return (self.renewal_date - date.today()).days

    @property
    def alert_status(self) -> str:
        dl = self.days_left
        if dl < 0:
            return 'Expired'
        elif dl <= 7:
            return 'Upcoming'
        return 'Active'

    @property
    def monthly_cost(self) -> float:
        if self.period == 'Annual':
            return round(self.cost / 12, 2)
        return round(self.cost, 2)

    @property
    def annual_cost(self) -> float:
        if self.period == 'Monthly':
            return round(self.cost * 12, 2)
        return round(self.cost, 2)

    # ── Auto-renewal ───────────────────────────────────────────────────────

    def advance_renewal(self):
        """Push renewal_date forward by one billing cycle."""
        if self.period == 'Monthly':
            self.renewal_date = self.renewal_date + relativedelta(months=1)
        else:
            self.renewal_date = self.renewal_date + relativedelta(years=1)

    # ── Serialisation ──────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            'id':           self.id,
            'service':      self.service,
            'cost':         self.cost,
            'period':       self.period,
            'renewal_date': self.renewal_date.isoformat(),
            'days_left':    self.days_left,
            'alert':        self.alert_status,
            'category':     self.category,
            'monthly_cost': self.monthly_cost,
            'annual_cost':  self.annual_cost,
        }

    def __repr__(self):
        return f'<Subscription {self.service} ({self.period})>'

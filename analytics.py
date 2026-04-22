"""
analytics.py
Blueprint for the analytics dashboard and JSON chart data endpoints.
"""
from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from models import Subscription
from collections import defaultdict

analytics_bp = Blueprint('analytics', __name__)


# ── Analytics Page ────────────────────────────────────────────────────────────
@analytics_bp.route('/analytics')
@login_required
def analytics():
    subs = Subscription.query.filter_by(user_id=current_user.id, is_active=True).all()

    total_monthly = round(sum(s.monthly_cost for s in subs), 2)
    total_annual  = round(sum(s.annual_cost  for s in subs), 2)
    sub_count     = len(subs)
    upcoming      = sum(1 for s in subs if s.alert_status == 'Upcoming')

    return render_template(
        'analytics.html',
        total_monthly=total_monthly,
        total_annual=total_annual,
        sub_count=sub_count,
        upcoming=upcoming,
    )


# ── Chart: Spending by Category (Pie) ─────────────────────────────────────────
@analytics_bp.route('/api/analytics/category')
@login_required
def chart_category():
    subs = Subscription.query.filter_by(user_id=current_user.id, is_active=True).all()
    data: dict[str, float] = defaultdict(float)
    for s in subs:
        data[s.category] += s.monthly_cost

    return jsonify({
        'labels': list(data.keys()),
        'values': [round(v, 2) for v in data.values()],
    })


# ── Chart: Monthly vs Annual billing mix (Doughnut) ──────────────────────────
@analytics_bp.route('/api/analytics/period')
@login_required
def chart_period():
    subs = Subscription.query.filter_by(user_id=current_user.id, is_active=True).all()
    monthly = round(sum(s.monthly_cost for s in subs if s.period == 'Monthly'), 2)
    annual  = round(sum(s.monthly_cost for s in subs if s.period == 'Annual'),  2)
    return jsonify({
        'labels': ['Monthly Billing', 'Annual Billing'],
        'values': [monthly, annual],
    })


# ── Chart: Top 6 Most Expensive Subscriptions (Bar) ──────────────────────────
@analytics_bp.route('/api/analytics/top')
@login_required
def chart_top():
    subs = (
        Subscription.query
        .filter_by(user_id=current_user.id, is_active=True)
        .all()
    )
    # Sort by monthly cost descending, take top 6
    subs_sorted = sorted(subs, key=lambda s: s.monthly_cost, reverse=True)[:6]
    return jsonify({
        'labels': [s.service for s in subs_sorted],
        'values': [s.monthly_cost for s in subs_sorted],
    })


# ── Chart: Category monthly spend detail (for table) ─────────────────────────
@analytics_bp.route('/api/analytics/summary')
@login_required
def chart_summary():
    subs = Subscription.query.filter_by(user_id=current_user.id, is_active=True).all()
    return jsonify([s.to_dict() for s in subs])

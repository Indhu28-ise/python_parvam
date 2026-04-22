"""
subscriptions.py
Main blueprint – dashboard, CRUD, and JSON API for subscriptions.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Subscription
from datetime import datetime

main = Blueprint('main', __name__)

CATEGORIES = ['Entertainment', 'Work', 'Health', 'Education', 'Shopping', 'Finance', 'Utilities', 'Other']

SERVICE_ICONS = {
    'netflix':   '🎬', 'spotify':   '🎵', 'youtube':   '▶️',
    'amazon':    '📦', 'disney':    '🏰', 'apple':     '🍎',
    'hulu':      '📺', 'hbo':       '🎭', 'notion':    '📝',
    'slack':     '💬', 'zoom':      '📹', 'github':    '🐙',
    'dropbox':   '📁', 'adobe':     '🎨', 'microsoft': '🪟',
    'google':    '🔍', 'linkedin':  '💼', 'twitter':   '🐦',
    'discord':   '🎮', 'figma':     '✏️',
}

def get_icon(service_name: str) -> str:
    key = service_name.lower()
    for k, icon in SERVICE_ICONS.items():
        if k in key:
            return icon
    return '📱'


# ── Dashboard ─────────────────────────────────────────────────────────────────
@main.route('/')
@main.route('/dashboard')
@login_required
def dashboard():
    category_filter = request.args.get('category', 'All')
    search          = request.args.get('search', '').strip()

    query = Subscription.query.filter_by(user_id=current_user.id, is_active=True)

    if category_filter != 'All':
        query = query.filter_by(category=category_filter)

    if search:
        query = query.filter(Subscription.service.ilike(f'%{search}%'))

    subscriptions = query.order_by(Subscription.renewal_date).all()

    # Attach icon to each sub (passed as extra attribute)
    for sub in subscriptions:
        sub.icon = get_icon(sub.service)

    # Summary stats
    all_subs       = Subscription.query.filter_by(user_id=current_user.id, is_active=True).all()
    total_monthly  = round(sum(s.monthly_cost for s in all_subs), 2)
    total_annual   = round(sum(s.annual_cost  for s in all_subs), 2)
    upcoming_count = sum(1 for s in all_subs if s.alert_status == 'Upcoming')
    expired_count  = sum(1 for s in all_subs if s.alert_status == 'Expired')
    active_count   = sum(1 for s in all_subs if s.alert_status == 'Active')

    return render_template(
        'dashboard.html',
        subscriptions=subscriptions,
        categories=CATEGORIES,
        selected_category=category_filter,
        search=search,
        total_monthly=total_monthly,
        total_annual=total_annual,
        upcoming_count=upcoming_count,
        expired_count=expired_count,
        active_count=active_count,
    )


# ── Add ───────────────────────────────────────────────────────────────────────
@main.route('/add', methods=['GET', 'POST'])
@login_required
def add_subscription():
    if request.method == 'POST':
        service      = request.form.get('service', '').strip()
        cost         = request.form.get('cost', 0)
        period       = request.form.get('period', 'Monthly')
        renewal_str  = request.form.get('renewal_date', '')
        category     = request.form.get('category', 'Other')

        if not service or not renewal_str:
            flash('Service name and renewal date are required.', 'danger')
            return redirect(url_for('main.add_subscription'))

        try:
            cost         = float(cost)
            renewal_date = datetime.strptime(renewal_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid cost or date format.', 'danger')
            return redirect(url_for('main.add_subscription'))

        sub = Subscription(
            user_id      = current_user.id,
            service      = service,
            cost         = cost,
            period       = period,
            renewal_date = renewal_date,
            category     = category,
        )
        db.session.add(sub)
        db.session.commit()
        flash(f'✅ {service} subscription added successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('add_subscription.html', categories=CATEGORIES)


# ── Edit ──────────────────────────────────────────────────────────────────────
@main.route('/edit/<int:sub_id>', methods=['GET', 'POST'])
@login_required
def edit_subscription(sub_id):
    sub = Subscription.query.filter_by(id=sub_id, user_id=current_user.id).first_or_404()

    if request.method == 'POST':
        sub.service      = request.form.get('service', '').strip()
        sub.period       = request.form.get('period', 'Monthly')
        sub.category     = request.form.get('category', 'Other')

        try:
            sub.cost         = float(request.form.get('cost', 0))
            sub.renewal_date = datetime.strptime(request.form.get('renewal_date', ''), '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid cost or date format.', 'danger')
            return redirect(url_for('main.edit_subscription', sub_id=sub_id))

        db.session.commit()
        flash(f'✏️ {sub.service} updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('edit_subscription.html', sub=sub, categories=CATEGORIES)


# ── Delete ────────────────────────────────────────────────────────────────────
@main.route('/delete/<int:sub_id>', methods=['POST'])
@login_required
def delete_subscription(sub_id):
    sub = Subscription.query.filter_by(id=sub_id, user_id=current_user.id).first_or_404()
    name = sub.service
    sub.is_active = False          # Soft-delete
    db.session.commit()
    flash(f'🗑️ {name} removed from your subscriptions.', 'info')
    return redirect(url_for('main.dashboard'))


# ── Restore ───────────────────────────────────────────────────────────────────
@main.route('/restore/<int:sub_id>', methods=['POST'])
@login_required
def restore_subscription(sub_id):
    sub = Subscription.query.filter_by(id=sub_id, user_id=current_user.id).first_or_404()
    sub.is_active = True
    db.session.commit()
    flash(f'♻️ {sub.service} restored!', 'success')
    return redirect(url_for('main.dashboard'))


# ── JSON API ──────────────────────────────────────────────────────────────────
@main.route('/api/subscriptions')
@login_required
def api_subscriptions():
    subs = Subscription.query.filter_by(user_id=current_user.id, is_active=True).all()
    return jsonify([s.to_dict() for s in subs])

"""
scheduler.py
APScheduler jobs:
  1. Daily email reminders for subscriptions renewing within 7 days.
  2. Midnight auto-renewal: advances expired renewal dates by one billing cycle.
"""
from apscheduler.schedulers.background import BackgroundScheduler
from flask_mail import Message
from datetime import date
import logging

logger = logging.getLogger(__name__)


# ── Email Reminder Job ────────────────────────────────────────────────────────
def send_reminder_emails(app, mail, db, Subscription, User):
    """Find subscriptions renewing in ≤7 days and email each user."""
    with app.app_context():
        today = date.today()
        subs  = Subscription.query.filter_by(is_active=True).all()

        # Group upcoming subs by user
        user_subs: dict[int, list] = {}
        for sub in subs:
            dl = (sub.renewal_date - today).days
            if 0 <= dl <= 7:
                user_subs.setdefault(sub.user_id, []).append(sub)

        for user_id, upcoming in user_subs.items():
            user = User.query.get(user_id)
            if not user:
                continue

            rows = ''.join([
                f'''<tr>
                  <td style="padding:10px 14px;border-bottom:1px solid #2d2d44">{s.service}</td>
                  <td style="padding:10px 14px;border-bottom:1px solid #2d2d44">₹{s.cost:,.0f}</td>
                  <td style="padding:10px 14px;border-bottom:1px solid #2d2d44">{s.period}</td>
                  <td style="padding:10px 14px;border-bottom:1px solid #2d2d44;
                     color:{"#ff6b6b" if s.days_left <= 3 else "#ffa94d"};font-weight:600">
                    {"TODAY!" if s.days_left == 0 else f"{s.days_left} day{'s' if s.days_left != 1 else ''}"}
                  </td>
                </tr>'''
                for s in sorted(upcoming, key=lambda x: x.days_left)
            ])

            html_body = f"""
            <div style="font-family:'Segoe UI',sans-serif;max-width:620px;margin:auto;
                        background:#12121e;color:#e2e2f0;padding:36px;border-radius:16px;
                        border:1px solid #2d2d44">
              <h2 style="color:#a78bfa;margin-top:0">🔔 Subscription Renewal Reminder</h2>
              <p style="color:#b0b0cc">Hi <strong>{user.username}</strong>,<br>
                 The following subscriptions are renewing soon. Make sure you're ready!</p>
              <table style="width:100%;border-collapse:collapse;margin-top:16px">
                <thead>
                  <tr style="background:#1e1e3a;color:#a78bfa;text-align:left">
                    <th style="padding:10px 14px">Service</th>
                    <th style="padding:10px 14px">Cost</th>
                    <th style="padding:10px 14px">Period</th>
                    <th style="padding:10px 14px">Renews In</th>
                  </tr>
                </thead>
                <tbody>{rows}</tbody>
              </table>
              <p style="margin-top:24px;color:#7070a0;font-size:13px">
                Manage your subscriptions at
                <a href="http://localhost:5000" style="color:#a78bfa;text-decoration:none">
                  Subscription Tracker
                </a>
              </p>
            </div>
            """

            try:
                msg = Message(
                    subject = '⚠️ Subscription Renewal Alert – Action Required',
                    recipients = [user.email],
                    html = html_body,
                )
                mail.send(msg)
                logger.info(f'Reminder email sent to {user.email}')
            except Exception as exc:
                logger.warning(f'Mail error for {user.email}: {exc}')


# ── Auto-Renewal Job ──────────────────────────────────────────────────────────
def auto_renew(app, db, Subscription):
    """Advance renewal_date for any subscription whose date has passed."""
    with app.app_context():
        today   = date.today()
        expired = Subscription.query.filter(
            Subscription.renewal_date < today,
            Subscription.is_active   == True,
        ).all()

        for sub in expired:
            old = sub.renewal_date
            sub.advance_renewal()
            logger.info(f'Auto-renewed {sub.service}: {old} → {sub.renewal_date}')

        if expired:
            db.session.commit()
            logger.info(f'Auto-renewed {len(expired)} subscription(s).')


# ── Scheduler Bootstrap ───────────────────────────────────────────────────────
def start_scheduler(app, mail, db, Subscription, User) -> BackgroundScheduler:
    scheduler = BackgroundScheduler(timezone='Asia/Kolkata')

    # Email reminders – every day at 09:00 IST
    scheduler.add_job(
        func    = lambda: send_reminder_emails(app, mail, db, Subscription, User),
        trigger = 'cron',
        hour    = 9, minute = 0,
        id      = 'email_reminder',
    )

    # Auto-renewal – every day at 00:01 IST
    scheduler.add_job(
        func    = lambda: auto_renew(app, db, Subscription),
        trigger = 'cron',
        hour    = 0, minute = 1,
        id      = 'auto_renew',
    )

    scheduler.start()
    logger.info('Scheduler started: email_reminder + auto_renew jobs active.')
    return scheduler

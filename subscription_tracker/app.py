from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import json, os, uuid

app = Flask(__name__)
app.secret_key = "subscription_tracker_secret_2024"

SUBSCRIPTIONS_FILE = "subscriptions.json"
USERS_FILE = "users.json"

CATEGORIES = ["Entertainment", "Work", "Music", "Gaming", "News", "Fitness", "Education", "Other"]

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def calculate_days_left(renewal_date_str):
    try:
        renewal = datetime.strptime(renewal_date_str, "%Y-%m-%d").date()
        return (renewal - date.today()).days
    except:
        return 0

def get_alert_status(days_left):
    if days_left < 0:
        return "Expired"
    elif days_left <= 7:
        return "Upcoming"
    return "Active"

def to_monthly(cost, period):
    return cost if period == "Monthly" else round(cost / 12, 2)

def to_yearly(cost, period):
    return cost * 12 if period == "Monthly" else cost

def enrich_subscriptions(subs):
    for s in subs:
        s["days_left"] = calculate_days_left(s["renewal_date"])
        s["alert"] = get_alert_status(s["days_left"])
        s["monthly_cost"] = to_monthly(s["cost"], s["period"])
        s["yearly_cost"] = to_yearly(s["cost"], s["period"])
    return subs

# ── Auth ──────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        data = load_json(USERS_FILE)
        users = data.get("users", [])
        if any(u["username"] == username for u in users):
            flash("Username already exists.", "error")
            return render_template("register.html")
        users.append({
            "id": str(uuid.uuid4()),
            "username": username,
            "password": generate_password_hash(password)
        })
        save_json(USERS_FILE, {"users": users})
        flash("Account created! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        data = load_json(USERS_FILE)
        users = data.get("users", [])
        user = next((u for u in users if u["username"] == username), None)
        if user and check_password_hash(user["password"], password):
            session["user"] = username
            return redirect(url_for("dashboard"))
        flash("Invalid username or password.", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# ── Dashboard ─────────────────────────────────────────────────────────────────

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    data = load_json(SUBSCRIPTIONS_FILE)
    subs = enrich_subscriptions(data.get("subscriptions", []))

    total_monthly = sum(s["monthly_cost"] for s in subs if s["alert"] != "Expired")
    total_annual  = round(sum(s["yearly_cost"] for s in subs if s["alert"] != "Expired"), 2)
    upcoming = sum(1 for s in subs if s["alert"] == "Upcoming")
    expired  = sum(1 for s in subs if s["alert"] == "Expired")

    # Analytics: per-service monthly spend
    chart_labels = [s["service"] for s in subs if s["alert"] != "Expired"]
    chart_data   = [s["monthly_cost"] for s in subs if s["alert"] != "Expired"]

    # Category breakdown for analytics
    cat_totals = {}
    for s in subs:
        if s["alert"] != "Expired":
            cat = s.get("category", "Other")
            cat_totals[cat] = round(cat_totals.get(cat, 0) + s["monthly_cost"], 2)

    return render_template(
        "dashboard.html",
        subscriptions=subs,
        total_monthly=round(total_monthly, 2),
        total_annual=total_annual,
        upcoming=upcoming,
        expired=expired,
        username=session["user"],
        categories=CATEGORIES,
        chart_labels=chart_labels,
        chart_data=chart_data,
        cat_totals=cat_totals
    )

# ── CRUD ──────────────────────────────────────────────────────────────────────

@app.route("/add", methods=["POST"])
def add_subscription():
    if "user" not in session:
        return redirect(url_for("login"))
    data = load_json(SUBSCRIPTIONS_FILE)
    subs = data.get("subscriptions", [])
    new_id = max((s["id"] for s in subs), default=0) + 1
    subs.append({
        "id": new_id,
        "service":      request.form["service"].strip(),
        "cost":         float(request.form["cost"]),
        "period":       request.form["period"],
        "renewal_date": request.form["renewal_date"],
        "category":     request.form.get("category", "Other")
    })
    save_json(SUBSCRIPTIONS_FILE, {"subscriptions": subs})
    return redirect(url_for("dashboard"))

@app.route("/delete/<int:sub_id>", methods=["POST"])
def delete_subscription(sub_id):
    if "user" not in session:
        return redirect(url_for("login"))
    data = load_json(SUBSCRIPTIONS_FILE)
    subs = [s for s in data.get("subscriptions", []) if s["id"] != sub_id]
    save_json(SUBSCRIPTIONS_FILE, {"subscriptions": subs})
    return redirect(url_for("dashboard"))

@app.route("/renew/<int:sub_id>", methods=["POST"])
def renew_subscription(sub_id):
    """Auto-advance the renewal date by 1 period (month or year)."""
    if "user" not in session:
        return redirect(url_for("login"))
    data = load_json(SUBSCRIPTIONS_FILE)
    subs = data.get("subscriptions", [])
    for s in subs:
        if s["id"] == sub_id:
            current = datetime.strptime(s["renewal_date"], "%Y-%m-%d").date()
            if s["period"] == "Monthly":
                new_date = current + relativedelta(months=1)
            else:
                new_date = current + relativedelta(years=1)
            s["renewal_date"] = new_date.strftime("%Y-%m-%d")
            break
    save_json(SUBSCRIPTIONS_FILE, {"subscriptions": subs})
    return redirect(url_for("dashboard"))

@app.route("/api/subscriptions")
def api_subscriptions():
    data = load_json(SUBSCRIPTIONS_FILE)
    subs = enrich_subscriptions(data.get("subscriptions", []))
    return jsonify({"subscriptions": subs})

if __name__ == "__main__":
    app.run(debug=True)
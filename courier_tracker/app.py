from flask import Flask, render_template, request, redirect, url_for, jsonify
import json, os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "parcels.json"
STATUSES = ["Picked Up", "In Transit", "Out for Delivery", "Delivered"]

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"parcels": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def days_in_transit(timeline):
    for entry in timeline:
        if entry["status"] == "Picked Up":
            try:
                t = datetime.strptime(entry["time"][:16], "%Y-%m-%d %H:%M")
                return (datetime.now() - t).days
            except:
                return 0
    return 0

def build_chart_data(parcels):
    status_counts = {"Picked Up": 0, "In Transit": 0, "Out for Delivery": 0, "Delivered": 0}
    daily = {}
    for p in parcels:
        s = p.get("status", "")
        if s in status_counts:
            status_counts[s] += 1
        if p["timeline"]:
            try:
                day = p["timeline"][0]["time"][:10]
                daily[day] = daily.get(day, 0) + 1
            except:
                pass
    sorted_days = sorted(daily.items())[-7:]
    return {
        "status_labels": list(status_counts.keys()),
        "status_values": list(status_counts.values()),
        "daily_labels": [d[0] for d in sorted_days],
        "daily_values": [d[1] for d in sorted_days],
    }

@app.route("/")
def index():
    q = request.args.get("q", "").strip().lower()
    f = request.args.get("filter", "all").strip()
    data = load_data()
    parcels = data["parcels"]

    for p in parcels:
        p["days_in_transit"] = days_in_transit(p["timeline"])
        p["is_delayed"] = p["days_in_transit"] > 5 and p["status"] != "Delivered"

    filtered = parcels
    if q:
        filtered = [p for p in filtered if q in p["id"].lower()
                    or q in p["sender"].lower()
                    or q in p["receiver"].lower()
                    or q in p["destination"].lower()]
    if f == "delayed":
        filtered = [p for p in filtered if p["is_delayed"]]
    elif f != "all":
        filtered = [p for p in filtered if p["status"].lower() == f.lower()]

    chart = build_chart_data(parcels)
    total = len(parcels)
    in_transit = sum(1 for p in parcels if p["status"] == "In Transit")
    delivered  = sum(1 for p in parcels if p["status"] == "Delivered")
    delayed    = sum(1 for p in parcels if p.get("is_delayed"))

    return render_template("index.html",
        parcels=filtered, statuses=STATUSES,
        total=total, in_transit=in_transit,
        delivered=delivered, delayed=delayed,
        chart=chart, q=q, active_filter=f)

@app.route("/add", methods=["POST"])
def add_parcel():
    data = load_data()
    pid = request.form["parcel_id"].strip()
    if any(p["id"] == pid for p in data["parcels"]):
        return redirect(url_for("index"))
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    data["parcels"].append({
        "id": pid,
        "sender": request.form["sender"].strip(),
        "receiver": request.form["receiver"].strip(),
        "destination": request.form["destination"].strip(),
        "status": "Picked Up",
        "timeline": [{"status": "Picked Up", "time": now}]
    })
    save_data(data)
    return redirect(url_for("index"))

@app.route("/update_status/<parcel_id>", methods=["POST"])
def update_status(parcel_id):
    data = load_data()
    new_status = request.form["status"]
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    for p in data["parcels"]:
        if p["id"] == parcel_id and p["status"] != new_status:
            p["status"] = new_status
            p["timeline"].append({"status": new_status, "time": now})
            break
    save_data(data)
    return redirect(url_for("index"))

@app.route("/delete/<parcel_id>", methods=["POST"])
def delete_parcel(parcel_id):
    data = load_data()
    data["parcels"] = [p for p in data["parcels"] if p["id"] != parcel_id]
    save_data(data)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
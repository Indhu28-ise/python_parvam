from flask import Flask, render_template, request, redirect, send_file
import json, csv
from datetime import datetime

app = Flask(__name__)
FILE = "parcels.json"

# ---------------- FILE HANDLING ---------------- #

def load_data():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {"parcels": []}

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- HOME ---------------- #

@app.route("/")
def index():
    data = load_data()

    for parcel in data["parcels"]:
        start = datetime.strptime(parcel["created_at"], "%Y-%m-%d %H:%M:%S")
        parcel["days"] = (datetime.now() - start).days
        parcel["delayed"] = parcel["days"] > 5

    return render_template("index.html", parcels=data["parcels"])

# ---------------- ADD ---------------- #

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        data = load_data()

        # Prevent duplicate ID
        for p in data["parcels"]:
            if p["id"] == request.form["id"]:
                return "Parcel ID already exists!"

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        parcel = {
            "id": request.form["id"],
            "sender": request.form["sender"],
            "receiver": request.form["receiver"],
            "destination": request.form["destination"],
            "status": "Picked Up",
            "created_at": now,
            "timeline": [{"status": "Picked Up", "time": now}]
        }

        data["parcels"].append(parcel)
        save_data(data)

        return redirect("/")

    return render_template("add.html")

# ---------------- UPDATE ---------------- #

@app.route("/update/<pid>", methods=["GET", "POST"])
def update(pid):
    data = load_data()

    for parcel in data["parcels"]:
        if parcel["id"] == pid:
            if request.method == "POST":
                new_status = request.form["status"]
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                parcel["status"] = new_status
                parcel["timeline"].append({
                    "status": new_status,
                    "time": now
                })

                save_data(data)
                return redirect("/")

            return render_template("update.html", parcel=parcel)

    return "Parcel not found"

# ---------------- DELETE ---------------- #

@app.route("/delete/<pid>")
def delete(pid):
    data = load_data()
    data["parcels"] = [p for p in data["parcels"] if p["id"] != pid]
    save_data(data)
    return redirect("/")

# ---------------- SEARCH ---------------- #

@app.route("/search", methods=["POST"])
def search():
    pid = request.form["id"]
    data = load_data()

    results = [p for p in data["parcels"] if p["id"] == pid]

    return render_template("index.html", parcels=results)

# ---------------- EXPORT CSV ---------------- #

@app.route("/export")
def export():
    data = load_data()

    filename = "report.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Sender", "Receiver", "Destination", "Status"])

        for p in data["parcels"]:
            writer.writerow([p["id"], p["sender"], p["receiver"], p["destination"], p["status"]])

    return send_file(filename, as_attachment=True)

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(debug=True)
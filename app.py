from flask import Flask, render_template, request, redirect, url_for
 
app = Flask(__name__)
 
hospitals = [
    {"name": "City General Hospital", "address": "12 MG Road, Pune", "city": "pune", "blood_group": "A+", "status": "Have Blood to Donate", "contact": "020-12345678"},
    {"name": "Apollo Care", "address": "45 Baner Road, Pune", "city": "pune", "blood_group": "O-", "status": "Need Blood", "contact": "020-98765432"},
    {"name": "Sunrise Medical", "address": "7 FC Road, Pune", "city": "pune", "blood_group": "B+", "status": "Have Blood to Donate", "contact": "020-11223344"},
    {"name": "Metro Hospital", "address": "88 Anna Salai, Chennai", "city": "chennai", "blood_group": "A+", "status": "Need Blood", "contact": "044-55667788"},
    {"name": "Ruby Hall Clinic", "address": "40 Sassoon Road, Pune", "city": "pune", "blood_group": "AB+", "status": "Have Blood to Donate", "contact": "020-66778899"},
]
 
BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
 
@app.route("/")
def index():
    return render_template("index.html", hospitals=None, searched=False, blood_groups=BLOOD_GROUPS)
 
@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name", "").strip()
    address = request.form.get("address", "").strip()
    city = request.form.get("city", "").strip().lower()
    blood_group = request.form.get("blood_group", "").strip()
    status = request.form.get("status", "").strip()
    contact = request.form.get("contact", "").strip()
 
    error = None
    if not all([name, address, city, blood_group, status, contact]):
        error = "All fields are required."
    elif blood_group not in BLOOD_GROUPS:
        error = "Invalid blood group selected."
 
    if error:
        return render_template("index.html", hospitals=None, searched=False,
                               blood_groups=BLOOD_GROUPS, reg_error=error, active_tab="register")
 
    hospitals.append({
        "name": name,
        "address": address,
        "city": city,
        "blood_group": blood_group,
        "status": status,
        "contact": contact,
    })
    return render_template("index.html", hospitals=None, searched=False,
                           blood_groups=BLOOD_GROUPS, reg_success=True, active_tab="register")
 
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        blood_group = request.form.get("blood_group", "").strip()
        city = request.form.get("city", "").strip().lower()
 
        all_matches = [h for h in hospitals if h["blood_group"] == blood_group]
        city_matches = [h for h in all_matches if h["city"] == city]
 
        results = city_matches if city_matches else all_matches
        same_city = bool(city_matches)
 
        return render_template("index.html", hospitals=results, searched=True,
                               blood_groups=BLOOD_GROUPS, search_bg=blood_group,
                               search_city=city.title(), same_city=same_city,
                               active_tab="search")
 
    return render_template("index.html", hospitals=None, searched=False,
                           blood_groups=BLOOD_GROUPS, active_tab="search")
 
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=10000)
 

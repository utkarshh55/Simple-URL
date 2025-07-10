import random, string
from flask import request, redirect, render_template
from app import app, db
from app.models import URL

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        original_url = request.form["url"]
        short_code = generate_code()
        url = URL(original_url=original_url, short_code=short_code)
        db.session.add(url)
        db.session.commit()
        return f"Shortened URL: http://localhost:5000/{short_code}"
    return render_template("index.html")

@app.route("/<short_code>")
def redirect_to_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    return redirect(url.original_url) if url else "URL not found", 404

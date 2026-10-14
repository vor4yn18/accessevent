from dotenv import load_dotenv
 
load_dotenv()
 
from flask import Flask, render_template, jsonify
 
from config import Config
from models import db
from routes.auth import auth_bp
from routes.events import events_bp
from routes.registrations import reg_bp
from routes.communication import comm_bp
 
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
 
app.register_blueprint(auth_bp)
app.register_blueprint(events_bp)
app.register_blueprint(reg_bp)
app.register_blueprint(comm_bp)
 
 
@app.route("/")
def index():
    return render_template("index.html")
 
 
@app.route("/register")
def register_page():
    return render_template("register.html")
 
 
@app.route("/login")
def login_page():
    return render_template("login.html")
 
 
@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")
 
 
@app.route("/events/<int:event_id>")
def event_detail_page(event_id):
    return render_template("event_detail.html", event_id=event_id)
 
 
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)


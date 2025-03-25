from app import app
from app.routes.user_routes import user
from flask import render_template

@app.route('/')
def index():
    return render_template("index.html")

app.register_blueprint(user, url_prefix='/user')
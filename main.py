from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.static_folder = 'static'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedb.db'
app.debug = True
db = SQLAlchemy(app)
app.secret_key = 'fobi_llhuy_zerdo'




with app.app_context():
    db.create_all()


@app.route('/', methods=['GET','POST'])
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")

if __name__=="__main__":
    app.run(debug=True)
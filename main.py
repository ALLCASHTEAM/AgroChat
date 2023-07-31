'''
Роут сайта и его страниц
Пока на питоне нихуя не обрабатывается
ибо для этого нужны рабочие Модели ИИ
'''

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



@app.route('/chatbot', methods=['GET','POST'])
def chatbot():
    return render_template("chatbot.html")

@app.route('/', methods=['GET','POST'])
@app.route('/photobot', methods=['GET','POST'])
def photobot():
    return render_template("photobot.html")


@app.route('/about')
def about():
    return render_template("about.html")

if __name__=="__main__":
    app.run(debug=True)
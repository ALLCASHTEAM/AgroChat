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



@app.route('/photobot', methods=['GET','POST'])
def photobot():

    return render_template("photobot.html")

@app.route('/', methods=['GET','POST'])

@app.route('/about', methods=['GET','POST'])
def about():
    if request.method == 'POST':
        checkbox_value = request.form.get('checkbox')
        print(checkbox_value)
        if checkbox_value:
            return redirect(url_for('/photobot'))
    return render_template("about.html")

@app.route('/get_user_text', methods=['POST'])
def get_user_text():
    if request.method == 'POST':
        print(request.form)
        print(request.form.get('user_text'))
        return ('', 204)
@app.route('/handler_click', methods=['POST'])
def handler_click():
    user_text = request.form['user_text']
    print('КЛИКА КЛИКА ПЕСАААААААААААДО:', user_text)
    return redirect('/photobot')

if __name__=="__main__":
    app.run(debug=True)
'''
Роут сайта и его страниц
Пока на питоне нихуя не обрабатывается
ибо для этого нужны рабочие Модели ИИ
'''
import random
from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import sys
import os
######lameshit######
# Получите текущий каталог (папку) вашего скрипта
current_dir = os.path.dirname(os.path.abspath(__file__))

# Создайте путь к папке AI_PRO_MAX, предполагая, что она находится в текущем каталоге
ai_pro_max_dir = os.path.join(current_dir, 'AI_PRO_MAX')

# Добавьте этот путь в sys.path
sys.path.append(ai_pro_max_dir)

# Импортируйте функцию из скрипта AI_PRO_MAX
from AI_PRO_MAX import mainAI
###################


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
        user_query = request.form.get('user_text')
        print("#####################\n", user_query, "\n##########################################")
        dialog = "-чем полить кукурузу?\n-Биостим кукуруза подойдет для полива кукурузы\n"
        result = mainAI.AI_COMPIL(dialog,user_query)
        print("ОТВЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕТ#####################\n", result, "\n##########################################")
        return ('', 205)

@app.route('/get_bot_text', methods=['POST'])
def get_bot_text():
    if request.method == 'POST':
        print(request.form.get('bot_text'))
        return ('', 204)

@app.route('/send_bot_answer', methods=['GET'])
def send_bot_answer():
    if request.method == 'GET':

        data = f"{random.randrange(1,1000)}"
        return data

@app.route('/handler_click', methods=['POST'])
def handler_click():
    user_text = request.form['user_text']
    print('КЛИКА КЛИКА ПЕСАААААААААААДО:', user_text)
    return redirect('/photobot')

if __name__=="__main__":
    app.run(debug=True)
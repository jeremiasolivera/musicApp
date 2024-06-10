from flask import Flask, session,request, render_template,redirect,url_for
from config import config
from collections import OrderedDict
import os
import json
from random import random
from flask_cors import CORS, cross_origin
# Mis clases
from src.models.users import User
from src.models.meetings import Meetings
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key='secret_key'

CORS(app)





@app.route('/')
def index():
    if 'user' in session:
        session_user = session['user'].get('email','')
        return render_template('routes/home.html', session_user=session_user)
    else:
        return render_template('routes/home.html')


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']


        resp = User.login_user(email,password)
        if resp:
            return redirect(url_for('index'))       


    if 'user' in session:
        return redirect(url_for('index'))
    else:
        return render_template('login.html')


@app.route('/register', methods=['POST','GET'])
def register():

    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        file = request.files['photo_url']
        password = request.form['password']
        rol = request.form['rol']

        prefix_photo = str(random())
        # Validación para guardar foto de perfil
        if file:
            filename = prefix_photo + file.filename 
            filepath = os.path.join('static/user_photo/', filename)
            file.save(filepath)
        else:
            filename = 'default-user.png'

        
        resp = User.register_user(email,password)
        if resp:
            User.data_user_db(name,email,filename,rol)
            return redirect(url_for('login'))  


    return render_template('register.html') 


@app.route('/logout')
def logout():
    User.logout_user()
    return redirect(url_for('index'))


@app.route('/perfil')
@app.route('/perfil/<id>')
def perfil(id=None):
    if 'user' in session:
        
        data_register = Meetings.all_meetings()
        order_dict_meets = OrderedDict(data_register)
        data_meetings_dict = order_dict_meets.values()

        if id is not None:
            useremail = id
        else:
            useremail = session['user'].get('email')
       
        account_user = User.user_account(useremail)
        perfil = OrderedDict(account_user)


        user_profile = {
            'data_meetings_dict':data_meetings_dict,
            'perfil':perfil
        }

        if id is not None:
            return render_template('perfils.html', user_profile=user_profile) 
        else:
            return render_template('perfil.html', user_profile=user_profile) 
    
    else:
        return redirect(url_for('login'))





# Meetings

def next_weekday(weekday):
    """Devuelve la próxima fecha de un día de la semana especificado."""
    # Obtener la fecha de hoy
    today = datetime.now()
    # Calcular la diferencia entre el día de la semana deseado y el día de hoy
    days_ahead = weekday - today.weekday()
    # Si el día deseado ya pasó esta semana, sumar 7 días para obtener el próximo
    if days_ahead <= 0:
        days_ahead += 7
    # Devolver la fecha del próximo día de la semana deseado
    next_day = today + timedelta(days=days_ahead)
    return next_day.date()

@app.route('/add_meeting', methods=['POST','GET'])
def add_meeting():

    if 'user' in session:
        if request.method == 'POST':
            leader = session['user'].get('name')
            leader_mail = session['user'].get('email')
            date = request.form['date']
            praise = request.form.getlist('praise[]')
            worship = request.form.getlist('worship[]')
            description = request.form['description']
            hour = request.form['hour']

            if date == 'sabado':
                date = next_weekday(5)
            elif date == 'miercoles':
                date = next_weekday(2)
            
            fecha = datetime.strptime(str(date), '%Y-%m-%d').strftime('%d-%m-%Y')
            Meetings.add_meeting(leader, str(fecha), praise, worship, str(hour), leader_mail, description)

            
            return redirect(url_for('meeting')) 
        else: 
            return render_template('routes/add_meeting.html') 
    else:
        return redirect(url_for('login')) 



@app.route('/reuniones', methods=['POST','GET'])
def meeting():
    if 'user' in session:    
        data_register = Meetings.all_meetings()
        order_dict_meets = OrderedDict(data_register)

        data_meetings_dict = order_dict_meets.values()

        today =  datetime.now().strftime('%d-%m-%Y')
        
        #datetime.strptime(str(today), '%Y-%m-%d').strftime('%d-%m-%Y')

        data = {'data_meetings_dict':data_meetings_dict,
                'next_weekday':next_weekday,
                'today': today}

        return render_template('routes/meetings.html', data=data)
    else:
        return redirect(url_for('login')) 


@cross_origin
@app.route('/news')
def news():
    with open('static/news.json') as j:
        data = json.load(j)
    news = data.get('news')


    return render_template('routes/news.html',news=news)



if __name__ == '__main__':
    app.run(debug=True)
    
    app.config.from_object(config['development'])

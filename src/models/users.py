from ..services.firebase import firebase_auth_connection,firebase_db_connection
from flask import session,flash
from random import random


# Authentication user
auth = firebase_auth_connection()
# Base de datos
db = firebase_db_connection()


class User:

    instance_count = 0

    def __init__(self,name,surname, email):
        User.instance_count += 1
        self.name = name
        self.surname = surname
        self.email = email

    

    #Funciones de registro 
    @staticmethod   
    def register_user(email, password):   #TODO
        if email and password:
            try:
                user = auth.create_user_with_email_and_password(email,password)
                auth.send_email_verification(user['idToken'])
                flash('Enviamos un email para confirmar la cuenta!.')
                return True
            except:
                return flash('Email registrado, solo puedes tener una cuenta por dispositivo!.')

        else:
            return flash('Utiliza credenciales válidas!.')       
    
    @staticmethod
    def login_user(email, password):
        
        if email and password:
            try:
                
                user = auth.sign_in_with_email_and_password(email,password)
                account_info = auth.get_account_info(user['idToken'])
                user_info = account_info['users'][0]
                #print(account_info)
               
                is_verified = user_info['emailVerified'] 
                #email_user = user_info['email'] 
                #user_name = user_info['display_name'] 

                if is_verified:
                    #session['user'] = email
                    #Tomar los datos de la DB
                    get_db_users = db.child("users").get()
                    #user_in_session = None                

                    for user in get_db_users.each():
                        if user.val().get('email') == email:
                            data_user = user.val()
                            his_name = str(data_user.get('name'))
                            his_email = str(data_user.get('email'))
                            his_photo_url = str(data_user.get('photo_url'))
                            his_rol = str(data_user.get('his_rol'))

                            session['user'] = {
                                'name': his_name.title(),
                                'email': his_email,
                                'photo_url': his_photo_url,
                                'rol': his_rol
                            } 
                            
                            return True

                else: 
                    return flash('Recuerda verificar tu cuenta')
                    

            except:
                return flash('Ocurrió un error, intentalo de nuevo!.')

        else:
            return flash('Introduce credenciales válidas')   
   
    @staticmethod
    def logout_user():
        try:
            session.clear()
            return True
        
        except:
            return False

    # Datos de usuario
    @staticmethod
    def data_user_db(name, email, photo_url,rol):
        try:
            email_key = email.replace('.', '_').replace('@', '_')
            
            data = {"email": email, "name":name.title(),"photo_url":str(photo_url),"rol":int(rol)}
            db.child("users").child(email_key).set(data)
            
            #db.update(data)
        except Exception as ex:
            return flash(f"Se produjo un error en la base de datos: {ex}")


    @staticmethod
    def info_user():
        pass

    @staticmethod
    def all_users():
        data = db.child("users").get()
        users = data.val()
        return users
    
    @staticmethod
    def get_user(user_email):
        data = db.child("users").get(user_email)
        users = data.val()
        return users
    
    @staticmethod
    def user_account(user_email):
        email_key = user_email.replace('.', '_').replace('@', '_')
        data = db.child("users").child(email_key).get()
        if user_email == data.val().get('email'):
            
            data = db.child("users").child(email_key).get()
            perfil = data.val()
            return perfil
        else:
            return "Perfil no encontrado"
   


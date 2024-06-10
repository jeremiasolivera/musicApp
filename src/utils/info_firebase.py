# Conexión con Firebase Authentication

config_firebase = {
    'apiKey': "AIzaSyCzbmqFW2e4chMILKMlh5eGldjbmlbeXaU",
    'authDomain': "music-app-d53fe.firebaseapp.com",
    'projectId': "music-app-d53fe",
    'storageBucket': "music-app-d53fe.appspot.com",
    'messagingSenderId': "67647931327",
    'appId': "1:67647931327:web:6934a57140a09b11c1d70a",
    'measurementId': "G-91R1YZMCYB",
    'databaseURL' : 'https://music-app-d53fe-default-rtdb.firebaseio.com/'
}


firebase = pyrebase.initialize_app(config_firebase)
auth = firebase.auth()


email = 'jeremiasolivera166@gmail.com'
password = 'jeremias'

# Crear usuario 
#user = auth.create_user_with_email_and_password(email,password)
#print(user)

# Iniciar sesión
#user = auth.sign_in_with_email_and_password(email,password)
#print(user)

# Infomación de la cuenta
#info = auth.get_account_info(user['idToken'])
#print(info)

# Enviar correo para verificar cuenta
#info_user = auth.get_account_info(user['idToken'])

# Cambiar la contraseña
#info = send_password_reset_email(email)

# Actualizar características de usuario


user = auth.sign_in_with_email_and_password(email,password)
info_user = auth.get_account_info(user['idToken'])


auth.update_profile(user['idToken'],'jeremias','jeremiasfoto.jpg',None)

# Base de datos 

db = firebase.database()

data = {
    "users/jeremias": {
        "name": "jeremias",
        "apellido": "olivera",
        "email": "jeremiasolivera166@gmail.com",
    },
}

db.child("music-app").child("usuarios").update(data)




###############



#new_display_name = "Nuevo Nombre"
#new_photo_url = "https://url-de-la-nueva-foto.com/foto.jpg"

#user = auth.update_profile(user["idToken"], {
#    'display_name': "Nuevo Nombre",
#    'photo_url': "https://url-de-la-nueva-foto.com/foto.jpg"
#})








######################################


@app.route('/')
def index():
    current_user = auth.current_user
    mi_user = current_user['displayName']
    print(mi_user)
    users = db.child("music-app").child("usuarios").child(mi_user).get()
        
    return users
import pyrebase

# config_firebase = {
#     'apiKey': "AIzaSyCzbmqFW2e4chMILKMlh5eGldjbmlbeXaU",
#     'authDomain': "music-app-d53fe.firebaseapp.com",
#     'projectId': "music-app-d53fe",
#     'storageBucket': "music-app-d53fe.appspot.com",
#     'messagingSenderId': "67647931327",
#     'appId': "1:67647931327:web:6934a57140a09b11c1d70a",
#     'measurementId': "G-91R1YZMCYB",
#     'databaseURL' : 'https://music-app-d53fe-default-rtdb.firebaseio.com/'
# }

config_firebase = {
  'apiKey': "AIzaSyBFrEz3CHK2IrctQWtHQYXos9cRhVPqdDU",
  'authDomain': "music-project-d2904.firebaseapp.com",
  'projectId': "music-project-d2904",
  'storageBucket': "music-project-d2904.appspot.com",
  'messagingSenderId': "120388552536",
  'appId': "1:120388552536:web:514c8995bc771fa169072d",
  'databaseURL' : 'https://music-project-d2904-default-rtdb.firebaseio.com/'
}


firebase = pyrebase.initialize_app(config_firebase)

def firebase_auth_connection():
    auth = firebase.auth()

    return auth

def firebase_db_connection():
    db = firebase.database()
    return db
from ..services.firebase import firebase_auth_connection,firebase_db_connection
from flask import session,flash
from random import random


# Authentication user
auth = firebase_auth_connection()
# Base de datos
db = firebase_db_connection()


class Meetings:


    @staticmethod
    def add_meeting(leader, date, praise, worship, hour ,leader_mail,description=""):
        try:
            id = date + "_" + hour
            data = {"leader": leader, "date":date,"songs":{'praise': praise, 'worship':worship}, 'hour':hour,'description': description,'leader_mail':leader_mail}
            db.child("meetings").child(id).set(data)
            
            #db.update(data)
        except Exception as ex:
            return flash(f"Se produjo un error en la base de datos: {ex}")

    @staticmethod
    def all_meetings():
        data = db.child("meetings").get()
        meetings = data.val()
        return meetings
    

   


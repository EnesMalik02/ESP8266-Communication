import pyrebase

config = {
  "apiKey": "AIzaSyAVAx4WmrXw8CpKUc8wqIbW8PJARCqVkTk",
  "authDomain": "espdb-8634b.firebaseapp.com",
  "databaseURL": "https://espdb-8634b-default-rtdb.firebaseio.com",
  "projectId": "espdb-8634b",
  "storageBucket": "espdb-8634b.appspot.com",
  "messagingSenderId": "573751744419",
  "appId": "1:573751744419:web:0bee881b05a3aefa256c16"
  }

config_2 = {
  "apiKey": "AIzaSyBzcHGPYpG-5BgKSdBcOn2AloVtOhLhhlc",
  "authDomain": "espdata-90e79.firebaseapp.com",
  "databaseURL": "https://espdata-90e79-default-rtdb.firebaseio.com",
  "projectId": "espdata-90e79",
  "storageBucket": "espdata-90e79.appspot.com",
  "messagingSenderId": "262886042750",
  "appId": "1:262886042750:web:a50d1986e52e46cea1bc2f",
  "measurementId": "G-HY8LQQ45GW"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

class getDataBase:
    def get_heath(self):
        data = db.child("test").get()
        data_dict = data.val()
        value = data_dict["sicaklik"]
        return value

    def get_humidity(self):
        data = db.child("test").get()
        data_dict = data.val()
        value = data_dict["nem"]
        return value

    def get_distance(self):
        data = db.child("test").get()
        data_dict = data.val()
        value = data_dict["distance"]
        return value

    def get_led(self):
        data = db.child("control").get()
        data_dict = data.val()
        value = data_dict["led"]
        return value

class setDataBase:
  def set_led(self, value):
      db.child("control").update({"led": value})

# db_instance = dataBase()
# distance = db_instance.get_distance()
# print(distance)

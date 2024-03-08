import pyrebase

config = {
  "apiKey": "",
  "authDomain": "",
  "databaseURL": "",
  "projectId": "",
  "storageBucket": "",
  "messagingSenderId": "",
  "appId": ""
  }

firebase = pyrebase.initialize_app(config)
db = firebase.database()

#get data from the database
class getDataBase:
    def get_heath(self):
        data = db.child("test").get()
        data_dict = data.val()
        value = data_dict["sicaklik"]#name of the database value
        return value

    def get_humidity(self):
        data = db.child("test").get()
        data_dict = data.val()
        value = data_dict["nem"]#name of the database value
        return value

    def get_distance(self):
        data = db.child("test").get()
        data_dict = data.val()
        value = data_dict["distance"]#name of the database value
        return value

    def get_led(self,ledId):
        data = db.child("control").get()
        data_dict = data.val()
        value = data_dict[ledId]
        return value

#send data to the database
class setDataBase:
  def set_led(self, ledId,value):
      db.child("control").update({ledId: value})



#Check if data can be retrieved from the database
      
# db_instance = dataBase()
# distance = db_instance.get_distance()
# print(distance)

// AIzaSyBuhgvasYB0DI64DibqmgBFk3PpumqgP8Y --> google maps api

#include <Arduino.h>
//#include <WiFi.h>               //we are using the ESP32
#include <ESP8266WiFi.h>      // uncomment this line if you are using esp8266 and comment the line above
#include <Firebase_ESP_Client.h>
#include <DHT.h>
// ESP Main Data Card

//Provide the token generation process info.
#include "addons/TokenHelper.h"
//Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"

// Insert your network credentials
#define WIFI_SSID "Omer"
#define WIFI_PASSWORD "omer5555"

// Insert Firebase project API Key
#define API_KEY "AIzaSyAVAx4WmrXw8CpKUc8wqIbW8PJARCqVkTk"

// Insert RTDB URLefine the RTDB URL */
#define DATABASE_URL "espdb-8634b-default-rtdb.firebaseio.com" 

//Define Firebase Data object


#define TRIGGER_PIN D7
#define ECHO_PIN D6


#define DHTPIN D5   // DHT11 sensörünün bağlı olduğu pin
#define DHTTYPE DHT11   // DHT11 sensörünün tipi

DHT dht(DHTPIN, DHTTYPE);
FirebaseData fbdo;

FirebaseAuth auth;
FirebaseConfig config;

unsigned long sendDataPrevMillis = 0;
int count = 0;
bool signupOK = false;                     //since we are doing an anonymous sign in 



void setup(){
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED){
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  /* Assign the api key (required) */
  config.api_key = API_KEY;

  /* Assign the RTDB URL (required) */
  config.database_url = DATABASE_URL;

  /* Sign up */
  if (Firebase.signUp(&config, &auth, "", "")){
    Serial.println("ok");
    signupOK = true;
  }
  else{
    Serial.printf("%s\n", config.signer.signupError.message.c_str());
  }

  /* Assign the callback function for the long running token generation task */
  config.token_status_callback = tokenStatusCallback; //see addons/TokenHelper.h
  
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);

  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  dht.begin();
  
}


void loop(){
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  int distance= calculateDistance();

  //Serial.print("Mesafe: ");
  //Serial.print(distance);
  //Serial.println(" cm");
  //delay(2000);

  if (Firebase.ready() && signupOK && (millis() - sendDataPrevMillis > 15000 || sendDataPrevMillis == 0)){
    sendDataPrevMillis = millis();
    // Write an Int number on the database path test/int
    /*if (Firebase.RTDB.setInt(&fbdo, "test/int", count)){
      Serial.println("PASSED");
      Serial.println("PATH: " + fbdo.dataPath());
      Serial.println("TYPE: " + fbdo.dataType());
    }
    else {
      Serial.println("FAILED");
      Serial.println("REASON: " + fbdo.errorReason());
    }*/
    count++;
    
    // Write an Float number on the database path test/float
    /*if (Firebase.RTDB.setFloat(&fbdo, "test/float", 0.01 + random(0,10))){
      Serial.println("PASSED");
      Serial.println("PATH: " + fbdo.dataPath());
      Serial.println("TYPE: " + fbdo.dataType());
    }
    else {
      Serial.println("FAILED");
      Serial.println("REASON: " + fbdo.errorReason());
    }*/
    if (Firebase.RTDB.setInt(&fbdo, "test/distance", distance)) {
      Serial.println("Mesafe verisi gönderildi.");
      Serial.println("PATH: "+fbdo.dataPath());
      Serial.println("TYPE: "+fbdo.dataType());d
    }else {
      Serial.println("Firebase'e veri gönderilirken hata: " + fbdo.errorReason());
    }
    if(Firebase.RTDB.setFloat(&fbdo, "test/sicaklik", temperature) && Firebase.RTDB.setFloat(&fbdo, "test/sicaklik", temperature)){
      Serial.print("Sicaklik ve nem gönderildi.");
      Serial.println("PATH: "+fbdo.dataPath());
      Serial.println("TYPE: "+fbdo.dataType());
      
    }
    else{
      Serial.println("Firebase'e veri gönderilirken hata: " + fbdo.errorReason());
    }
    /*if(Firebase.RTDB.setFloat(&fbdo, "test/nem", humidity)){
      Serial.print("Nem gönderildi.");
    }
    else{
      Serial.println("Firebase'e veri gönderilirken hata: " + fbdo.errorReason());
    }
    if(Firebase.RTDB.getInt(&fbdo, "/test/value")){
      Serial.print("Okunan deger: ");
      Serial.println(fbdo.to<String>());
    }else{
      Serial.print("Veri okuma basarisiz."+ fbdo.errorReason());
      
    }*/
    // Firebase'den gelen LED kontrol değerini oku


  }
}

long calculateDistance()
{
  long duration, distance;
  digitalWrite(TRIGGER_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);

  duration = pulseIn(ECHO_PIN, HIGH);
  distance = (duration / 2) / 29.1; 
  delay(2000);
  return distance;
   
}



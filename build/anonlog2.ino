#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <Firebase_ESP_Client.h>

#include "addons/TokenHelper.h"
#include "addons/RTDBHelper.h"

#define WIFI_SSID "Omer"
#define WIFI_PASSWORD "omer5555"

#define API_KEY "AIzaSyAVAx4WmrXw8CpKUc8wqIbW8PJARCqVkTk"
#define DATABASE_URL "espdb-8634b-default-rtdb.firebaseio.com"

const int greenLed = D6;
const int redLed = D5;
const int blueLed = D4;

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

bool signupOK = false;

void setup() {
  Serial.begin(115200);
  pinMode(greenLed, OUTPUT);
  pinMode(redLed, OUTPUT);
  pinMode(blueLed, OUTPUT);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(300);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());

  config.api_key = API_KEY;
  config.database_url = DATABASE_URL;

  if (Firebase.signUp(&config, &auth, "", "")) {
    Serial.println("Firebase sign-up OK");
    signupOK = true;
  } else {
    Serial.printf("Firebase sign-up failed: %s\n", config.signer.signupError.message.c_str());
  }

  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
}

void controlLED(const String &path, int ledPin) {
  if (Firebase.RTDB.getString(&fbdo, path)) {
    String ledValue = fbdo.stringData();
    digitalWrite(ledPin, ledValue == "ON" ? HIGH : LOW);
  }
}

void loop() {
  if (Firebase.ready() && signupOK) {
    // Kontrol edilecek LED'ler ve ilgili Firebase yolları
    controlLED("/control/led", greenLed);
    controlLED("/control/led2", redLed);
    controlLED("/control/led3", blueLed);
  }
  delay(1000); // Veri okuma sıklığını kontrol etmek için gecikme süresi
}

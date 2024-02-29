int trigPin = D6;
int echoPin = D5;

int zaman;
int mesafe;
void setup() {
  pinMode(trigPin , OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(115200);
}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(trigPin, LOW);

  zaman = pulseIn(echoPin, HIGH);

  mesafe = zaman * 0.0345 /2;
  Serial.println(mesafe);
  delay(100);

}

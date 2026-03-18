uint8_t trigPin=12;
uint8_t echoPin=11;
uint8_t relayPin=10;
long duration;
float distance;
void setup() {
  Serial.begin(9600);
  Serial.println("Uno level detector started");
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(relayPin, OUTPUT  );
  digitalWrite(relayPin, HIGH);
  pinMode(echoPin, INPUT);
  digitalWrite(trigPin, LOW);
  
  
}

void loop() {
  char distStr[32];
  
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
 
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
 
  duration = pulseIn(echoPin, HIGH);
 
  distance = duration*0.034/2;
 
  Serial.print("Distance = ");
  dtostrf( distance, 6, 3, distStr );
  Serial.print(distance);
  
  Serial.println(" cm");
  if (distance > 32.17)
  {
    digitalWrite(relayPin, LOW);  
  }
  if (distance < 26.17)
  {
    digitalWrite(relayPin, HIGH);  
  }

  // put your main code here, to run repeatedly:
  delay(100);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
}

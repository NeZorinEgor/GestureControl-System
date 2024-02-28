void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(9600); 
}

void loop() {
  if (Serial.available() > 0) {
    char receivedChar = Serial.read(); 
    if (receivedChar == '1') {
      digitalWrite(13, HIGH); 
    } else if (receivedChar == '0') {
      digitalWrite(13, LOW); 
    }

  }
}

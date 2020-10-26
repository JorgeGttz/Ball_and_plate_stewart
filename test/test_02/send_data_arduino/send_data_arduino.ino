void setup(){
  Serial.begin(115200);
}

void loop(){
  for(int i = 0;i<11;i++){
    Serial.println("a"+String(i));
    delay(500);
  }
  Serial.println("b0");
  delay(2000);
}

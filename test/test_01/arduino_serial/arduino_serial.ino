void setup(){
  pinMode(13,OUTPUT);
  Serial.begin(115200);
}

void loop(){
  if(Serial.available()){
     int car = Serial.read();
     
     switch(car){
       case '0':
         digitalWrite(13,LOW);
         break;
        
       case '1':
         digitalWrite(13,HIGH);
         break;
        
       default:
         Serial.println("Action was not defined");
         break;
     }
  }
}

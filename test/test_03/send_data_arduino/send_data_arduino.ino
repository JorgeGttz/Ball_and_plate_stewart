
void setup(){
  Serial.begin(115200);
}

void loop(){
  if(Serial.available()){
    int char_ = Serial.read();
    
    switch(char_){
       case 's':
         test_data();
         break;
       
       default:
         break;
    }
  }
}

void test_data(void){
  for(int i = 0;i<11;i++){
    Serial.println("a"+String(i*2)+","+String(i)+","+String(i*100));
    delay(500);
  }
  Serial.println("b0");
  delay(2000);
}

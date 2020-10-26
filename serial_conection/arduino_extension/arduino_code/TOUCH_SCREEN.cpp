#include "TOUCH_SCREEN.h"

int x_range[2],y_range[2];
int filter_values[2][FILTER_SIZE];

int counter_out = 0;

void reset_range_values(void){
  x_range[0] = 1024;
  x_range[1] = 0;
  y_range[0] = 1024;
  y_range[1] = 0;
}

int get_x_value(void){
  int x_pos;
  pinMode(Y1,INPUT);
  pinMode(Y2,INPUT);
  digitalWrite(Y2,LOW);
  
  pinMode(X1,OUTPUT);
  digitalWrite(X1,HIGH);
  pinMode(X2,OUTPUT);
  digitalWrite(X2,LOW);
  
    #ifdef SCREEN_WO_RESOLUTION
      x_pos=analogRead(Y1);  
    #else
      x_pos=map(analogRead(Y1),MIN_X_VALUE,MAX_X_VALUE,0,X_RESOLUTION);
      x_pos = x_pos < 0?0:x_pos;
      x_pos = x_pos > X_RESOLUTION?X_RESOLUTION:x_pos;
    #endif
    
  #ifdef SCREEN_WO_RESOLUTION
    x_range[0] = x_pos < x_range[0]?x_pos:x_range[0];
    x_range[1] = x_pos > x_range[1]?x_pos:x_range[1];
  #endif
  return x_pos;
}

int get_y_value(void){
  int y_pos;
  
  pinMode(X1,INPUT);
  pinMode(X2,INPUT);
  digitalWrite(X2,LOW);
  pinMode(Y1,OUTPUT);
  digitalWrite(Y1,HIGH);
  pinMode(Y2,OUTPUT);
  digitalWrite(Y2,LOW);
     #ifdef SCREEN_WO_RESOLUTION
       y_pos = analogRead(X1);
     #else
       y_pos=map(analogRead(X1),MIN_Y_VALUE,MAX_Y_VALUE,0,Y_RESOLUTION);
     #endif

  #ifdef SCREEN_WO_RESOLUTION
    y_range[0] = y_pos < y_range[0]?y_pos:y_range[0];
    y_range[1] = y_pos > y_range[1]?y_pos:y_range[1];
    y_pos = y_pos < 0?0:y_pos;
    y_pos = y_pos > Y_RESOLUTION?Y_RESOLUTION:y_pos;
  #endif
  return y_pos;
}

void average_filter(int new_val[]){
  int res[2]={0,0};
  int diff[2];
  diff[0] = new_val[0]-filter_values[0][FILTER_SIZE-1];
  diff[1] = new_val[1]-filter_values[1][FILTER_SIZE-1];

      for(int i = 0;i<(FILTER_SIZE-1);i++){
        filter_values[0][i] = filter_values[0][i+1];
        filter_values[1][i] = filter_values[1][i+1];  
        res[0]+=filter_values[0][i];
        res[1]+=filter_values[1][i];
      }
  
      filter_values[0][FILTER_SIZE-1] = new_val[0];
      filter_values[1][FILTER_SIZE-1] = new_val[1];
  
      res[0]+=filter_values[0][FILTER_SIZE-1];
      res[1]+=filter_values[1][FILTER_SIZE-1];

      new_val[0] = res[0]/FILTER_SIZE;
      new_val[1] = res[1]/FILTER_SIZE;
      
  if(((diff[0] < -OUT_RANGE_X)||(diff[0] > OUT_RANGE_X)) && ((diff[1] < -OUT_RANGE_Y)||(diff[1] > OUT_RANGE_Y))) counter_out = 0;
  else{
    counter_out++;
    //Serial.println("Variable dentro de rango, counter = "+String(counter_out));
    if(counter_out >= OUT_NUMBER){
      //Serial.println("No hay cambios bruscos de posicion");
      new_val[0]=-1;
      new_val[1]=-1;
    }
  } 
}

void reset_filter(void){
  counter_out = 0;
  for(int i = 0;i<FILTER_SIZE;i++){
    filter_values[0][i]=0;
    filter_values[1][i]=0;
  }
}


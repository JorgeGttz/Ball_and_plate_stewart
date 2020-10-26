#ifndef TOUCH_SCREEN_H
#define TOUCH_SCREEN_H
  #include <Arduino.h>

  //Arduino connections
  #define X1                A2
  #define X2                A0
  #define Y1                A1
  #define Y2                A3

  //Touch Screen Settings
  #define X_RESOLUTION     900
  #define Y_RESOLUTION     680

  #define MIN_X_VALUE       75
  #define MAX_X_VALUE      950     
  #define MIN_Y_VALUE      100
  #define MAX_Y_VALUE      910  

  //#define SCREEN_WO_RESOLUTION  

  #define FILTER_SIZE       40
  #define OUT_NUMBER        80
  #define OUT_RANGE_X       50
  #define OUT_RANGE_Y       50

  void reset_range_values(void);
  int get_x_value(void);
  int get_y_value(void);
  void average_filter(int new_val[]);
  void reset_filter(void);
#endif


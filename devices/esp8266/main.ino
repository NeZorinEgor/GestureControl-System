
#include "wifiManager.h"


void setup(){
  Serial.begin(9600);
  EEPROM.begin(EEPROM_SIZE);

  pinMode(LED_BUILTIN, OUTPUT);

  manageWiFiConnection();
  
}


void loop(){
  
  wifiManagerLoop();
  
}





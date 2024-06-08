#include "config.h"
#include "wifi.h"
#include "server.h"
#include <EEPROM.h>


bool isDataStored(int startAddr){
  return EEPROM.read(startAddr) == FLAG;
}


// Функция для сохранения строки в EEPROM
void saveStringToEEPROM(int startAddr, String str) {
  EEPROM.write(startAddr, FLAG); // Записываем контрольный байт
  int len = str.length();
  for (int i = 0; i < len; i++) {
    EEPROM.write(startAddr + 1 + i, str[i]);
  }
  EEPROM.write(startAddr + 1 + len, '\0'); // Завершающий нуль-символ
  EEPROM.commit();  // Сохранение изменений в EEPROM
}


// Функция для чтения строки из EEPROM
String readStringFromEEPROM(int startAddr) {
  char data[MAX_STRING_SIZE]; // Буфер для чтения строки
  int len = 0;
  unsigned char k;
  k = EEPROM.read(startAddr + 1); // Пропускаем контрольный байт
  while (k != '\0' && len < MAX_STRING_SIZE) {
    data[len] = k;
    len++;
    k = EEPROM.read(startAddr + 1 + len);
  }
  data[len] = '\0'; // Завершающий нуль-символ
  return String(data);
}


void manageWiFiConnection(){

  if (isDataStored(0) && isDataStored(MAX_STRING_SIZE+1)){

    SSID = readStringFromEEPROM(0);
    PASSWORD = readStringFromEEPROM(MAX_STRING_SIZE+1);


    start_connect = true;

  } else {
    Serial.println("Wake up " + AP_NAME);
    is_Wifi_on = init_WIFI(!CONNECT1);
  }
  server_init();

}


void startConnect(){
  saveStringToEEPROM(0, SSID);
  saveStringToEEPROM(MAX_STRING_SIZE+1, PASSWORD);
  Serial.println("SAVE");

  CLI_SSID = foo(SSID.c_str());
  PASS_SSID = foo(PASSWORD.c_str());
  
  Serial.println("Connect name: " + String(CLI_SSID) + " pass: " + String(PASS_SSID));
  start_client_mode(2);
  if (wifiMulti.run() == WL_CONNECTED) {
    CONNECT1 = true;
    Serial.println("Conneted your Wi-Fi");    
    off_AP_mode();
    
  } else {    
    Serial.println("Didn't connect your Wi-Fi");
    Serial.println("Wake up " + AP_NAME);
    CONNECT1 = false;
    is_Wifi_on = init_WIFI(!CONNECT1);
    //server_init();
    
  }
}


void wifiManagerLoop(){
  unsigned long currentMillis = millis();

  if (currentMillis - periousMillisWiFiManager >= intervalUpdateWiFiManager){
    periousMillisWiFiManager = currentMillis;

    server.handleClient();

    if(CONNECT1){    
      if (wifiMulti.run() != WL_CONNECTED){
        countMissWiFi += 1;
        if (countMissWiFi >= maxMiss){
          CONNECT1 = false;      
          Serial.println("Your WiFi died!");
          bool is_Wifi_on = init_WIFI(!CONNECT1);
        }
      } else{
        countMissWiFi = 0;
      }
    } else {

      if(start_connect){
        startConnect();
        start_connect = false;
      }
    }

  }

  
  
}


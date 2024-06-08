#include <ESP8266WiFi.h>
#include <WIFIClient.h>
#include <ESP8266WiFiMulti.h>


ESP8266WiFiMulti wifiMulti;
WiFiClient wifiClient;

String ip = "ip not set";


String id(){
  int mac_len = WL_MAC_ADDR_LENGTH;
  uint8_t mac[mac_len];
  WiFi.softAPmacAddress(mac);
  String mac_id = String(mac[mac_len-2], HEX) + String(mac[mac_len-1], HEX);
  return mac_id;
}


bool start_AP_mode(){
  String ssid_id = AP_NAME + "_" + id();
  IPAddress ap_IP(192, 168, 4, 1);
  WiFi.disconnect();
  WiFi.mode(WIFI_AP);
  WiFi.softAPConfig(ap_IP, ap_IP, IPAddress(255, 255, 255, 0));
  WiFi.softAP(ssid_id.c_str(), AP_PASSWORD.c_str());
  Serial.println("WiFi started in AD mode " + ssid_id);
  return true;
}


bool off_AP_mode(){
  WiFi.softAPdisconnect();
  Serial.println("WiFi ended in AD mode ");
  return true;
}



bool start_client_mode(int t = 10){
  wifiMulti.addAP(CLI_SSID, PASS_SSID);
  int count = 0;
  while(wifiMulti.run() != WL_CONNECTED){
    if (count >= t){
      return false;
    }
    Serial.println("TURN1");
    delay(1);
    Serial.println("TURN2");
    count += 1;
  }
  return true;
}

bool init_WIFI(bool AP_mode){
  if (AP_mode){
    start_AP_mode();
    ip = WiFi.softAPIP().toString();
  }else{
      if (start_client_mode()){
        ip = WiFi.localIP().toString();
        off_AP_mode();
        
      }else{
        return false;
      }
  }
  Serial.println("IP address: " + ip);
  return true;
}



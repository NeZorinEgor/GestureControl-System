#include <ESP8266WebServer.h>

ESP8266WebServer server(WEB_SERVER_PORT);

void handle_root(){
  String page_code = "<form action=\"/LED\" method=\"POST\">"; 
  page_code += "<input type=\"submit\" value=\"Switch Ted\">";
  page_code += "</form>";
  server.send(200, "text/html", page_code);
}


void handle_wifi(){
  String page_code = "<form action=\"/CONNECT\" method=\"POST\">";
  page_code += "Wi-Fi SSID: <input type=\"text\" name=\"ssid\"><br>";
  page_code += "Wi-Fi Password: <input type=\"password\" name=\"password\"><br>";
  page_code += "<input type=\"submit\" value=\"Connect to Wi-Fi\">";
  page_code += "</form>";

  server.send(200, "text/html", page_code);
}

char* foo(const char* ch) {
    return (char*)ch;
}



void handle_connect() {
  SSID = server.arg("ssid");
  PASSWORD = server.arg("password");

  start_connect = true;

  server.send(200, "text/html", "Connect to your Wi-Fi!");
}


void handle_sensor(){
  int val = analogRead(A0);
  Serial.print("MAC ");
  Serial.println(WiFi.macAddress());
  server.send(200, "text/html", String(val));
}

void getMac(){
  Serial.print("MAC ");
  Serial.println(WiFi.macAddress());
  server.send(200, "text/html", WiFi.macAddress());
}


void handle_not_found(){
  server.send(404, "text/html", "404: check URL");
}

void server_init(){
  server.on("/", HTTP_GET, handle_wifi);
  server.on("/SENSOR", HTTP_GET, handle_sensor);
  server.on("/HANDLE", HTTP_GET, handle_root);
  server.on("/MAC", HTTP_GET, getMac);
  server.on("/CONNECT", HTTP_POST, handle_connect);


  server.onNotFound(handle_not_found);

  server.begin();
  Serial.println("Server start on port: ");
  Serial.println(WEB_SERVER_PORT);
}
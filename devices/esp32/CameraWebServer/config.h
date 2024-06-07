
int countMissWiFi = 0;
int maxMiss = 2;

unsigned long periousMillisWiFiManager = 0;
const long intervalUpdateWiFiManager = 50;

String AP_NAME = "Oleg";
String AP_PASSWORD = "12345678";

bool CONNECT1 = false;
bool WORK = false;

const int EEPROM_SIZE = 512;
const int MAX_STRING_SIZE = 100;
const byte FLAG = 0xAA; 

//CLI WIFI client
char* CLI_SSID = "name";
char* PASS_SSID = "password";

String SSID = "";
String PASSWORD = "";

int WEB_SERVER_PORT = 80;

const char* mqtt_broker = "broker.emqx.io";
const int mqtt_port = 1883;


String state_topic = "tyt/state";
String topic = "tyt1/command";

bool start_connect = false;
bool is_Wifi_on = false;

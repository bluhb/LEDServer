#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

ESP8266WebServer Server(80);

int LEDR = 2;
int LEDG = 0;
int LEDB = 3;

const int ILOW = HIGH;
const int IHIGH = LOW;

void handleRoot();
void handleColor();
void handleNotFound();
IPAddress staticIP(192, 168, 2, 16);
IPAddress gateway(192, 168, 2, 254);
IPAddress subnet(255, 255, 255, 0);
IPAddress dns(192, 168, 2, 12);

void setup() {  
  // put your setup code here, to run once:
  wifi_set_sleep_type(NONE_SLEEP_T);
  //Serial.begin(115200);
  //Serial.println("Hello from me");
  WiFi.config(staticIP, subnet, gateway, dns);
  WiFi.mode(WIFI_STA);
  
  WiFi.begin("Gezelligheid", "BierIsFijn");
  analogWriteRange(255);
  pinMode(LEDR, OUTPUT);
  pinMode(LEDG, OUTPUT);
  pinMode(LEDB, OUTPUT);

  digitalWrite(LEDR, ILOW);
  digitalWrite(LEDG, ILOW);
  digitalWrite(LEDB, LOW);

  int RVal = IHIGH;
  while (WiFi.status() != WL_CONNECTED){
    digitalWrite(LEDR, !RVal);
    RVal = !RVal; 
    delay(100);
  }
  WiFi.hostname("ESP-01_Test");
  Server.on("/", HTTP_GET, handleRoot);
  Server.on("/color", HTTP_POST, handleColor);
  Server.onNotFound(handleNotFound);
  Server.begin();
  digitalWrite(LEDR, ILOW);
  digitalWrite(LEDG, IHIGH);
  delay(100);
  digitalWrite(LEDG, ILOW);
  delay(100);
  digitalWrite(LEDG, IHIGH);
  delay(100);
  digitalWrite(LEDG, ILOW);
  delay(100);
  analogWrite(LEDB, 0);
  delay(50);
  analogWrite(LEDB, 125);
  delay(50);
  analogWrite(LEDB, 255);
}

void handleRoot(){
  Server.send(200, "text/html", "use a post on /color");
}

void handleColor(){
  Server.send(200, "Color received");
  int r = 255 - Server.arg("plain").substring(1,4).toInt();
  int g = 255 - Server.arg("plain").substring(4,7).toInt();
  int b = 255 - Server.arg("plain").substring(7,10).toInt();
//  Serial.print(r); Serial.print(",");
//  Serial.print(g); Serial.print(",");  
//  Serial.print(b); Serial.println("");
  analogWrite(LEDR, r);
  analogWrite(LEDG, g);
  analogWrite(LEDB, b);

}

void handleNotFound(){
  Server.send(404);
}

void loop() {
  // put your main code here, to run repeatedly:
  Server.handleClient();
}

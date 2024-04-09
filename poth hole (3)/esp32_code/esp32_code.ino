#include <WebServer.h>
#include <WiFi.h>
#include <esp32cam.h>

const char* WIFI_SSID = "SRC 24G";
const char* WIFI_PASS = "src@internet";
 
WebServer server(80);

int buz=12;
int bt=13;

static auto loRes = esp32cam::Resolution::find(320, 240);
static auto midRes = esp32cam::Resolution::find(350, 530);
static auto hiRes = esp32cam::Resolution::find(800, 600);


float get_distance_cm()
{
  // Connect the arduino to the SR04 pins as defined here
  //  (you can change A4 and A5 to any other unused pins for GPIO mode)
  const int SR04_Trig_RX_SCL = 15;
  const int SR04_Echo_TX_SDA = 14;
  
  // Ensure the pins are in the correct mode
  pinMode(SR04_Echo_TX_SDA,INPUT);
  pinMode(SR04_Trig_RX_SCL,OUTPUT);
  
  // We need to delay by at least 30ms between readings
  //  so we don't get a false reading
  static unsigned long lastread = 0;
  if(millis() - lastread < 30)
  {
    delay(millis()-lastread);  
  }
  lastread = millis();

  // Send a trigger pulse
  digitalWrite(SR04_Trig_RX_SCL,HIGH);
  delayMicroseconds(500);
  digitalWrite(SR04_Trig_RX_SCL,LOW);

  // Read the distance pulse, 
  // the number of microseconds for a return trip at the speed of sound
  unsigned long microseconds  = pulseIn(SR04_Echo_TX_SDA,HIGH);

  // Sound travels in air at about 343 m/s at 20degrees C
  //  that is 343 / 1000000 m per microsecond
  //  that is ( 343 / 1000000  * 100) cm per microsecond
  // Note thoat we need to "cast" to a float here to calculate correctly
  float distance  = microseconds * ( (float) 343 / 1000000 * 100); 
  distance  = distance/2; // divide by 2 since that was a return trip

  return distance;
}
void serveJpg()
{
  auto frame = esp32cam::capture();
  if (frame == nullptr) {
    Serial.println("CAPTURE FAIL");
    server.send(503, "", "");
    return;
  }
  Serial.printf("CAPTURE OK %dx%d %db\n", frame->getWidth(), frame->getHeight(),
                static_cast<int>(frame->size()));
 
  server.setContentLength(frame->size());
  server.send(200, "image/jpeg");
  WiFiClient client = server.client();
  frame->writeTo(client);
}

void handleRoot() {
 float distance = get_distance_cm();
  String json = "{\"distance\":" + String(distance)+","+ String(digitalRead(bt)) + "}";

  server.send(200, "application/json", json);
  if(distance>10)
  {
    digitalWrite(buz,1);
    
    
  }
  else
  {
    digitalWrite(buz,0);
  }
}
 
void handleJpgLo()
{
  if (!esp32cam::Camera.changeResolution(loRes)) {
    Serial.println("SET-LO-RES FAIL");
  }
  serveJpg();
}
 
void handleJpgHi()
{
  if (!esp32cam::Camera.changeResolution(hiRes)) {
    Serial.println("SET-HI-RES FAIL");
  }
  serveJpg();
}
 
void handleJpgMid()
{
  if (!esp32cam::Camera.changeResolution(midRes)) {
    Serial.println("SET-MID-RES FAIL");
  }
  serveJpg();
}
 
 
void  setup(){
  Serial.begin(9600);
  Serial.println();
  {
    using namespace esp32cam;
    Config cfg;
    cfg.setPins(pins::AiThinker);
    cfg.setResolution(hiRes);
    cfg.setBufferCount(2);
    cfg.setJpeg(80);
 
    bool ok = Camera.begin(cfg);
    Serial.println(ok ? "CAMERA OK" : "CAMERA FAIL");
  }
  WiFi.persistent(false);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  Serial.print("http://");
  Serial.println(WiFi.localIP());
  Serial.println("  /cam-lo.jpg");
  Serial.println("  /cam-hi.jpg");
  Serial.println("  /cam-mid.jpg");
 
  server.on("/cam-lo.jpg", handleJpgLo);
  server.on("/cam-hi.jpg", handleJpgHi);
  server.on("/cam-mid.jpg", handleJpgMid);
  server.on("/", handleRoot);

 pinMode(bt,INPUT);
 pinMode(buz,OUTPUT);
 
  server.begin();
}
 
void loop()
{
  server.handleClient();
 
}

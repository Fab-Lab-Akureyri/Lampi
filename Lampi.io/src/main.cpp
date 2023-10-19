/*********
  Rui Santos
  Complete project details at https://randomnerdtutorials.com  
*********/

// Import required libraries
#include "WiFi.h"
#include "ESPAsyncWebServer.h"
#include "SPIFFS.h"
#include "AsyncTCP.h"
#include <Adafruit_NeoPixel.h>


// Replace with your network credentials
const char* ssid = "Hotspot";
const char* password = "Password";

// Create AsyncWebServer object on port 80
AsyncWebServer server(80);

// Set LED GPIO
const int ledPin = D6;

// Set Servo pin
#define SERVO_PIN D0

// Stores LED state
String ledState;

// Set Neopixel
#define NEO_PIN D1
#define LED_COUNT 12
String neoState = "";

// Create Neopixel object
Adafruit_NeoPixel strip(LED_COUNT, NEO_PIN, NEO_GRBW + NEO_KHZ800);

// Replaces placeholder with LED state value
String processor(const String& var){
  Serial.println(var);
  if(var == "LEDSTATE"){
    if(digitalRead(ledPin)){
      ledState = "ON";
    }
    else{
      ledState = "OFF";
    }
    Serial.print(ledState);
    return ledState;
  } else if (var == "NEOSTATE"){
    Serial.println(neoState);
    return neoState;
  }
  return String();
}

// Servo helper functions for ESP32-C3
void generatePWM(int pulseWidthMicros) {
  int pulsePeriodMicros = 20000; // Corresponds to 50Hz  
  digitalWrite(SERVO_PIN, HIGH);
  delayMicroseconds(pulseWidthMicros);
  digitalWrite(SERVO_PIN, LOW);
  delayMicroseconds(pulsePeriodMicros - pulseWidthMicros);
}

void setServoAngle(int angle) {
  int pulseWidth = map(angle, 0, 180, 1000, 2000); // Map angle to 1-2ms pulse width
  generatePWM(pulseWidth);
}

 
void setup(){
  // Serial port for debugging purposes
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  pinMode(SERVO_PIN, OUTPUT);


  // Init Neopixel
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'

  for(int i = 0; i < 12; i++){
    strip.setPixelColor(i, 0, 0, 0, 32);  
    delay(50);
    strip.show();
  }

  for(int i = 0; i < 12; i++){
    strip.setPixelColor(i, 0, 0, 0, 0);  
    delay(50);
    strip.show();
  }

  // Sweep from 0 to 180 degrees
  for (int angle = 0; angle <= 180; angle++) {
    setServoAngle(angle);
    //delay(25); // Delay for smooth movement
  }
  
  // Sweep back from 180 to 0 degrees
  for (int angle = 180; angle >= 0; angle--) {
    setServoAngle(angle);
    //delay(25); // Delay for smooth movement
  }

  // Initialize SPIFFS
  if(!SPIFFS.begin(true)){
    Serial.println("An Error has occurred while mounting SPIFFS");
    return;
  }

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }

  // Print ESP32 Local IP Address
  Serial.println(WiFi.localIP());

  // Route for root / web page
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(SPIFFS, "/index.html", String(), false, processor);
  });
  
  // Route to load style.css file
  server.on("/style.css", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(SPIFFS, "/style.css", "text/css");
  });

  // Route to set GPIO to HIGH
  server.on("/ledon", HTTP_GET, [](AsyncWebServerRequest *request){
    digitalWrite(ledPin, HIGH);    
    request->send(SPIFFS, "/index.html", String(), false, processor);
  });
  
  // Route to set GPIO to LOW
  server.on("/ledoff", HTTP_GET, [](AsyncWebServerRequest *request){
    digitalWrite(ledPin, LOW);    
    request->send(SPIFFS, "/index.html", String(), false, processor);
  });

  server.on("/neored", HTTP_GET, [](AsyncWebServerRequest *request){  
    for(int i = 0; i < LED_COUNT; i++){
      strip.setPixelColor(i, 64, 0, 0, 0);  
      //delay(100);
      strip.show();
    }   
    neoState = "Red";
    request->send(SPIFFS, "/index.html", String(), false, processor);
  });

  server.on("/neogreen", HTTP_GET, [](AsyncWebServerRequest *request){  
    for(int i = 0; i < LED_COUNT; i++){
      strip.setPixelColor(i, 0, 64, 0, 0);  
      //delay(100);
      strip.show();
    }   
    neoState = "Green";
    request->send(SPIFFS, "/index.html", String(), false, processor);
  });

  server.on("/neoblue", HTTP_GET, [](AsyncWebServerRequest *request){  
    for(int i = 0; i < LED_COUNT; i++){
      strip.setPixelColor(i, 0, 0, 64, 0);  
      //delay(100);
      strip.show();
    }   
    neoState = "Blue";
    request->send(SPIFFS, "/index.html", String(), false, processor);
  });

  server.on("/neowhite", HTTP_GET, [](AsyncWebServerRequest *request){  
    for(int i = 0; i < LED_COUNT; i++){
      strip.setPixelColor(i, 0, 0, 0, 64);  
      //delay(100);
      strip.show();
    }
    neoState = "White";
    request->send(SPIFFS, "/index.html", String(), false, processor);
  });

  server.on("/neooff", HTTP_GET, [](AsyncWebServerRequest *request){  
    for(int i = 0; i < LED_COUNT; i++){
      strip.setPixelColor(i, 0, 0, 0, 0);  
      //delay(100);
      strip.show();
    }
    neoState = "Off";
    request->send(SPIFFS, "/index.html", String(), false, processor);
  });

  // Start server
  server.begin();
}
 
void loop(){
  
}
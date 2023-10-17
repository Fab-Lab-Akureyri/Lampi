#include <Adafruit_NeoPixel.h>
#define LED_PIN D1
#define LED_COUNT 12
#define SERVO_PIN D0 // Connected to D0

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_RGBW + NEO_KHZ800);

void setup() {
  pinMode(SERVO_PIN, OUTPUT);
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
}

void loop() {
  // Sweep from 0 to 180 degrees
  for (int angle = 0; angle <= 180; angle++) {
    setServoAngle(angle);
    //delay(1); // Delay for smooth movement
  }
  
  // Sweep back from 180 to 0 degrees
  for (int angle = 180; angle >= 0; angle--) {
    setServoAngle(angle);
    //delay(1); // Delay for smooth movement
  }

  for(int i = 0; i < 12; i++){
    strip.setPixelColor(i, 0, 0, 0, 32);  
    delay(100);
    strip.show();
  }

  for(int i = 0; i < 12; i++){
    strip.setPixelColor(i, 0, 0, 0, 0);  
    delay(100);
    strip.show();
  }
}

void setServoAngle(int angle) {
  int pulseWidth = map(angle, 0, 180, 1000, 2000); // Map angle to 1-2ms pulse width
  generatePWM(pulseWidth);
}

void generatePWM(int pulseWidthMicros) {
  int pulsePeriodMicros = 20000; // Corresponds to 50Hz
  
  digitalWrite(SERVO_PIN, HIGH);
  delayMicroseconds(pulseWidthMicros);
  digitalWrite(SERVO_PIN, LOW);
  delayMicroseconds(pulsePeriodMicros - pulseWidthMicros);
}

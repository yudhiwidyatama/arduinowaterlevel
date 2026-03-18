#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Watchdog.h>

Watchdog watchdog;
#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
// The pins for I2C are defined by the Wire-library. 
// On an arduino UNO:       A4(SDA), A5(SCL)
// On an arduino MEGA 2560: 20(SDA), 21(SCL)
// On an arduino LEONARDO:   2(SDA),  3(SCL), ...
#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#define NUMFLAKES     10 // Number of snowflakes in the animation example

#define LOGO_HEIGHT   16
#define LOGO_WIDTH    16
static const unsigned char PROGMEM logo_bmp[] =
{ 0b00000000, 0b11000000,
  0b00000001, 0b11000000,
  0b00000001, 0b11000000,
  0b00000011, 0b11100000,
  0b11110011, 0b11100000,
  0b11111110, 0b11111000,
  0b01111110, 0b11111111,
  0b00110011, 0b10011111,
  0b00011111, 0b11111100,
  0b00001101, 0b01110000,
  0b00011011, 0b10100000,
  0b00111111, 0b11100000,
  0b00111111, 0b11110000,
  0b01111100, 0b11110000,
  0b01110000, 0b01110000,
  0b00000000, 0b00110000 };
uint8_t trigPin=12;
uint8_t echoPin=11;
uint8_t relayPin=10;
long duration;
float distance;
void setup() {
  watchdog.enable(Watchdog::TIMEOUT_4S);
  Serial.begin(9600);
  Serial.println("Uno level detector started");
  
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(relayPin, OUTPUT  );
  digitalWrite(relayPin, HIGH);
  pinMode(echoPin, INPUT);
  digitalWrite(trigPin, LOW);
  // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    // for(;;); // Don't proceed, loop forever
  }
  else 
    display.display();
  delay(500);
}

void loop() {
  char distStr[32];
  
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
 
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
 
  duration = pulseIn(echoPin, HIGH);
 
  distance = duration*0.034/2;
  display.clearDisplay();

  Serial.print("Distance = ");
  dtostrf( distance, 6, 3, distStr );
  Serial.print(distance);
  display.setTextSize(2);      // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE); // Draw white text
  display.setCursor(0, 0);     // Start at top-left corner
  display.cp437(true);         // Use full 256 char 'Code Page 437' font
  display.print("Distance = ");
  display.print(distance);
  display.print(" cm");
  Serial.println(" cm");
  //if (distance > 32.17)
  if (distance > 29.6)
  {
    digitalWrite(relayPin, LOW);
    display.println("");
    display.println(" PUMP ON ");
  }
  //if (distance < 26.17)
  if (distance < 24.6)
  {
    digitalWrite(relayPin, HIGH);
    display.println("");
    display.println(" PUMP OFF "); 
  }
  display.setTextSize(1); 
  display.println("sketch_jun29a");
  display.display();
  

  // put your main code here, to run repeatedly:
  delay(100);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
  display.clearDisplay();
  display.setCursor(0, 0);     // Start at top-left corner
  display.setTextSize(2);
  display.print("Distance = ");
  display.print(distance);
  display.print(" cm");
  display.println(" ");
  display.setTextSize(1); 
  display.println("sketch_jun29a");
  display.display();
  delay(500);
  watchdog.reset();
}

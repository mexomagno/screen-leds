#include <Arduino.h>
// La velocidad depende del modelo de ESP-01
// siendo habituales 9600 y 115200
const long baudRate = 9600;
 
#include "SoftwareSerial.h"
SoftwareSerial softSerial(2, 3); // RX, TX
 
void setup()
{
   Serial.begin(baudRate);
   softSerial.begin(baudRate);
   delay(5000);
}
 
void loop(){
   String in = "";
   boolean ready = false;

   while(softSerial.available()) {
      in = softSerial.readString();
      ready = true;
   }
   if (ready) {
      Serial.println("Receiving string"  + in);
   }
}

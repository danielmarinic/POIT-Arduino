#include <ArduinoJson.h>
#include <dht.h>


#define dht_apin A0 // Analog Pin sensor is connected to
#define led_dpin 8

dht DHT;
int led_enable = 0;
const char* led_color = "red";
DynamicJsonDocument doc(1024);
 
void setup() {
 
  Serial.begin(9600);
  delay(500);//Wait before accessing Sensor
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  delay(1000);//Wait before accessing Sensor
}
 
void loop(){
    DHT.read11(dht_apin);

    //print JSON
    Serial.print("{\"humidity\":");
    Serial.print(DHT.humidity);
    Serial.print(", \"temperature\":");
    Serial.print(DHT.temperature); 
    Serial.println("}");

    //riadenie LED prost. Serial input
    if(Serial.available() > 0) {
      String incoming_json = Serial.readString();
      deserializeJson(doc, incoming_json);
      const char* sensor = doc["sensor"];
      led_color = doc["led_color"];
      led_enable = doc["led_enabled"];
    }

    //turn on LED by color
    if(strcmp("red", led_color) == 0) {
      digitalWrite(8, led_enable);
      delay(100);
      digitalWrite(9, LOW);
      delay(100);
      digitalWrite(10, LOW);
      delay(1000);
    } else if (strcmp("green", led_color) == 0) {
      digitalWrite(9, led_enable);
      digitalWrite(8, LOW);
      delay(100);
      digitalWrite(10, LOW);
      delay(1000);
    } else if(strcmp("blue", led_color) == 0) {
      digitalWrite(10, led_enable);
      delay(100);
      digitalWrite(8, LOW);
      delay(100);
      digitalWrite(9, LOW);
      delay(1000);
    }

    
    delay(5000);//Wait 5 seconds before accessing sensor again. 
}

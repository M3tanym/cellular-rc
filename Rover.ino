#include <Servo.h>
// Steering range 1100 - 1900 (center 1500)
// Driving range 1100 -  1500 (fast to stop)
#define S_R 800
#define D_R 400
#define BIAS 1100

Servo servo, motor;

void setup() {
  Serial.begin(115200);
  
  servo.attach(A0);
  motor.attach(A1);
  pinMode(A2, INPUT);
}
boolean started = false;
boolean ended = false;
boolean sentVoltage = false;

String packet = "";

#define SOP '<'
#define EOP '>'

void loop() {
  while (Serial.available() > 0) {
    char inChar = Serial.read();
    if (inChar == SOP) {
      started = true;
    }
    else if (inChar == EOP) {
      ended = true;
      break;
    }
    else {
      if (started) {
        packet += inChar;
      }
    }
  }
  if (started && ended) {
    if (packet.length() <= 5 && packet.length() >= 3 && packet[1] == ':') {
      char type = packet[0];
      String data = packet.substring(2);
      int i = atoi(data.c_str());
//      Serial.print("val ");
//      Serial.print(type);
//      Serial.print(" = ");
//      Serial.println(i);
      if (type == 's') {
        int m = (int)(i/256.0 * S_R) + BIAS;
        servo.writeMicroseconds(m);
      }
      else if (type == 'd') {
        int m = (D_R - (int)(i/256.0 * D_R)) + BIAS;
        Serial.println(m);
        motor.writeMicroseconds(m);
      }
    }
    packet = "";
    started = false;
    ended = false;
  }

  if (millis() % 1000 == 0) {
    if (!sentVoltage) {
      float voltage = analogRead(A2) / 65.1; // conversion factor for voltage divider
      // something like ([(47 + 100) / 47] * [5.02/1023]) ^-1
      Serial.print("<v:");
      Serial.print(voltage);
      Serial.println(">");
      sentVoltage = true;
    }
  }
  else {
    sentVoltage = false;
  }
}

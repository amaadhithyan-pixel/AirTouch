#include <ESP32Servo.h>

const int RED_PIN = 25;
const int GREEN_PIN = 26;
const int BLUE_PIN = 27;
const int MOTOR_PIN = 14;
const int SERVO_PIN = 12;
const int BUZZER_PIN = 13;

const int LOCK_ANGLE = 0;
const int UNLOCK_ANGLE = 90;

Servo doorServo;
String inputBuffer = "";

void setup() {
  Serial.begin(9600);

  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  pinMode(MOTOR_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  doorServo.attach(SERVO_PIN);
  doorServo.write(LOCK_ANGLE);

  setLED(0, 0, 0);
  digitalWrite(MOTOR_PIN, LOW);

  Serial.println("AirTouch ESP32 ready.");
}

void loop() {
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n') {
      handleCommand(inputBuffer);
      inputBuffer = "";
    } else {
      inputBuffer += c;
    }
  }
}

void handleCommand(String cmd) {
  cmd.trim();

  if (cmd == "FAN_ON") {
    digitalWrite(MOTOR_PIN, HIGH);
    beep(1);
  } else if (cmd == "FAN_OFF") {
    digitalWrite(MOTOR_PIN, LOW);
    beep(1);
  } else if (cmd == "LED_RED") {
    setLED(255, 0, 0);
    beep(1);
  } else if (cmd == "LED_GREEN") {
    setLED(0, 255, 0);
    beep(1);
  } else if (cmd == "LED_BLUE") {
    setLED(0, 0, 255);
    beep(1);
  } else if (cmd == "LED_OFF") {
    setLED(0, 0, 0);
    beep(1);
  } else if (cmd == "LOCK_DOOR") {
    doorServo.write(LOCK_ANGLE);
    beep(2);
  } else if (cmd == "UNLOCK_DOOR") {
    doorServo.write(UNLOCK_ANGLE);
    beep(2);
  } else {
    Serial.println("ERR: Unknown command -> " + cmd);
    return;
  }

  Serial.println("OK: " + cmd);
}

void setLED(int r, int g, int b) {
  analogWrite(RED_PIN, r);
  analogWrite(GREEN_PIN, g);
  analogWrite(BLUE_PIN, b);
}

void beep(int times) {
  for (int i = 0; i < times; i++) {
    tone(BUZZER_PIN, 1000, 100);
    delay(150);
  }
}

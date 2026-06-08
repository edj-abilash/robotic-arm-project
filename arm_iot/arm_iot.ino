#include <Servo.h>

Servo s1, s2, s3, s4;

void setup() {
  Serial.begin(9600);
  s1.attach(9);
  s2.attach(10);
  s3.attach(11);
  s4.attach(6);

  s1.write(90); s2.write(90);
  s3.write(90); s4.write(90);

  Serial.println("ARM_READY");
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    // Expected format: S1:90  S2:45  S3:120  S4:60
    if (cmd.length() >= 4 && cmd[0] == 'S') {
      int servoNum = cmd[1] - '0';       // 1–4
      int angle = cmd.substring(3).toInt();
      angle = constrain(angle, 0, 180);

      if      (servoNum == 1) s1.write(angle);
      else if (servoNum == 2) s2.write(angle);
      else if (servoNum == 3) s3.write(angle);
      else if (servoNum == 4) s4.write(angle);

      Serial.print("OK:");
      Serial.println(cmd);
    }
  }
}
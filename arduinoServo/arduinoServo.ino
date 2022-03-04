#include <Servo.h> 

Servo servo; // servo object representing the MG 996R servo
Servo servo2; // servo object representing the MG 996R servo

int x;
int y;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  
  servo.attach(10); // servo is wired to Arduino on digital pin 10
  servo2.attach(9); // servo is wired to Arduino on digital pin 9
}

void loop() {
  while (!Serial.available());
  x = Serial.readString().toInt();
  Serial.println(x + 1);
  if (x == 1) {
    nod();
  }
  
  if (x == 2) {
    lookLeft();
  }
  
  if (x == 3) {
    lookRight();
  }
  
  if (x == 4) {
    lookStraight();
  }
  
}

void nod () {
  servo2.write(135); // move MG996R's shaft to angle 0°
  delay(200); // wait for one second
  
  servo2.write(70); // move MG996R's shaft to angle 0°
  delay(200); // wait for one second
  
  servo2.write(90); // move MG996R's shaft to angle 0°
  delay(200); // wait for one second
}

void lookLeft () {
  servo.write(180); // move MG996R's shaft to angle 0°
  delay(500); // wait for one second
}

void lookRight () {
  servo.write(0); // move MG996R's shaft to angle 0°
  delay(500); // wait for one second
}

void lookStraight () {
  servo.write(90); // move MG996R's shaft to angle 0°
  servo2.write(90); // move MG996R's shaft to angle 0°
}
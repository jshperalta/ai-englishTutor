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
  
  pinMode(11, OUTPUT);    // sets the digital pin 13 as output
  pinMode(12, OUTPUT);    // sets the digital pin 13 as output

  digitalWrite(11, HIGH); // sets the digital pin 13 on
  digitalWrite(12, HIGH); // sets the digital pin 13 on
}

void loop() {
  while (!Serial.available());
  x = Serial.readString().toInt();
  Serial.println(x);
 
  
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
  
  if (x == 5) {
    lookUp();
  }
  
  if (x == 6) {
    lookDown();
  }
  
  if (x == 7) {
    notNod();
  }
  
  if (x == 11) {
    ledWhite();
  }
  
  if (x == 12) {
    ledBlue();
  }
  
  if (x == 13) {
    ledOff();
  }
  
  if (x == 14) {
    ledAll();
  }
}


void ledAll() {
  digitalWrite(11, HIGH); // sets the digital pin 13 on
  digitalWrite(12, HIGH); // sets the digital pin 13 on
  delay(300); // wait for one second
}

void ledOff (){
  digitalWrite(11, LOW); // sets the digital pin 13 on
  digitalWrite(12, LOW);  // sets the digital pin 13 off
}

void ledWhite (){
  digitalWrite(11, HIGH); // sets the digital pin 13 on
  digitalWrite(12, LOW);  // sets the digital pin 13 off
}

void ledBlue (){
  digitalWrite(12, HIGH); // sets the digital pin 13 on
  digitalWrite(11, LOW);  // sets the digital pin 13 off
}

void nod () {
  lookStraight();
  lookUp();
  lookDown();
  lookStraight();
}

void notNod () {
  lookStraight();
  lookLeft();
  lookRight();
  lookStraight();
}


void lookUp () {
  servo2.write(120); // move MG996R's shaft to angle 0°
  delay(350); // wait for one second
}

void lookDown () {
  servo2.write(70); // move MG996R's shaft to angle 0°
  delay(350); // wait for one second
}

void lookLeft () {
  servo.write(140); // move MG996R's shaft to angle 0°
  delay(350); // wait for one second
}

void lookRight () {
  servo.write(40); // move MG996R's shaft to angle 0°
  delay(350); // wait for one second
}

void lookStraight () {
  servo.write(90); // move MG996R's shaft to angle 0°
  servo2.write(90); // move MG996R's shaft to angle 0°
  delay(350); // wait for one second
}

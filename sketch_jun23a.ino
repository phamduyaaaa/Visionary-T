
#define Buzzer 3
int Sensor = A1;
void setup()
{
  Serial.begin(9600);
  pinMode (Buzzer, OUTPUT);
}
void loop()
{
  int value = analogRead (Sensor);
  Serial.print("gia tri cam bien: ");
  Serial.println(value);
  if (value> 400){
  digitalWrite(Buzzer, HIGH);
  } else {
  digitalWrite (Buzzer, LOW);
  }
} 
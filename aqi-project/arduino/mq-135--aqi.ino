int sensorPin=A0;
int sensorData;
void setup()
{  
  Serial.begin(9600);   
  pinMode(sensorPin,INPUT);                         
 }
void loop()
{
  sensorData = analogRead(sensorPin);       
  Serial.print("Air Quality Index: ");
  Serial.println(sensorData);               
  delay(5000);                                   
}
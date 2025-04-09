
int sensorData;
void setup()
{  
  Serial.begin(9600);   
  pinMode(0,INPUT);                         
 }
void loop()
{
  sensorData = analogRead(0);       
  Serial.println(sensorData);               
  delay(5000);                                   
}
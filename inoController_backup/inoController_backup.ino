const int MAGNET_1 = 9;
const int MAGNET_2 = 6;

void setup() {
  //Serial.begin(9600);
}

void loop() {
  // Wait for data from Raspberry Pi
  // while (!Serial.available()) {
  //   // Do nothing until data is received
  // }


  // static int duration  = 10000;

  // // Read the data from Raspberry Pi
  // String values = Serial.readStringUntil('\n');
  // values.trim();

  // // Extract the two values
  // int commaIndex = values.indexOf(',');
  // String value1Str = values.substring(0, commaIndex);
  // String value2Str = values.substring(commaIndex + 1);
  // int delay = value1Str.toInt();
  // int max_pwm = value2Str.toInt();

  // // Print the received values
  // Serial.print(delay);
  // Serial.print(",");
  // Serial.println(max_pwm);
  int delay = 50;
  int max_pwm = 25;
  int duration = 10000; 

  run_magnet_increase(delay, max_pwm);

  // Signal Raspberry Pi that it can send the next values
  Serial.println("Ready");
}

void run_magnet_increase(int delayVal, int max_pwm){
  static int ts = millis();
  int duration = 10000;

	while(millis() - ts < duration ){
      analogWrite(MAGNET_1, max_pwm);
  }

		
	
}

void run_magnet_steady(int delayVal, int max_pwm, int duration){
	static int ts = millis();

	while(millis() - ts < duration){
		analogWrite(MAGNET_1, max_pwm);
	}

}


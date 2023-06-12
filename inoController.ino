void setup() {
  Serial.begin(9600);
}

void loop() {
  // Wait for data from Raspberry Pi
  while (!Serial.available()) {
    // Do nothing until data is received
  }

  // Read the data from Raspberry Pi
  int value = Serial.parseInt();

  // Print the received value
  Serial.println(value);

  // Signal Raspberry Pi that it can send the next number
  Serial.println("Ready");
}

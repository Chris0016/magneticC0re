const int MAGNET_1 = 9;
const int MAGNET_2 = 6;

//states

typedef enum state_t {
  S_READ,          // 0
  S_RUNNING,       // 1
  S_HOLD_MAX_PWM,  // 2
  S_IDLE,          //3

};

static state_t state = S_READ;

//Having a delay as curr_pwm changes towards  target_pwm makes the transition between values smoother and more visible to the user(TO BE TESTED)
static int delay_value = 100;

static int prev_pwm_target = 0;
static int curr_pwm_target = 0;
static int curr_pwm = 0;

static int flag = 1;  //Used for either moving up or down in pwm

static int TARGET_PWM_HOLD_DURATION = 7000;  //Milliseconds, subject to change TODO tunning
static int IDLE_DURATION = 5000;

unsigned long ts = millis();



void setup() {
  pinMode(MAGNET_1, OUTPUT);
  Serial.begin(9600);
 
}

void loop() {

  Serial.println("state " + String(state));


  switch (state) {
    case S_READ:
      {
        // Signal Raspberry Pi that it can send the next values
        Serial.println("Ready");

         //Maybe remove?
          while (!Serial.available()) {
          }
          //Maybe remove?

        // Read the data from Raspberry Pi
        String values = Serial.readStringUntil('\n');
        values.trim();


        // Extract the two values
        int commaIndex = values.indexOf(',');
        String value1Str = values.substring(0, commaIndex);
        String value2Str = values.substring(commaIndex + 1);


        //using only curr_pwm & target_pwm is not explicit when comparing them for switching flag
        // if only using curr_pwm & target_pwm then:
        //    on flag switch target_pwm means the "current value"(vs the "previous"(curr_pwm) )
        //    target_pwm also means what curr_pwm is trying to reach in the other cases

        prev_pwm_target = curr_pwm_target;

        delay_value = value1Str.toInt();  //To be deleted? better or worse to have constant delay??
        curr_pwm_target = value2Str.toInt();

        /*
        Implementing sophisticated logic to switch becomes to eleborate
       
        Because you can have consecutive values less than then don't switch flag if it's -1 already. 
        Same goes for consecutive values that are greater than the previous. 

        if (curr_pwm_target < prev_pwm_target && flag == 1 )
          flag = -1
        else if (curr_pwm_target > prev_pwm_target && flag == -1 )
          flag = 1

        Below is a rudamentary but faster solution
      */

        state = S_RUNNING;
        int diff = curr_pwm_target - prev_pwm_target;

        if (diff > 0)
          flag = 1;
        else if (diff < 0)
          flag = -1;
        else
          state = S_HOLD_MAX_PWM;

        //Cannot set first timer for delay within the S_RUNNING case
        ts = millis();
      }
      break;

    case S_RUNNING:
      {

        analogWrite(MAGNET_1, curr_pwm);
        while ( (unsigned long)(millis() - ts) < delay_value) {
        }

        curr_pwm += flag;

        if ((curr_pwm_target == curr_pwm && flag == 1) || (curr_pwm_target == curr_pwm && flag == -1)) {
          state = S_HOLD_MAX_PWM;
        }

        ts = millis();
      }
      break;

    case S_HOLD_MAX_PWM:
      {
        //Serial.println("STATE HOLD");
        analogWrite(MAGNET_1, curr_pwm);
        if ( (unsigned long)(millis() - ts) > TARGET_PWM_HOLD_DURATION) {
          state = S_IDLE;
          ts = millis();  //TESTING
        }
        break;
      }
    case S_IDLE:
      {
        analogWrite(MAGNET_1, 0);
        while (  (unsigned long) (millis() - ts) < IDLE_DURATION) {
          //do nothing
        }
        ts = millis();
        state = S_READ;
      }
      break;
    default:
      {
        state = S_RUNNING;
        //Serial.println("DEFAULT");
      }
      break;
  }

  Serial.print(delay_value);
  Serial.print(",");
  Serial.print(curr_pwm_target);
  Serial.print(",");
  Serial.print(curr_pwm);
  Serial.print(",");
  Serial.print(String(flag));
  Serial.println(String(ts));
}

//void run_magnet_increase(int delayVal, int max_pwm){
//
//  for(int i = 0; i < max_pwm; i++){
//    analogWrite(MAGNET_1, i);
//    delay(delayVal);
//  }
//}
//
//
//void run_magnet_steillis();
//
//  while(millis() - ts < duration){
//    analogWrite(MAGNET_1, max_pwm);
//    delay(delayVal);
//  }
//
//}

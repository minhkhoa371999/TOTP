// GetCode.ino
// 
// Basic example for the TOTP library
//
// This example uses the opensource SwRTC library as a software real-time clock
// you can download from https://github.com/leomil72/swRTC
// for real implementation it's suggested the use of an hardware RTC

#include "sha1.h"
#include "TOTP.h"
#include "swRTC.h"

// The shared secret is 3799361033KKD
uint8_t hmacKey[] = {0x33, 0x37, 0x39, 0x39, 0x33, 0x36, 0x31, 0x30, 0x33, 0x33, 0x4b, 0x4b, 0x44};

TOTP totp = TOTP(hmacKey, 13);
swRTC rtc;
char code[7];


void setup() {
  
  Serial.begin(9600);
  rtc.stopRTC();
  
  // Adjust the following values to match the current date and time
  // and power on Arduino at the time set (use GMT timezone!)
  rtc.setDate(12, 04, 2023);
  rtc.setTime(7, 00, 00);
  
  rtc.startRTC();
}

void loop() {

  long GMT = rtc.getTimestamp();
  char* newCode = totp.getCode(GMT);
  if(strcmp(code, newCode) != 0) {
    strcpy(code, newCode);
    Serial.println(code);
  }  
}

#include <Adafruit_BusIO_Register.h>
#include <Adafruit_I2CDevice.h>
#include <Adafruit_I2CRegister.h>
#include <Adafruit_SPIDevice.h>

#include <LiquidCrystal_I2C.h>
#include <SimpleHMAC.h>
#include <SimpleHOTP.h>
#include <SimpleSHA1.h>
#include <TOTP.h>
#include <RTClib.h>
#include<swRTC.h>
LiquidCrystal_I2C lcd(0x27,16,2); 

// The shared secret is MyLegoDoor
uint8_t hmacKey[] = {0x4d, 0x79, 0x4c, 0x65, 0x67, 0x6f, 0x44, 0x6f, 0x6f, 0x72};
TOTP totp = TOTP(hmacKey, 10);
swRTC rtc;
char code[7];


void setup() {
  lcd.init();                    
  lcd.backlight();
  Serial.begin(9600);
  rtc.stopRTC();
  
  // Adjust the following values to match the current date and time
  // and power on Arduino at the time set (use GMT timezone!)
  rtc.setDate(22, 03, 2023);
  rtc.setTime(06, 00, 00);
  rtc.startRTC();
}

void loop() {

  long GMT = rtc.getTimestamp();
  char* newCode = totp.getCode(GMT);
  lcd.setCursor(6,0);//Di chuyển con trỏ đến cột tương ứng
  lcd.print("OTP:");//Xuất ra màn hình từ vị trí con trỏ
  lcd.setCursor(5,1);
  if(strcmp(code, newCode) != 0) 
  {
    strcpy(code, newCode);
    lcd.print(code);
  } 
}

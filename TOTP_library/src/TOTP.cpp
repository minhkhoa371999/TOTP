// OpenAuthentication Time-based One-time Password Algorithm (RFC 6238)
// For the complete description of the algorithm see
// http://tools.ietf.org/html/rfc4226#section-5.3
//
// Luca Dentella (http://www.lucadentella.it)

#include "TOTP.h"
#include "sha1.h"


// Tao thu vien bang khoa bi mat va thoi gian T 
TOTP::TOTP(uint8_t* hmacKey, int keyLength, int timeStep) {

	_hmacKey = hmacKey;
	_keyLength = keyLength;
	_timeStep = timeStep;
};


// khoi tao thu vien bang khoa rieng, do dai khoa va thoi gian thay doi 30s  
TOTP::TOTP(uint8_t* hmacKey, int keyLength) {

	_hmacKey = hmacKey;
	_keyLength = keyLength;
	_timeStep = 30;
};

// Generate a code, using the timestamp provided
char* TOTP::getCode(long timeStamp) {
	
	long steps = timeStamp / _timeStep;
	return getCodeFromSteps(steps);
}

// Generate a code, using the number of steps provided
// 
char* TOTP::getCodeFromSteps(long steps) {
	
	// STEP 0, map the number of steps in a 8-bytes array (counter value)
	// anh xa so buoc trong mang 8 bytes 
	_byteArray[0] = 0x00;
	_byteArray[1] = 0x00;
	_byteArray[2] = 0x00;
	_byteArray[3] = 0x00;
	_byteArray[4] = (int)((steps >> 24) & 0xFF);
	_byteArray[5] = (int)((steps >> 16) & 0xFF);
	_byteArray[6] = (int)((steps >> 8) & 0XFF);
	_byteArray[7] = (int)((steps & 0XFF));
	
	// STEP 1, 
	// lay ham bam HMAC tu bo dem khoa 
	Sha1.initHmac(_hmacKey, _keyLength);
	Sha1.write(_byteArray, 8);
	_hash = Sha1.resultHmac();
	
	// STEP 2, 
	// su dung truncate de cat lay chuoi 4 byte 
	_offset = _hash[20 - 1] & 0xF; 
	_truncatedHash = 0;
	for (int j = 0; j < 4; ++j) {
		_truncatedHash <<= 8;
		_truncatedHash  |= _hash[_offset + j];
	}

	// STEP 3, 
	// Tinh gia tri OTP 
	_truncatedHash &= 0x7FFFFFFF;
	_truncatedHash %= 1000000;
	
	// Chuyen doi gia tri trong chuoi 
	sprintf(_code, "%06ld", _truncatedHash);
	return _code;
}

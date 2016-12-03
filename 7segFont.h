/*
 * _7segFont.h
 *
 * Created: 2015-11-11 19:17:55
 *  Author: Emaus
 */ 


#ifndef SEVSEGFONT_H_
#define SEVSEGFONT_H_

char ASCII_2_7Seg(const uint8_t BYTE);

char ASCII_2_7Seg(const uint8_t BYTE) {
	char r = 0;
	switch (BYTE) {
		case '0':
			r = 0x7E;
			break;
		case '1':
			r = 0x30;
			break;
		case '2':
			r = 0x6D;
			break;
		case '3':
			r = 0x79;
			break;
		case '4':
			r = 0x33;
			break;
		case '5':
			r = 0x5B;
			break;
		case '6':
			r = 0x5F;
			break;
		case '7':
			r = 0x70;
			break;
		case '8':
			r = 0x7F;
			break;
		case '9':
			r = 0x7B;
			break;
		case 'A':
			r = 0x77;
			break;
		case 'B':
			r = 0x1F;
			break;
		case 'C':
			r = 0x4E;
			break;
		case 'D':
			r = 0x3D;
			break;
		case 'E':
			r = 0x4F;
			break;
		case 'F':
			r = 0x47;
			break;
		case 'G':
			r = 0x7B;
			break;
		case 'H':
			r = 0x17;
			break;
		case 'I':
			r = 0x06;
			break;
		case 'J':
			r = 0x3C;
			break;
		case 'K':
			r = 0x07;
			break;
		case 'L':
			r = 0x0E;
			break;
		case 'M':
			r = 0x76;
			break;
		case 'N':
			r = 0x15;
			break;
		case 'O':
			r = 0x1D;
			break;
		case 'P':
			r = 0x67;
			break;
		case 'Q':
			r = 0x6B;
			break;
		case 'R':
			r = 0x05;
			break;
		case 'S':
			r = 0x5B;
			break;
		case 'T':
			r = 0x0F;
			break;
		case 'U':
			r = 0x9C;
			break;
		case 'V':
			r = 0x1C;
			break;
		case 'W':
			r = 0x3F;
			break;
		case 'X':
			r = 0x37;
			break;
		case 'Y':
			r = 0x3B;
			break;
		case 'Z':
			r = 0x6D;
			break;
	}
	return r;
}

#endif /* 7SEGFONT_H_ */
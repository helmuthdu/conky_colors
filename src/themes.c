#define _ISOC99_SOURCE // for snprintf
#include <string.h>
#include <stdio.h>
#include "themes.h"
#include "variables.h"

int 	radiance=0, ambiance=0, elementary=0, custom=0,
		dark=0, black=0, white=0;

char 	theme[31],
		defaultcolor[31],
		color0[31],
		color1[31],
		color2[31],
		color3[31],
		color4[31];

//Themes
void themes () {
	if(strcmp("brave",theme) == 0) {
		snprintf(color1, 31, "3465A4");
		snprintf(color3, 31, "204A87");
		snprintf(color4, 31, "3465A4 204A87");
	}
	else
		if(strcmp("black",theme) == 0) {
			snprintf(color1, 31, "1E1C1A");
			snprintf(color3, 31, "1E1C1A");
			snprintf(color4, 31, "1E1C1A");
		}
	else
		if(strcmp("white",theme) == 0) {
			snprintf(color1, 31, "FFFFFF");
			snprintf(color3, 31, "FFFFFF");
			snprintf(color4, 31, "FFFFFF");
		}
	else
		if(strcmp("dust",theme) == 0) {
			snprintf(color1, 31, "906E4C");
			snprintf(color3, 31, "745536");
			snprintf(color4, 31, "906E4C 745536");
		}
	else
		if(strcmp("illustrious",theme) == 0) {
			snprintf(color1, 31, "DC6472");
			snprintf(color3, 31, "C6464B");
			snprintf(color4, 31, "DC6472 C6464B");
		}
	else
		if(strcmp("noble",theme) == 0) {
			snprintf(color1, 31, "77507b");
			snprintf(color3, 31, "5C3566");
			snprintf(color4, 31, "77507B 5C3566");
		}
	else
		if(strcmp("wine",theme) == 0) {
			snprintf(color1, 31, "C22F2F");
			snprintf(color3, 31, "A40000");
			snprintf(color4, 31, "C22F2F A40000");
		}
	else
		if(strcmp("wise",theme) == 0) {
			snprintf(color1, 31, "709937");
			snprintf(color3, 31, "51751E");
			snprintf(color4, 31, "709937 51751E");
		}
	else
		if(strcmp("carbonite",theme) == 0) {
			snprintf(color1, 31, "555753");
			snprintf(color3, 31, "2E3436");
			snprintf(color4, 31, "555753 2E3436");
		}
	else
		if(strcmp("tribute",theme) == 0) {
			snprintf(color1, 31, "9C9E8A");
			snprintf(color3, 31, "7D7E60");
			snprintf(color4, 31, "9C9E8A 7D7E60");
		}
	else
		if(strcmp("blue",theme) == 0) {
			snprintf(color1, 31, "1E90FF");
			snprintf(color3, 31, "0084C8");
			snprintf(color4, 31, "1E90FF 0084C8");
		}
	else
		if(strcmp("red",theme) == 0) {
			snprintf(color1, 31, "FF4141");
			snprintf(color3, 31, "DC0000");
			snprintf(color4, 31, "FF4141 DC0000");
		}
	else
		if(strcmp("orange",theme) == 0) {
			snprintf(color1, 31, "FFAC0B");
			snprintf(color3, 31, "FF9900");
			snprintf(color4, 31, "FFAC0B FF9900");
		}
	else
		if(strcmp("green",theme) == 0) {
			snprintf(color1, 31, "CCFF42");
			snprintf(color3, 31, "9ADE00");
			snprintf(color4, 31, "CCFF42 9ADE00");
		}
	else
		if(strcmp("purple",theme) == 0) {
			snprintf(color1, 31, "E296FF");
			snprintf(color3, 31, "D76CFF");
			snprintf(color4, 31, "E296FF D76CFF");
		}
	else
		if(strcmp("cyan",theme) == 0) {
			snprintf(color1, 31, "30B6BF");
			snprintf(color3, 31, "0E97B9");
			snprintf(color4, 31, "30B6BF 0E97B9");
		}
	else
		if(strcmp("radiance",theme) == 0) {
			snprintf(color0, 31, "292927");
			snprintf(color1, 31, "CCCCCC");
			snprintf(color2, 31, "292927");
    		snprintf(color3, 31, "AEA79F");
			snprintf(color4, 31, "CCCCCC AEA79F");
		}
	else
		if(strcmp("ambiance",theme) == 0) {
			snprintf(color0, 31, "F0EBE2");
			snprintf(color1, 31, "77216F");
			snprintf(color2, 31, "E6E6E6");
			snprintf(color3, 31, "2C001E");
			snprintf(color4, 31, "77216F 2C001E");
		}
	else
		if(strcmp("elementary",theme) == 0) {
			snprintf(color0, 31, "F2F2F2");
			snprintf(color1, 31, "7296BB");
			snprintf(color2, 31, "FFFFFF");
    		snprintf(color3, 31, "7296BB");
			snprintf(color4, 31, "7296BB 7296BB");
		}
	else
		if(custom == True)
			snprintf(color3, 31, "%s", color1);
	else {
		snprintf(color1, 31, "CE5C00 ");
		snprintf(color3, 31, "E07A1F");
		snprintf(color3, 31, "CE5C00");
		snprintf(color4, 31, "E07A1F CE5C00");
	}
}


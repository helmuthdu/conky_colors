#define _ISOC99_SOURCE // for snprintf
#include <string.h>
#include <stdio.h>
#include "themes.h"
#include "variables.h"

int 	radiance=0, ambiance=0, elementary=0, custom=0,
		dark=0, alldark=0, alllight=0;

char 	theme[31],
		defaultcolor[31],
		color0[31],
		color1[31],
		color2[31],
		color3[31];

//Themes
void themes () {
	if(strcmp("brave",theme) == 0) {
		snprintf(color1, 31, "3465A4");
		if (alldark == True)
			snprintf(color3, 31, "1E1C1A 1E1C1A");
		else
			if (alllight == True)
				snprintf(color3, 31, "white white");
			else
				snprintf(color3, 31, "204A87 3465A4");
	}
	else
		if(strcmp("dust",theme) == 0) {
			snprintf(color1, 31, "906E4C");
		if (alldark == True)
			snprintf(color3, 31, "1E1C1A 1E1C1A");
		else
			if (alllight == True)
				snprintf(color3, 31, "white white");
			else
				snprintf(color3, 31, "745536 906E4C");
		}
	else
		if(strcmp("illustrious",theme) == 0) {
			snprintf(color1, 31, "dc6472");
		if (alldark == True)
			snprintf(color3, 31, "1E1C1A 1E1C1A");
		else
			if (alllight == True)
				snprintf(color3, 31, "white white");
			else
				snprintf(color3, 31, "C6464B DC6472");
		}
	else
		if(strcmp("noble",theme) == 0) {
			snprintf(color1, 31, "77507b");
		if (alldark == True)
			snprintf(color3, 31, "1E1C1A 1E1C1A");
		else
			if (alllight == True)
				snprintf(color3, 31, "white white");
			else
				snprintf(color3, 31, "5C3566 77507B");
		}
	else
		if(strcmp("wine",theme) == 0) {
			snprintf(color1, 31, "C22F2F");
		if (alldark == True)
			snprintf(color3, 31, "1E1C1A 1E1C1A");
		else
			if (alllight == True)
				snprintf(color3, 31, "white white");
			else
				snprintf(color3, 31, "A40000 C22F2F");
		}
	else
		if(strcmp("wise",theme) == 0) {
			snprintf(color1, 31, "709937");
		if (alldark == True)
			snprintf(color3, 31, "1E1C1A 1E1C1A");
		else
			if (alllight == True)
				snprintf(color3, 31, "white white");
			else
				snprintf(color3, 31, "51751E 709937");
		}
	else
		if(strcmp("carbonite",theme) == 0) {
			snprintf(color1, 31, "555753");
		if (alldark == True)
			snprintf(color3, 31, "1E1C1A 1E1C1A");
		else
			if (alllight == True)
				snprintf(color3, 31, "white white");
			else
				snprintf(color3, 31, "2E3436 555753");
		}
	else
		if(strcmp("tribute",theme) == 0) {
			snprintf(color1, 31, "9C9E8A");
		if (alldark == True)
			snprintf(color3, 31, "1E1C1A 1E1C1A");
		else
			if (alllight == True)
				snprintf(color3, 31, "white white");
			else
				snprintf(color3, 31, "7D7E60 9C9E8A");
		}
	else
		if(strcmp("blue",theme) == 0) {
			snprintf(color1, 31, "1E90FF");
		if (alldark == True)
			snprintf(color3, 31, "1E1C1A 1E1C1A");
		else
			if (alllight == True)
				snprintf(color3, 31, "white white");
			else
				snprintf(color3, 31, "1E90FF 0084C8");
		}
	else
		if(strcmp("red",theme) == 0) {
			snprintf(color1, 31, "DC0000");
		if (alldark == True)
			snprintf(color3, 31, "1E1C1A 1E1C1A");
		else
			if (alllight == True)
				snprintf(color3, 31, "white white");
			else
				snprintf(color3, 31, "DC0000 FF4141");
		}
	else
		if(strcmp("orange",theme) == 0) {
			snprintf(color1, 31, "FFAC0B");
		if (alldark == True)
			snprintf(color3, 31, "1E1C1A 1E1C1A");
		else
			if (alllight == True)
				snprintf(color3, 31, "white white");
			else
				snprintf(color3, 31, "FFAC0B FF9900");
		}
	else
		if(strcmp("green",theme) == 0) {
			snprintf(color1, 31, "9ADE00");
		if (alldark == True)
			snprintf(color3, 31, "1E1C1A 1E1C1A");
		else
			if (alllight == True)
				snprintf(color3, 31, "white white");
			else
				snprintf(color3, 31, "9ADE00 CCFF42");
		}
	else
		if(strcmp("grey",theme) == 0) {
			snprintf(color1, 31, "CCCCCC");
		if (alldark == True)
			snprintf(color3, 31, "1E1C1A 1E1C1A");
		else
			if (alllight == True)
				snprintf(color3, 31, "white white");
			else
				snprintf(color3, 31, "CCCCCC CCCCCC");
		}
	else
		if(strcmp("purple",theme) == 0) {
			snprintf(color1, 31, "D76CFF");
		if (alldark == True)
			snprintf(color3, 31, "1E1C1A 1E1C1A");
		else
			if (alllight == True)
				snprintf(color3, 31, "white white");
			else
				snprintf(color3, 31, "D76CFF F1CAFF");
		}
	else
		if(strcmp("radiance",theme) == 0) {
			snprintf(color0, 31, "292927");
			snprintf(color1, 31, "C6B9A6");
			snprintf(color2, 31, "292927");
			snprintf(color3, 31, "C6B9A6 C6B9A6");
		}
	else
		if(strcmp("ambiance",theme) == 0) {
			snprintf(color0, 31, "F0EBE2");
			snprintf(color1, 31, "FF6666");
			snprintf(color2, 31, "E6E6E6");
			snprintf(color3, 31, "CD646B F56F6E");
		}
	else
		if(strcmp("elementary",theme) == 0) {
			snprintf(color0, 31, "F2F2F2");
			snprintf(color1, 31, "7296BB");
			snprintf(color2, 31, "FFFFFF");
			snprintf(color3, 31, "7296BB 7296BB");
		}
	else
		if(custom == True)
			snprintf(color3, 31, color1);
	else {
		snprintf(color1, 31, "E07A1F");
		if (alldark == True)
			snprintf(color3, 31, "1E1C1A 1E1C1A");
		else
			if (alllight == True)
				snprintf(color3, 31, "white white");
			else
				snprintf(color3, 31, "CE5C00 E07A1F");
	}
}


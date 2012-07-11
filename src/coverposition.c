#include "coverposition.h"
#include "variables.h"

//Cover Position
void coverposition () {
	if (cpu == 1)
		yc += 126;
	else {
		yc += 112;
		for (i = 1; i <= cpu; i++)
		yc += 12;
	}
	if (aptget == True)
		yc += 13;
	if (gmail == True)
		yc += 13;
	if (set_battery == True)
		yc += 14;
	if (swap == True)
		yc += 31;
	if (set_process == True) {
		yc += 14;
		for (i = True; i <= proc; i++)
		yc += 12;
	}
	if (nodata == False) {
		if (clocktype == 1)
			yc += 150;
			else
				if (clocktype == 2)
					yc += 168;
			else
				if (clocktype == 3)
					yc += 58;
			else
				if (clocktype == 4)
					yc += 78;
			else
				if (clocktype == 5)
					yc += 60;
			else
				if (clocktype == 6)
					yc += 28;
			else
				yc += 62;
		if (set_calendar > 0)
			yc += 70;
	}
	if (set_photo == 1 || set_photo == 2) {
		yc += 132;
	}
	if (cover == 3 || cover == 6 || cover == 7)
		yc -= 2;
}


void coverposition_cairo () {
	if (cpu == 1 || cputype == True)
		yc += 278;
	else {
		yc += 214;
		for (i = 1; i <= cpu; i++)
			yc += 64;
	}
	if (swap == True)
		yc += 64;
	if (clocktype == 7)
		yc += 64;
	else if(clocktype == 8)
		yc += 104;

}

void coverposition_ring () {
	if (cpu > 2)
		yc += 64;
	yc += 447;
}

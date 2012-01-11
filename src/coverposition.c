#include "coverposition.h"
#include "variables.h"

//Cover Position
void coverposition () {
	if (cpu == 1)
		yc += 139;
	else {
		yc += 125;
		for (i = 1; i <= cpu; i++)
		yc += 12;
	}
	if (aptget == True)
		yc += 13;
	if (gmail == True && pidgin == False)
		yc += 13;
	if (set_battery == True)
		yc += 18;
	if (swap == True)
		yc += 31;
	if (set_process == True) {
		yc += 18;
		for (i = True; i <= proc; i++)
		yc += 12;
	}
	if (nodata == False) {
		if (clocktype == 1)
			yc += 156;
			else
				if (clocktype == 2)
					yc += 174;
			else
				if (clocktype == 3)
					yc += 65;
			else
				if (clocktype == 4)
					yc += 84;
			else
				if (clocktype == 5)
					yc += 63;
			else
				if (clocktype == 6)
					yc += 32;
			else
				yc += 68;
		if (set_calendar > 0)
			yc += 82;
	}
	if (set_photo == 1 || set_photo == 2) {
		yc += 142;
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

#include "photoposition.h"
#include "variables.h"

//Photo Position
void photoposition () {
	if (cpu == 1)
		yp += 124;
	else {
		yp += 108;
		for (i = True; i <= cpu; i++)
		yp += 12;
	}
	if (aptget == True)
		yp += 13;
	if (gmail == True && pidgin == False)
		yp += 13;
	if (set_battery == True)
		yp += 18;
	if (swap == True)
		yp += 30;
	if (set_process == True) {
		yp += 18;
		for (i = True; i <= proc; i++)
		yp += 12;
	}
	if (nodata == False) {
		if (clocktype == 1)
			yp += 156;
			else
				if (clocktype == 2)
					yp += 174;
			else
				if (clocktype == 3)
					yp += 65;
			else
				if (clocktype == 4)
					yp += 84;
			else
				if (clocktype == 5)
					yp += 63;
			else
				if (clocktype == 6)
					yp += 32;
			else
				yp += 68;
		if (set_calendar > 0)
			yp += 82;
	}
}


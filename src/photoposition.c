#include "photoposition.h"
#include "variables.h"

//Photo Position
void photoposition () {
    if (cpu == 1)
        yp += 116;
    else {
        yp += 100;
        for (i = True; i <= cpu; i++)
            yp += 12;
    }
    if (aptget == True)
        yp += 13;
    if (gmail == True)
        yp += 13;
    if (set_battery == True)
        yp += 14;
    if (swap == True)
        yp += 30;
    if (set_process == True) {
        yp += 14;
        for (i = True; i <= proc; i++)
            yp += 12;
    }
    if (nodata == False) {
        if (clocktype == 1)
            yp += 150;
        else
            if (clocktype == 2)
                yp += 168;
        else
            if (clocktype == 3)
                yp += 58;
        else
            if (clocktype == 4)
                yp += 78;
        else
            if (clocktype == 5)
                yp += 60;
        else
            if (clocktype == 6)
                yp += 28;
        else
            yp += 62;
        if (set_calendar > 0)
            yp += 68;
    }
}

#include "variables.h"

int 	i, True=1, False=0;

int 	cpu=1, cputemp=0, cputype=0,
		aptget=0,
		proc=0, set_process=0,
		swap=0,
		set_battery=0, battery_value=0,
		nodata=0, clocktype=0, set_calendar=0, clock_12h=0,
		nvidia=0,
		set_hd=0, hdtype=0, hdtemp1=0, hdtemp2=0, hdtemp3=0, hdtemp4=0,
		mpd=0, rhythmbox=0, banshee=0, clementine=0,cover=0, covergloobus=0,
		set_photo=0,
		gmail=0,
		todo=0,
		bbccode=3849, set_weather=0, unit=0,
		set_network=0, set_wireless=0, eth=0, wlan=0, ppp=0,
		logo=0,
		go2=32, yp=0, yc=0,
		board=0, slim=0, nobg=0, posfix=0,
		cairo_set=0, ring=0,
		sls=0,
		argb_value=ARGB_VALUE;

float	board_width=0, board_height=0;

char 	player[32],
		side[32],
		weather_code[32], imperial[32],
		logo_letter[32],
		user[32], password[32],
		dev1[32], dev2[32], dev3[32], dev4[32];

const char *datadir=0;

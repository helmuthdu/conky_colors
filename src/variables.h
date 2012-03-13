#ifndef _variables_
#define _variables_

extern int 	i, True, False;

extern int		cpu, cputemp, cputype,
				aptget,
				proc, set_process,
				swap,
				set_battery, battery_value,
				nodata, clocktype, set_calendar, clock_12h,
				nvidia,
				set_hd, hdtype, hdtemp1, hdtemp2, hdtemp3, hdtemp4,
				mpd, rhythmbox, banshee, exaile, clementine, cover, covergloobus,
				set_photo,
				pidgin, limit, gmail,
				todo,
				bbccode, set_weather, unit,
				set_network, set_wireless, eth, wlan, ppp,
				logo,
				go2, yp, yc,
				board, slim, nobg, posfix,
				cairo_set, ring,
				sls,
				argb_value;

extern float	board_width, board_height;

extern char 	player[32],
				side[32],
				weather_code[32], imperial[32],
				logo_letter[32],
				user[32], password[32],
				dev1[32], dev2[32], dev3[32], dev4[32];

extern const char *datadir;

#define LEN_CHAR 256
#define ARGB_VALUE 180

#endif // #ifndef _variables_


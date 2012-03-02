#include <stdio.h>
#include <stdlib.h>
#include "conkyforecast.h"
#include "themes.h"
#include "translations.h"
#include "variables.h"
#include "utils.h"
#include "finddir.h"

//Create and write conkyForecast.template
void conkyforecast () {

	FILE *fp;

	fp = fopenf("%s/conkyForecast.template", "w", tempdir());
	if(fp == 0)
	{
		printf("Failed to open %s/conkyForecast.template with write permission", tempdir());
		return;
	}

	fprintf(fp,"${voffset -10}${alignr 56}${color2}${font ConkyWeather:style=Bold:size=40}[--datatype=WF]${font}${color}\n");
	fprintf(fp,"${voffset -50}${color2}${font Weather:size=40}y${font}${color2}  ${voffset -38}${color2}${font Arial Black:size=26}[--datatype=HT]${font}${color}\n");
	fprintf(fp,"${voffset 2}\n");
	fprintf(fp,"${font Droid Sans:style=Bold:size=8}${voffset 0}${goto 13}[--datatype=DW --startday=1 --shortweekday] ${goto 59}[--datatype=DW --startday=2 --shortweekday] ${goto 105}[--datatype=DW --startday=3 --shortweekday] ${goto 150}[--datatype=DW --startday=4 --shortweekday]${font}\n");
	fprintf(fp,"${voffset 0}${color2}${font ConkyWeather:size=28}[--datatype=WF --startday=1 --endday=4 --spaces=1]${font}${color}\n");
	fprintf(fp,"${font Droid Sans:style=Bold:size=8}${voffset 0}${goto 8}[--datatype=HT --startday=1 --hideunits --centeredwidth=3]/[--datatype=LT --startday=1 --hideunits --centeredwidth=3] ${goto 53}[--datatype=HT --startday=2 --hideunits --centeredwidth=3]/[--datatype=LT --startday=2 --hideunits --centeredwidth=3] ${goto 98}[--datatype=HT --startday=3 --hideunits --centeredwidth=3]/[--datatype=LT --startday=3 --hideunits --centeredwidth=3] ${goto 145}[--datatype=HT --startday=4 --hideunits --centeredwidth=3]/[--datatype=LT --startday=4 --hideunits --centeredwidth=3]${font}\n");
	if (weatherplus == True) {
		fprintf(fp,"${voffset 5}${goto 12}${font Moon Phases:style=Bold:size=36}${color2}[--datatype=MF]${color}${font}\n");
		fprintf(fp,"${voffset 6}${goto 10}${font ConkyWindNESW:size=40}${color2}[--datatype=BS]${color}${font}\n");
		fprintf(fp,"${voffset 4}${goto 22}[--datatype=WS]\n");
		fprintf(fp,"${voffset -116}${goto 70}${font Droid Sans Mono:style=Bold:size=10}${color2}[--datatype=CT]${color}${font}\n");
		fprintf(fp,"${voffset 8}${goto 70}%s: [--datatype=OB]\n", station);
		fprintf(fp,"${goto 70}%s: [--datatype=PC]\n", rain);
		fprintf(fp,"${goto 70}UV: [--datatype=UI] - [--datatype=UT]\n");
		fprintf(fp,"${goto 70}%s: [--datatype=HM]\n", humidity);
		fprintf(fp,"${goto 70}%s: [--datatype=SR]\n", sunrise);
		fprintf(fp,"${goto 70}%s: [--datatype=SS]\n", sunset);
		fprintf(fp,"${goto 70}%s: [--datatype=MP]\n", moon);
	}
	fprintf(fp,"${voffset -10}");

	fclose(fp);
}


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "conkyrc_sls.h"
#include "finddir.h"
#include "translations.h"
#include "themes.h"
#include "variables.h"
#include "utils.h"

void conkyrc_sls () {

	FILE *fp;

	int i;

	fp = fopenf("%s/conkyrc", "w", tempdir());
	if(fp == 0)
	{
		printf("failed to open %s with write permission.\n", tempdir());
		return;
	}

	const char *forecastdir=finddir("bin/conkyWeather");
	const char *yahooweatherdir=finddir("bin/conkyYahooWeather");
	const char *conkysls=finddir("scripts/conkySLS.lua");

	//Global Setup
	fprintf(fp,"######################\n");
	fprintf(fp,"# - Conky settings - #\n");
	fprintf(fp,"######################\n");
	fprintf(fp,"update_interval 1\n");
	fprintf(fp,"total_run_times 0\n");
	fprintf(fp,"net_avg_samples 1\n");
	fprintf(fp,"cpu_avg_samples 1\n");
	fprintf(fp,"\n");
	fprintf(fp,"imlib_cache_size 0\n");
	fprintf(fp,"double_buffer yes\n");
	fprintf(fp,"no_buffers yes\n");
	fprintf(fp,"\n");
	fprintf(fp,"format_human_readable\n");
	fprintf(fp,"\n");
	fprintf(fp,"#####################\n");
	fprintf(fp,"# - Text settings - #\n");
	fprintf(fp,"#####################\n");
	fprintf(fp,"use_xft yes\n");
	fprintf(fp,"xftfont Ubuntu:size=8\n");
	fprintf(fp,"override_utf8_locale yes\n");
	fprintf(fp,"text_buffer_size 2048\n");
	fprintf(fp,"\n");
	fprintf(fp,"#############################\n");
	fprintf(fp,"# - Window specifications - #\n");
	fprintf(fp,"#############################\n");
	fprintf(fp,"own_window_class Conky\n");
	fprintf(fp,"own_window yes\n");
    fprintf(fp,"own_window_type normal\n");
	fprintf(fp,"own_window_transparent yes\n");
	fprintf(fp,"own_window_hints undecorated,below,sticky,skip_taskbar,skip_pager\n");
	fprintf(fp,"\n");
	fprintf(fp,"alignment top_right\n");
	fprintf(fp,"gap_x 5\n");
	fprintf(fp,"gap_y 25\n");
	fprintf(fp,"minimum_size 235 0\n");
	fprintf(fp,"maximum_width 235\n");
	fprintf(fp,"\n");
	fprintf(fp,"#########################\n");
	fprintf(fp,"# - Graphics settings - #\n");
	fprintf(fp,"#########################\n");
	fprintf(fp,"draw_shades no\n");
	if(elementary == True && dark == True)
		fprintf(fp,"\ndefault_color 2B2B2B\n");
	else
		if(dark == True || black == True)
			fprintf(fp,"\ndefault_color 212526\n");
	else
		if(ambiance == True)
			fprintf(fp,"\ndefault_color E2DACB\n");
	else
		if(radiance == True)
			fprintf(fp,"\ndefault_color 3C3B37\n");
	else
		if(elementary == True)
			fprintf(fp,"\ndefault_color D6D6D6\n");
	else
		fprintf(fp,"\ndefault_color cccccc\n");
	fprintf(fp,"\n");
	//COLOR0
    if (dark == True || black == True)
        fprintf(fp,"color0 1E1C1A\n");
    else
        if (custom == True || radiance == True || ambiance == True || elementary == True)
            fprintf(fp,"color0 %s\n", color0);
    else
        fprintf(fp,"color0 white\n");
	//COLOR1
    fprintf(fp,"color1 %s\n", color1);
	//COLOR2
    if (dark == True || black == True)
        fprintf(fp,"color2 1E1C1A\n");
	else
        if (custom == True || radiance == True || ambiance == True || (elementary == True && dark != True))
            fprintf(fp,"color2 %s\n", color2);
	else
		fprintf(fp,"color2 white\n");
	//COLOR3
    fprintf(fp,"color3 %s\n", color3);
	fprintf(fp,"\n");
	//LUA SCRIPTS
	fprintf(fp,"\nlua_load %s/scripts/conkySLS.lua\n", conkysls);
	fprintf(fp,"lua_draw_hook_pre conky_main ");
	//DEFAULT COLOR
	if (dark == True || black == True || radiance == True)
			fprintf(fp,"black ");
	else
			fprintf(fp,"white ");
	//THEME
	fprintf(fp,"%s ", color3);
	//DRAW_BACKGROUND
	if (nobg != True)
		fprintf(fp,"on ");
	else
		fprintf(fp,"off ");
	//WEATHER
	fprintf(fp,"%s ", weather_code );

	//BATTERY
	fprintf(fp,"%s " battery_value );

	fprintf(fp,"\n");
	fprintf(fp,"\n");
	fprintf(fp,"TEXT\n\n");
	fprintf(fp,"${voffset 90}\n");
	fprintf(fp,"#############\n");
	fprintf(fp,"# - CLOCK - #\n");
	fprintf(fp,"#############\n");
	fprintf(fp,"${alignc 80}${font Ubuntu:size=24}${color2}${time %%H:%%M}${font}${color}\n");
	fprintf(fp,"${alignc 55}${voffset 4}${font Ubuntu:size=8}${color2}${time %%A}${font}${color}\n");
	fprintf(fp,"${alignc 55}${voffset -2}${font Ubuntu:size=8}${color2}${time %%d %%b %%Y}${font}${color}\n");
	fprintf(fp,"###############\n");
	fprintf(fp,"# - WEATHER - #\n");
	fprintf(fp,"###############\n");
	fprintf(fp,"${execpi 1800 %s/bin/conkyWeather %s}\n", forecastdir,weather_code);
    if (unit == True) {
        fprintf(fp,"${alignr 10}${voffset -8}${font Ubuntu:style=Bold:size=10}${color2}${font}${execi 600 %s/bin/conkyYahooWeather cur %s f}°F${color}\n", yahooweatherdir, weather_code);
    }
    else {
        fprintf(fp,"${alignr 10}${voffset -8}${font Ubuntu:style=Bold:size=10}${color2}${font}${execi 600 %s/bin/conkyYahooWeather cur %s c}°C${color}\n", yahooweatherdir, weather_code);
    }
	fprintf(fp,"${voffset 60}\n");
	fprintf(fp,"#################\n");
	fprintf(fp,"# - PROCESSES - #\n");
	fprintf(fp,"#################\n");
	char *ucs = NULL;
	for(ucs=processes;*ucs;ucs++)
		*ucs=toupper(*ucs);
	fprintf(fp,"${goto 65}${color0}${font Ubuntu:style=Bold:size=8}%s${color}${font}${voffset 5}\n", processes);
	for (i = 1; i <= 3; i++)
		fprintf(fp,"${goto 65}${voffset -5}${font Ubuntu:size=6}${top name %d}${color}${goto 150}${top cpu %d}${alignr 10}${top mem %d}${font}\n", i, i, i);
	fprintf(fp,"${voffset 62}\n");
	fprintf(fp,"#############\n");
	fprintf(fp,"# - GMAIL - #\n");
	fprintf(fp,"#############\n");
	fprintf(fp,"${goto 46}${color0}${font Ubuntu:style=Bold:size=10}${execpi 1200 %s/bin/conkyEmail -m IMAP -s imap.googlemail.com -e -u %s -p %s -i 10}${color}${font}\n", finddir("bin/conkyEmail"), user, password);
	fprintf(fp,"${goto 65}${voffset -8}${color0}${font Ubuntu:style=Bold:size=8}GMAIL${color}${font}\n");
	fprintf(fp,"${goto 65}${voffset -4}${font Ubuntu:size=6}YOU HAVE ${execpi 1200 %s/bin/conkyEmail -m IMAP -s imap.googlemail.com -e -u %s -p %s -i 10} NEW MAIL(S)${font}\n", finddir("bin/conkyEmail"), user, password);
	fprintf(fp,"###############\n");
	fprintf(fp,"# - NETWORK - #\n");
	fprintf(fp,"###############\n");
	fprintf(fp,"${voffset -8}\n");
	fprintf(fp,"# |--WLAN0\n");
	fprintf(fp,"${if_up wlan0}\n");
	fprintf(fp,"${goto 65}%s: ${font Ubuntu:style=Bold:size=8}${color1}${upspeed wlan0}${color}${font}\n", up);
	fprintf(fp,"${goto 65}%s: ${font Ubuntu:style=Bold:size=8}${color2}${totalup wlan0}${color}${font}\n", total);
	fprintf(fp,"${goto 65}%s: ${font Ubuntu:style=Bold:size=8}${color1}${downspeed wlan0}${color}${font}\n", down);
	fprintf(fp,"${goto 65}%s: ${font Ubuntu:style=Bold:size=8}${color2}${totaldown wlan0}${color}${font}\n", total);
	fprintf(fp,"${goto 65}%s: ${color2}${addr wlan0}${color}\n", localip);
	fprintf(fp,"# |--ETH0\n");
	fprintf(fp,"${else}${if_up eth0}\n");
	fprintf(fp,"${goto 65}%s: ${font Ubuntu:style=Bold:size=8}${color1}${upspeed eth0}${color}${font}\n", up);
	fprintf(fp,"${goto 65}%s: ${font Ubuntu:style=Bold:size=8}${color2}${totalup eth0}${color}${font}\n", total);
	fprintf(fp,"${goto 65}%s: ${font Ubuntu:style=Bold:size=8}${color1}${downspeed eth0}${color}${font}\n", down);
	fprintf(fp,"${goto 65}%s: ${font Ubuntu:style=Bold:size=8}${color2}${totaldown eth0}${color}${font}\n", total);
	fprintf(fp,"${goto 65}%s: ${color2}${addr eth0}${color}\n", localip);
	fprintf(fp,"# |--PPP0\n");
	fprintf(fp,"${else}${if_up ppp0}\n");
	fprintf(fp,"${goto 65}%s: ${font Ubuntu:style=Bold:size=8}${color1}${upspeed ppp0}${color}${font}\n", up);
	fprintf(fp,"${goto 65}%s: ${font Ubuntu:style=Bold:size=8}${color2}${totalup ppp0}${color}${font}\n", total);
	fprintf(fp,"${goto 65}%s: ${font Ubuntu:style=Bold:size=8}${color1}${downspeed ppp0}${color}${font}\n", down);
	fprintf(fp,"${goto 65}%s: ${font Ubuntu:style=Bold:size=8}${color2}${totaldown ppp0}${color}${font}\n", total);
	fprintf(fp,"${goto 65}%s: ${color2}${addr ppp0}${color}\n", localip);
	fprintf(fp,"${else}${voffset 4}${color0}${font Wingdings:size=20}N${font}${color}${goto 32}%s${voffset 14}${endif}${endif}${endif}\n", nonet);
	fprintf(fp,"${voffset -40}\n");

	fclose(fp);
}


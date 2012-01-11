#ifndef _conkyrc_board_
#define _conkyrc_board_

#include <stdio.h>
#include <stdlib.h>
#include "conkyrc_board.h"
#include "finddir.h"
#include "themes.h"
#include "finddir.h"
#include "variables.h"
#include "utils.h"

void conkyrc_board () {

	FILE *fp;

	float value_temp1, value_temp2, value_temp3;

/*	const char *playerdir=finddir("bin/conky%s", player);*/
/*	const char *playertemplatedir=finddir("/templates/conkyPlayer.template");*/
/*	const char *coverdir=finddir("bin/conkyCover");*/
	const char *forecastconfdir=finddir(".conkyForecast.config");

	if(board_width == 0 || board_height == 0)
	{
		printf("You have to set the width AND height of your screen (ex: 1280x800): --w=1280 --h=800\n");
		exit(0);
	}

	fp = fopenf("%s/conkyrc", "w", tempdir());
	if(fp == 0)
	{
		printf("failed to open %s/conkyrc with write permission", tempdir());
		return;
	}

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
	fprintf(fp,"own_window_argb_visual yes\n");
	fprintf(fp,"own_window_argb_value %d\n", argb_value);
	fprintf(fp,"own_window_transparent yes\n");
	fprintf(fp,"own_window_hints undecorated,below,sticky,skip_taskbar,skip_pager\n");
	fprintf(fp,"\n");
	fprintf(fp,"alignment top_left\n");
	fprintf(fp,"gap_x 0\n");
	fprintf(fp,"gap_y %.0f\n", board_height/4);
	fprintf(fp,"minimum_size %.0f %.0f\n", board_width, board_height/2);
	fprintf(fp,"maximum_width %.0f %.0f\n", board_width, board_height/2);
	fprintf(fp,"\n");
	fprintf(fp,"default_bar_size 60 8\n");
	fprintf(fp,"\n");
	fprintf(fp,"#########################\n");
	fprintf(fp,"# - Graphics settings - #\n");
	fprintf(fp,"#########################\n");
	fprintf(fp,"draw_shades no\n");
	if(elementary == True && dark == True)
		fprintf(fp,"\ndefault_color 2B2B2B\n");
	else
		if(elementary == True)
			fprintf(fp,"\ndefault_color D6D6D6\n");
	else
		if(ambiance == True)
			fprintf(fp,"\ndefault_color E2DACB\n");
	else
		if(radiance == True)
			fprintf(fp,"\ndefault_color 3C3B37\n");
	else
		if(dark == True || alldark == True)
			fprintf(fp,"\ndefault_color 212526\n");
	else
		fprintf(fp,"\ndefault_color cccccc\n");
	fprintf(fp,"\n");
	//COLOR0
	if (dark == True || alldark == True)
			fprintf(fp,"color0 1E1C1A\n");
	else
		if (custom == True || radiance == True || ambiance == True || elementary == True)
			fprintf(fp,"color0 %s\n", color0);
	else
		fprintf(fp,"color0 white\n");
	//COLOR1
	if (custom == True || radiance == True || ambiance == True || elementary == True)
		fprintf(fp,"color1 %s\n", color1);
	else
		if (alldark == True)
			fprintf(fp,"color1 1E1C1A\n");
	else
		if (alllight == True)
			fprintf(fp,"color1 white\n");
	else
		fprintf(fp,"color1 %s\n", color1);
	//COLOR2
	if (custom == True || radiance == True || ambiance == True || (elementary == True && dark != True))
		fprintf(fp,"color2 %s\n", color2);
	else
		if (dark == True || alldark == True)
			fprintf(fp,"color2 1E1C1A\n");
	else
		fprintf(fp,"color2 white\n");
	// LUA SCRIPTS
	fprintf(fp,"\nlua_load %s/scripts/conkyBoard.lua\n", finddir("scripts/conkyBoard.lua") );
	fprintf(fp,"lua_draw_hook_pre main ");

	if (elementary == True || ambiance == True)
			fprintf(fp,"black ");
	else
		if (dark == True || alldark == True || radiance == True)
			fprintf(fp,"white ");
	else
			fprintf(fp,"black ");

	fprintf(fp,"%s ", color1);

	if ( nobg == True )
		fprintf(fp,"off ");
	else
		fprintf(fp,"on ");

	if (set_weather == 1)
		fprintf(fp,"on %s", weather_code);
	else
		fprintf(fp,"off %s", weather_code);

	fprintf(fp,"\n");
	fprintf(fp,"\n");
	fprintf(fp,"TEXT\n");
	//Clock
	fprintf(fp,"${voffset 40}\n");
	fprintf(fp,"#############\n");
	fprintf(fp,"# - CLOCK - #\n");
	fprintf(fp,"#############\n");
	if (clocktype == 0)
	{
		fprintf(fp,"${goto %.0f}${voffset -%.0f}${font Arial Black:size=%.0f}${color2}${time %%H}${color}${font}${voffset -%.0f}${font Ubuntu:style=Bold:size=%.0f}${color2}${time :%%M}${time :%%S}${color}${font}\n", board_width/3, board_width*0.035, board_width*0.083, board_width*0.0764, board_width*0.0208);
		fprintf(fp,"${goto %.0f}${voffset -2}${font Ubuntu:style=Bold:size=%.0f}${color1}${time %%B}${color}${font}\n", board_width*0.483, board_width*0.0208);
		fprintf(fp,"${goto %.0f}${font Ubuntu:style=Bold:size=%.0f}${time %%d %%a %%Y}\n", board_width*0.483, board_width*0.0208);
	}
	fprintf(fp,"##############\n");
	fprintf(fp,"# - SYSTEM - #\n");
	fprintf(fp,"##############\n");

	value_temp1 = board_width/3 + 30;
	value_temp2 = board_width/3;
	value_temp3 = board_width/3;

	if ( set_weather == True )
		fprintf(fp,"${voffset %.0f}\n", board_width*0.029);
	else
		fprintf(fp,"${voffset %.0f}\n", board_width*0.026);

	fprintf(fp,"# |--CPU\n");
	if (cpu == 1) {
			fprintf(fp,"${goto %.0f}${color0}${font Poky:size=24}P${font}${offset -27}${voffset 9}${cpubar cpu1 4,22}${color}${voffset -40}\n", value_temp2);
			fprintf(fp,"${goto %.0f}${font Ubuntu:style=Bold:size=8}${color2}${freq_g}${color} GHZ${font}\n",value_temp1);
			fprintf(fp,"${goto %.0f}CPU1: ${font Ubuntu:style=Bold:size=8}${color1}${cpu cpu1}%%${color}${font}\n",value_temp1);
			if (unit == True)
				fprintf(fp,"${goto %.0f}Tmp: ${font Ubuntu:style=Bold:size=8}${color1}${execi 30 sensors -f | grep 'Core 0' | cut -c15-17}°F${color}${font}\n",value_temp1);
			else
				fprintf(fp,"${goto %.0f}Temp: ${font Ubuntu:style=Bold:size=8}${color1}${execi 30 sensors | grep 'Core 0' | cut -c16-17}°C${color}${font}\n",value_temp1);
			fprintf(fp,"${voffset 60}\n");
	}

	// More then 1 cpu
	else {
		for (i = 1; i <= cpu; i++) {
			fprintf(fp,"${goto %.0f}${color0}${font Poky:size=24}P${font}${offset -27}${voffset 9}${cpubar cpu%d 4,22}${color}${voffset -40}\n",value_temp2, i);
			fprintf(fp,"${goto %.0f}${font Ubuntu:style=Bold:size=8}${color2}${freq_g %d}${color} GHZ${font}\n",value_temp1, i);
			fprintf(fp,"${goto %.0f}CPU%d: ${font Ubuntu:style=Bold:size=8}${color1}${cpu cpu%d}%%${color}${font}\n",value_temp1, i, i);
			if (unit == True)
				fprintf(fp,"${goto %.0f}Tmp: ${font Ubuntu:style=Bold:size=8}${color1}${execi 30 sensors -f | grep 'Core 0' | cut -c15-17}°F${color}${font}\n",value_temp1);
			else
				fprintf(fp,"${goto %.0f}Temp: ${font Ubuntu:style=Bold:size=8}${color1}${execi 30 sensors | grep 'Core 0' | cut -c16-17}°C${color}${font}\n",value_temp1);

			if ( i == 2 && cpu > 2 )
			{
				value_temp1 += value_temp3/5;
				value_temp2 += value_temp3/5;
				fprintf(fp,"${voffset -157}\n");
			}
			if ( i < cpu)
				fprintf(fp,"${voffset 12}\n");
		}
	}

	if ( cpu > 2 ) {
		value_temp1 += value_temp3/5;
		value_temp2 += value_temp3/5;
	}
	else {
		value_temp1 += value_temp3/4;
		value_temp2 += value_temp3/4;
	}
	//Mem
	fprintf(fp,"# |--MEM\n");
	fprintf(fp,"${voffset -127}\n");
	fprintf(fp,"${goto %.0f}${color0}${font Poky:size=20}M${font}${offset -25}${voffset 9}${membar 4,22}${color}${voffset -40}\n",value_temp2);
	fprintf(fp,"${goto %.0f}RAM: ${font Ubuntu:style=Bold:size=8}${color1}$memperc%%${color}${font}\n",value_temp1);
	fprintf(fp,"${goto %.0f}F: ${font Ubuntu:style=Bold:size=8}${color2}${memeasyfree}${color}${font}\n",value_temp1);
	fprintf(fp,"${goto %.0f}U: ${font Ubuntu:style=Bold:size=8}${color2}${mem}${color}${font}\n",value_temp1);
	//Swap
	fprintf(fp,"# |--SWAP\n");
	fprintf(fp,"${voffset 20}\n");
	fprintf(fp,"${goto %.0f}${color0}${font Poky:size=18}s${font}${offset -24}${voffset 9}${swapbar 4,22}${color}${voffset -40}\n",value_temp2);
	fprintf(fp,"${goto %.0f}SWAP: ${font Ubuntu:style=Bold:size=8}${color1}$swapperc%%${color}${font}\n",value_temp1);
	fprintf(fp,"${goto %.0f}F: ${font Ubuntu:style=Bold:size=8}${color2}${swapmax}${color}${font}\n",value_temp1);
	fprintf(fp,"${goto %.0f}U: ${font Ubuntu:style=Bold:size=8}${color2}${swap}${color}${font}\n",value_temp1);

	if ( cpu > 2 ) {
		value_temp1 += value_temp3/5;
		value_temp2 += value_temp3/5;
	}
	else {
		value_temp1 += value_temp3/4;
		value_temp2 += value_temp3/4;
	}
	//HD
	fprintf(fp,"##########\n");
	fprintf(fp,"# - HD - #\n");
	fprintf(fp,"##########\n");
	fprintf(fp,"${voffset -125}\n");
	fprintf(fp,"${goto %.0f}${color0}${font Poky:size=20}y${font}${offset -26}${voffset 9}${fs_bar 4,22 /}${color}${voffset -40}\n",value_temp2);
	fprintf(fp,"${goto %.0f}Root: ${font Liberation Sans:style=Bold:size=8}${color1}${fs_free_perc /}%%${color}${font}\n",value_temp1);
	fprintf(fp,"${goto %.0f}F: ${font Ubuntu:style=Bold:size=8}${color2}${fs_free /}${color}${font}\n",value_temp1);
	fprintf(fp,"${goto %.0f}U: ${font Ubuntu:style=Bold:size=8}${color2}${fs_used /}${color}${font}\n",value_temp1);
	fprintf(fp,"${voffset 16}\n");
	fprintf(fp,"${goto %.0f}${color0}${font Poky:size=20}y${font}${offset -26}${voffset 9}${fs_bar 4,22 /home}${color}${voffset -40}\n",value_temp2);
	fprintf(fp,"${goto %.0f}Home: ${font Liberation Sans:style=Bold:size=8}${color1}${fs_free_perc /home}%%${color}${font}\n",value_temp1);
	fprintf(fp,"${goto %.0f}F: ${font Ubuntu:style=Bold:size=8}${color2}${fs_free /home}${color}${font}\n",value_temp1);
	fprintf(fp,"${goto %.0f}U: ${font Ubuntu:style=Bold:size=8}${color2}${fs_used /home}${color}${font}\n",value_temp1);

	if ( cpu > 2 ) {
		value_temp1 += value_temp3/5;
		value_temp2 += value_temp3/5;
	}
	else {
		value_temp1 += value_temp3/4;
		value_temp2 += value_temp3/4;
	}
	//Network Widget
	fprintf(fp,"###############\n");
	fprintf(fp,"# - NETWORK - #\n");
	fprintf(fp,"###############\n");
	fprintf(fp,"${voffset -120}\n");
	fprintf(fp,"${goto %.0f}${color0}${font Poky:size=18}w${font}${voffset -46}\n",value_temp2);
	fprintf(fp,"# |--WLAN%d\n", wlan);
	fprintf(fp,"${if_up wlan%d}\n", wlan);
	fprintf(fp,"${goto %.0f}Up: ${font Ubuntu:style=Bold:size=8}${color1}${upspeed wlan%d}${color}${font}\n",value_temp1, wlan);
	fprintf(fp,"${goto %.0f}Total: ${font Ubuntu:style=Bold:size=8}${color2}${totalup wlan%d}${color}${font}\n",value_temp1, wlan);
	fprintf(fp,"${goto %.0f}Down: ${font Ubuntu:style=Bold:size=8}${color1}${downspeed wlan%d}${color}${font}\n",value_temp1, wlan);
	fprintf(fp,"${goto %.0f}Total: ${font Ubuntu:style=Bold:size=8}${color2}${totaldown wlan%d}${color}${font}\n",value_temp1, wlan);
	fprintf(fp,"${goto %.0f}Signal: ${font Ubuntu:style=Bold:size=8}${color1}${wireless_link_qual_perc wlan%d}%%${color}${font}\n",value_temp1, wlan);
	fprintf(fp,"# |--eth%d\n", eth);
	fprintf(fp,"${else}${if_up eth%d}\n", eth);
	fprintf(fp,"${goto %.0f}Up: ${font Ubuntu:style=Bold:size=8}${color1}${upspeed eth%d}${color}${font}\n",value_temp1, eth);
	fprintf(fp,"${goto %.0f}Total: ${font Ubuntu:style=Bold:size=8}${color2}${totalup eth%d}${color}${font}\n",value_temp1, eth);
	fprintf(fp,"${goto %.0f}Down: ${font Ubuntu:style=Bold:size=8}${color1}${downspeed eth%d}${color}${font}\n",value_temp1, eth);
	fprintf(fp,"${goto %.0f}Total: ${font Ubuntu:style=Bold:size=8}${color2}${totaldown eth%d}${color}${font}\n",value_temp1, eth);
	fprintf(fp,"# |--ppp%d\n", ppp);
	fprintf(fp,"${else}${if_up ppp%d}\n", ppp);
	fprintf(fp,"${goto %.0f}Up: ${font Ubuntu:style=Bold:size=8}${color1}${upspeed ppp%d}${color}${font}\n",value_temp1, ppp);
	fprintf(fp,"${goto %.0f}Total: ${font Ubuntu:style=Bold:size=8}${color2}${totalup ppp%d}${color}${font}\n",value_temp1, ppp);
	fprintf(fp,"${goto %.0f}Down: ${font Ubuntu:style=Bold:size=8}${color1}${downspeed ppp%d}${color}${font}\n",value_temp1, ppp);
	fprintf(fp,"${goto %.0f}Total: ${font Ubuntu:style=Bold:size=8}${color2}${totaldown ppp%d}${color}${font}\n",value_temp1, ppp);
	fprintf(fp,"${endif}${endif}${endif}\n");
	fprintf(fp,"###############\n");
	fprintf(fp,"# - WEATHER - #\n");
	fprintf(fp,"###############\n");
	fprintf(fp,"# For a working weather script you NEED to define, in a user specific config file, a partner id and registration code for the weather.com xoap service. For this purpose copy .conkyForecast.config in %s folder to your home and setup as required.\n", forecastconfdir);
	fprintf(fp,"# http://www.weather.com/services/xmloap.html\n");
	fprintf(fp,"${voffset -%.0f}\n",board_height/4);
	fclose(fp);
}

#endif // #ifndef _conkyrc_board_

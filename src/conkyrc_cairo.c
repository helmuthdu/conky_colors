#ifndef _conkyrc_cairo_
#define _conkyrc_cairo_

#include <stdio.h>
#include <stdlib.h>
#include "conkyrc_cairo.h"
#include "themes.h"
#include "finddir.h"
#include "variables.h"
#include "translations.h"
#include "utils.h"

void conkyrc_cairo () {

	FILE *fp;

	const char *playerdir=finddir("bin/conky%s", player);
	const char *playertemplatedir=finddir("/templates/conkyPlayer.template");
	const char *coverdir=finddir("bin/conkyCover");
	const char *conkycairo=finddir("scripts/conkyCairo.lua");

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
	fprintf(fp,"own_window_transparent yes\n");
  fprintf(fp,"own_window_argb_visual yes\n");
  fprintf(fp,"own_window_argb_value %d\n", argb_value);
	fprintf(fp,"own_window_hints undecorated,below,sticky,skip_taskbar,skip_pager\n");
	fprintf(fp,"\n");
	fprintf(fp,"alignment top_right\n");
	fprintf(fp,"gap_x 0\n");
	fprintf(fp,"gap_y 40\n");
	fprintf(fp,"minimum_size 182 0\n");
	fprintf(fp,"maximum_width 182\n");
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
	// LUA SCRIPTS
	fprintf(fp,"lua_load %s/scripts/conkyCairo.lua\n", conkycairo);
	fprintf(fp,"lua_draw_hook_post conky_main ");

    if (dark == True || black == True)
        fprintf(fp,"black ");
    else
        fprintf(fp,"white ");

	if (dark == True || black == True)
		fprintf(fp,"000000 ");
	else if (white == True)
		fprintf(fp,"ffffff ");
	else
		fprintf(fp,"%s ", color1);

	//cpu_number
	fprintf(fp,"%d ", cpu);

	//swap widget
	if (swap == True)
		fprintf(fp,"on ");
	else
		fprintf(fp,"off ");

	//clock Widget
	if (clocktype == 4)
		fprintf(fp,"cairo ");
	else if (clocktype == 5)
		fprintf(fp,"bigcairo ");
	else
		fprintf(fp,"off ");

	//Media Widget
	if (rhythmbox == True || banshee == True || clementine == True)
		fprintf(fp,"%s ", player);
	else
		fprintf(fp,"off ");

	if (cover == 8)
		fprintf(fp,"cairo ");
	else
		if (cover == 9)
		fprintf(fp,"lua ");
	else
		if (cover == 10 || cover == 11 || cover == 12)
		fprintf(fp,"cairocover ");
	else
		fprintf(fp,"off ");
	if (set_wireless == True)
		fprintf(fp,"on %d", wlan);
	else
		fprintf(fp,"off 0");

	fprintf(fp,"\n");
	fprintf(fp,"\n");
	fprintf(fp,"TEXT\n");
	fprintf(fp,"${voffset 10}\n");
	fprintf(fp,"##############\n");
	fprintf(fp,"# - SYSTEM - #\n");
	fprintf(fp,"##############\n");
	fprintf(fp,"# |--CPU\n");
	//One Ring CPU mode
	if (cputype == True) {
		fprintf(fp,"${goto 100}${font Ubuntu:style=Bold:size=8}${color2}${freq_g}${color} GHZ${font}\n");
		fprintf(fp,"${goto 100}CPU: ${font Ubuntu:style=Bold:size=8}${color1}${cpu cpu0}%%${color}${font}\n");
		if (unit == True)
			fprintf(fp,"${goto 100}Tmp: ${font Ubuntu:style=Bold:size=8}${color1}${execi 30 sensors -f | grep 'Core 0' | awk '{print $3}' | sed 's/+//' | sed 's/.0.*//'}${color}${font}\n");
		else
			fprintf(fp,"${goto 100}Temp: ${font Ubuntu:style=Bold:size=8}${color1}${execi 30 sensors | grep 'Core 0' | awk '{print $3}' | sed 's/+//' | sed 's/.0.*//'}${color}${font}\n");
	}
	else {
		if (cpu == 1) {
				fprintf(fp,"${goto 100}${font Ubuntu:style=Bold:size=8}${color2}${freq_g}${color} GHZ${font}\n");
				fprintf(fp,"${goto 100}CPU1: ${font Ubuntu:style=Bold:size=8}${color1}${cpu cpu1}%%${color}${font}\n");
				if (unit == True)
					fprintf(fp,"${goto 100}Tmp: ${font Ubuntu:style=Bold:size=8}${color1}${execi 30 sensors -f | grep 'Core 0' | awk '{print $3}' | sed 's/+//' | sed 's/.0.*//'}${color}${font}\n");
				else
					fprintf(fp,"${goto 100}Temp: ${font Ubuntu:style=Bold:size=8}${color1}${execi 30 sensors | grep 'Core 0' | awk '{print $3}' | sed 's/+//' | sed 's/.0.*//'}${color}${font}\n");
		}
		// More then 1 cpu
		else {
			for (i = 1; i <= cpu; i++) {
				fprintf(fp,"${goto 100}${font Ubuntu:style=Bold:size=8}${color2}${freq_g %d}${color} GHZ${font}\n", i);
				fprintf(fp,"${goto 100}CPU%d: ${font Ubuntu:style=Bold:size=8}${color1}${cpu cpu%d}%%${color}${font}\n", i, i);
				if (unit == True)
					fprintf(fp,"${goto 100}Tmp: ${font Ubuntu:style=Bold:size=8}${color1}${execi 30 sensors -f | grep 'Core %d' | awk '{print $3}' | sed 's/+//' | sed 's/.0.*//'}${color}${font}\n", i-1);
				else
					fprintf(fp,"${goto 100}Temp: ${font Ubuntu:style=Bold:size=8}${color1}${execi 30 sensors | grep 'Core %d' | awk '{print $3}' | sed 's/+//' | sed 's/.0.*//'}${color}${font}\n", i-1);
				if ( i < cpu)
					fprintf(fp,"${voffset 15}\n");
			}
		}
	}
	fprintf(fp,"# |--MEM\n");
	fprintf(fp,"${voffset 15}\n");
	fprintf(fp,"${goto 100}RAM: ${font Ubuntu:style=Bold:size=8}${color1}$memperc%%${color}${font}\n");
	fprintf(fp,"${goto 100}F: ${font Ubuntu:style=Bold:size=8}${color2}${memeasyfree}${color}${font}\n");
	fprintf(fp,"${goto 100}U: ${font Ubuntu:style=Bold:size=8}${color2}${mem}${color}${font}\n");
	//Swap
	if (swap == True) {
		fprintf(fp,"# |--SWAP\n");
		fprintf(fp,"${voffset 15}\n");
		fprintf(fp,"${goto 100}SWAP: ${font Ubuntu:style=Bold:size=8}${color1}$swapperc%%${color}${font}\n");
		fprintf(fp,"${goto 100}F: ${font Ubuntu:style=Bold:size=8}${color2}${swapmax}${color}${font}\n");
		fprintf(fp,"${goto 100}U: ${font Ubuntu:style=Bold:size=8}${color2}${swap}${color}${font}\n");
	}
	//Clock
	if (clocktype == 4) {
		fprintf(fp,"#############\n");
		fprintf(fp,"# - CLOCK - #\n");
		fprintf(fp,"#############\n");
		fprintf(fp,"${voffset 15}\n");
		fprintf(fp,"${alignr 82}${font Ubuntu:style=Bold:size=11}${color2}${time %%H}${time :%%M}${time :%%S}${color}${font}\n");
		fprintf(fp,"${alignr 65}${voffset -2}${font Ubuntu:style=Bold:size=8}${color2}${time %%A}${color}${font}\n");
		fprintf(fp,"${alignr 64}${time %%d %%b %%Y}\n");
	}
	else
		if (clocktype == 5) {
		fprintf(fp,"#############\n");
		fprintf(fp,"# - CLOCK - #\n");
		fprintf(fp,"#############\n");
		fprintf(fp,"${voffset 92}\n");
	}
	//HD
	fprintf(fp,"##########\n");
	fprintf(fp,"# - HD - #\n");
	fprintf(fp,"##########\n");
	fprintf(fp,"${voffset 15}\n");
	fprintf(fp,"${goto 100}Root: ${font Ubuntu:style=Bold:size=8}${color1}${fs_free_perc /}%%${color}${font}\n");
	fprintf(fp,"${goto 100}F: ${font Ubuntu:style=Bold:size=8}${color2}${fs_free /}${color}${font}\n");
	fprintf(fp,"${goto 100}U: ${font Ubuntu:style=Bold:size=8}${color2}${fs_used /}${color}${font}\n");
	fprintf(fp,"${voffset 15}\n");
	fprintf(fp,"${goto 100}Home: ${font Ubuntu:style=Bold:size=8}${color1}${fs_free_perc /home}%%${color}${font}\n");
	fprintf(fp,"${goto 100}F: ${font Ubuntu:style=Bold:size=8}${color2}${fs_free /home}${color}${font}\n");
	fprintf(fp,"${goto 100}U: ${font Ubuntu:style=Bold:size=8}${color2}${fs_used /home}${color}${font}\n");
	//Media Player Widget
	if (rhythmbox == True || banshee == True || clementine == True) {
		fprintf(fp,"####################\n");
		fprintf(fp,"# - MEDIA PLAYER - #\n");
		fprintf(fp,"####################\n");
		fprintf(fp,"${voffset 0}\n");
		if (cover > 9)
			fprintf(fp,"${execi 6 %s/bin/conkyCover}", coverdir);
		fprintf(fp,"${execpi 10 %s/bin/conky%s -t %s/templates/conkyPlayer.template}${voffset -10}\n", playerdir, player, playertemplatedir);
	}
	if (set_wireless == True) {
		fprintf(fp,"################\n");
		fprintf(fp,"# - WIRELESS - #\n");
		fprintf(fp,"################\n");
		fprintf(fp,"${voffset 15}\n");
		fprintf(fp,"${goto 100}%s: ${font Ubuntu:style=Bold:size=8}${color1}${wireless_link_qual wlan%d}%%${color}${font}\n", sinal, wlan);
		fprintf(fp,"${alignr 33}${color2}${wireless_essid wlan%d}${color}\n", wlan);
		fprintf(fp,"${alignr 35}${font Ubuntu:style=Bold:size=8}${color2}${execi 10800 curl ifconfig.me}${color}${font}\n");
	}
	//Network Widget
	if (set_network == True) {
		fprintf(fp,"###############\n");
		fprintf(fp,"# - NETWORK - #\n");
		fprintf(fp,"###############\n");
		fprintf(fp,"${voffset 4}\n");
		fprintf(fp,"# |--WLAN%d\n", wlan);
		fprintf(fp,"${if_up wlan%d}\n", wlan);
		fprintf(fp,"${goto 100}Up: ${font Ubuntu:style=Bold:size=8}${color1}${upspeed wlan%d}${color}${font}\n", wlan);
		fprintf(fp,"${goto 100}Total: ${font Ubuntu:style=Bold:size=8}${color2}${totalup wlan%d}${color}${font}\n", wlan);
		fprintf(fp,"${goto 100}Down: ${font Ubuntu:style=Bold:size=8}${color1}${downspeed wlan%d}${color}${font}\n", wlan);
		fprintf(fp,"${goto 100}Total: ${font Ubuntu:style=Bold:size=8}${color2}${totaldown wlan%d}${color}${font}\n", wlan);
		fprintf(fp,"${goto 100}Signal: ${font Ubuntu:style=Bold:size=8}${color1}${wireless_link_qual wlan%d}%%${color}${font}\n", wlan);
		fprintf(fp,"# |--ETH%d\n", eth);
		fprintf(fp,"${else}${if_up eth%d}\n", eth);
		fprintf(fp,"${goto 100}Up: ${font Ubuntu:style=Bold:size=8}${color1}${upspeed eth%d}${color}${font}\n", eth);
		fprintf(fp,"${goto 100}Total: ${font Ubuntu:style=Bold:size=8}${color2}${totalup eth%d}${color}${font}\n", eth);
		fprintf(fp,"${goto 100}Down: ${font Ubuntu:style=Bold:size=8}${color1}${downspeed eth%d}${color}${font}\n", eth);
		fprintf(fp,"${goto 100}Total: ${font Ubuntu:style=Bold:size=8}${color2}${totaldown eth%d}${color}${font}\n", eth);
		fprintf(fp,"# |--PPP%d\n", ppp);
		fprintf(fp,"${else}${if_up ppp%d}\n", ppp);
		fprintf(fp,"${goto 100}Up: ${font Ubuntu:style=Bold:size=8}${color1}${upspeed ppp%d}${color}${font}\n", ppp);
		fprintf(fp,"${goto 100}Total: ${font Ubuntu:style=Bold:size=8}${color2}${totalup ppp%d}${color}${font}\n", ppp);
		fprintf(fp,"${goto 100}Down: ${font Ubuntu:style=Bold:size=8}${color1}${downspeed ppp%d}${color}${font}\n", ppp);
		fprintf(fp,"${goto 100}Total: ${font Ubuntu:style=Bold:size=8}${color2}${totaldown ppp%d}${color}${font}\n", ppp);
		fprintf(fp,"${endif}${endif}${endif}");
	}
	fprintf(fp,"\n");
	fclose(fp);
}

#endif // #ifndef _conkyrc_cairo_

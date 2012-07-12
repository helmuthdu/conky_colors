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

/*	const char *playerdir=finddir("bin/conky%s", player);*/
/*	const char *playertemplatedir=finddir("/templates/conkyPlayer.template");*/
/*	const char *coverdir=finddir("bin/conkyCover");*/

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
	fprintf(fp,"own_window_type desktop\n");
	fprintf(fp,"own_window_argb_visual yes\n");
	fprintf(fp,"own_window_argb_value %d\n", argb_value);
	fprintf(fp,"own_window_transparent yes\n");
	fprintf(fp,"own_window_hints undecorated,below,sticky,skip_taskbar,skip_pager\n");
	fprintf(fp,"\n");
	fprintf(fp,"alignment top_left\n");
	fprintf(fp,"gap_x 0\n");
	fprintf(fp,"gap_y %.0f\n", board_height/4);
	fprintf(fp,"minimum_size %.0f %.0f\n", board_width, board_height);
	fprintf(fp,"maximum_width %.0f %.0f\n", board_width, board_height);
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
	fprintf(fp,"\n");
	// LUA SCRIPTS
	fprintf(fp,"\nlua_load %s/scripts/conkyBoard.lua\n", finddir("scripts/conkyBoard.lua") );
	fprintf(fp,"lua_draw_hook_pre main ");

    if (dark == True || white == True || radiance == True)
        fprintf(fp,"white ");
    else
        fprintf(fp,"black ");

	fprintf(fp,"%s ", color3);
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

	fclose(fp);
}

#endif // #ifndef _conkyrc_board_

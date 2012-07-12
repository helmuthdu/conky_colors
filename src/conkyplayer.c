#include <stdio.h>
#include <stdlib.h>
#include "conkyplayer.h"
#include "finddir.h"
#include "translations.h"
#include "variables.h"
#include "utils.h"

//Create and write conkyPlayer.template
void conkyplayer () {

	FILE *fp;

	int			w=0,h=0;
	const char *playerdir = finddir("bin/conky%s", player);

	fp = fopenf("%s/conkyPlayer.template", "w", tempdir());
	if(fp == 0)
	{
		printf("failed to open %s/conkyPlayer.template with write premission.\n", tempdir());
		return;
	}

	void trackinfo ()
	{
			if (banshee == True)
			fprintf(fp,"${if_running banshee-1}\n");
			else
				if (rhythmbox == True)
				fprintf(fp,"${if_running rhythmbox}\n");
			else
				fprintf(fp,"${if_running clementine}\n");
			fprintf(fp,"${voffset -22}${offset -2}${color0}${font Webdings:size=20}Ø${font}${color}${voffset -8}${goto %d}%s:${alignr}${color2}[--datatype=ST]${color}\n", go2, status);
			fprintf(fp,"${goto 100}${voffset 4}${color2}[--datatype=AR]${color}\n");
			fprintf(fp,"${goto 100}${color2}[--datatype=AL]${color}\n");
			fprintf(fp,"${goto 100}${color2}[--datatype=TI]${color}\n");
			fprintf(fp,"${goto 100}${color2}[--datatype=PT]/[--datatype=LE]${color}${voffset -8}\n");
			fprintf(fp,"$else\n");
			fprintf(fp,"${voffset -22}${offset -2}${color0}${font Webdings:size=20}Ø${font}${color}${voffset -8}${goto 32}Status:${alignr}${color2}off${color}\n");
			fprintf(fp,"${goto 105}${voffset 24}${execi 10 %s/bin/conkyCover}${font Droid Sans:style=Bold:size=8}${color2}%s${color}${font}${voffset 8}\n", finddir("bin/conkyCover"), player);
			fprintf(fp,"$endif");
	}

	void trackinfo_cairo(int alignr, int type)
	{
			if (banshee == True)
			fprintf(fp,"${if_running banshee-1}\n");
			else
				if (rhythmbox == True)
				fprintf(fp,"${if_running rhythmbox}\n");
			else
				fprintf(fp,"${if_running clementine}\n");
			fprintf(fp,"${voffset -1}\n");
			fprintf(fp,"${alignr %d}${color2}${execp %s/bin/conky%s --datatype=AR | fold -w 18 | sed '1!d'}${color}\n", alignr, playerdir, player);
			fprintf(fp,"${alignr %d}${color2}${execp %s/bin/conky%s --datatype=AL | fold -w 18 | sed '1!d'}${color}\n", alignr, playerdir, player);
			fprintf(fp,"${alignr %d}${color2}${execp %s/bin/conky%s --datatype=TI | fold -w 18 | sed '1!d'}${color}", alignr, playerdir, player);
			if (cover > 9)
				fprintf(fp,"\n${voffset 3}${goto 146}${font Droid Sans:style=Bold:size=8}${color2}${execp %s/bin/conky%s --datatype=PT}${color}${font}${voffset -8}$else\n", playerdir, player);
			else
				fprintf(fp,"$else\n");
			fprintf(fp,"${voffset 12}\n");
			if (type == 1)
				fprintf(fp,"${alignr 66}");
			else
				fprintf(fp,"${goto 100}");
			fprintf(fp,"${font Droid Sans:style=Bold:size=8}${color2}%s${color}${font}\n", player);
			fprintf(fp,"$endif");
	}

	//cairo-glassy Theme
	if (cover == 12) {
		w = 56; h = 45;
		trackinfo_cairo(64, 1);
		fprintf(fp,"${image %s/conkyCover.png -s %dx%d -p 122,%d}", tempdir(), w, h, yc);
	}
	//cairo-glassy Theme
	else
		if (cover == 11) {
			w = 56; h = 49;
			trackinfo_cairo(64, 1);
			fprintf(fp,"${image %s/conkyCover.png -s %dx%d -p 120,%d}", tempdir(), w, h, yc-2);
		}
	//cairo-cd Theme
	else
		if (cover == 10) {
			w = 51; h = 45;
			trackinfo_cairo(64, 1);
			fprintf(fp,"${image %s/conkyCover.png -s %dx%d -p 124,%d}", tempdir(), w, h, yc);
		}
	//lua Theme
	else
		if (cover == 9) {
			trackinfo_cairo(35, 2);
		}
	//cairo Theme
	else
		if (cover == 8) {
			trackinfo_cairo(64, 1);
		}
	//oldvinyl Theme
	else
		if (cover == 7) {
			w = 98; h = 58;
			fprintf(fp,"${image %s/conkyCover.png -s %dx%d -p 20,%d}\n", tempdir(), w, h, yc);
			trackinfo();
		}
	//glassy Theme
	else
		if (cover == 6) {
			w = 68; h = 60;
			fprintf(fp,"${image %s/conkyCover.png -s %dx%d -p 24,%d}\n", tempdir(), w, h, yc);
			trackinfo();
		}
	//case Theme
	else
		if (cover == 5) {
			w = 68;	h = 55;
			fprintf(fp,"${image %s/conkyCover.png -s %dx%d -p 24,%d}\n", tempdir(), w, h, yc);
			trackinfo();
		}
	//cd Theme
	else
		if (cover == 4) {
			w = 63;	h = 55;
			fprintf(fp,"${image %s/conkyCover.png -s %dx%d -p 24,%d}\n", tempdir(), w, h, yc);
			trackinfo();
		}
	else
	//vinyl Theme
		if (cover == 3) {
			w = 88;	h = 62;
			fprintf(fp,"${image %s/conkyCover.png -s %dx%d -p 16,%d}\n", tempdir(), w, h, yc);
			trackinfo();
		}
	//simple Theme
	else
		if (cover == 2) {
			if (banshee == True)
			fprintf(fp,"${if_running banshee-1}\n");
			else
				if (rhythmbox == True)
				fprintf(fp,"${if_running rhythmbox}\n");
			else
				fprintf(fp,"${if_running clementine}\n");
			fprintf(fp,"${voffset -12}${color0}${font Musicelements:size=18}z${font}${color}${voffset -8}${goto %d}%s:${alignr}${color2}[--datatype=ST]${color}\n", go2, status);
			fprintf(fp,"${voffset 4}${goto %d}${color2}[--datatype=AR]${color}\n", go2);
			fprintf(fp,"${color2}${goto %d}[--datatype=AL]${color}\n", go2);
			fprintf(fp,"${color2}${goto %d}[--datatype=TI]${color}\n", go2);
			fprintf(fp,"${voffset 4}${goto %d}${color2}[--datatype=PT]/[--datatype=LE]${color}", go2);
			fprintf(fp,"${alignr}${color2}${execbar %s/bin/conky%s --datatype=PP}${color}", playerdir, player);
			fprintf(fp,"$else\n");
			fprintf(fp,"${voffset -12}${color0}${font Webdings:size=16}U${font}${color}${voffset -2}${goto 32}Status:${alignr}${color2}off${color}\n");
			fprintf(fp,"${voffset 12}$alignc${font Droid Sans:style=Bold:size=8}${color2}%s${color}${font}${voffset -10}\n", player);
			fprintf(fp,"$endif");
		}
		//default Theme
		else {
			if (banshee == True)
			fprintf(fp,"${if_running banshee-1}\n");
			else
				if (rhythmbox == True)
				fprintf(fp,"${if_running rhythmbox}\n");
			else
				fprintf(fp,"${if_running clementine}\n");
			fprintf(fp,"${voffset -12}${color0}${font Webdings:size=16}U${font}${color}${voffset -2}${goto %d}%s:${alignr}${color2}[--datatype=ST]${color}\n", go2, status);
			fprintf(fp,"${voffset 4}${color0}${color0}${font Musicelements:size=19}z${font}${color}${voffset -8}${goto %d}%s:${alignr}${color2}[--datatype=AR]${color}\n", go2, song);
			fprintf(fp,"${color2}${alignr}[--datatype=AL]${color}\n");
			fprintf(fp,"${color2}${alignr}[--datatype=TI]${color}\n");
			fprintf(fp,"${voffset -7}${color0}${font Martin Vogel's Symbols:size=19}U${font}${color}${voffset -4}${goto %d}%s:${alignr}${color2}[--datatype=PT]/[--datatype=LE]${color}${voffset 2}", go2, tempo);
			fprintf(fp,"$else\n");
			fprintf(fp,"${voffset -12}${color0}${font Webdings:size=16}U${font}${color}${voffset -2}${goto 32}Status:${alignr}${color2}off${color}\n");
			fprintf(fp,"${voffset 12}$alignc${font Droid Sans:style=Bold:size=8}${color2}%s${color}${font}${voffset -10}\n", player);
			fprintf(fp,"$endif");
		}

	fclose(fp);
}


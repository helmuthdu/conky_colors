#ifndef _conkycover_
#define _conkycover_

#include <stdio.h>
#include <stdlib.h>
#include "conkycover.h"
#include "finddir.h"
#include "variables.h"
#include "utils.h"

//Create and write conkyCover
void conkycover ()
{

	FILE *fp;

	fp = fopenf("%s/conkyCover", "w", tempdir());
	if(fp == 0)
	{
		printf("Failed to open %s/conkyCover with write permission\n", tempdir());
		return;
	}

	void cover_size (int size) {
		fprintf(fp,"\tcp \"$player\" $cover\n");
		fprintf(fp,"\tconvert $cover -thumbnail %dx%d $cover\n", size*2, size);
		fprintf(fp,"\tconvert $cover -gravity Center -crop %dx%d+0+0 +repage $cover\n", size, size);
	}

	fprintf(fp,"#!/bin/sh\n");
	fprintf(fp,"#\n");
	fprintf(fp,"# Album art with cd theme in conky\n");
	fprintf(fp,"# by helmuthdu\n\n");
	if (banshee == True) {
		fprintf(fp,"player=\"`%s/bin/conkyBanshee --datatype=CA | sed -e 's/\\\\\\//g'`\"\n", finddir("bin/conkyBanshee") );
		fprintf(fp,"icon=%s/icons/Players/banshee.png\n", finddir("icons/Players/banshee.png") );
	}
	else if (rhythmbox == True) {
		fprintf(fp,"album=\"`%s/bin/conkyRhythmbox -d AL`\"\n", finddir("bin/conkyRhythmbox") );
		fprintf(fp,"player=\"`find ~/.cache/rhythmbox/covers/ -name '*'\"$album\"'*'`\"\n");
		fprintf(fp,"#player=\"`%s/bin/conkyRhythmbox -d CA | sed -e 's/\\%%20/\\\\ /g'`\"\n", finddir("bin/conkyRhythmbox"));
		fprintf(fp,"icon=%s/icons/Players/rhythmbox.png\n", finddir("icons/Players/rhythmbox.png") );
	}
	else {
		fprintf(fp,"player=\"`%s/bin/conkyClementine --datatype=CA | sed -e 's/\\\\\\//g'`\"\n", finddir("bin/conkyClementine") );
		fprintf(fp,"icon=%s/icons/Players/rhythmbox.png\n", finddir("icons/Players/rhythmbox.png") );
	}
	fprintf(fp,"cover=%s/conkyCover.png\n", tempdir() );
	fprintf(fp,"\n");
	fprintf(fp,"width=`identify -format %%w $photo`\n");
	fprintf(fp,"height=`identify -format %%h $photo`\n");
	fprintf(fp,"picture_aspect=`expr $width - $height`\n");
	fprintf(fp,"\n");
	fprintf(fp,"if [ ! -f \"$player\" ]; then\n");
	if (cover == 4 || cover == 10) {
		fprintf(fp,"\t#cp $icon $cover\n");
		fprintf(fp,"\tconvert %s/icons/CD/base.png %s/icons/CD/top.png -geometry +0+0 -composite $cover\n", finddir("icons/CD/base.png"), finddir("icons/CD/top.png") );
	}
	else
		if (cover == 5 || cover == 12) {
			fprintf(fp,"\tconvert %s/icons/Case/base.png %s/icons/Case/top.png -geometry +0+0 -composite $cover\n", finddir("icons/Case/base.png"), finddir("icons/Case/top.png") );
		}
	else
		if (cover == 6 || cover == 11) {
			fprintf(fp,"\tconvert %s/icons/Glassy/base.png %s/icons/Glassy/top.png -geometry +0+0 -composite $cover\n", finddir("icons/Glassy/base.png"), finddir("icons/Glassy/top.png") );
		}
	else
		if (cover == 7) {
			fprintf(fp,"\tconvert %s/icons/oldVinyl/base.png %s/icons/oldVinyl/top.png -geometry +0+0 -composite $cover\n", finddir("icons/oldVinyl/base.png"), finddir("icons/oldVinyl/top.png"));
		}
	else
		fprintf(fp,"\tconvert %s/icons/Vinyl/base.png $icon -geometry +36+18 -composite $cover\n", finddir("icons/Vinyl/base.png") );
	fprintf(fp,"else\n");
	if (cover == 4 || cover == 10) {
		cover_size(98);
		fprintf(fp,"\tconvert %s/icons/CD/base.png $cover -geometry +21+5 -composite %s/icons/CD/top.png -geometry +0+0 -composite $cover\n", finddir("icons/CD/base.png"), finddir("icons/CD/top.png") );
	}
	else
		if (cover == 5 || cover == 12) {
		cover_size(99);
			fprintf(fp,"\tconvert %s/icons/Case/base.png $cover -geometry +8+1 -composite %s/icons/Case/top.png -geometry +0+0 -composite $cover\n", finddir("icons/Case/base.png"), finddir("icons/Case/top.png") );
		}
	else
		if (cover == 6 || cover == 11) {
		cover_size(92);
			fprintf(fp,"\tconvert %s/icons/Glassy/base.png $cover -geometry +24+8 -composite %s/icons/Glassy/top.png -geometry +0+0 -composite $cover\n", finddir("icons/Glassy/base.png"), finddir("icons/Glassy/top.png") );
		}
	else
		if (cover == 7) {
		cover_size(86);
		fprintf(fp,"\tconvert %s/icons/oldVinyl/base.png $cover -geometry +4+3 -composite %s/icons/oldVinyl/top.png -geometry +0+0 -composite $cover\n", finddir("icons/oldVinyl/base.png"), finddir("icons/oldVinyl/top.png") );
		}
	else {
		cover_size(112);
		fprintf(fp,"\tconvert %s/icons/Vinyl/base.png $cover -geometry +32+6 -composite %s/icons/Vinyl/top.png -geometry +0+0 -composite $cover\n", finddir("icons/Vinyl/base.png"), finddir("icons/Vinyl/top.png") );
	}
	fprintf(fp,"fi\n");
	fprintf(fp,"\n");
	fprintf(fp,"exit 0\n");

	fclose(fp);

}

#endif // #ifndef _conkycover_

/*
# Copyright (C) 2011 Helmuth Saatkamp (helmuthdu)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "themes.h"
#include "translations.h"
#include "options.h"
#include "conkycover.h"
#include "conkyplayer.h"
#include "coverposition.h"
#include "photoposition.h"
#include "conkyrc_default.h"
#include "conkyrc_cairo.h"
#include "conkyrc_ring.h"
#include "conkyrc_board.h"
#include "conkyrc_slim.h"
#include "conkyrc_sls.h"
#include "finddir.h"
#include "variables.h"
#include "confinstall.h"
#include "utils.h"
#include "initialize.h"


//Create and write .conkyrc
void create_conkyrc () {

	if (cairo_set == True)
	{
		coverposition_cairo();
		conkycover();
		conkyplayer();
		conkyrc_cairo();
	}
	else if (ring == True)
  {
    coverposition_ring();
    conkycover();
    conkyplayer();
    conkyrc_ring();
  }
	else if (board == True)
  {
    conkyrc_board();
  }
	else if (slim == True)
  {
    conkyrc_slim();
  }
	else if (sls == True)
  {
    conkyrc_sls();
  }
	else
	{
		coverposition();
		photoposition();
		if (cover > 2)
			conkycover();
		conkyplayer();
		conkyrc_default();
	}
}

int main(int argc, char *argv[])
{

	if(initialize_finddir() != 0)
		return -1;

	int result = options (argc, argv);
	if(result == OPTIONS_PREMATURE_END)
		return 0;
	else if(result == OPTIONS_ERROR)
		return -1;
	else if(result != 0)
		return -2;

	initialize();
	translation();
	themes();
	create_conkyrc();
	confinstall();

	return 0;
}

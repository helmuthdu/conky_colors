#define _ISOC99_SOURCE
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdarg.h>
#include "themes.h"
#include "initialize.h"
#include "utils.h"
#include "variables.h"
#include "finddir.h"

#define CREATE(...) if(systemf(__VA_ARGS__) == -1) return create_error();
#define MKDIRa(su) if(systemf("if test ! -d %s/" #su "; then mkdir -p %s/" #su "; fi", datadir, datadir) == -1) \
		{ snprintf(dir, LEN_CHAR, "%s/%s", datadir, #su); return mkdir_error(dir); }
#define MKDIR(su) MKDIRa(su)
		
int initialize_files();
int create_error();
int mkdir_error(const char * dir);

int initialize()
{

	const char *datadir=0;
	char dir[LEN_CHAR];

	datadir=get_install_datadir();
	if(datadir == 0)
	{
		printf("datadir is NULL\n");
		return -1;
	}

	// Make template directory if absent.
	MKDIR(templates)
	// CREATE files to template directory.

	// Make bin directory if absent.
	MKDIR(bin)
	// CREATE files to bin directory
	
	CREATE("touch %s/templates/conkyPlayer.template", datadir);
	if (cover > 2)
		CREATE("touch %s/bin/conkyCover", datadir);
	if (set_weather > 0)
		CREATE("touch %s/templates/conkyForecast.template", datadir);

	return 0;
}

int create_error()
{
	printf("error while creating configuration files to %s\n", datadir);
	return -1;
}

int mkdir_error(const char* dir)
{
	printf("error on making %s\n", dir);
	return -1;
}


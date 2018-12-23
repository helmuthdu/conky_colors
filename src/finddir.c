#define _ISOC99_SOURCE // for vsnprintf
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include "finddir.h"
#include "utils.h"

int i;

struct finddir_info {
	char nofilecheck;

	char nullchar[FINDDIR_CHAR_LEN];

	char datadir[NUM_DATADIR][FINDDIR_CHAR_LEN];

	char tempdir[FINDDIR_CHAR_LEN];
};

struct finddir_info info;
int install=FINDDIR_LOCAL;

int initialize_finddir()
{
	char path[FINDDIR_CHAR_LEN - strlen("/." BINARY_NAME)];

	info.nofilecheck=0;

	sprintf(info.nullchar, "(null)");

	if(strncpycmd(path, "echo -n ~", FINDDIR_CHAR_LEN) != 0)
		return -1;

	info.datadir[FINDDIR_CUSTOM][0] = '\0';
	snprintf(info.datadir[FINDDIR_LOCAL], FINDDIR_CHAR_LEN, "%s/." BINARY_NAME, path);
	snprintf(info.datadir[FINDDIR_SYSTEM], FINDDIR_CHAR_LEN,
	         "%s/share/" BINARY_NAME, DESTDIR);
	snprintf(info.tempdir, FINDDIR_CHAR_LEN, "/tmp/" BINARY_NAME);

	if(systemf("if ! test -d %s; then mkdir -p %s; fi", info.tempdir, info.tempdir) != 0)
	{
		printf("Failed to make %s\n", info.tempdir);
		return -1;
	}

	return 0;
}

void finddir_set_nofilecheck()
{
	info.nofilecheck=1;
}

const char *finddir(const char * format, ...)
{
	static char pathtofile[FINDDIR_CHAR_LEN*2];
	char nofilecheck=info.nofilecheck;

	va_list ap;
	char file[FINDDIR_CHAR_LEN];

	va_start(ap, format);
	vsnprintf(file, FINDDIR_CHAR_LEN, format, ap);
	va_end(ap);

	for(i=0; i< NUM_DATADIR; ++i)
	{
		if(info.datadir[i][0] != '\0')
		{
			sprintf(pathtofile, "%s/%s", info.datadir[i], file);
			if(nofilecheck || access(pathtofile, F_OK) == 0)
				return info.datadir[i];
		}
	}

	return info.nullchar;
}


const char *finddir_nullchar()
{
	return info.nullchar;
}

int num_default_datadir()
{
	return NUM_DATADIR-1;
}

int num_datadir()
{
	return NUM_DATADIR;
}

const char* get_datadir(unsigned int n)
{
	return info.datadir[n];
}

int get_install_type()
{
	return install;
}

void set_install_type(int type)
{
	if(type >= 0 && type < NUM_DATADIR)
		install=type;
	else
		printf("You specified a wrong install type.\n");
}

const char * get_install_datadir()
{
	const char *datadir=0;

	if(install == FINDDIR_CUSTOM)
	{
		datadir=customdir();
		if(datadir[0] == '\0')
		{
			printf("When you specify --install=custom, you need to specify --datadir, too.\n");
			return 0;
		}

		return datadir;
	}
	else if(install < NUM_DATADIR && install >= 0)
		return get_datadir(install);

	return 0;
}

void print_default_datadir()
{
	for(i=FINDDIR_CUSTOM+1; i<NUM_DATADIR; ++i)
		printf("%s\n", info.datadir[i]);
}

char *customdir()
{
	return info.datadir[FINDDIR_CUSTOM];
}

const char *systemdir()
{
	return info.datadir[FINDDIR_SYSTEM];
}

const char * localdir()
{
	return info.datadir[FINDDIR_LOCAL];
}

const char * tempdir()
{
	return info.tempdir;
}

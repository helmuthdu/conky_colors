#define _BSD_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include "utils.h"
#include "variables.h"

// execute cmd, and copy the standard ouput to dest.
int strncpycmd(char *dest, const char *cmd, size_t size)
{
	FILE* cmdfd;
	size_t offset=0;
	// Open a pipeline for the command.
	cmdfd = popen(cmd, "r");

	if(cmdfd == NULL)
		return -1;
	// Read the standrad output from the pipeline
	// until dest is filled fully or the standard output gets flushed.
	while(fgets(dest + offset, size-offset, cmdfd) != NULL)
		offset+=strlen(dest+offset);
	// Close the pipeline.
	if(pclose(cmdfd) != 0)
		return -1;

	return 0;
}

int systemf(const char* format, ...)
{
	char str[LEN_CHAR];
	va_list ap;

	va_start(ap, format);
	vsnprintf(str, LEN_CHAR, format, ap);
	va_end(ap);

	return system(str);
}

FILE *fopenf(const char *format, const char* mode, ...)
{
	char str[LEN_CHAR];
	va_list ap;

	va_start(ap, mode);
	vsnprintf(str, LEN_CHAR, format, ap);
	va_end(ap);

	return fopen(str, mode);
}

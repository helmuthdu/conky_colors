#define _ISOC99_SOURCE
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdarg.h>
#include "confinstall.h"
#include "utils.h"
#include "variables.h"
#include "finddir.h"

#define COPY(...) if(systemf(__VA_ARGS__) == -1) return copy_error();

int copy_error();

int confinstall()
{
	const char *datadir=0;

	datadir=get_install_datadir();

  if (rhythmbox == True || banshee == True || clementine == True)
	{
    COPY("mv %s/conkyPlayer.template %s/templates/conkyPlayer.template", tempdir(), datadir);
  }

	if (cover > 2)
	{
		COPY("mv %s/conkyCover %s/bin/conkyCover; chmod +x %s/bin/conkyCover", tempdir(), datadir, datadir);
  }

	if(set_photo == 1)
	{
		COPY("cp -i %s/bin/conkyPhoto %s/bin/conkyPhoto; chmod +x %s/bin/conkyPhoto", systemdir(), datadir, datadir);
  }
	else if(set_photo == 2)
  {
    COPY("cp -i %s/bin/conkyPhotoRandom %s/bin/conkyPhotoRandom; chmod +x %s/bin/conkyPhotoRandom", systemdir(), datadir, datadir);
  }

	// finish
	systemf("mv %s/conkyrc %s", tempdir(), localdir());
	printf("Your conkyrc was copied to %s\n", localdir());
	printf("Generated configuration files are copied to %s\n", datadir);
	printf("\nTo run conky-colors and conky type: \nconky -c %s/conkyrc\n", localdir());

	return 0;
}

int copy_error()
{
	printf("error while copying generated configuration files to %s\n", datadir);
	return -1;
}


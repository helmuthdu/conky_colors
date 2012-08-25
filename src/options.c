#define _BSD_SOURCE
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <ctype.h>
#include "options.h"
#include "themes.h"
#include "translations.h"
#include "help.h"
#include "variables.h"
#include "finddir.h"
#include "utils.h"

int set_default_values();

//Options
int options (int argc, char *argv[]) {

	char *arg;
	char *key, *value;

	set_default_values();

	if(argc == 1)
	{
		help();
		return OPTIONS_ERROR;
	}

	while (--argc) {

		arg = *++argv;
		key = strsep(&arg, "=");
		value = strsep(&arg, "=");

		OPTION("--theme", key) {
			OR_OPTION_START("brave", value) OR_OPTION("carbonite", value) OR_OPTION("dust", value)
			OR_OPTION("human", value) OR_OPTION("illustrious", value) OR_OPTION("noble", value)
			OR_OPTION("tribute", value) OR_OPTION("wine", value) OR_OPTION("wise", value)
			OR_OPTION("blue", value) OR_OPTION("orange", value) OR_OPTION("red", value)
			OR_OPTION("green", value) OR_OPTION("cyan", value) OR_OPTION_END("purple", value)
			{
				snprintf(theme, 31, "%s", value);
			}
			else OPTION("black", value)
			{
				snprintf(theme, 31, "%s", value);
				black = True;
			}
			else OPTION("white", value)
			{
				snprintf(theme, 31, "%s", value);
				white = True;
			}
			else OPTION("radiance", value)
			{
				snprintf(theme, 31, "%s", value);
				radiance = True;
			}
			else OPTION("ambiance", value)
			{
				snprintf(theme, 31, "%s", value);
				ambiance = True;
			}
			else OPTION("elementary", value)
			{
				snprintf(theme, 31, "%s", value);
				elementary = True;
			}
			else OPTION("custom", value)
				custom = True;
			else
			{
				printf("ERRO: THEME unavaliable\n");
				return OPTIONS_ERROR;
			}
		}
		else OPTION_WITH_VALUE("--default-color", key)
			snprintf(defaultcolor, 31, "%s", value);
		else OPTION_WITH_VALUE("--color0", key)
			snprintf(color0, 31, "%s", value);
		else OPTION_WITH_VALUE("--color1", key)
			snprintf(color1, 31, "%s", value);
		else OPTION_WITH_VALUE("--color2", key)
			snprintf(color2, 31, "%s", value);
		else OPTION_WITH_VALUE("--color3", key)
			snprintf(color3, 31, "%s", value);
		else OPTION("--dark", key)
			dark = True;
		else OPTION("--lang", key)
		{
			OR_OPTION_START("portuguese", value) OR_OPTION("pt", value) OR_OPTION("english", value) OR_OPTION("en", value)
			OR_OPTION("deutsch", value) OR_OPTION("de", value) OR_OPTION("spanish", value) OR_OPTION("es", value)
			OR_OPTION("italian", value) OR_OPTION("it", value) OR_OPTION("polish", value) OR_OPTION("pl", value)
			OR_OPTION("estonian", value) OR_OPTION("et", value) OR_OPTION("russian", value) OR_OPTION("ru", value)
			OR_OPTION("french", value) OR_OPTION("fr", value) OR_OPTION("bulgarian", value) OR_OPTION("bg", value)
			OR_OPTION("ukrainian", value) OR_OPTION_END("uk", value)
				snprintf(language, 31, "%s", value);
			else
			{
				printf("ERRO: LANGUAGE unavaliable\n");
				return OPTIONS_ERROR;
			}
		}
		else OPTION("--cairo", key)
			cairo_set = True;
		else OPTION("--ring", key)
			ring = True;
		else OPTION("--board", key)
			board = True;
		else OPTION("--slim", key)
			slim = True;
		else OPTION("--sls", key)
			sls = True;
		else OPTION("--nobg", key)
			nobg = True;
		else OPTION("--w", key)
			board_width = atoi(value);
		else OPTION("--h", key)
			board_height = atoi(value);
		else OPTION("--posfix", key)
			posfix = atoi(value);
		else OPTION_WITH_VALUE("--side", key)
			snprintf(side, 31, "%s", value);
		else OPTION_WITH_VALUE("--cpu", key)
			cpu = atoi(value);
		else OPTION("--orcpu", key)
			cputype = True;
		else OPTION("--cputemp", key)
			cputemp = True;
		else OPTION("--updates", key)
			aptget = True;
		else OPTION("--swap", key)
			swap = True;
		else OPTION_WITH_VALUE("--proc", key)
		{
			proc = atoi(value);
			set_process = True;
		}
		else OPTION("--nvidia", key)
			nvidia = True;
		else OPTION("--clock", key)
		{
			OPTION("default", value)
				clocktype = 0;
			else OPTION("classic", value)
				clocktype = 1;
			else OPTION("slim", value)
				clocktype = 2;
			else OPTION("modern", value)
				clocktype = 3;
			else OPTION("lucky", value)
				clocktype = 4;
			else OPTION("digital", value)
				clocktype = 5;
			else OPTION("off", value)
				clocktype = 6;
			else OPTION("cairo", value)
				clocktype = 7;
			else OPTION("bigcairo", value)
				clocktype = 8;
			else OPTION("ring", value)
				clocktype = 8;
			else
			{
				printf("ERRO: CLOCK option unavaliable\n");
				return OPTIONS_ERROR;
			}
		}
		else OPTION("--nodata", key)
			nodata = True;
		else OPTION("--calendar", key)
			set_calendar = True;
		else OPTION("--calendarzim", key)
			set_calendar = 2;
		else OPTION("--calendarm", key)
			set_calendar = 3;
		else OPTION("--photo", key)
			set_photo = 1;
		else OPTION("--photord", key)
			set_photo = 2;
		else OPTION("--task", key)
			todo = True;
		else OPTION("--battery", key)
			set_battery = True;
		else OPTION("--battery-value", key)
			battery_value = atoi(value);
		else OPTION("--hd", key)
		{
			OPTION("default", value)
				hdtype = 1;
			else OPTION("meerkat", value)
				hdtype = 2;
			else OPTION("mix", value)
				hdtype = 3;
			else OPTION("simple", value)
				hdtype = 4;
			else
			{
				printf("ERRO: HD option unavaliable\n");
				return OPTIONS_ERROR;
			}

			set_hd = True;
		}
		else OPTION_WITH_VALUE("--hdtemp1", key)
		{
			snprintf(dev1, 31, "%s", value);
			hdtemp1 = True;
		}
		else OPTION_WITH_VALUE("--hdtemp2", key)
		{
			snprintf(dev2, 31, "%s", value);
			hdtemp2 = True;
		}
		else OPTION_WITH_VALUE("--hdtemp3", key)
		{
			snprintf(dev3, 31, "%s", value);
			hdtemp3 = True;
		}
		else OPTION_WITH_VALUE("--hdtemp4", key)
		{
			snprintf(dev4, 31, "%s", value);
			hdtemp4 = True;
		}
		else OPTION("--mpd", key)
			mpd = True;
		else OPTION("--covergloobus", key)
			covergloobus = True;
		else OR_OPTION_START("--rhythmbox", key) OR_OPTION("--clementine", key) OR_OPTION_END("--banshee", key)
		{
			// Copy key to player without "--".
			snprintf(player, 31, key+2);
			// Capitalize the first character.
			player[0]=toupper(player[0]);

			OPTION("--rhythmbox", key)
				rhythmbox = True;
			else OPTION("--banshee", key)
				banshee = True;
			else OPTION("--clementine", key)
				clementine = True;

			OPTION("default", value)
				cover = 1;
			else OPTION("simple", value)
				cover = 2;
			else OPTION("vinyl", value)
				cover = 3;
			else OPTION("cd", value)
				cover = 4;
			else OPTION("case", value)
				cover = 5;
			else OPTION("glassy", value)
				cover = 6;
			else OPTION("oldvinyl", value)
				cover = 7;
			else OPTION("cairo", value)
				cover = 8;
			else OPTION("lua", value)
				cover = 9;
			else OPTION("cairo-cd", value)
				cover = 10;
			else OPTION("cairo-glassy", value)
				cover = 11;
			else OPTION("cairo-case", value)
				cover = 12;
			else OPTION("ring-cd", value)
				cover = 10;
			else OPTION("ring-glassy", value)
				cover = 11;
			else OPTION("ring-case", value)
				cover = 12;
			else
			{
				printf("ERR0: PLAYER option %s unavailable\n", value);
				return OPTIONS_ERROR;
			}
		}
		else OPTION("--gmail", key)
			gmail = True;
		else OPTION_WITH_VALUE("--user", key)
			snprintf(user, 31, "%s", value);
		else OPTION_WITH_VALUE("--passwd", key)
			snprintf(password, 31, "%s", value);
		else OPTION("--network", key)
			set_network = True;
		else OPTION("--wireless", key)
			set_wireless = True;
		else OPTION_WITH_VALUE("--eth", key)
			eth = atoi(value);
		else OPTION_WITH_VALUE("--wlan", key)
			wlan = atoi(value);
		else OPTION_WITH_VALUE("--ppp", key)
			ppp = atoi(value);
		else OPTION_WITH_VALUE("--weather", key)
		{
			snprintf(weather_code, 31, "%s", value);
			set_weather = 1;
		}
		else OPTION_WITH_VALUE("--bbcweather", key)
		{
			bbccode = atoi(value);
			set_weather = 2;
		}
		else OPTION("--unit", key)
		{
			OPTION("F", value)
			{
				snprintf(imperial, 31, " -i");
				unit = True;
			}
			else OPTION("C", value)
				;
			else
			{
				printf("ERRO: UNIT unavaliable\n");
				return OPTIONS_ERROR;
			}
		}
		else OPTION("--ubuntu", key)
		{
			sprintf(logo_letter, "u");
			logo = True;
		}
		else OPTION("--fedora", key)
		{
			sprintf(logo_letter, "N");
			logo = True;
		}
		else OPTION("--arch", key)
		{
			sprintf(logo_letter, "A");
			logo = True;
		}
		else OPTION("--opensuse", key)
		{
			sprintf(logo_letter, "h");
			logo = True;
		}
		else OPTION("--pardus", key)
		{
			sprintf(logo_letter, "i");
			logo = True;
		}
		else OPTION("--debian", key)
		{
			sprintf(logo_letter, "J");
			logo = True;
		}
		else OPTION("--gentoo", key)
		{
			sprintf(logo_letter, "Q");
			logo = True;
		}
		else OPTION("--xfce", key)
		{
			sprintf(logo_letter, "y");
			logo = True;
		}
		else OPTION("--gnome", key)
		{
			sprintf(logo_letter, "T");
			logo = True;
		}
		else OPTION("--kde", key)
		{
			sprintf(logo_letter, "Y");
			logo = True;
		}
		else OR_OPTION_START("-h", key) OR_OPTION_END("--help", key)
		{
			help();
			return OPTIONS_PREMATURE_END;
		}
		else OPTION("--datadir", key)
		{
			int len=strlen(value);
			// remove a trailing '/'.
			if(value[len-1] == '/')
				value[len-1]='\0';
			snprintf(customdir(), FINDDIR_CHAR_LEN, "%s", value);
		}
		else OPTION("--createlocalcopy", key)
		{
			system("mkdir -p ~/.conkycolors");
			systemf("cp -r %s/* %s", systemdir(), localdir());
			printf("system data were copied to %s", localdir());
			return OPTIONS_PREMATURE_END;
		}
		else OPTION("--nofilecheck", key)
			finddir_set_nofilecheck();
		else OPTION("--default_datadir", key)
		{
			print_default_datadir();
			return OPTIONS_PREMATURE_END;
		}
		else OPTION_WITH_VALUE("--finddir", key)
		{
			printf("%s\n", finddir(value));
			return OPTIONS_PREMATURE_END;
		}
		else OPTION_WITH_VALUE("--argb-value", key)
			argb_value = atoi(value);
		else OPTION_WITH_VALUE("--install", key)
		{
			OPTION("local", value)
				set_install_type(FINDDIR_LOCAL);
			else OPTION("system", value)
				set_install_type(FINDDIR_SYSTEM);
			else OPTION("custom", value)
				set_install_type(FINDDIR_CUSTOM);
			else
			{
				printf("Wrong argument (%s) for --install", value);
				return OPTIONS_ERROR;
			}
		}
		else OPTION("--systemdir", key)
		{
			printf("%s\n", systemdir());
			return OPTIONS_PREMATURE_END;
		}
		else OPTION("--localdir", key)
		{
			printf("%s\n", localdir());
			return OPTIONS_PREMATURE_END;
		}
		else
		{
			printf("Wrong option. %s", key);
			return OPTIONS_ERROR;
		}
	}

	return 0;
}

int set_default_values()
{
	strcpy(imperial,"");
	strcpy(user,"<user>");
	strcpy(password,"<password>");
	strcpy(weather_code,"BRXX0043");

	strcpy(defaultcolor, "212526");
	strcpy(color0, "E6E6E6");
	strcpy(color1, "E07A1F");
	strcpy(color2, "E6E6E6");
	strcpy(color3, "CE5C00 E07A1F");

	return 0;
}

#ifndef _options_
#define _options_

#define OPTIONS_PREMATURE_END -1
#define OPTIONS_ERROR -2

// OPTION_START(a, b) compares a with b
#define OPTION(a, b) if( strcmp(a, b) == 0 && strlen(a) == strlen(b) )
#define OPTION_WITH_VALUE(a,b) OPTION(a,b) if(value == NULL) printf("Wrong argument for %s",a); else

#define OR_OPTION_START(a, b) if( ( strcmp(a, b) == 0 && strlen(a) == strlen(b) )
#define OR_OPTION(a, b)  || ( strcmp(a,b) == 0 && strlen(a) == strlen(b) )
#define OR_OPTION_END(a,b) || ( strcmp(a,b) == 0 && strlen(a) == strlen(b) ) )

//Options
int options (int argc, char *argv[]);

#endif // #ifndef _options_

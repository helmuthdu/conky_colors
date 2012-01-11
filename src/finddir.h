#ifndef _finddir_
#define _finddir_

#define FINDDIR_CHAR_LEN 256
#define NUM_DATADIR 3

#define FINDDIR_CUSTOM 0
#define FINDDIR_LOCAL 1
#define FINDDIR_SYSTEM 2

int initialize_finddir();

const char * finddir(const char * format, ...);
char * customdir();
const char * localdir();
const char * systemdir();
const char * tempdir();
const char * get_install_datadir();
const char * get_datadir(unsigned int n);

const char * finddir_nullchar();

int num_default_datadir();
int num_datadir();
void finddir_set_nofilecheck();

int get_install_type();
void set_install_type(int type);

void print_default_datadir();

#endif // #ifndef _finddir_


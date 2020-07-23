PREFIX=/usr/local
VPATH=src/
CFLAGS:=$(CFLAGS) -fcommon -DDESTDIR=\"$(DESTDIR)$(PREFIX)\" -Wall -std=c99
CWD:=$(shell pwd)

all: conky-colors
conky-colors: conky-colors.c conkycover.c conkyplayer.c \
	conkyrc_cairo.c conkyrc_ring.c conkyrc_board.c conkyrc_default.c conkyrc_slim.c conkyrc_sls.c \
	coverposition.c finddir.c help.c options.c photoposition.c themes.c translations.c variables.c \
	confinstall.c utils.c initialize.c

install: conky-colors conkyrc
	install -Dm755 conky-colors $(DESTDIR)$(PREFIX)/bin/conky-colors
	find conkycolors/bin -type f -exec install -Dm755 {} $(DESTDIR)$(PREFIX)/share/{} \;
	find conkycolors/scripts -type f -exec install -Dm755 {} $(DESTDIR)$(PREFIX)/share/{} \;
	find conkycolors/icons -type f -exec install -Dm644 {} $(DESTDIR)$(PREFIX)/share/{} \;
	find conkycolors/templates -type f -exec install -Dm644 {} $(DESTDIR)$(PREFIX)/share/{} \;
	find fonts/conkycolors -type f -exec install -Dm644 {} $(DESTDIR)$(PREFIX)/share/{} \;
	ln -fs $(DESTDIR)$(PREFIX)/share/conkycolors/bin/conkyTask $(DESTDIR)$(PREFIX)/bin/ct

conkyrc: conky-colors

clean:
	rm -f conky-colors

uninstall:
	rm -rf $(DESTDIR)$(PREFIX)/share/conkycolors
	rm -fr $(DESTDIR)$(PREFIX)/share/fonts/conkycolors
	rm $(DESTDIR)$(PREFIX)/bin/conky-colors
	rm $(DESTDIR)$(PREFIX)/bin/ct

.PHONY: all clean install uninstall


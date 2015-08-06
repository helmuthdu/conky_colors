VPATH=src/
CFLAGS=-Wall -std=c99
CWD:=$(shell pwd)

all: conky-colors
conky-colors: conky-colors.c conkycover.c conkyplayer.c \
	conkyrc_cairo.c conkyrc_ring.c conkyrc_board.c conkyrc_default.c conkyrc_slim.c conkyrc_sls.c \
	coverposition.c finddir.c help.c options.c photoposition.c themes.c translations.c variables.c \
	confinstall.c utils.c initialize.c

install: conky-colors conkyrc
	install -Dm755 conky-colors $(DESTDIR)/bin/conky-colors
	find conkycolors/bin -type f -exec install -Dm755 {} $(DESTDIR)/usr/share/{} \;
	find conkycolors/scripts -type f -exec install -Dm755 {} $(DESTDIR)/usr/share/{} \;
	find conkycolors/icons -type f -exec install -Dm644 {} $(DESTDIR)/usr/share/{} \;
	find conkycolors/templates -type f -exec install -Dm644 {} $(DESTDIR)/usr/share/{} \;
	find fonts/conkycolors -type f -exec install -Dm644 {} $(DESTDIR)/usr/share/{} \;
	ln -fs $(DESTDIR)/usr/share/conkycolors/bin/conkyTask $(DESTDIR)/usr/bin/ct

conkyrc: conky-colors

clean:
	rm -f conky-colors

uninstall:
	rm -rf $(DESTDIR)/usr/share/conkycolors
	rm -fr $(DESTDIR)/usr/share/fonts/conkycolors
	rm $(DESTDIR)/usr/bin/conky-colors
	rm $(DESTDIR)/usr/bin/ct

.PHONY: all clean install uninstall


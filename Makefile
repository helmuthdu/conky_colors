VPATH=src/
CFLAGS=-Wall -std=c99
CWD:=$(shell pwd)

all: conky-colors
conky-colors: conky-colors.c conkycover.c conkyplayer.c \
	conkyrc_cairo.c conkyrc_ring.c conkyrc_board.c conkyrc_default.c conkyrc_slim.c conkyrc_sls.c \
	coverposition.c finddir.c help.c options.c photoposition.c themes.c translations.c variables.c \
	confinstall.c utils.c initialize.c

install: conky-colors conkyrc
	mkdir -p $(DESTDIR)/usr/share
	mkdir -p $(DESTDIR)/usr/share/fonts/TTF/conky
	mkdir -p $(DESTDIR)/usr/share/fonts/OTF/conky
	mkdir -p $(DESTDIR)/usr/bin
	cp -v conky-colors $(DESTDIR)/usr/bin
	cp -v -r conkycolors $(DESTDIR)/usr/share
	ln -fs $(DESTDIR)/usr/share/conkycolors/bin/conkyTask $(DESTDIR)/usr/bin/ct
	cp -v fonts/conkycolors/*.ttf fonts/conkycolors/*.TTF $(DESTDIR)/usr/share/fonts/TTF/conky
	chmod +x $(DESTDIR)/usr/share/conkycolors/scripts/*
	chmod +x $(DESTDIR)/usr/share/conkycolors/bin/*
	chmod -R 755 $(DESTDIR)/usr/share/conkycolors/

conkyrc: conky-colors

clean:
	rm -f conky-colors

uninstall:
	rm -rf $(DESTDIR)/usr/share/conkycolors
	rm $(DESTDIR)/usr/bin/conky-colors
	rm $(DESTDIR)/usr/bin/ct
	for file in $$(find $(CWD)/fonts/conkycolors -iname *.ttf -print0); do \
		rm $(DESTDIR)/usr/share/fonts/TTF/conky/$$(basename $$file); \
		done

.PHONY: all clean install uninstall


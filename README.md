[Conky](http://conky.sourceforge.net/) is a free, light-weight system monitor for X, that displays any information on your desktop.

**CONKY-colors** is an easier way to configure Conky.

This conky script support multilanguage:
Bulgarian, English, German, Italian, Polish, Portuguese, Russian, Spanish and Ukrainian

How to install
==============

Go to a terminal and type:

```
$sudo apt-get install aptitude python-statgrab python-keyring ttf-ubuntu-font-family hddtemp curl lm-sensors conky-all
$sudo chmod u+s /usr/sbin/hddtemp
$sudo sensors-detect #answering Yes (default) to all questions, even that last one that defaults to No
```

Now restart your session.

Download and extract the _conky-colors.tar.gz_ and type in terminal in the same directory that has been extracted.

```
$make
$sudo make install
$conky-colors {options}
```

Ex: if your cpu is quad-core and you want the noble color, with hd, network and pidgin monitor and all in portuguese

```
conky-colors --theme=noble --lang=en --cpu=4 --network --hd=default --pidgin
```

For a working weather script you **NEED** to define, in a user specific config file, a partner id and registration code for the weather.com xoap service. For this purpose copy _.conkyForecast.config_ in _/usr/share/conkycolors_ folder to your home and setup as required.

_bbcweather/yahooweather_ widget don't need any kind of registration

For a working photo widget you need to specify a file or directory in _conkyPhoto_ or _conkyPhotoRandom_ script in _~/.conkycolors/bin/_

Update your font cache:

```
$sudo fc-cache -v -f
```

SCRIPTS
=======

In follow links you will find instructions about how to use those scripts:

Conky Weather Script: http://ubuntuforums.org/showthread.php?t=869328

Conky SSL Mail Script: http://ubuntuforums.org/showthread.php?t=869771

Conky Pidgin Script: http://ubuntuforums.org/showthread.php?t=969933&highlight=pidgin+conky

Conky Rhythmbox Script: http://ubuntuforums.org/showthread.php?t=928168&highlight=conky+rhythmbox

Conky Banshee Script: http://ubuntuforums.org/showthread.php?p=7683570

Conky Exaile Script: http://ubuntuforums.org/showthread.php?t=926041

in terminal type `conky -c ~/.conkycolors/conkyrc`.

To run conky at startup, go to _System_ > _Preferences_ > _Startup Applications_, click "Add" and add the path to the conkyStart file (_/usr/share/conkycolors/bin/conkyStart_)

Have Fun!

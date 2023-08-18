# Conky :tw-1f4a0: 
[Conky](http://conky.sourceforge.net/) is a free, light-weight system monitoring tool designed for X Window System environments. It provides a highly customizable and visually appealing way to display various types of information directly on your desktop. Conky can show real-time data such as CPU usage, memory utilization, network activity, disk usage, system temperatures, and more, in the form of text and graphical elements.

**CONKY-colors** 🎨 is an easier way to configure Conky.

This conky script supports multilanguage 🌐:
Bulgarian, English, German, Italian, Polish, Portuguese, Russian, Spanish, and Ukrainian.

## How to install 

Open a terminal and type:

```shell
sudo apt-get install aptitude python-statgrab python-keyring ttf-ubuntu-font-family hddtemp curl lm-sensors conky-all
sudo chmod u+s /usr/sbin/hddtemp
sudo sensors-detect #answering Yes (default) to all questions, even that last one that defaults to No
```

Now restart your session.

Download and extract the _conky-colors.tar.gz_ and type in the terminal in the same directory that has been extracted:

```shell
make
sudo make install
conky-colors {options}
```

For example, if your CPU is quad-core and you want the noble color, with HD, network, and Pidgin monitor, all in Portuguese:

```shell
conky-colors --theme=noble --lang=en --cpu=4 --network --hd=default --pidgin
```

For a working weather script, you **NEED** to define, in a user-specific config file, a partner id and registration code for the weather.com xoap service. For this purpose, copy _.conkyForecast.config_ in _/usr/share/conkycolors_ folder to your home and set up as required.

_bbcweather/yahooweather_ widget doesn't need any kind of registration.

For a working photo widget, you need to specify a file or directory in _conkyPhoto_ or _conkyPhotoRandom_ script in _~/.conkycolors/bin/_.

Update your font cache:

```shell
sudo fc-cache -v -f
```

## Scripts 📜

In the following links, you will find instructions about how to use those scripts:

- [Conky Weather Script](http://ubuntuforums.org/showthread.php?t=869328)
- [Conky SSL Mail Script](http://ubuntuforums.org/showthread.php?t=869771)
- [Conky Pidgin Script](http://ubuntuforums.org/showthread.php?t=969933&highlight=pidgin+conky)
- [Conky Rhythmbox Script](http://ubuntuforums.org/showthread.php?t=928168&highlight=conky+rhythmbox)
- [Conky Banshee Script](http://ubuntuforums.org/showthread.php?p=7683570)
- [Conky Exaile Script](http://ubuntuforums.org/showthread.php?t=926041)


###  Launching Conky with Custom Configuration

To start Conky with a specific configuration file, use the following command:

``` 
conky -c ~/.conkycolors/conkyrc
```
To run Conky at startup, follow these steps:
  - Open the **System** menu.
  - Go to **Preferences** and select **Startup Applications**.
  - Click "Add" to add a new startup application.
  - Add the path to the conkyStart file: `/usr/share/conkycolors/bin/conkyStart`.

This will ensure that Conky starts automatically when you log in to your system.

Have Fun! 🎉
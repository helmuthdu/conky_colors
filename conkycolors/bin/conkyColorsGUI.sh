#!/bin/bash
check_exit_option()
{
	if [ $? = 1 ]; then
		zenity --info --title="Quitting" --text="Thank you for using this script"
		exit
	fi
}
#Language
LANG=$(zenity --list \
	--title="Welcome to Conky-colors configuration script" \
	--text="Choose Your language" \
	--radiolist \
	--column="" --column="Option" \
	TRUE "english" \ FALSE "bulgarian" \ FALSE "deutsch" \ FALSE "estonian" \ FALSE "italian" \ FALSE "polish" \ FALSE "portugese" \ FALSE "russian" \ FALSE "spanish");
case $LANG in
	"english") LANG=' --lang=en' ;;
"bulgarian") LANG=' --lang=bg' ;;
"deutsch") LANG='  --lang=de' ;;
"estonian") LANG='  --lang=et' ;;
"italian") LANG='  --lang=it' ;;
"polish") LANG='  --lang=pl' ;;
"portugese") LANG='  --lang=pt' ;;
"russian") LANG='  --lang=ru' ;;
"spanish") LANG='  --lang=es';;
esac
check_exit_option
#Theme
CHOICE2=$(zenity --list \
	--title="Welcome to Conky-colors configuration script" \
	--text="Choose Your theme" \
	--radiolist \
	--column="" --column="Option" \
	TRUE "gnome-human" \ FALSE "gnome-brave" \ FALSE "gnome-carbonite" \ FALSE "gnome-noble" \ FALSE "gnome-tribute" \ FALSE "gnome-wine" \ FALSE "gnome-wise" \ FALSE "shiki-brave" \ FALSE "shiki-human" \ FALSE "shiki-noble" \ FALSE "shiki-wine" \ FALSE "shiki-wise" \ FALSE "shiki-dust" \ FALSE "dust" \ FALSE "radiance" \ FALSE "ambiance" \ FALSE "elementary");
check_exit_option
echo $CHOICE2
#widgets 1
CHOICE3=$(zenity --list \
	--title="Welcome to Conky-colors configuration script" \
	--text="Choose widgets 1" \
	--checklist \
	--column="" --column="Option" \
	FALSE "Enable CPU temperature" \ FALSE "Enable SWAP" \ FALSE "Enable battery" \ FALSE "Show updates of Debian/Ubuntu" \ FALSE "Enable CoverGloobus widget" \ FALSE "Enable MPD widget" \ FALSE "Enable nvidia gpu widget" \ FALSE "Disable Data widget" \ FALSE "Enable ToDo widget");
check_exit_option
if [[ $CHOICE3 =~ "Enable CPU temperature" ]]; then
	CPU=" --cputemp"
fi
if [[ $CHOICE3 =~ "Enable SWAP" ]]; then
	SWAP=" --swap"
fi
if [[ $CHOICE3 =~ "Enable battery" ]]; then
	BAT=" --battery"
fi
if [[ $CHOICE3 =~ "Show updates of Debian/Ubuntu" ]]; then
	UPDATES=" --updates"
fi
if [[ $CHOICE3 =~ "Enable CoverGloobus widget" ]]; then
	GLOO=" --covergloobus"
fi
if [[ $CHOICE3 =~ "Enable MPD widget" ]]; then
	MPD=" --mpd"
fi
if [[ $CHOICE3 =~ "Enable nvidia gpu widget" ]]; then
	NVIDIA=" --nvidia"
fi
if [[ $CHOICE3 =~ "Disable Data widget" ]]; then
	DATA=" --nodata"
fi
if [[ $CHOICE3 =~ "Enable ToDo widget" ]]; then
	TODO=" --todo"
fi
if [[ $CHOICE3 = "" ]]; then
	zenity --title "Conky-colors configuration script" --question --text "You didn't choose anything, do you want to continue whithout those widgets ??"
fi
#cores
CHOICE4=$(zenity --scale --title "Cores" --text "How many cores do You have..." --min-value=1 --max-value=6 --value=2);
check_exit_option
echo $CHOICE4
#logo
if zenity --question --text="Do you want to choose Your Distro-logo?"; then
	LOGO=$(zenity --list \
		--title="Welcome to Conky-colors configuration script" \
		--text="Choose Your Distro-logo" \
		--radiolist \
		--column="" --column="Option" \
		TRUE "ubuntu" \ FALSE "fedora" \ FALSE "opensuse" \ FALSE "debian" \ FALSE "arch" \ FALSE "gentoo" \ FALSE "pardus" \ FALSE "xfce" \ FALSE "gnome");
	case $LOGO in
		"ubuntu") LOGO=' --ubuntu' ;;
	"fedora") LOGO=' --fedora' ;;
"opensuse") LOGO=' --opensuse' ;;
"debian") LOGO=' --debian' ;;
"arch") LOGO=' --arch' ;;
"gentoo") LOGO=' --gentoo' ;;
"pardus") LOGO=' --pardus' ;;
"xfce") LOGO=' --xfce' ;;
"gnome") LOGO=' --gnome';;
esac
check_exit_option
fi
#clock
if zenity --question --text="Enable clock widget and set type?"; then
	CLOCK=$(zenity --list \
		--title="Welcome to Conky-colors configuration script" \
		--text="Enable clock widget and set type" \
		--radiolist \
		--column="" --column="Option" \
		TRUE "default" \ FALSE "classic" \ FALSE "slim" \ FALSE "modern" \ FALSE "lucky" \ FALSE "digital");
	case $CLOCK in
		"default") CLOCK=' --clock=default' ;;
	"classic") CLOCK=' --clock=classic' ;;
"slim") CLOCK=' --clock=slim' ;;
"modern") CLOCK=' --clock=modern' ;;
"lucky") CLOCK=' --clock=lucky' ;;
"digital") CLOCK=' --clock=digital' ;;
esac
check_exit_option
fi
#Calendar widget CAL ############################
CAL=$(zenity --list \
	--title="Welcome to Conky-colors configuration script" \
	--text="Enable/disable Calendar widget?" \
	--radiolist \
	--column="" --column="Option" \
	TRUE "Enable" \ FALSE "Enable and set monday as first day in the week" \ FALSE "Disable");
case $CAL in
	"Enable") CAL=' --calendar' ;;
"Enable and set monday as first day in the week") CAL=' --calendar -m' ;;
"Disable") CAL=' ' ;;
esac
check_exit_option
#HD widget
if zenity --question --text="Enable HD widget?"; then
	HD=$(zenity --list \
		--title="Welcome to Conky-colors configuration script" \
		--text="Choose Your HD widget" \
		--radiolist \
		--column="" --column="Option" \
		TRUE "default" \ FALSE "meerkat" \ FALSE "mix" \ FALSE "simple");
	case $HD in
		"default") HD=' --hd=default' ;;
	"meerkat") HD=' --hd=meerkat' ;;
"mix") HD=' --hd=mix' ;;
"simple") HD=' --hd=simple' ;;
esac
check_exit_option
fi
conky-colors --theme=${CHOICE2} --cpu=${CHOICE4} $LANG$LOGO$CPU$SWAP$BAT$UPDATES$GLOO$MPD$NVIDIA$DATA$TODO$CLOCK$HD$CAL

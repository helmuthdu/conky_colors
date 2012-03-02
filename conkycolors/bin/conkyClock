#!/bin/sh
# clock.sh
# Written by Crinos512
# Original concept by t-mo_
#
# Usage: ${execpi 20 ~/.conky/conkyparts/clock.sh hour}
#         - or -
#        ${execpi 20 ~/.conky/conkyparts/clock.sh minute}

#Hour
case "$1" in
'hour')
  HOUR=`date +%H`
  MINUTE=`date +%M`
  case $HOUR in
    00 | 12)
      case $MINUTE in
        0[0-9] | 1[0-2]) echo "A" ;;
        1[3-9] | 2[0-2]) echo "B" ;;
        2[3-9] | 3[0-5]) echo "C" ;;
        3[6-9] | 4[0-8]) echo "D" ;;
        49 | 5[0-9]) echo "E" ;;
        *) echo "ERROR in Hour mod 00"   ;;
      esac
      ;;
    01 | 13)
      case $MINUTE in
        0[0-9] | 1[0-2]) echo "F" ;;
        1[3-9] | 2[0-2]) echo "G" ;;
        2[3-9] | 3[0-5]) echo "H" ;;
        3[6-9] | 4[0-8]) echo "I" ;;
        49 | 5[0-9]) echo "J" ;;
        *) echo "ERROR in Hour mod 01"   ;;
      esac
      ;;
    02 | 14)
      case $MINUTE in
        0[0-9] | 1[0-2]) echo "K" ;;
        1[3-9] | 2[0-2]) echo "L" ;;
        2[3-9] | 3[0-5]) echo "M" ;;
        3[6-9] | 4[0-8]) echo "N" ;;
        49 | 5[0-9]) echo "O" ;;
        *) echo "ERROR in Hour mod 02"   ;;
      esac
      ;;
    03 | 15)
      case $MINUTE in
        0[0-9] | 1[0-2]) echo "P" ;;
        1[3-9] | 2[0-2]) echo "Q" ;;
        2[3-9] | 3[0-5]) echo "R" ;;
        3[6-9] | 4[0-8]) echo "S" ;;
        49 | 5[0-9]) echo "T" ;;
        *) echo "ERROR in Hour mod 03"   ;;
      esac
      ;;
    04 | 16)
      case $MINUTE in
        0[0-9] | 1[0-2]) echo "U" ;;
        1[3-9] | 2[0-2]) echo "V" ;;
        2[3-9] | 3[0-5]) echo "W" ;;
        3[6-9] | 4[0-8]) echo "X" ;;
        49 | 5[0-9]) echo "Y" ;;
        *) echo "ERROR in Hour mod 04"   ;;
      esac
      ;;
    05 | 17)
      case $MINUTE in
        0[0-9] | 1[0-2]) echo "Z" ;;
        1[3-9] | 2[0-2]) echo "a" ;;
        2[3-9] | 3[0-5]) echo "b" ;;
        3[6-9] | 4[0-8]) echo "c" ;;
        49 | 5[0-9]) echo "d" ;;
        *) echo "ERROR in Hour mod 05"   ;;
      esac
      ;;
    06 | 18)
      case $MINUTE in
        0[0-9] | 1[0-2]) echo "e" ;;
        1[3-9] | 2[0-2]) echo "f" ;;
        2[3-9] | 3[0-5]) echo "g" ;;
        3[6-9] | 4[0-8]) echo "h" ;;
        49 | 5[0-9]) echo "i" ;;
        *) echo "ERROR in Hour mod 06"   ;;
      esac
      ;;
    07 | 19)
      case $MINUTE in
        0[0-9] | 1[0-2]) echo "j" ;;
        1[3-9] | 2[0-2]) echo "k" ;;
        2[3-9] | 3[0-5]) echo "l" ;;
        3[6-9] | 4[0-8]) echo "m" ;;
        49 | 5[0-9]) echo "n" ;;
        *) echo "ERROR in Hour mod 07"   ;;
      esac
      ;;
    08 | 20)
      case $MINUTE in
        0[0-9] | 1[0-2]) echo "o" ;;
        1[3-9] | 2[0-2]) echo "p" ;;
        2[3-9] | 3[0-5]) echo "q" ;;
        3[6-9] | 4[0-8]) echo "r" ;;
        49 | 5[0-9]) echo "s" ;;
        *) echo "ERROR in Hour mod 08"   ;;
      esac
      ;;
    09 | 21)
      case $MINUTE in
        0[0-9] | 1[0-2]) echo "t" ;;
        1[3-9] | 2[0-2]) echo "u" ;;
        2[3-9] | 3[0-5]) echo "v" ;;
        3[6-9] | 4[0-8]) echo "w" ;;
        49 | 5[0-9]) echo "x" ;;
        *) echo "ERROR in Hour mod 09"   ;;
      esac
      ;;
    10 | 22)
      case $MINUTE in
        0[0-9] | 1[0-2]) echo "y" ;;
        1[3-9] | 2[0-2]) echo "z" ;;
        2[3-9] | 3[0-5]) echo "1" ;;
        3[6-9] | 4[0-8]) echo "2" ;;
        49 | 5[0-9]) echo "3" ;;
        *) echo "ERROR in Hour mod 10"   ;;
      esac
      ;;
    11 | 23)
      case $MINUTE in
        0[0-9] | 1[0-2]) echo "4" ;;
        1[3-9] | 2[0-2]) echo "5" ;;
        2[3-9] | 3[0-5]) echo "6" ;;
        3[6-9] | 4[0-8]) echo "7" ;;
        49 | 5[0-9]) echo "8" ;;
        *) echo "ERROR in Hour mod 11"   ;;
      esac
      ;;
     *) echo "ERROR finding Hour"   ;;
  esac
  ;;

'minute')
  MINUTE=`date +%M`
  case $MINUTE in
    00) echo "A" ;;
    01) echo "B" ;;
    02) echo "C" ;;
    03) echo "D" ;;
    04) echo "E" ;;
    05) echo "F" ;;
    06) echo "G" ;;
    07) echo "H" ;;
    08) echo "I" ;;
    09) echo "J" ;;
    10) echo "K" ;;
    11) echo "L" ;;
    12) echo "M" ;;
    13) echo "N" ;;
    14) echo "O" ;;
    15) echo "P" ;;
    16) echo "Q" ;;
    17) echo "R" ;;
    18) echo "S" ;;
    19) echo "T" ;;
    20) echo "U" ;;
    21) echo "V" ;;
    22) echo "W" ;;
    23) echo "X" ;;
    24) echo "Y" ;;
    25) echo "Z" ;;
    26) echo "a" ;;
    27) echo "b" ;;
    28) echo "c" ;;
    29) echo "d" ;;
    30) echo "e" ;;
    31) echo "f" ;;
    32) echo "g" ;;
    33) echo "h" ;;
    34) echo "i" ;;
    35) echo "j" ;;
    36) echo "k" ;;
    37) echo "l" ;;
    38) echo "m" ;;
    39) echo "n" ;;
    40) echo "o" ;;
    41) echo "p" ;;
    42) echo "q" ;;
    43) echo "r" ;;
    44) echo "s" ;;
    45) echo "t" ;;
    46) echo "u" ;;
    47) echo "v" ;;
    48) echo "w" ;;
    49) echo "x" ;;
    50) echo "y" ;;
    51) echo "z" ;;
    52) echo "1" ;;
    53) echo "2" ;;
    54) echo "3" ;;
    55) echo "4" ;;
    56) echo "5" ;;
    57) echo "6" ;;
    58) echo "7" ;;
    59) echo "8" ;;
    *) echo "ERROR finding Minute" ;;
  esac
  ;;
esac
exit 0

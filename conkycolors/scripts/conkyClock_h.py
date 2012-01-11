import time
h1=["u\u0021", "u\u0022", "u\u0023", "u\u0024", "u\u0025"]
h2=["u\u0026","u\u0027","u\u0028","u\u0029","u\u002A"]
h3=["u\u002B","u\u002C","u\u002D","u\u002E","u\u002F"]
h4=["0","1","2","3","4"]
h5=["5","6","7","8","9"]
h6=["u\u003A","u\u003B","u\u003C","u\u003D","u\u003E"]
h7=["u\u003F","u\u0040","A","B","C"]
h8=["D","E","F","G","H"]
h9=["I","J","K","L","M"]
h10=["N","O","P","Q","R"]
h11=["S","T","U","V","W"]
h12=["X","Y","Z","u\u005B","u\u005C"]

hIntervals = [h1,h2,h3,h4,h5,h6,h7,h8,h9,h10,h11,h12]

h = int(time.strftime("%l"))
if h==12:
    h=0;
min = int(time.strftime("%M"))

print (hIntervals[h][int(min/12)])

import time,os
i1=["u\u0022","u\u0023","u\u0024","u\u0025","u\u0026"]
i2=["u\u0027","u\u0028","u\u0029","u\u002A","u\u002B"]
i3=["u\u002C","u\u002D","u\u002E","u\u002F","0"]
i4=["1","2","3","4","5"]
i5=["6","7","8","9","u\u003A"]
i6=["u\u003B","u\u003C","u\u003D","u\u003E","u\u003F"]
i7=["u\u0040","A","B","C","D"]
i8=["E","F","G","H","I"]
i9=["J","K","L","M","N"]
i10=["O","P","Q","R","S"]
i11=["T","U","V","W","X"]
i12=["Y","Z","u\u005B","u\u005C","!"]

minList = [i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,i11,i12]
min = int(time.strftime("%M"))

print (minList[int(min/5)][int(min%5)])

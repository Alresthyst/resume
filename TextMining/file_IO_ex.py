# writedata.py
f = open("C:\Alrescha\Research\FILE_LO\새파일.txt", 'w')
a=[0, 1, 0, 2]
strasd = ','.join(str(x) for x  in a)
f.write(strasd+"\n")
f.close()
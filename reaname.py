import os

#os.rename('a.txt', 'b.kml')
path = "D:\OnePiece\One Piece S03"
pathfile = "D:\OnePiece\One Piece S03\{}"
start = 77
for x in os.listdir(path):
    if x != "desktop.ini":
        print(x)
        Season = 0
        Episode = 0
        renamestr = ""
        for x2 in x:
            if x2 == "S":
                Spos = x.find(x2)
                Season = int(x[Spos+1:Spos+3])
                print(Season)
            if x2 == "E":
                Spos = x.find(x2)
                num = 4
                try:
                    Episode = int(x[Spos+1:Spos+4])
                except:
                    Episode = int(x[Spos+1:Spos+3])
                    num = 3
                print(Episode)
                renamestr = x[:Spos+1] + str(Episode+start) + " " + x[Spos+num:]
    print(renamestr)
    #os.rename(pathfile.format(x),pathfile.format(renamestr))
        
                
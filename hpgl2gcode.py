import sys
import re

#open file passed as argument
if len(sys.argv)>1:
 f = open(sys.argv[1],'r')
else:
 print('usage: python hpgl2code.py inputfile.hpgl > outputfile.gcode')
 sys.exit(1)

#decoded commands
#PA x,y;  //pen advance xy unit=25um ie 40 units/mm
#PU;    //pen up - replace with G1 Z'up' (safe Z heigh constant)
#PD;    //pen down - - replace with G1 Z'dn' (engrawing depth constant)

#constants
zup=5 # 5mm should be safe enough
zdn=0 # using 0, for engraving negative values to be used
upm=40 # hpgl units per mm (in theory should be 40.2)
epm=0 # extrude per mm - in case I'm trying to plot with PLA
feed=500 #default feedrate

#init stuff - whatever g commands 
print("G21") # units in mm
print("G1 Z",zup," F",feed,sep="") # pen up before 1st move
#process the input file
pa = re.compile('^PA ([0-9]*),([0-9]*);') #regex for parsing PA command
for line in f:
 if re.search('^PA',line):
  #parse a bit
  mpa=pa.match(line);
  x=int(mpa.group(1))/upm
  y=int(mpa.group(2))/upm
  print("G1 X",x," Y",y," F",feed,sep="")
 else:
  if re.search('^PU',line ):
   print("G1 Z",zup," F",feed,sep="")
  else:
   if re.search('^PD',line ):
    print("G1 Z",zdn," F",feed,sep="")
 

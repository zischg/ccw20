import arcpy
import numpy
myfile="D:/CCW20/input/BestandeskarteGR/bk_best_F_View.shp"
numcursor = arcpy.da.UpdateCursor(myfile, ["GDICK", "Buche"])
for row in numcursor:
    in2 = str(row[0])
    if "BU" in in2:
        row[1]=1
    else:
        row[1]=0
    numcursor.updateRow(row)

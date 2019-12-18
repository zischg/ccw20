import arcpy
import os
import sys
import shutil

projectdir="D:/CCW20"
targetgeodatabase=projectdir+"/GIS/"+"geocover.gdb"
targetworkspace=targetgeodatabase+"/GC_ROCK_BODIES"
bedrock="GC_BEDROCK"
exploit_PLG="GC_EXPLOIT_GEOMAT_PLG"
exploit_PT="GC_EXPLOIT_GEOMAT_PT"
fossils="GC_FOSSILS"
linearobjects="GC_LINEAR_OBJECTS"
pointobjects="GC_POINT_OBJECTS"
surfaces="GC_SURFACES"
unco="GC_UNCO_DESPOSIT"

#list all directories
os.chdir(importdir)
V2maplist=[]
for f in os.listdir(importdir):
    if "-V2-" in f and ".zip" not in f:
        V2maplist.append(f)
#load data into target geodatabase
for geocoverdir in V2maplist:
    print geocoverdir
    if "Data" in os.listdir(importdir+"/"+geocoverdir):
        if "FGDB" in os.listdir(importdir+"/"+geocoverdir+"/"+"Data"):
            os.chdir(importdir + "/" + geocoverdir+"/"+"Data/FGDB/de")
            for gd in os.listdir(importdir + "/" + geocoverdir+"/"+"Data/FGDB/de"):
                if ".gdb" in gd:
                    sourcegeodatabase=importdir + "/" + geocoverdir+"/"+"Data/FGDB/de/"+gd
                    #load data
                    #arcpy.LoadData_production(targetgeodatabase, sourcegeodatabase+"/GC_ROCK_BODIES", targetgeodatabase+"/GC_ROCK_BODIES")
                    arcpy.Append_management([sourcegeodatabase+"/GC_ROCK_BODIES/"+bedrock], targetworkspace+"/"+bedrock, "TEST")
                    arcpy.Append_management([sourcegeodatabase + "/GC_ROCK_BODIES/" + exploit_PLG],targetworkspace + "/" + exploit_PLG, "TEST")
                    arcpy.Append_management([sourcegeodatabase + "/GC_ROCK_BODIES/" + exploit_PT], targetworkspace + "/" + exploit_PT, "TEST")
                    arcpy.Append_management([sourcegeodatabase + "/GC_ROCK_BODIES/" + fossils],targetworkspace + "/" + fossils, "TEST")
                    arcpy.Append_management([sourcegeodatabase + "/GC_ROCK_BODIES/" + linearobjects],targetworkspace + "/" + linearobjects, "TEST")
                    arcpy.Append_management([sourcegeodatabase + "/GC_ROCK_BODIES/" + pointobjects], targetworkspace + "/" + pointobjects, "TEST")
                    arcpy.Append_management([sourcegeodatabase + "/GC_ROCK_BODIES/" + surfaces],targetworkspace + "/" + surfaces, "TEST")
                    arcpy.Append_management([sourcegeodatabase + "/GC_ROCK_BODIES/" + unco],targetworkspace + "/" + unco, "TEST")
                    shutil.rmtree(importdir + "/" + geocoverdir, ignore_errors=True)
                    print geocoverdir+" loaded ..."
print "done .."
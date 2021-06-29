import numpy
def gridasciitonumpyarrayint(ingridfilefullpath):
    i=0
    row = 0
    headerstr=''
    infile=open(ingridfilefullpath, "r")
    for line in infile:
        if i==0:
            ncols=int(line.strip().split()[-1])
            headerstr+=line
        elif i==1:
            nrows=int(line.strip().split()[-1])
            headerstr += line
        elif i==2:
            xllcorner=float(line.strip().split()[-1])
            headerstr += line
        elif i==3:
            yllcorner=float(line.strip().split()[-1])
            headerstr += line
        elif i==4:
            cellsize=float(line.strip().split()[-1])
            headerstr += line
        elif i==5:
            NODATA_value=float(line.strip().split()[-1])
            arr=numpy.zeros((nrows, ncols), dtype=int)
            arr[:,:]=NODATA_value
            headerstr += line.replace("\n","")
        elif i>5 and i<nrows:
            col=0
            while col<ncols:
                for item in line.strip().split():
                    arr[row,col]=float(item)
                    col+=1
            row+=1
        i+=1
    infile.close()
    return arr, ncols, nrows, xllcorner, yllcorner, cellsize, NODATA_value, headerstr
def gridasciitonumpyarrayfloat(ingridfilefullpath):
    i=0
    row = 0
    headerstr=''
    infile=open(ingridfilefullpath, "r")
    for line in infile:
        if i==0:
            ncols=int(line.strip().split()[-1])
            headerstr+=line
        elif i==1:
            nrows=int(line.strip().split()[-1])
            headerstr += line
        elif i==2:
            xllcorner=float(line.strip().split()[-1])
            headerstr += line
        elif i==3:
            yllcorner=float(line.strip().split()[-1])
            headerstr += line
        elif i==4:
            cellsize=float(line.strip().split()[-1])
            headerstr += line
        elif i==5:
            NODATA_value=float(line.strip().split()[-1])
            arr=numpy.zeros((nrows, ncols), dtype=float)
            arr[:,:]=NODATA_value
            headerstr += line.replace("\n","")
        elif i>5 and i<nrows:
            col=0
            while col<ncols:
                for item in line.strip().split():
                    arr[row,col]=float(item)
                    col+=1
            row+=1
        i+=1
    infile.close()
    return arr, ncols, nrows, xllcorner, yllcorner, cellsize, NODATA_value, headerstr
maxupstreampixels=20
NODATA_value=-9999
myworkspace="D:CCW20/GIS"


#print "read rasters ..."
demarr, ncols, nrows, xllcorner, yllcorner, cellsize, NODATA_value, headerstr=gridasciitonumpyarrayfloat(myworkspace+"/dhm25fill.asc")
#print "DEM read ..."
#print "ncols: "+str(ncols)
#print "nrows: "+str(nrows)
#print "cellsize: "+str(cellsize)
pharr=gridasciitonumpyarrayint(myworkspace+"/chli_ph.asc")[0]
fdarr=gridasciitonumpyarrayint(myworkspace+"/dhm25fd.asc")[0]
rasrows=numpy.shape(demarr)[0]
rascols=numpy.shape(demarr)[1]
#print "ph basis read ..."


#*****************************************************************************************************************
#loop through pharr until no cell with value == -1 exists
count9999s = 0
i=1
while i<rasrows-1:
    #print i
    print(i)
    j=1
    while j<rascols-1:
        if pharr[i,j]==-1 and 1<=fdarr[i,j] <=128 and demarr[i,j]!=NODATA_value:
            # look around for the 8 neighbors and chose the cell with the highest z-value (higher than center cell)
            x = i
            y = j
            z1=demarr[i,j]
            stopcondition = 0
            counter =0
            while x >= 0 and x < rasrows and y >= 0 and y < rascols and stopcondition == 0 and demarr[x,y]>=z1:
                if fdarr[x,y]==1:
                    y-=1
                elif fdarr[x,y]==2:
                    x-=1
                    y-=1
                elif fdarr[x,y]==4:
                    x-=1
                elif fdarr[x,y]==8:
                    x-=1
                    y+=1
                elif fdarr[x,y]==16:
                    y+=1
                elif fdarr[x,y]==32:
                    x+=1
                    y+=1
                elif fdarr[x,y]==64:
                    x+=1
                elif fdarr[x,y]==128:
                    x+=1
                    y-=1
                else:
                    stopcondition=1
                counter += 1
                z2 = demarr[x, y]
                if x==i and y==j:
                    stopcondition=1
                if z2<z1:
                    stopcondition = 1
                ph=pharr[x,y]
                if 0<ph<=8:
                    pharr[i,j]=ph
                    stopcondition=1
                if counter>200:
                    stopcondition=1
        j+=1
    i+=1


count=0
i=1
while i<rasrows-1:
    print(i)
    j=1
    while j<rascols-1:
        if pharr[i,j]==-1:
            count+=1
        j+=1
    i+=1
print(count)


print "write the output...."
numpy.savetxt(myworkspace+"/"+"chli_phfilled"+".asc", pharr, fmt='%i',delimiter=' ',newline='\n', header=headerstr, comments='')
print "output written to ASCII files"
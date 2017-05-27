import ginlib
import sys
import zipfile

def extractor(romfile):
    framework = ''
    print 'Checking ROM type...'
    lena = len(romfile)
    extension = romfile[lena-3:lena]
    print 'ROM type:', extension
    if extension == 'ftf':
        framework = ginlib.sin(romfile)
    elif extension == 'zip':
        z = zipfile.ZipFile(romfile)
        dir1 = 'system/framework/framework-res.apk'
        dir2 = 'system.new.dat'
        #lst = []
        flag = 0
        for i in range(len(z.namelist())):
            t = str(z.namelist()[i])
            #lst.append(t)
            if dir1 == t:
                framework = ginlib.raw(romfile)
                flag = 1
                break
            if dir2 == t:
                framework = ginlib.dat(romfile)
                flag = 1
                break

        #if dir1 in lst:
            #framework = ginlib.raw(romfile)
        #elif dir2 in lst:
            #framework = ginlib.dat(romfile)
        if flag == 0:
            print "Unsupported ROM..."
    else:
        print 'Unsupported ROM.'
    return framework

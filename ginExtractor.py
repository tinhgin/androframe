import ginlib
import zipfile

def extractor(romfile):
    framework = ''
    print 'Checking ROM type...'
    extension = romfile[-3:len(romfile)]
    print 'ROM type:', extension
    if extension == 'ftf':
        framework = ginlib.sin(romfile)
    elif extension == 'zip':
        z = zipfile.ZipFile(romfile)
        dir1 = 'system/framework/framework-res.apk'
        dir2 = 'system.new.dat'
        flag = 0
        for i in range(len(z.namelist())):
            t = str(z.namelist()[i])
            if dir1 == t:
                framework = ginlib.raw(romfile)
                flag = 1
                break
            if dir2 == t:
                framework = ginlib.dat(romfile)
                flag = 1
                break

        if flag == 0:
            print "Unsupported ROM..."
    else:
        print 'Unsupported ROM.'
    return framework

#extractor('rr8.zip')

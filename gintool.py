from ginExtractor import extractor
import sys
import os
import shutil
from androsim import androsimplus


def getfilename(dir):
    k=[]
    for root, directories, filenames in os.walk(dir):
        for filename in filenames:
            k.append(os.path.join(root,filename))
    return k

def splitfilename(files):
    files1 = []
    for i in range(len(files)):
        files1.append(files[i].split('/', 1)[1])
    return files1



def dump2(b1, file_to_check, report):
    jarfile = b1 + file_to_check
    tmp = 'apktool d ' + jarfile
    os.system(tmp)
    directory = jarfile.split('/')[len(jarfile.split('/'))-1]
    if os.path.exists('codedump/' + directory):
        os.system('rm -rf ' + 'codedump/' + directory)
    os.makedirs('codedump/' + directory)
    out = directory + '.out'
    if directory[len(directory)-4:len(directory)] == '.apk':
        out = directory[0:len(directory)-4]    
    files = getfilename(out + '/smali')
    files1 = splitfilename(splitfilename(files))
    for i in range(len(files1)):
        k = files1[i].replace('/','.')
        shutil.copy2(files[i], 'codedump/' + directory + '/' + k)
    os.system('mv -f ' + out + ' smali')
    report.append(file_to_check + "#Dumped")


report = []

def main(argv):
    #a = extractor(argv[1])
    #b = extractor(argv[2])

    a='framework_2017-05-24_07-12-19'
    b='framework_2017-05-24_07-12-49'
    aa = getfilename(a)
    bb = getfilename(b)
    aaa = []
    bbb = []
    #print aa,'\n\n',bb############
    a1 = a + '/'
    #print a1#################
    for i in range(len(aa)):
        tmp = aa[i].split('/',1)[1]
        aaa.append(tmp)

    report.append(aaa)

    b1 = b + '/'
    #print b1################
    for i in range(len(bb)):
        tmp = bb[i].split('/',1)[1]
        bbb.append(tmp)
    #print aaa,'\n\n',bbb###############

    report.append(bbb)

    file_to_compare = []
    file_to_check = []
    for i in range(len(bbb)):
        try:
            aaa.index(bbb[i])
            file_to_compare.append(bbb[i])
        except:
            file_to_check.append(bbb[i])
    #print file_to_compare,'\n\n',file_to_check##############
    #print len(file_to_check), len(file_to_compare)
    #return 0

    report.append(file_to_check)
    report.append(file_to_compare)
    report.append(len(file_to_compare))

    for i in range(len(file_to_compare)):
        try:
            #tmp2 = 'python androsim.py -i ' + a1 + file_to_compare[i] + ' ' + b1 + file_to_compare[i] + ' -c ZLIB -p'
            androsimplus(a1 + file_to_compare[i],b1, file_to_compare[i],report)
            #os.system(tmp2)
        except:
            show = file_to_compare[i] + '#Error'
            report.append(show)
            print show

    report.append(len(file_to_check))
    for i in range(len(file_to_check)):
        try:
            dump2(b1, file_to_check[i],report)
        except:
            show = file_to_check[i] + '#Error'
            report.append(show)
            print show

    print report





if __name__ == '__main__':
    main(sys.argv)

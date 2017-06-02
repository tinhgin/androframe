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

def write_data_report(data, list, name):
    data.write('^^\n' + name + '\n')
    data.write(str(len(list)) + '\n')
    for x in list:
        data.write(x + '\n')

def splitfilename(files):
    files1 = []
    for i in range(len(files)):
        files1.append(files[i].split('/', 1)[1])
    return files1



def dump2(b1, file_to_check, data):
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
    #report.append(file_to_check + "#Dumped")


def main(argv):
    data = open('data.txt', 'w+')
    a = extractor(argv[1], data)
    b = extractor(argv[2], data)
    data.write(argv[1] + '\n')
    data.write(argv[2] + '\n')
    #a='framework_2017-05-28_04-01-07'
    #b='framework_2017-05-28_04-01-44'
    aa = getfilename(a)
    bb = getfilename(b)
    for i in range(0,len(aa)):
        aa[i] = aa[i].replace('\\', '/')
    for i in range(0,len(bb)):
        bb[i] = bb[i].replace('\\', '/')
    aaa = []
    bbb = []
    #print aa,'\n\n',bb############
    a1 = a + '/'
    #print a1#################
    for i in range(len(aa)):
        tmp = aa[i].split('/', 1)[1]

        aaa.append(tmp)

    write_data_report(data, aaa, 'framework_folder1')
    b1 = b + '/'
    #print b1################
    for i in range(len(bb)):
        tmp = bb[i].split('/', 1)[1]

        bbb.append(tmp)

    write_data_report(data, bbb, 'framework_folder2')

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

    write_data_report(data, file_to_check, 'listfile2check')
    write_data_report(data, file_to_compare, 'listfile2compare')

    for i in range(len(file_to_compare)):
        try:
            #tmp2 = 'python androsim.py -i ' + a1 + file_to_compare[i] + ' ' + b1 + file_to_compare[i] + ' -c ZLIB -p'
            androsimplus(a1 + file_to_compare[i],b1, file_to_compare[i], data)
            #os.system(tmp2)
        except:
            show = file_to_compare[i] + '#Error'
            data.write(show.replace('#Error', '\n<br>ERROR\n'))
            print show

    for i in range(len(file_to_check)):
        try:
            dump2(b1, file_to_check[i],data)
        except:
            show = file_to_check[i] + '#Error'
            data.write(show.replace('#Error', '\n<br>ERROR\n'))
            print show
    data.close()


if __name__ == '__main__':
    main(sys.argv)

from ginExtractor import extractor
import sys
import os
import shutil
from androsim import androsimplus

def make_clean():
    if os.path.exists('Result'):
        shutil.rmtree('Result')

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
    directory = jarfile.split('/')[len(jarfile.split('/')) - 1]
    os.system('java -jar "../Tool/baksmali-2.2.1.jar" d --pr false -o smali/' + directory + ' ' + jarfile)
    if not os.path.exists('smali/' + directory):
        os.chdir('smali/' + directory)
    os.makedirs('codedump_check/' + directory)
    out = 'smali/' + directory
    files = getfilename(out)
    files1 = splitfilename(files)
    for i in range(len(files1)):
        if sys.platform == "linux" or sys.platform == "linux2":
            k = files1[i].replace('/', '.')
        elif sys.platform == "win32":
            k = files1[i].replace('\\', '.')
        shutil.copy2(files[i], 'codedump_check/' + directory + '/' + k)
        if not os.path.exists('methoddump_check'):
            os.makedirs('methoddump_check')
        if not os.path.exists('methoddump_check/' + directory):
            os.makedirs('methoddump_check/' + directory)
        with open('codedump_check/' + directory + '/' + k) as infile:
            copy = False
            for line in infile:
                if ".method" in line:
                    copy = True
                    name_method = line.split(' ')[-1].replace('<','@').replace('>','@').split('(')[0]
                    outfile = open('methoddump_check/' + directory + '/' + k + name_method + '.method', 'w+')
                    outfile.write(line)
                    continue
                if copy == False:
                    continue
                else:
                    if '.end method' not in line:
                        outfile.write(line)
                    else:
                        copy = False
                        outfile.write('.end method')
                        outfile.close()


def main(argv):
    os.mkdir("Result")
    data = open('Result/data.txt', 'w+')
    a = extractor(argv[1], data)
    b = extractor(argv[2], data)
    data.write(argv[1] + '\n')
    data.write(argv[2] + '\n')
    #a='framework_h9.zip'
    #b='framework_h9b.zip'
    os.chdir("Result")
    aa = getfilename(a)
    bb = getfilename(b)
    for i in range(0,len(aa)):
        aa[i] = aa[i].replace('\\', '/')
    for i in range(0,len(bb)):
        bb[i] = bb[i].replace('\\', '/')
    aaa = []
    bbb = []
    a1 = a + '/'
    for i in range(len(aa)):
        tmp = aa[i].split('/', 1)[1]
        aaa.append(tmp)

    write_data_report(data, aaa, 'framework_folder1')
    b1 = b + '/'
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

    write_data_report(data, file_to_check, 'listfile2check')
    write_data_report(data, file_to_compare, 'listfile2compare')

    for i in range(len(file_to_compare)):
        try:
            androsimplus(a1 + file_to_compare[i],b1, file_to_compare[i], data)
            #os.system(tmp2)
        except:
            show = file_to_compare[i] + '#Error'
            data.write(show.replace('#Error', '\n<br>ERROR\n'))
            print show
    data.write("^^\n")
    for i in range(len(file_to_check)):
        try:
            dump2(b1, file_to_check[i],data)
        except:
            show = file_to_check[i] + '#Error'
            data.write(show.replace('#Error', '\n<br>ERROR\n'))
            print show


    data.close()


if __name__ == '__main__':
    make_clean()
    main(sys.argv)

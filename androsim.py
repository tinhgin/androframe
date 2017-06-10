def androsimplus(jar_o, b1, file_to_compare, data):
    jar_e = b1 + file_to_compare
    # !/usr/bin/env python

    # This file is part of Androguard.
    #
    # Copyright (C) 2012, Anthony Desnos <desnos at t0t0.fr>
    # All rights reserved.
    #
    # Androguard is free software: you can redistribute it and/or modify
    # it under the terms of the GNU Lesser General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.
    #
    # Androguard is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU Lesser General Public License for more details.
    #
    # You should have received a copy of the GNU Lesser General Public License
    # along with Androguard.  If not, see <http://www.gnu.org/licenses/>.

    import sys, os
    from sets import Set
    import shutil

    # from optparse import OptionParser

    from androguard.core import androconf
    from androguard.core.bytecodes import apk, dvm
    from androguard.core.analysis import analysis
    from androguard.util import read

    sys.path.append("./elsim")
    from elsim import elsim
    from elsim.elsim_dalvik import ProxyDalvik, FILTERS_DALVIK_SIM
    from elsim.elsim_dalvik import ProxyDalvikStringMultiple, ProxyDalvikStringOne, FILTERS_DALVIK_SIM_STRING

    def check_one_file(data, file_to_compare, a, d1, dx1, FS, threshold, file_input, view_strings=False, new=True,
                       library=True):
        d2 = None
        ret_type = androconf.is_android(file_input)
        if ret_type == "APK":
            b = apk.APK(file_input)
            d2 = dvm.DalvikVMFormat(b.get_dex())
        elif ret_type == "DEX":
            d2 = dvm.DalvikVMFormat(read(file_input))

        if d2 == None:
            return
        dx2 = analysis.VMAnalysis(d2)

        el = elsim.Elsim(ProxyDalvik(d1, dx1), ProxyDalvik(d2, dx2), FS, threshold, options['compressor'],
                         libnative=library)

        elshow = file_to_compare + el.show1() + "\n--> methods: " + str(
            el.get_similarity_value(new)) + "% of similarities\n"
        elshow1 = elshow.replace('\n\t', '<br>')
        elshow1 = elshow1.replace('#Elements:', '\n').replace('\n-->', '<br>-->')
        data.write(elshow1)
        print elshow

        if options['dump']:
            print '\nDumping smali code...'
            tmp1 = options['input'][1].split('/')

            jarname = tmp1[len(tmp1) - 1]
            if not os.path.exists('smali'):
                os.makedirs('smali')
            os.system('java -jar baksmali-2.2.1.jar d --pr false -o smali/' + jarname + ' ' + options['input'][1])

            classes = Set([])
            classes1 = Set([])
            diff_methods = el.get_similar_elements()
            for i in diff_methods:
                x = el.show_similar_class_name(i)
                y = el.show_similar_method_name(i)
                for j in range(0, len(x)):
                    classes.add(x.pop())
                for j in range(0, len(y)):
                    classes1.add(y.pop())

            new_methods = el.get_new_elements()
            for i in new_methods:
                x = el.show_new_class_name(i)
                classes.add(x)
                y = el.show_new_method_name(i)
                classes1.add(y)

            if not os.path.exists('codedump'):
                os.makedirs('codedump')
            os.chdir('codedump')

            if os.path.exists(jarname):
                if sys.platform == "linux" or sys.platform == "linux2":
                    os.system('rm -rf ' + jarname)
                elif sys.platform == "win32":
                    shutil.rmtree(jarname)
            os.makedirs(jarname)
            os.chdir('..')
            for i in range(0, len(classes)):
                # os.makedirs('codedump/' + jarname)
                filepath = classes.pop()
                filename = filepath.replace('/', '.')
                shutil.copy2('smali/' + jarname + '/' + filepath, 'codedump/' + jarname + '/' + filename)

            if sys.platform == "linux" or sys.platform == "linux2":
                try:
                    os.system('rmdir codedump/' + jarname)
                except:
                    print ""
            elif sys.platform == "win32":
                try:
                    os.system('rmdir codedump\\' + jarname)
                except:
                    print ""

            start = ''
            end = '.end method'
            if not os.path.exists('methoddump'):
                os.makedirs('methoddump')

            for i in range(0, len(classes1)):
                x1 = classes1.pop()
                xx = x1.split(' ', 1)
                if not os.path.exists('methoddump/' + jarname):
                    os.makedirs('methoddump/' + jarname)
                with open('codedump/' + jarname + '/' + xx[0]) as infile:
                    for line in infile:
                        if (xx[1].split('(')[0] in line) and ('.method' in line):
                            start = line.replace('\n', '')
                            break
                med = xx[1].split('(', 1)[0]
                med = med.replace('<', '@').replace('>', '@')
                with open('codedump\\' + jarname + '\\' + xx[0]) as infile, open('methoddump\\' + jarname + '\\' + xx[
                    0] + '.' + med + '.method', 'w+') as outfile:
                    copy = False
                    outfile.write(start + '\n')
                    for line1 in infile:
                        if line1.strip() == start:
                            copy = True
                        elif line1.strip() == end:
                            copy = False
                        elif copy:
                            outfile.write(line1)
                    outfile.write(end)

            print 'DUMP SMALI CODE SUCCESSFULLY.'

        if options['display']:
            print "SIMILAR methods:"
            diff_methods = el.get_similar_elements()
            for i in diff_methods:
                el.show_element(i)

            print "IDENTICAL methods:"
            new_methods = el.get_identical_elements()
            for i in new_methods:
                el.show_element(i)

            print "NEW methods:"
            new_methods = el.get_new_elements()
            for i in new_methods:
                el.show_element(i, False)

            print "DELETED methods:"
            del_methods = el.get_deleted_elements()
            for i in del_methods:
                el.show_element(i)

            print "SKIPPED methods:"
            skipped_methods = el.get_skipped_elements()
            for i in skipped_methods:
                el.show_element(i)

        if view_strings:
            els = elsim.Elsim(ProxyDalvikStringMultiple(d1, dx1),
                              ProxyDalvikStringMultiple(d2, dx2),
                              FILTERS_DALVIK_SIM_STRING,
                              threshold,
                              options['compressor'],
                              libnative=library)
            # els = elsim.Elsim( ProxyDalvikStringOne(d1, dx1),
            #    ProxyDalvikStringOne(d2, dx2), FILTERS_DALVIK_SIM_STRING, threshold, options.compressor, libnative=library )
            els.show()
            print "\t--> strings: %f%% of similarities" % els.get_similarity_value(new)

            if options['display']:
                print "SIMILAR strings:"
                diff_strings = els.get_similar_elements()
                for i in diff_strings:
                    els.show_element(i)

                print "IDENTICAL strings:"
                new_strings = els.get_identical_elements()
                for i in new_strings:
                    els.show_element(i)

                print "NEW strings:"
                new_strings = els.get_new_elements()
                for i in new_strings:
                    els.show_element(i, False)

                print "DELETED strings:"
                del_strings = els.get_deleted_elements()
                for i in del_strings:
                    els.show_element(i)

                print "SKIPPED strings:"
                skipped_strings = els.get_skipped_elements()
                for i in skipped_strings:
                    els.show_element(i)

    def check_one_directory(data, file_to_compare, a, d1, dx1, FS, threshold, directory, view_strings=False, new=True,
                            library=True):
        for root, dirs, files in os.walk(directory, followlinks=True):
            if files != []:
                for f in files:
                    real_filename = root
                    if real_filename[-1] != "/":
                        real_filename += "/"
                    real_filename += f

                    print "filename: %s ..." % real_filename
                    check_one_file(data, file_to_compare, a, d1, dx1, FS, threshold, real_filename, view_strings, new,
                                   library)

    ############################################################
    def mainn(options):
        if options['input'] != None:
            a = None
            ret_type = androconf.is_android(options['input'][0])
            if ret_type == "APK":
                a = apk.APK(options['input'][0])
                d1 = dvm.DalvikVMFormat(a.get_dex())
            elif ret_type == "DEX":
                d1 = dvm.DalvikVMFormat(read(options['input'][0]))

            dx1 = analysis.VMAnalysis(d1)

            threshold = None
            if options['threshold'] != None:
                threshold = float(options['threshold'])

            FS = FILTERS_DALVIK_SIM
            FS[elsim.FILTER_SKIPPED_METH].set_regexp(options['exclude'])
            FS[elsim.FILTER_SKIPPED_METH].set_size(options['size'])

            new = True
            if options['new'] != None:
                new = False

            library = True
            if options['library'] != None:
                library = options['library']
                if options['library'] == "python":
                    library = False

            if os.path.isdir(options['input'][1]) == False:
                check_one_file(data, file_to_compare, a, d1, dx1, FS, threshold, options['input'][1],
                               options['xstrings'], new, library)
            else:
                check_one_directory(data, file_to_compare, a, d1, dx1, FS, threshold, options['input'][1],
                                    options['xstrings'], new, library)

        elif options['version'] != None:
            print "Androsim version %s" % androconf.ANDROGUARD_VERSION

    print 'Please wait...\nComparing smali code...'
    options = {'dump': 1, 'xstrings': None, 'library': None, 'compressor': 'ZLIB', 'version': None, 'exclude': None,
               'threshold': None, 'input': (jar_o, jar_e), 'new': None, 'display': None, 'size': None}
    mainn(options)

    # androsimplus('framework_2017-05-24_07-12-19/android.test.runner.jar', 'framework_2017-05-24_07-12-49/', 'android.test.runner.jar', [])
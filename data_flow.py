#!/usr/bin/env python
import re, os, sys, string

class MethodItem:
    def __init__(self):
        self.path=""
        self.listInstruction=[]

class result:
    def __init__(self):
        sink = ""
        source = ""
        detail = ""
        path=""

def extract_register_index_out_splitted_values(registers_raw_list_splitted):
    """
        @param : registers_raw_list_splitted : a list of registers still containing the 'v' prefix [' v1 ', ' v2 ' ...]

        @rtype : an ordered list of register indexes ['1', '2' ...]
    """
    relevant_registers = []

    # Trim the values
    registers_raw_list_splitted[:] = (value.strip() for value in registers_raw_list_splitted if len(value) > 0)

    for value in registers_raw_list_splitted:

        # Remove that 'v'
        p_register_index_out_of_split = re.compile('^v([0-9]+)$')

        if p_register_index_out_of_split.match(value):
            # print p_register_index_out_of_split.match(value).groups()
            register_index = p_register_index_out_of_split.match(value).groups()[0]

            relevant_registers.append(register_index)

        else:
            relevant_registers.append('N/A')

    return relevant_registers
def relevant_registers_for_the_method(current_instruction):
    """
        @param method : a method instance
        @param index_to_find : index of the matching method

        @rtype : an ordered list of register indexes related to that method call
    """
    relevant_registers = []


    p_invoke_name = re.compile('^invoke-(?:static|virtual|direct|super|interface|interface-range|virtual-quick|super-quick).*')
    p_invoke_range_name = re.compile('^invoke-(?:static|virtual|direct|super|interface|interface-range|virtual-quick|super-quick)(?:\/range).*')

    if p_invoke_name.match(current_instruction):

        p_invoke_registers = re.compile('(v[0-9]+),')

        if p_invoke_registers.findall(current_instruction):
            registers_raw_list_splitted = p_invoke_registers.findall(current_instruction)
            relevant_registers = extract_register_index_out_splitted_values(registers_raw_list_splitted)

    if p_invoke_range_name.match(current_instruction):
        # We're facing implicit an implicit range declaration, for instance "invoke v19..v20"
        p_invoke_registers_range = re.compile('^.*v([0-9]+) .. v([0-9]+), L.*$')

        if p_invoke_registers_range.match(current_instruction):
            register_start_number = p_invoke_registers_range.match(current_instruction).groups()[0]
            register_end_number = p_invoke_registers_range.match(current_instruction).groups()[1]

            if int(register_start_number) > int(register_end_number):
                xx=1
            else:
                relevant_registers = [str(i) for i in xrange(int(register_start_number), int(register_end_number)+1)]
                # +1 because range does not provide the higher boundary value

    return relevant_registers
def find_register_value(method, index, registers_found):
    p_const = re.compile('^const(?:\/4|\/16|\/high16|-wide(?:\/16|\/32)|-wide\/high16|)? v([0-9]+), (.*)$')
    p_const_string = re.compile('^const-string(?:||\/jumbo) v([0-9]+), (?:\'|\")(.*)(?:\"|\')$')
    p_move = re.compile('^move(?:|\/from16|-wide(?:\/from16|\/16)|-object(?:|\/from16|\/16))? v([0-9]+), v([0-9]+)$')
    p_invoke = re.compile('^invoke-.*$')
    p_invoke_static = re.compile('^invoke-static.*')
    p_move_result = re.compile('^move(?:-result(?:|-wide|-object)|-exception)? v([0-9]+)$')
    p_new_instance = re.compile('^new-instance v([0-9]+), (L(?:.*);)$')
    result=0
    if p_invoke.match(method[index]):
        old = ""
        relevant_registers = relevant_registers_for_the_method(method[index])
        if p_move_result.match(method[index+1]):
            register_number = p_move_result.match(method[index+1]).groups()[0]
        else:
            register_number = relevant_registers[0]
        instmp = method[index]
        instmp = instmp.replace(instmp[instmp.index("("):instmp.index(")")+1], "())", 1)
        if p_invoke_static.match(method[index]):
            istart = 0
        else:
            istart = 1
        number = len(relevant_registers)
        for i in range(istart, number, 1):
            register = relevant_registers[i]
            if registers_found.has_key(register):
                if i +1 != number:
                    instmp = instmp.replace("))", registers_found[register]+", ))", 1)
                else:
                    instmp = instmp.replace("))", registers_found[register] + "))", 1)
            else:
                if i +1 != number:
                    instmp = instmp.replace("))", "v" + register+", ))", 1)
                else:
                    instmp = instmp.replace("))", "v" + register + "))", 1)
        instmp = instmp.replace("))", ")", 1)
        new = instmp[instmp.index(">") + 1:]
        result = new
        if registers_found.has_key(register_number):
            old = registers_found[register_number]
        if "sink" in new:
            new = new[:new.index("~sink")]
        if old:
            registers_found[register_number] = new + " | " + old
        else:
            registers_found[register_number] = new
    if p_new_instance.match(method[index]):
        register_number = p_new_instance.match(method[index]).groups()[0]
        register_value = p_new_instance.match(method[index]).groups()[1]
        registers_found[register_number] = register_value
    if p_const.match(method[index]):
        register_number = p_const.match(method[index]).groups()[0]
        register_value = p_const.match(method[index]).groups()[1]
        registers_found[register_number] = register_value
    if p_const_string.match(method[index]):
        register_number = p_const_string.match(method[index]).groups()[0]
        register_value = '"'+p_const_string.match(method[index]).groups()[1]+'"'
        registers_found[register_number] = register_value
    if p_move.match(method[index]):
        register_number = p_move.match(method[index]).groups()[0]
        register_number1 = p_move.match(method[index]).groups()[1]
        if registers_found.has_key(register_number1):
            registers_found[register_number] = registers_found[register_number1]
        else:
            registers_found[register_number] = "v"+register_number1
    return result

def get_method_diff(dumpfolder):
    if sys.platform == "linux" or sys.platform == "linux2":
        end = '\r\n'
        numend=2
    elif sys.platform == "win32":
        end = '\n'
        numend=1
    MethodDiff=[]
    filesink = open('./Ouput_CatSinks.txt')
    filesource = open('./Ouput_CatSources.txt')
    for root, dirs, files in os.walk("./" + dumpfolder, topdown=False):
        for name in files:
            print(os.path.join(root, name))
            with open(os.path.join(root, name)) as codefile:
                tmp = MethodItem()
                tmp.path = os.path.join(root, name)
                check=0
                for line in codefile:
                    t = ""
                    if line[:-numend]:
                        if line.split()[0][0].isalpha():
                            for linesink in filesink:
                                if linesink.endswith(":"+end):
                                    type = linesink[:-numend-1]
                                elif linesink[:-1] in line[:-1]:
                                    t = line[4:-1] + "~sink" + ":" + type + "@@"
                                    tmp.listInstruction.append(t)
                                    check=1
                                    break
                            filesink.seek(0, 0)
                            if t=="":
                                for linesource in filesource:
                                    if linesource.endswith(":"+end):
                                        type = linesource[:-numend-1]
                                    elif linesource[:-numend] in line[:-numend]:
                                        t = line[4:-numend] + "~source" + ":" + type + "@"
                                        tmp.listInstruction.append(t)
                                        check=1
                                        break
                                filesource.seek(0, 0)
                            if t == "":
                                tmp.listInstruction.append(line[4:-numend])
            if check:
                MethodDiff.append(tmp)
    return MethodDiff
def data_flow(dumpfolder):
    listmethod = get_method_diff(dumpfolder)
    list_result = []
    for file in listmethod:
        method = file.listInstruction
        k=0
        registers_found = {}
        while(k < len(method)):
            if "{" in method[k]:
                method[k] = method[k].replace("{","")
                method[k] = method[k].replace("}","")
            t = find_register_value(method, k, registers_found)
            if "sink" in method[k]:
                instmp = t
                if "source" in instmp:
                    tmpresult = result()
                    tmpresult.path = file.path
                    tmpresult.detail = instmp
                    tmpresult.sink = instmp[instmp.index("sink:"):instmp.index("@@")]
                    tmpresult.source = instmp[instmp.index("source:"):instmp.index("@")]
                    list_result.append(tmpresult)
            k = k + 1
    return list_result
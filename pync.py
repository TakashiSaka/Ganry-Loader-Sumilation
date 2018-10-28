# -*- coding: utf-8 -*-
import re
import pprint

def main_program_macro_val(program_file):
    file = open(program_file, 'r')
    lines = file.readlines()
    global macro_val
    macro_val = {}
    for line in lines:
        if line.startswith('O'):
            pass
        if line.startswith('('):
            pass
        if line.startswith('N'):
            nline = line.lstrip('N')
            line = nline.lstrip(re.compile(r'[0-9]*').search(nline).group())
        if line.startswith('#'):
            line = [line[:4], line[5:-1]]
            line[0] = '#' + line[0][1:]
            #print(line[0], line[1])
            macro_val[line[0]] = float(line[1])
    file.close()
    print(macro_val)
    return macro_val

            
def main_program2sub_program(program_file):
    file = open(program_file, 'r')
    lines = file.readlines()
    sub_program_line = []
    for line in lines:
        if line.startswith('M98'):
            mline = [line[:3], line[4:8]]
            sub_o_num = mline[1].lstrip('P')
            sub_program = open(sub_o_num, 'r')
            sub_program_file = sub_program.readlines()
            for sub_line in sub_program_file:
                sub_program_line.append(sub_line.strip())
    file.close()
    pprint.pprint(sub_program_line)
    sub_program_macro_val(sub_program_line)

def sub_program_macro_val(sub_program_line):
    for line in sub_program_line:
        if line.startswith('O'):
            continue
        if line.startswith('('):
            continue
        if line.startswith('N'):
            nline = line.lstrip('N')
            line = nline.lstrip(re.compile(r'[0-9]*').search(nline).group())
        line = line.replace('#', '#')
        line = re.sub(r'\(.*\)?', '', line)
        if line.startswith('#'):
            if len(line) == 14:
                macro_val[line[:4]] = macro_val[line[5:9]]\
                                    +float(line[9:10]+'1.0')*macro_val[line[10:14]]
            elif len(line) == 19:
                macro_val[line[:4]] = macro_val[line[5:9]]\
                                    +float(line[9:10]+'1.0')*macro_val[line[10:14]]\
                                    +float(line[14:15]+'1.0')*macro_val[line[15:19]]
            elif len(line) == 24:
                macro_val[line[:4]] = macro_val[line[5:9]]\
                                    +float(line[9:10]+'1.0')*macro_val[line[10:14]]\
                                    +float(line[14:15]+'1.0')*macro_val[line[15:19]]\
                                    +float(line[19:20]+'1.0')*macro_val[line[20:24]]
            elif len(line) == 29:
                macro_val[line[:4]] = macro_val[line[5:9]]\
                                    +float(line[9:10]+'1.0')*macro_val[line[10:14]]\
                                    +float(line[14:15]+'1.0')*macro_val[line[15:19]]\
                                    +float(line[19:20]+'1.0')*macro_val[line[20:24]]\
                                    +float(line[24:25]+'1.0')*macro_val[line[25:29]]
            elif len(line) == 34:
                macro_val[line[:4]] = macro_val[line[5:9]]\
                                    +float(line[9:10]+'1.0')*macro_val[line[10:14]]\
                                    +float(line[14:15]+'1.0')*macro_val[line[15:19]]\
                                    +float(line[19:20]+'1.0')*macro_val[line[20:24]]\
                                    +float(line[24:25]+'1.0')*macro_val[line[25:29]]\
                                    +float(line[29:30]+'1.0')*macro_val[line[30:34]]
            else:
                raise Exception
            #print(line[:4], line[5:9], line[9:10], line[10:14])
    pprint.pprint(macro_val)

main_program_macro_val(r'C:\Data\Data\Sakamoto\Python\Project_1\LD_PRO_MANU\1NC_1LD\MAIN')
main_program2sub_program(r'C:\Data\Data\Sakamoto\Python\Project_1\LD_PRO_MANU\1NC_1LD\MAIN')

"""
#100-#199
d = re.compile(r'^#1[0-9][0-9]$')
d.search('#100').group()
"""
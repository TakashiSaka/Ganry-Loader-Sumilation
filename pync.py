# -*- coding: utf-8 -*-
import re
import pprint

def main_program_macro_val(program_file):
    file = open(program_file, 'r')
    lines = file.readlines()
    global macro_val_dict
    macro_val_dict = {}
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
            macro_val_dict[line[0]] = float(line[1])
    file.close()
    print(macro_val_dict)
    return macro_val_dict

            
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
            line_fomula = line[5:]
            fomula_parenthesis = line_fomula.maketrans({'[': '(', ']': ')'})
            translated_line = line_fomula.translate(fomula_parenthesis)
            macro_list = re.compile(r'#[0-9]*').findall(translated_line)
            macro_val_list = []
            for i in range(len(macro_list)):
                macro_val_list.append(macro_val_dict[macro_list[i]])
            translated_fomula = re.sub(r'#\d\d\d', '#', translated_line)
            for i in range(len(macro_val_list)):
                translated_fomula = translated_fomula.replace('#', str(macro_val_list[i]), 1)
            print(translated_fomula)
            macro_result = eval(translated_fomula)
            print(macro_result)
            macro_val_dict[line[:4]] = macro_result
            
    pprint.pprint(macro_val_dict)

main_program_macro_val(r'C:\Data\Data\Sakamoto\Python\Project_1\LD_PRO_MANU\1NC_1LD\MAIN')
main_program2sub_program(r'C:\Data\Data\Sakamoto\Python\Project_1\LD_PRO_MANU\1NC_1LD\MAIN')


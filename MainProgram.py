# -*- coding: utf-8 -*-
import re
import pprint
from system_macro_input_dict import system_macro_input_dict

main_program_file = r'C:\Data\Data\Sakamoto\Python\Project_1\LD_PRO_MANU\1NC_1LD\MAIN'

macro_val_dict = {} #dictionary of macro variable
system_macro_output_dict = {} #dictionary of system macro variable
whole_macro_val_dict = {**macro_val_dict, **system_macro_input_dict}
sub_program_line = [] #list of sub program line
sub_program_line_withoutN = [] #list of sub program line without N sequence

class MainProgram:    
    def main_program_macro_val(self, main_program_file):
        """
        Change macro variable of main program to dict
        """
        file = open(main_program_file, 'r')
        lines = file.readlines()
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
        #print(macro_val_dict)
        return macro_val_dict
    
                
    def main_program2sub_program(self, main_program_file):
        """
        Invoke sub program (M98P****) from mainprogram
        """
        file = open(main_program_file, 'r')
        lines = file.readlines()
        #sub_program_line = [] #list of sub program line
        for line in lines:
            if line.startswith('M98'):
                mline = [line[:3], line[4:8]]
                sub_o_num = mline[1].lstrip('P')
                sub_program = open(sub_o_num, 'r')
                sub_program_file = sub_program.readlines()
                #print(sub_program_file)
                for sub_line in sub_program_file:
                    sub_line = re.sub(r'\(.*\)?', '', sub_line) #remove (comment)
                    sub_program_line.append(sub_line.strip())
        file.close()
        #pprint.pprint(sub_program_line)
        #sub_program_macro_val(sub_program_line)
    
    def sub_program_removeN(self, sub_program_line):
        """
        Remove N from sub program line
        """
        for line in sub_program_line:
            if line.startswith('N'): #delete N sequence number
                line = line.lstrip('N')
                line = line.lstrip(re.compile(r'[0-9]*').search(line).group())
                sub_program_line_withoutN.append(line)
            else:
                sub_program_line_withoutN.append(line)
            
    def sub_program_macro_val(self, sub_program_line_wothoutN):
        """
        Calculation of sub program macro variable
        """
        for line in sub_program_line_withoutN:
            if line.startswith('#'):
                if line[4:5] == '=': #macro variable #***
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
                    #print(translated_fomula)
                    macro_result = eval(translated_fomula)
                    #print(macro_result)
                    macro_val_dict[line[:4]] = macro_result
                
                if line[5:6] == '=': #system variable #****
                    if line[6:7] == '1':
                        system_macro_output_dict[line[:5]] = 1
                    if line[6:7] == '0':
                        system_macro_output_dict[line[:5]] = 0
                    if line[6:7] == '#':
                        system_macro_output_dict[line[:5]] = macro_val_dict[line[6:]]
                    #print(line)
                    
    def macro_fomula_handler(self, macro_fomula):
        """
        Calculation of macro fomula
        """
        if macro_fomula.startswith('#'):
            if macro_fomula[4:5] == '=': #macro variable #***
                line_fomula = macro_fomula[5:]
                fomula_parenthesis = line_fomula.maketrans({'[': '(', ']': ')'})
                translated_line = line_fomula.translate(fomula_parenthesis)
                macro_list = re.compile(r'#[0-9]*').findall(translated_line)
                macro_val_list = []
                for i in range(len(macro_list)):
                    macro_val_list.append(macro_val_dict[macro_list[i]])
                translated_fomula = re.sub(r'#\d\d\d', '#', translated_line)
                for i in range(len(macro_val_list)):
                    translated_fomula = translated_fomula.replace('#', str(macro_val_list[i]), 1)
                #print(translated_fomula)
                macro_result = eval(translated_fomula)
                #print(macro_result)
                macro_val_dict[macro_fomula[:4]] = macro_result
            
            if macro_fomula[5:6] == '=': #system variable #****
                if macro_fomula[6:7] == '1':
                    system_macro_output_dict[macro_fomula[:5]] = 1
                if macro_fomula[6:7] == '0':
                    system_macro_output_dict[macro_fomula[:5]] = 0
                if macro_fomula[6:7] == '#':
                    system_macro_output_dict[macro_fomula[:5]] = macro_val_dict[macro_fomula[6:]] 
    
    def sub_program_if_stat(self, sub_program_line_withoutN):
        """
        Handle IF statement
        """
        global goto_num
        for line in sub_program_line_withoutN:                
            if line.startswith('IF'):
                if line.find('GOTO') > 2:
                    if_condition = re.compile(r'\[.*\]').search(line).group()
                    if_condition = if_condition.lstrip('[')
                    if_condition = if_condition.rstrip(']')
                    trans_if_condi = self.translate_if_condition(if_condition)
                    if_condi_result = self. replace_macro2valuable(trans_if_condi)
                    if if_condi_result:
                        goto_num = line.split('GOTO')[1]
                    #print(trans_if_condi)
                    #print(goto_num)
                    
                elif line.find('THEN') > 2:
                    if_condition = re.compile(r'\[.*\]').search(line).group()
                    if_condition = if_condition.lstrip('[')
                    if_condition = if_condition.rstrip(']')
                    trans_if_condi = self.translate_if_condition(if_condition)
                    if_condi_result = self.replace_macro2valuable(trans_if_condi)
                    if if_condi_result:
                        then_comd = line.split('THEN')[1]
                        self.macro_fomula_handler(then_comd)
                        #print(then_comd)
                else:
                    pass
                
    def translate_if_condition(self, if_condition):
        if_condition = if_condition.replace('EQ', '==')
        if_condition = if_condition.replace('NE', '!=')
        if_condition = if_condition.replace('GE', '>=')
        if_condition = if_condition.replace('LE', '<=')
        if_condition = if_condition.replace('GT', '>')
        if_condition = if_condition.replace('LT', '<')
        if_condition = if_condition.replace('AND', ' and ')
        if_condition = if_condition.replace('[', '')
        if_condition = if_condition.replace(']', '')
        return if_condition
    
    def replace_macro2valuable(self, trans_if_condi):
        macro_list = re.compile(r'#[0-9]*').findall(trans_if_condi)
        macro_val_list = []
        for i in range(len(macro_list)):
            macro_val_list.append(whole_macro_val_dict[macro_list[i]])
        translated_fomula = re.sub(r'#[0-9]*', '#', trans_if_condi)
        for i in range(len(macro_val_list)):
            translated_fomula = translated_fomula.replace('#', str(macro_val_list[i]), 1)
        if_condi_result = eval(translated_fomula)
        #print(translated_fomula)
        #print(macro_val_list)
        #print(if_condi_result)
        return if_condi_result
            
Main = MainProgram()    
Main.main_program_macro_val(main_program_file)
Main.main_program2sub_program(main_program_file)
Main.sub_program_removeN(sub_program_line)
Main.sub_program_macro_val(sub_program_line_withoutN)
whole_macro_val_dict = {**macro_val_dict, **system_macro_input_dict}
Main.sub_program_if_stat(sub_program_line_withoutN)
whole_macro_val_dict = {**macro_val_dict, **system_macro_input_dict}
#pprint.pprint(sub_program_line)
#pprint.pprint(sub_program_line_withoutN)
#pprint.pprint(macro_val_dict)
#pprint.pprint(system_macro_output_dict)
#pprint.pprint(system_macro_input_dict)
#pprint.pprint(whole_macro_val_dict)

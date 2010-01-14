'''
Created on Jan 13, 2010

@author: risdenkj
'''

import csv
import fileinput
import sys
import os
from bitstring import BitString

h = sys.argv[2];
h = '';

def makeMachineCode(inst):
    opcode = str(inst_map[inst[0]][0]);
    code = opcode + h;
    
    format = str(inst_map[inst[0]][1]);
    if(format == 'R'):
        code += registers_map[inst[2]] + h + registers_map[inst[3]] +  h + registers_map[inst[1]][1:]
    elif(format == 'M'):
        code += registers_map[inst[2]] +  h + str(inst_map[inst[0]][2]) +  h + registers_map[inst[1]][1:]
    elif(format == 'I'):
        code += inst[2] +  h + registers_map[inst[1]][1:]
    elif(format == 'B'):
        code += registers_map[inst[2]][1:] + h + inst[3] + h + registers_map[inst[1]][1:];        
    elif(format == 'J'):
        #code += inst[1];
        code += '___________';
    #print code;
    return code

def parseInstruction(inst):
    inst = inst.strip().replace('$', '').replace(',', '').split(" ");
    #print inst;
    return inst;

def storeLabel(inst):
    #print inst;
    return

if __name__ == '__main__':
    
    inst_map=dict();
    registers_map = dict();
    
    instructions = csv.reader(open('config/instructions.csv'), delimiter=',')
    for row in instructions:
        if(len(row)==4):
            inst_map[row[0]] = list((row[1], row[2], row[3]));
        else:
            inst_map[row[0]] = list((row[1], row[2]));
        
    registers = csv.reader(open('config/registers.csv'), delimiter=',')
    for row in registers:
        registers_map[row[0]] = row[1];
    
    inputFileName = sys.argv[1];
    print sys.argv
    outputFileName = inputFileName + "_machine.txt";
    if(os.path.exists(outputFileName)):
        os.remove(outputFileName);
    f = open(outputFileName, 'a');
    for line in fileinput.input(inputFileName):
        if(line.find(":") == -1):
            newline = makeMachineCode(parseInstruction(line));
            printline = line.strip() + '\t'
            if(newline.find('_') == -1):
                if(len(sys.argv) > 2):
                    if(sys.argv[3] == 'bin'):
                        printline += BitString(bin=newline, length=16).bin
                    elif(sys.argv[3] == 'hex'):
                        printline += BitString(bin=newline, length=16).hex
                    else:
                        printline += newline
                else:
                    printline += newline
            else:
                printline += newline
            
            print printline
            #print line.strip() + '\t' + newline;
            f.write(newline + '\n');
        else:
            storeLabel(line);
    f.close();
    fileinput.close();
    
    f = open(outputFileName, 'r+');
    for line in f:
        if(line.find('_') != -1):
            print '';
            #print line;
    f.close();

    pass
# Adapted from https://github.com/cocotb/cocotb/blob/master/examples/doc_examples/quickstart/test_my_design.py

import pytest

import os,sys,argparse, subprocess, re
from os.path import dirname, abspath
from termcolor import colored

import numpy as np

TAB = "    "
END = "\n"

def alu(x,y, code):
    if code == "101010":
        return 0
    elif  code == "111111":
        return 1
    elif code == "111010":
        return 65535 #-1
    elif code == "001100":
        return x
    elif code == "110000":
        return y
    elif code == "001101":
        return ~x
    elif code == "110001":
        return ~y
    elif code == "001111":
        return (65536-x) if (x!= 0) else 0  #-x
    elif code == "110011":
        return (65536-y) if (y!= 0) else 0  #-y
    elif code == "011111":
        return (x+1) if (x < 65535) else 0  #x+1
    elif code == "110111":
        return (y+1) if (y < 65535) else 0  #y+1
    elif code == "001110":
        return (x-1) if (x > 0) else 65535  #x-1
    elif code == "110010":
        return (y-1) if (y > 0) else 65535  #y-1
    elif code == "000010":
        return (x+y) if ( (np.uint32(x)+np.uint32(y)) <= 65535) else (np.uint32(x)+np.uint32(y)-65536)  #x+y
    elif code == "010011":
        return (x-y) if (x >= y) else (65536-(y-x))  #x-y
    elif code == "000111":
        return (y-x) if ( y >= x) else (65536-(x-y))  #y-x
    elif code == "000000":
        return x&y
    elif code == "010101":
        return x|y
    else:
        return 0

def run_CPU(name="add", nTests=1, sTime=100):
    mif = "bin/hack/"+name+".mif"
    erro = 0

    print("\n\n===================================================")

    # verifica se arquivo existe
    if os.path.isfile(mif):
        # simulate
        for test in range(0, int(nTests)):
            ramIn = "tests/" + name + "/" + name +"{}".format(test)+ "_in.mif"
            ramTest = "tests/" + name + "/" + name +"{}".format(test)+ "_tst.mif"

            RAM = [0] * (16*1024+4800+2)
            ROM = [0] * 32*1024
            #Import initial conditions from file
            file_in = open(mif,"r")
            Lines_in = file_in.readlines() 
            file_in.close()
            
            for l in Lines_in:
                if ":" in l:
                    no_line = int( l.split(":")[0].strip() )
                    value = int( l.split(":")[1].replace(";", "").strip(),2 )
                    ROM[no_line] = value 

            file_in = open(ramIn,"r")
            Lines_in = file_in.readlines() 
            file_in.close()
            
            for l in Lines_in:
                if ":" in l:
                    no_line = int( l.split(":")[0].strip() )
                    value = int( l.split(":")[1].replace(";", "").strip(),2 )
                    RAM[no_line] = value  

            #### novo CPU ####
            regA = np.uint16(0)
            regD = np.uint16(0)
            regPC = np.uint16(0)

            for i in range( sTime ):
                instruction = ROM[regPC]
                instruction = '{0:018b}'.format(instruction)
                regPC += 1

                if instruction[0] == '0':
                    regA = np.uint16(int(instruction[2:],2))
                else:
                    if instruction[4] == '0':
                        resultado = alu(regD,regA, instruction[5:11])
                    else:
                        resultado = alu(regD,RAM[regA], instruction[5:11])
                    if instruction[12] == '1':
                        RAM[regA] = np.uint16(resultado)
                    if instruction[13] == '1':
                        regD = np.uint16(resultado)
                    if instruction[14] == '1':
                        regA = np.uint16(resultado)
                    if (instruction[15] == '1') and (resultado >= 32768):
                        regPC = regA
                    if (instruction[16] == '1') and (resultado == 0):
                        regPC = regA
                    if (instruction[17] == '1') and (resultado < 32768) and (resultado > 0):
                        regPC = regA

            #Verification final results
            file_in = open(ramTest,"r")
            Lines_in = file_in.readlines() 
            file_in.close()

            for l in Lines_in:
                if ":" in l:
                    no_line = int( l.split(":")[0].strip() )
                    value = int( l.split(":")[1].replace(";", "").strip(),2 )

                    condition = (RAM[no_line] == value)
                    if not condition:
                        print("Error in test " + name + "{}".format(test))
                        print("Expected value RAM[" + str(no_line) + "]: " + "{0:016b}".format(value) + " Obtained value RAM[" + str(no_line) + "]: " + "{0:016b}".format(int(RAM[no_line])) )
                        print( 'Test {:15s}: '.format(name + "{}".format(test)) + colored('Failed', 'red'))
                        erro = 1
                    else:
                        print( 'Test {:15s}: '.format(name + "{}".format(test)) + colored('Passed', 'green'))
    
    if erro == 1:
        return False
    else:
        return True
    print("===================================================")

def callJava(jar, nasm, hack):
    #by Rafael Corsi
    command = "java -jar " + jar + " -i " + nasm + " -o " + hack
    proc = subprocess.Popen(command, shell=True)
    err = proc.wait()
    return(err)
            
def toMIF(mem, mif):
    #by Rafael Corsi
    cnt = 0
    try:
        fw = open(mif,"w")
        fr = open(mem,"r")

        # verifica quantas instrucoes possui
        num_lines = sum(1 for line in open(mem))

        fw.write("-- Elementos de Sistema - INSPER.edu.br"+END)
        fw.write("-- Rafael Corsi"+END)
        fw.write("-- File generated by toMIF.py"+END)
        fw.write("-- originated from"+mem+""+END)
        fw.write("-- to be used on ALTERA FPGAs"+END+END)

        fw.write("WIDTH=18;"+END)
        fw.write("DEPTH={};".format(num_lines)+END)
        fw.write(""+END)
        fw.write("ADDRESS_RADIX=UNS;"+END)
        fw.write("DATA_RADIX=BIN;"+END)
        fw.write(""+END)
        fw.write("CONTENT BEGIN"+END)

        for line in fr:
            fw.write( TAB
                      + '{:4d}'.format(cnt)
                      +" : "
                      +line.rstrip()
                      +";"
                      +""+END)
            cnt = cnt + 1
        # colocar for aqui
        fw.write("END;"+END)

        fw.close()
        fr.close()

    except IOError:
        print("Arquivo não encontrado")  

def assemblerFile(name="add"):
    #adapted from Rafael Corsi
    error = 0
    
    jar = "jar/Z01-Assembler.jar"
    pwd = dirname(abspath(__file__))
    nasm = pwd+"/src/"
    hack = pwd+"/bin/hack/"
    
    nHack = hack+name+".hack"
    nMif  = hack+name+".mif"
    nNasm = nasm+name+".nasm"

    if not os.path.exists(os.path.dirname(hack)):
        os.makedirs(os.path.dirname(hack))

    print("   - {} to {}".format(os.path.basename(nasm), os.path.basename(hack)))
    if callJava(jar, nNasm, nHack) != 0:
        status = 'Assembler Fail'
        error  = 1
    else:
        status = 'Assembler Ok'
        error = 0
    toMIF(nHack, nMif)
    log = ({'name': nMif, 'status': status})

    return error, log  

          
def test_add():
    assemblerFile(name="add")
    certo = run_CPU("add",1,1000)

    if not certo:
        assert False
    print("===================================================")

def test_sub():
    assemblerFile(name="sub")
    certo = run_CPU("sub",1,1000)

    if not certo:
        assert False
    print("===================================================")

def test_mov():
    assemblerFile(name="mov")
    certo = run_CPU("mov",1,1000)

    if not certo:
        assert False
    print("===================================================")

def test_abs():
    assemblerFile(name="abs")
    certo = run_CPU("abs",2,1000)

    if not certo:
        assert False
    print("===================================================")

def test_max():
    assemblerFile(name="max")
    certo = run_CPU("max",2,10000)

    if not certo:
        assert False
    print("===================================================")

def test_mult():
    assemblerFile(name="mult")
    certo = run_CPU("mult",1,10000)

    if not certo:
        assert False
    print("===================================================")

def test_mod():
    assemblerFile(name="mod")
    certo = run_CPU("mod",2,10000)

    if not certo:
        assert False
    print("===================================================")


def test_div():
    assemblerFile(name="div")
    certo = run_CPU("div",2,10000)

    if not certo:
        assert False
    print("===================================================")


def test_pow():
    assemblerFile(name="pow")
    certo = run_CPU("pow",2,10000)

    if not certo:
        assert False
    print("===================================================")


def test_isEven():
    assemblerFile(name="isEven")
    certo = run_CPU("isEven",2,1000)

    if not certo:
        assert False
    print("===================================================")


def test_stringLength():
    assemblerFile(name="stringLength")
    certo = run_CPU("stringLength",2,2000)

    if not certo:
        assert False
    print("===================================================")


def test_palindromo():
    assemblerFile(name="palindromo")
    certo = run_CPU("palindromo",2,1000)

    if not certo:
        assert False
    print("===================================================")


def test_vectorMean():
    assemblerFile(name="vectorMean")
    certo = run_CPU("vectorMean",2,2000)

    if not certo:
        assert False
    print("===================================================")


def test_max():
    assemblerFile(name="max")
    certo = run_CPU("max",2,10000)

    if not certo:
        assert False
    print("===================================================")


def test_SWeLED():
    assemblerFile(name="SWeLED")
    certo = run_CPU("SWeLED",1,1000)

    if not certo:
        assert False
    print("===================================================")


def test_factorial():
    assemblerFile(name="factorial")
    certo = run_CPU("factorial",2,10000)

    if not certo:
        assert False
    print("===================================================")


def test_SWeLED2():
    assemblerFile(name="SWeLED2")
    certo = run_CPU("SWeLED2",1,1000)

    if not certo:
        assert False
    print("===================================================")


def test_mult_SW():
    assemblerFile(name="mult_SW")
    certo = run_CPU("mult_SW",1,10000)

    if not certo:
        assert False
    print("===================================================")




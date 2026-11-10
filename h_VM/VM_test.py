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
            if name.endswith(".vm"):
                ramIn = "tests/" + name[:-3] + "/" + name[:-3] +"{}".format(test)+ "_in.mif"
                ramTest = "tests/" + name[:-3] + "/" + name[:-3] +"{}".format(test)+ "_tst.mif"
            else:
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
    
def callJava_VM(jar, vm, nasm):
    #by Rafael Corsi
    command = "java -jar " + jar + " " + vm + " -o " + nasm + " -n"
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    err = proc.wait()
    return(err)
    
      
def genJAR():
    print("==== gerando jar ====================================")
    f = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'VMtranslator/')
    os.system("mvn -f {} package -q -e".format(f))

            
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

def assemblerFile(name="1a-Add"):
    #adapted from Rafael Corsi
    error = 0
    
    jar = "jar/Z01-Assembler.jar"
    pwd = dirname(abspath(__file__))
    nasm = pwd+"/bin/nasm/"
    hack = pwd+"/bin/hack/"
    
    nHack = hack+name+".hack"
    nMif  = hack+name+".mif"
    nNasm = nasm+name+".nasm"

    if not os.path.exists(os.path.dirname(hack)):
        os.makedirs(os.path.dirname(hack))

    print("   - {} to {}".format(nNasm, nHack))
    if callJava(jar, nNasm, nHack) != 0:
        status = 'Assembler Fail'
        error  = 1
    else:
        status = 'Assembler Ok'
        error = 0
    toMIF(nHack, nMif)
    log = ({'name': nMif, 'status': status})

    return error, log  
    
def translatorFile(name="1a-Add",jar = "jar/Z01-VMTranslator.jar", vm="/src/vm/"):
    #adapted from Rafael Corsi
    error = 0
       
    pwd = dirname(abspath(__file__))
    vm = pwd+vm
    nasm = pwd+"/bin/nasm/"
    
    nNasm = nasm+name+".nasm"

    if not os.path.exists(os.path.dirname(nasm)):
        os.makedirs(os.path.dirname(nasm))

    print("   - {} to {}".format(vm+name, nNasm))
    if callJava_VM(jar, vm+name, nNasm) != 0:
        status = 'Translator Fail'
        error  = 1
    else:
        status = 'Translator Ok'
        error = 0

    return error

          
def test_1a_Add():
    translatorFile(name="1a-Add")
    assemblerFile(name="1a-Add")
    certo = run_CPU("1a-Add",1,1000)

    if not certo:
        assert False
    print("===================================================")
    
def test_1b_Calc():
    translatorFile(name="1b-Calc")
    assemblerFile(name="1b-Calc")
    certo = run_CPU("1b-Calc",1,1000)

    if not certo:
        assert False
    print("===================================================")
 
def test_1c_Div():
    translatorFile(name="1c-Div")
    assemblerFile(name="1c-Div")
    certo = run_CPU("1c-Div",1,1000)

    if not certo:
        assert False
    print("===================================================")
    
def test_1d_loop():
    translatorFile(name="1d-loop")
    assemblerFile(name="1d-loop")
    certo = run_CPU("1d-loop",1,10000)

    if not certo:
        assert False
    print("===================================================")

    
def test_2a_Calculadora():
    translatorFile(name="2a-Calculadora")
    assemblerFile(name="2a-Calculadora")
    certo = run_CPU("2a-Calculadora",1,1000)

    if not certo:
        assert False
    print("===================================================")

    
def test_2b_Calculadora():
    translatorFile(name="2b-Calculadora")
    assemblerFile(name="2b-Calculadora")
    certo = run_CPU("2b-Calculadora",1,1000)

    if not certo:
        assert False
    print("===================================================")

    
def test_2c_Calculadora():
    translatorFile(name="2c-Calculadora")
    assemblerFile(name="2c-Calculadora")
    certo = run_CPU("2c-Calculadora",1,1000)

    if not certo:
        assert False
    print("===================================================")

    
def test_add32():
    translatorFile(name="add32")
    assemblerFile(name="add32")
    certo = run_CPU("add32",4,1000)

    if not certo:
        assert False
    print("===================================================")

    
def test_diff():
    translatorFile(name="diff")
    assemblerFile(name="diff")
    certo = run_CPU("diff",1,1000)

    if not certo:
        assert False
    print("===================================================")

    
def test_fibonacci():
    translatorFile(name="fibonacci")
    assemblerFile(name="fibonacci")
    certo = run_CPU("fibonacci",1,1000)

    if not certo:
        assert False
    print("===================================================")

    
def test_invert():
    translatorFile(name="invert")
    assemblerFile(name="invert")
    certo = run_CPU("invert",1,1000)

    if not certo:
        assert False
    print("===================================================")

    
def test_overflow():
    translatorFile(name="overflow")
    assemblerFile(name="overflow")
    certo = run_CPU("overflow",3,1000)

    if not certo:
        assert False
    print("===================================================")

    
def test_remove():
    translatorFile(name="remove")
    assemblerFile(name="remove")
    certo = run_CPU("remove",2,1000)

    if not certo:
        assert False
    print("===================================================")

    
def test_roll():
    translatorFile(name="roll")
    assemblerFile(name="roll")
    certo = run_CPU("roll",1,1000)

    if not certo:
        assert False
    print("===================================================")

    
def test_somatoria():
    translatorFile(name="somatoria")
    assemblerFile(name="somatoria")
    certo = run_CPU("somatoria",1,1000)

    if not certo:
        assert False
    print("===================================================")

    
def test_trapz():
    translatorFile(name="trapz")
    assemblerFile(name="trapz")
    certo = run_CPU("trapz",1,1000)

    if not certo:
        assert False
    print("===================================================")

    
def test_xor():
    translatorFile(name="xor")
    assemblerFile(name="xor")
    certo = run_CPU("xor",1,1000)

    if not certo:
        assert False
    print("===================================================")
    
def test_Translator_SimplePushAdd():
    genJAR()
    translatorFile(name="SimplePushAdd.vm",jar = "VMtranslator/Z01-VMTranslator.jar", vm="/src/examples/")
    assemblerFile(name="SimplePushAdd.vm")
    certo = run_CPU("SimplePushAdd.vm",1,1000)

    if not certo:
        assert False
    print("===================================================")
    
def test_Translator_SimplePopTemp():
    genJAR()
    translatorFile(name="SimplePopTemp.vm",jar = "VMtranslator/Z01-VMTranslator.jar", vm="/src/examples/")
    assemblerFile(name="SimplePopTemp.vm")
    certo = run_CPU("SimplePopTemp.vm",1,1000)

    if not certo:
        assert False
    print("===================================================")
       
def test_Translator_SimpleAnd():
    genJAR()
    translatorFile(name="SimpleAnd.vm",jar = "VMtranslator/Z01-VMTranslator.jar", vm="/src/examples/")
    assemblerFile(name="SimpleAnd.vm")
    certo = run_CPU("SimpleAnd.vm",1,1000)

    if not certo:
        assert False
    print("===================================================")
    
def test_Translator_SimpleEq():
    genJAR()
    translatorFile(name="SimpleEq.vm",jar = "VMtranslator/Z01-VMTranslator.jar", vm="/src/examples/")
    assemblerFile(name="SimpleEq.vm")
    certo = run_CPU("SimpleEq.vm",1,1000)

    if not certo:
        assert False
    print("===================================================")
    
def test_Translator_SimpleGt():
    genJAR()
    translatorFile(name="SimpleGt.vm",jar = "VMtranslator/Z01-VMTranslator.jar", vm="/src/examples/")
    assemblerFile(name="SimpleGt.vm")
    certo = run_CPU("SimpleGt.vm",1,1000)

    if not certo:
        assert False
    print("===================================================")
    
def test_Translator_SimpleLt():
    genJAR()
    translatorFile(name="SimpleLt.vm",jar = "VMtranslator/Z01-VMTranslator.jar", vm="/src/examples/")
    assemblerFile(name="SimpleLt.vm")
    certo = run_CPU("SimpleLt.vm",1,1000)

    if not certo:
        assert False
    print("===================================================")
    
def test_Translator_SimpleNeg():
    genJAR()
    translatorFile(name="SimpleNeg.vm",jar = "VMtranslator/Z01-VMTranslator.jar", vm="/src/examples/")
    assemblerFile(name="SimpleNeg.vm")
    certo = run_CPU("SimpleNeg.vm",1,1000)

    if not certo:
        assert False
    print("===================================================")

def test_Translator_SimpleNot():
    genJAR()
    translatorFile(name="SimpleNot.vm",jar = "VMtranslator/Z01-VMTranslator.jar", vm="/src/examples/")
    assemblerFile(name="SimpleNot.vm")
    certo = run_CPU("SimpleNot.vm",1,1000)

    if not certo:
        assert False
    print("===================================================")
        
def test_Translator_SimpleOr():
    genJAR()
    translatorFile(name="SimpleOr.vm",jar = "VMtranslator/Z01-VMTranslator.jar", vm="/src/examples/")
    assemblerFile(name="SimpleOr.vm")
    certo = run_CPU("SimpleOr.vm",1,1000)

    if not certo:
        assert False
    print("===================================================")








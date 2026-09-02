from cocotb_test.simulator import run
import pytest
import os

def source(name):
	dir = os.path.dirname(__file__)
	src_dir = os.path.join(dir, 'src' )
	return os.path.join(src_dir, name)
     
def test_and16():
    run(vhdl_sources=[source("and16.vhd")], 
        toplevel="and16", 
        python_search=[os.path.join(os.path.dirname(__file__), 'test_cases')],
        module='tb_and16', 
        toplevel_lang="vhdl")

def test_or16():
    run(vhdl_sources=[source("or16.vhd")], 
        toplevel="or16",
        python_search=[os.path.join(os.path.dirname(__file__), 'test_cases')],
        module=1testcase='tb_or16', 
        toplevel_lang="vhdl")
    
def test_not16():
    run(vhdl_sources=[source("not16.vhd")], 
        toplevel="not16",
        python_search=[os.path.join(os.path.dirname(__file__), 'test_cases')],
        module='tb_not16', 
        toplevel_lang="vhdl")

def test_or8way():
    run(vhdl_sources=[source("or8way.vhd")], 
        toplevel="or8way",
        python_search=[os.path.join(os.path.dirname(__file__), 'test_cases')],
        module='tb_or8way', 
        toplevel_lang="vhdl")    
        
def test_nor8way():
    run(vhdl_sources=[source("nor8way.vhd")], 
        toplevel="nor8way",
        python_search=[os.path.join(os.path.dirname(__file__), 'test_cases')],
        module='tb_nor8way', 
        toplevel_lang="vhdl")  

def test_barrelshifter16():
    run(vhdl_sources=[source("barrelshifter16.vhd")], 
        toplevel="barrelshifter16",
        python_search=[os.path.join(os.path.dirname(__file__), 'test_cases')],
        module='tb_barrelshifter16', 
        toplevel_lang="vhdl")  
    
def test_dmux2way():
    run(vhdl_sources=[source("dmux2way.vhd")], 
        toplevel="dmux2way",
        python_search=[os.path.join(os.path.dirname(__file__), 'test_cases')],
        module='tb_dmux2way', 
        toplevel_lang="vhdl")  
  
def test_dmux4way():
    run(vhdl_sources=[source("dmux4way.vhd")], 
        toplevel="dmux4way",
        python_search=[os.path.join(os.path.dirname(__file__), 'test_cases')],
        module='tb_dmux4way', 
        toplevel_lang="vhdl")  

def test_dmux8way():
    run(vhdl_sources=[source("dmux8way.vhd")], 
        toplevel="dmux8way",
        python_search=[os.path.join(os.path.dirname(__file__), 'test_cases')],
        module='tb_dmux8way', 
        toplevel_lang="vhdl")
    
def test_mux2way():
    run(vhdl_sources=[source("mux2way.vhd")], 
        toplevel="mux2way",
        python_search=[os.path.join(os.path.dirname(__file__), 'test_cases')],
        module='tb_mux2way', 
        toplevel_lang="vhdl")
    
def test_mux4way():
    run(vhdl_sources=[source("mux4way.vhd")], 
        toplevel="mux4way",
        python_search=[os.path.join(os.path.dirname(__file__), 'test_cases')],
        module='tb_mux4way', 
        toplevel_lang="vhdl")                     

def test_mux8way():
    run(vhdl_sources=[source("mux8way.vhd")], 
        toplevel="mux8way",
        python_search=[os.path.join(os.path.dirname(__file__), 'test_cases')],
        module='tb_mux8way', 
        toplevel_lang="vhdl") 
    
def test_mux16():
    run(vhdl_sources=[source("mux16.vhd")], 
        toplevel="mux16",
        python_search=[os.path.join(os.path.dirname(__file__), 'test_cases')],
        module='tb_mux16', 
        toplevel_lang="vhdl")                       
        
def test_mux4way16():
    run(vhdl_sources=[source("mux4way16.vhd")], 
        toplevel="mux4way16",
        python_search=[os.path.join(os.path.dirname(__file__), 'test_cases')],
        module='tb_mux4way16', 
        toplevel_lang="vhdl")  
    
def test_mux8way16():
    run(vhdl_sources=[source("mux8way16.vhd")], 
        toplevel="mux8way16",
        python_search=[os.path.join(os.path.dirname(__file__), 'test_cases')],
        module='tb_mux8way16', 
        toplevel_lang="vhdl")  
        
def test_detector_de_moedas():
    run(vhdl_sources=[source("detectordemoedas.vhd")], 
        toplevel="detectordemoedas",
        python_search=[os.path.join(os.path.dirname(__file__), 'test_cases')],
        module='tb_detector_de_moedas', 
        toplevel_lang="vhdl")          
 
def test_circuito():
    run(vhdl_sources=[source("circuito.vhd")], 
        toplevel="circuito",
        python_search=[os.path.join(os.path.dirname(__file__), 'test_cases')],
        module='tb_circuito', 
        toplevel_lang="vhdl") 
    
def test_impressora():
    run(vhdl_sources=[source("impressora.vhd")], 
        toplevel="impressora", 
        module='tb_impressora', 
        toplevel_lang="vhdl") 
    
def test_sevenseg():
    run(vhdl_sources=[source("sevenseg.vhd")], 
        toplevel="sevenseg",
        python_search=[os.path.join(os.path.dirname(__file__), 'test_cases')],
        module='tb_sevenseg', 
        toplevel_lang="vhdl")      
    

if __name__ == "__main__":
    test_and16()
    test_or16()
    test_not16()
    test_or8way()
    test_nor8way()
    test_barrelshifter16()
    test_dmux2way()
    test_dmux4way()
    test_dmux8way()
    test_mux4way16()
    test_mux8way16()
    test_detector_de_moedas()
    test_circuito()
    test_impressora()
    test_sevenseg()

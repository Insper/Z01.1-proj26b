import cocotb
from cocotb.triggers import Timer
       
        
@cocotb.test()
async def tb_impressora(dut):

    insw1 = [0, 1, 1, 0, 0, 0, 1]
    insw2 = [0, 0, 1, 1, 1, 0, 1]
    insw3 = [0, 0, 0, 0, 1, 1, 1]
    insw4 = [1, 1, 0, 0, 1, 0, 1]
    outx =  [1, 1, 1, 1, 0, 1, 0]


    for i in range(len(insw1)):
        dut.sw1.value = insw1[i]
        dut.sw2.value = insw2[i]
        dut.sw3.value = insw3[i]
        dut.sw4.value = insw4[i]

        await Timer(1, units="ns")
        condition = (dut.x.value == outx[i])
        if not condition:
            dut._log.error("Expected value: " + "{0:b}".format(outx[i]) + " Obtained value: " + str(dut.x.value) )
            assert condition, "Error in test {0}!".format(i)
        await Timer(1, units="ns")



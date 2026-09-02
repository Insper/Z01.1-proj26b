import cocotb
from cocotb.triggers import Timer
       
        
@cocotb.test()
async def tb_detector_de_moedas(dut):

    inq =       [0, 1, 0, 0]
    inD =       [0, 0, 1, 0]
    inN =       [0, 0, 0, 1]
    outcents =  [0b00000, 0b11001, 0b01010, 0b00101]


    for i in range(len(inq)):
        dut.q.value = inq[i]
        dut.D.value = inD[i]
        dut.N.value = inN[i]

        await Timer(1, units="ns")
        condition = (dut.cents.value == outcents[i])
        if not condition:
            dut._log.error("Expected value: " + "{0:05b}".format(outcents[i]) + " Obtained value: " + str(dut.cents.value) )
            assert condition, "Error in test {0}!".format(i)
        await Timer(1, units="ns")



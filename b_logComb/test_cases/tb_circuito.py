import cocotb
from cocotb.triggers import Timer
       
        
@cocotb.test()
async def tb_circuito(dut):

    inA =   [0, 1, 1]
    inB =   [0, 1, 1]
    inC =   [0, 0, 1]
    outX =  [0, 1, 0]


    for i in range(len(inA)):
        dut.A.value = inA[i]
        dut.B.value = inB[i]
        dut.C.value = inC[i]

        await Timer(1, units="ns")
        condition = (dut.X.value == outX[i])
        if not condition:
            dut._log.error("Expected value: " + "{0:b}".format(outX[i]) + " Obtained value: " + str(dut.X.value) )
            assert condition, "Error in test {0}!".format(i)
        await Timer(1, units="ns")



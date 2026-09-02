import cocotb
from cocotb.triggers import Timer
       
        
@cocotb.test()
async def tb_mux4way(dut):

    inA =   [1, 1, 1, 1, 0, 0, 0, 0]
    inB =   [0, 0, 0, 0, 1, 1, 1, 1]
    inC =   [1, 1, 1, 1, 0, 0, 0, 0]
    inD =   [0, 0, 0, 0, 1, 1, 1, 1]
    inSel = [0b00, 0b01, 0b10, 0b11, 0b00, 0b01, 0b10, 0b11]
    outq =  [1, 0, 1, 0, 0, 1, 0, 1]


    for i in range(len(inA)):
        dut.a.value = inA[i]
        dut.b.value = inB[i]
        dut.c.value = inC[i]
        dut.d.value = inD[i]
        dut.sel.value = inSel[i]

        await Timer(1, units="ns")
        condition = (dut.q.value == outq[i])
        if not condition:
            dut._log.error("Expected value: " + "{0:b}".format(outq[i]) + " Obtained value: " + str(dut.q.value) )
            assert condition, "Error in test {0}!".format(i)
        await Timer(1, units="ns")


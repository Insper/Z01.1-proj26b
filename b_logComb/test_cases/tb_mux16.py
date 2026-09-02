import cocotb
from cocotb.triggers import Timer
       
        
@cocotb.test()
async def tb_mux16(dut):

    inA =   [0b1111000011110000, 0b0000000000000000, 0b1111000011110000, 0b0000000000000000]
    inB =   [0b0000000000000000, 0b1111000011110000, 0b0000000000000000, 0b1111000011110000]
    inSel = [0, 1, 1, 0]
    outq =  [0b1111000011110000, 0b1111000011110000, 0b0000000000000000, 0b0000000000000000]


    for i in range(len(inA)):
        dut.a.value = inA[i]
        dut.b.value = inB[i]
        dut.sel.value = inSel[i]

        await Timer(1, units="ns")
        condition = (dut.q.value == outq[i])
        if not condition:
            dut._log.error("Expected value: " + "{0:016b}".format(outq[i]) + " Obtained value: " + str(dut.q.value) )
            assert condition, "Error in test {0}!".format(i)
        await Timer(1, units="ns")


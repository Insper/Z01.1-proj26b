import cocotb
from cocotb.triggers import Timer
       
        
@cocotb.test()
async def tb_mux2way(dut):

    inA =   [0, 1, 1, 0]
    inB =   [1, 0, 0, 1]
    inSel = [0, 0, 1, 1]
    outq =  [0, 1, 0, 1]


    for i in range(len(inA)):
        dut.a.value = inA[i]
        dut.b.value = inB[i]
        dut.sel.value = inSel[i]

        await Timer(1, units="ns")
        condition = (dut.q.value == outq[i])
        if not condition:
            dut._log.error("Expected value: " + "{0:b}".format(outq[i]) + " Obtained value: " + str(dut.q.value) )
            assert condition, "Error in test {0}!".format(i)
        await Timer(1, units="ns")


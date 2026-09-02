import cocotb
from cocotb.triggers import Timer
       
        
@cocotb.test()
async def tb_or8way(dut):

    inA =   [0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
    inB =   [0, 0, 1, 0, 0, 0, 0, 0, 0, 1]
    inC =   [0, 0, 0, 1, 0, 0, 0, 0, 0, 1]
    inD =   [0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
    inE =   [0, 0, 0, 0, 0, 1, 0, 0, 0, 1]
    inF =   [0, 0, 0, 0, 0, 0, 1, 0, 0, 1]
    inG =   [0, 0, 0, 0, 0, 0, 0, 1, 0, 1]
    inH =   [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
    outq =  [0, 1, 1, 1, 1, 1, 1, 1, 1, 1]


    for i in range(len(inA)):
        dut.a.value = inA[i]
        dut.b.value = inB[i]
        dut.c.value = inC[i]
        dut.d.value = inD[i]
        dut.e.value = inE[i]
        dut.f.value = inF[i]
        dut.g.value = inG[i]
        dut.h.value = inH[i]

        await Timer(1, units="ns")
        condition = (dut.q.value == outq[i])
        if not condition:
            dut._log.error("Expected value: " + "{0:b}".format(outq[i]) + " Obtained value: " + str(dut.q.value) )
            assert condition, "Error in test {0}!".format(i)
        await Timer(1, units="ns")



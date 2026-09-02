import cocotb
from cocotb.triggers import Timer
       
        
@cocotb.test()
async def tb_mux4way16(dut):

    inA =   [0b1111000011110000, 0b0000000000000000, 0b1111000011110000, 0b0000000000000000, 0b1111000011110000, 0b0000000000000000]
    inB =   [0b0000000000000000, 0b1111000011110000, 0b0000000000000000, 0b1111000011110000, 0b0000000000000000, 0b1111000011110000]
    inC =   [0b1111000011110000, 0b0000000000000000, 0b1111000011110000, 0b0000000000000000, 0b1111000011110000, 0b0000000000000000]
    inD =   [0b0000000000000000, 0b1111000011110000, 0b0000000000000000, 0b1111000011110000, 0b0000000000000000, 0b1111000011110000]
    inSel = [0b00, 0b01, 0b10, 0b11, 0b11, 0b10]
    outq =  [0b1111000011110000, 0b1111000011110000, 0b1111000011110000, 0b1111000011110000, 0b0000000000000000, 0b0000000000000000]


    for i in range(len(inA)):
        dut.a.value = inA[i]
        dut.b.value = inB[i]
        dut.c.value = inC[i]
        dut.d.value = inD[i]
        dut.sel.value = inSel[i]

        await Timer(1, units="ns")
        condition = (dut.q.value == outq[i])
        if not condition:
            dut._log.error("Expected value: " + "{0:016b}".format(outq[i]) + " Obtained value: " + str(dut.q.value) )
            assert condition, "Error in test {0}!".format(i)
        await Timer(1, units="ns")


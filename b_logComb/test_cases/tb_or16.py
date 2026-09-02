import cocotb
from cocotb.triggers import Timer
       
        
@cocotb.test()
async def tb_or16(dut):

    inA = [0b1111000011110000, 0b1010101010101010, 0b0101010101010101, 0b0101010101010101, 0b0000000000000000, 0b1111111111111111, 0b0101010101010101, 0b1010101010101010]
    inB = [0b0000111100001111, 0b0000000000000000, 0b0000000000000000, 0b1010101010101010, 0b0000000000000000, 0b1111111111111111, 0b0101010101010101, 0b1010101010101010]
    outq =[0b1111111111111111, 0b1010101010101010, 0b0101010101010101, 0b1111111111111111, 0b0000000000000000, 0b1111111111111111, 0b0101010101010101, 0b1010101010101010]
    
    for i in range(len(inA)):
        dut.a.value = inA[i]
        dut.b.value = inB[i]

        await Timer(1, units="ns")
        condition = (dut.q.value == outq[i])
        if not condition:
            dut._log.error("Expected value: " + "{0:016b}".format(outq[i]) + " Obtained value: " + str(dut.q.value) )
            assert condition, "Error in test {0}!".format(i)
        await Timer(1, units="ns")


import cocotb
from cocotb.triggers import Timer
       
        
@cocotb.test()
async def tb_barrelshifter16(dut):

    inA = [0b0000000000000010, 0b0000000000000010, 0b0000000000000010, 0b0000000000000010, 0b0000000000000010, 0b0100000000000000, 0b0100000000000000, 0b0100000000000000, 0b0100000000000000, 0b0100000000000000]
    inDir = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    inSize = [0b000, 0b001, 0b010, 0b011, 0b100, 0b000, 0b001, 0b010, 0b011, 0b100]
    outq =[0b0000000000000010, 0b0000000000000100, 0b0000000000001000, 0b0000000000010000, 0b0000000000100000, 0b0100000000000000, 0b0010000000000000, 0b0001000000000000, 0b0000100000000000, 0b0000010000000000]
    
    for i in range(len(inA)):
        dut.a.value = inA[i]
        dut.dir.value = inDir[i]
        dut.size.value = inSize[i]

        await Timer(1, units="ns")
        condition = (dut.q.value == outq[i])
        if not condition:
            dut._log.error("Expected value: " + "{0:016b}".format(outq[i]) + " Obtained value: " + str(dut.q.value) )
            assert condition, "Error in test {0}!".format(i)
        await Timer(1, units="ns")


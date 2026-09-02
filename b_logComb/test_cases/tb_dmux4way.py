import cocotb
from cocotb.triggers import Timer
       
        
@cocotb.test()
async def tb_dmux4way(dut):

    inA =   [1, 1, 1, 1, 0, 0, 0, 0]
    inSel = [0b00, 0b01, 0b10, 0b11, 0b00, 0b01, 0b10, 0b11]
    outq0 = [1, 0, 0, 0, 0, 0, 0, 0]
    outq1 = [0, 1, 0, 0, 0, 0, 0, 0]
    outq2 = [0, 0, 1, 0, 0, 0, 0, 0]
    outq3 = [0, 0, 0, 1, 0, 0, 0, 0]

    for i in range(len(inA)):
        dut.a.value = inA[i]
        dut.sel.value = inSel[i]

        await Timer(1, units="ns")
        condition = (dut.q0.value == outq0[i] and dut.q1.value == outq1[i] and dut.q2.value == outq2[i] and dut.q3.value == outq3[i])
        if not condition:
            if not (dut.q0.value == outq0[i]):
                dut._log.error("Expected value q0: " + "{0:b}".format(outq0[i]) + " Obtained value q0: " + str(dut.q0.value) )
            if not (dut.q1.value == outq1[i]):
                dut._log.error("Expected value q1: " + "{0:b}".format(outq1[i]) + " Obtained value q1: " + str(dut.q1.value) )
            if not (dut.q2.value == outq2[i]):
                dut._log.error("Expected value q2: " + "{0:b}".format(outq2[i]) + " Obtained value q2: " + str(dut.q2.value) )
            if not (dut.q3.value == outq3[i]):
                dut._log.error("Expected value q3: " + "{0:b}".format(outq3[i]) + " Obtained value q3: " + str(dut.q3.value) )
            assert condition, "Error in test {0}!".format(i)
        await Timer(1, units="ns")



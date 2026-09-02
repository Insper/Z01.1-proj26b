import cocotb
from cocotb.triggers import Timer
       
        
@cocotb.test()
async def tb_dmux8way(dut):

    inA =   [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    inSel = [0b000, 0b001, 0b010, 0b011, 0b100, 0b101, 0b110, 0b111, 0b000, 0b001, 0b010, 0b011, 0b100, 0b101, 0b110, 0b111]
    outq0 = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outq1 = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outq2 = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outq3 = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outq4 = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outq5 = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outq6 = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outq7 = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(len(inA)):
        dut.a.value = inA[i]
        dut.sel.value = inSel[i]

        await Timer(1, units="ns")
        condition = (dut.q0.value == outq0[i] and dut.q1.value == outq1[i] and dut.q2.value == outq2[i] and dut.q3.value == outq3[i] and
                     dut.q4.value == outq4[i] and dut.q5.value == outq5[i] and dut.q6.value == outq6[i] and dut.q7.value == outq7[i]) 
        if not condition:
            if not (dut.q0.value == outq0[i]):
                dut._log.error("Expected value q0: " + "{0:b}".format(outq0[i]) + " Obtained value q0: " + str(dut.q0.value) )
            if not (dut.q1.value == outq1[i]):
                dut._log.error("Expected value q1: " + "{0:b}".format(outq1[i]) + " Obtained value q1: " + str(dut.q1.value) )
            if not (dut.q2.value == outq2[i]):
                dut._log.error("Expected value q2: " + "{0:b}".format(outq2[i]) + " Obtained value q2: " + str(dut.q2.value) )
            if not (dut.q3.value == outq3[i]):
                dut._log.error("Expected value q3: " + "{0:b}".format(outq3[i]) + " Obtained value q3: " + str(dut.q3.value) )
            if not (dut.q4.value == outq4[i]):
                dut._log.error("Expected value q4: " + "{0:b}".format(outq4[i]) + " Obtained value q4: " + str(dut.q4.value) )
            if not (dut.q5.value == outq5[i]):
                dut._log.error("Expected value q5: " + "{0:b}".format(outq5[i]) + " Obtained value q5: " + str(dut.q5.value) )
            if not (dut.q6.value == outq6[i]):
                dut._log.error("Expected value q6: " + "{0:b}".format(outq6[i]) + " Obtained value q6: " + str(dut.q6.value) )
            if not (dut.q7.value == outq7[i]):
                dut._log.error("Expected value q7: " + "{0:b}".format(outq7[i]) + " Obtained value q7: " + str(dut.q7.value) )
            assert condition, "Error in test {0}!".format(i)
        await Timer(1, units="ns")


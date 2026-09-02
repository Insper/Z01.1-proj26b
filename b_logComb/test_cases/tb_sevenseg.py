import cocotb
from cocotb.triggers import Timer
       
        
@cocotb.test()
async def tb_sevenseg(dut):

    inbcd =   [0b0000, 0b0011, 0b0111]
    outleds = [0b1000000, 0b0110000, 0b1111000]


    for i in range(len(inbcd)):
        dut.bcd.value = inbcd[i]

        await Timer(1, units="ns")
        condition = (dut.leds.value == outleds[i])
        if not condition:
            dut._log.error("Expected value: " + "{0:07b}".format(outleds[i]) + " Obtained value: " + str(dut.leds.value) )
            assert condition, "Error in test {0}!".format(i)
        await Timer(1, units="ns")


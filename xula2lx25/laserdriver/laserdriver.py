# Author: Rik Starmans
# Company: Hexastorm
from myhdl import block, always_comb, always, intbv, always_seq
from myhdl import instances, Signal, ResetSignal, delay

# TODO: usage of modbv results in error
# modbv results in error "should have full bit vector range"
# modbv would make the code prettiers

# CONSTANTS
XULA_FREQ = 12e6     # clock frequency xula2
DUTY_FREQ = 1   # frequency of duty cycles
PWMWIDTH = 1         # PULSE WIDTH MODULATION  = PWMWIDTH/PWMLENGTH
PWMLENGTH = 2
# print("Laser frequency is"+duty_freq/pwmlength)
# i.e. IFF duty_freq=21000 and pwmwdith=2 ---> laserfreq=duty_freq
# You create a DUTY trigger if you reach the maximum of duty_cntmax
DUTY_CNTMAX = round(XULA_FREQ/(DUTY_FREQ*2))


@block
def laserdriver(clock, reset, laserpin):
    duty_cnt = Signal(intbv(0, min=0, max=DUTY_CNTMAX))
    laser_cnt = Signal(intbv(0, min=0, max=PWMLENGTH))

    @always_comb
    def duty():
        if reset == 1:
            laserpin.next = 0
        elif laser_cnt < laser_cnt.max-1:
            laserpin.next = 1
        else:
            laserpin.next = 0

    @always_seq(clock.posedge, reset)
    def dutygen():
        if duty_cnt >= duty_cnt.max-1:
            duty_cnt.next = 0
            if laser_cnt >= laser_cnt.max-1:
                laser_cnt.next = 0
            else:
                laser_cnt.next = laser_cnt+1
        else:
            duty_cnt.next = duty_cnt+1

    return instances()


@block
def testbench():
    # Input Pins
    reset = ResetSignal(0, active=1, async=True)
    # Output Pins
    laserpin = Signal(bool(0))
    clock = Signal(bool(0))
    # Modules
    lasergen = laserdriver(clock, reset, laserpin)
    # Clock for simulator
    HALF_PERIOD = delay(round(1/(2*XULA_FREQ)*1e9))

    @always(HALF_PERIOD)
    def clkgen():
        clock.next = not clock

    return instances()


if __name__ == '__main__':
    test_inst = testbench()
    test_inst.config_sim(trace=True)
    test_inst.run_sim(DUTY_CNTMAX*40*1/(XULA_FREQ)*1e9)

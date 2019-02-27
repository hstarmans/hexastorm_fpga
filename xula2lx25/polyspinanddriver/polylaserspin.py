# Author: Rik Starmans
# Company: Hexastorm
from myhdl import *
# add https://pypi.python.org/pypi/xsconnect

# Xula board:
xula_freq=12e6  # frequency is 12 MHz on xula2

#   Polygon
poly_freq=1000  # max frequency polygon is 2.1 kHz
                # due to noise polygon speed has been reduced to 1 kHz

#   Laser
laser_freq=21000 # frequency at which laser is changed
pwmwidth=1      #  PWM  = PWMWIDTH/PWMLENGTH
pwmlength=12    # PWM LENGTH reduces resolution!!
# Constants [used to simplify code]
las_cntmax=round(xula_freq/(laser_freq*2)) # half period polygon motor pulse

@block
def polylaser(polypin, laserpin, clock, resetpoly,resetlaser):

    cnt_max =round(xula_freq/(poly_freq*2)) # clock_frequency*led_rate
    clk_cnt = Signal(intbv(0, min=0, max=cnt_max))

    @always_seq(clock.posedge,resetpoly)
    def polygen():
        if clk_cnt >= cnt_max-1:
            clk_cnt.next=0
            polypin.next=not polypin # results in warning; output pin read internally
        else:
            clk_cnt.next=clk_cnt+1


    las_cnt = Signal(intbv(0, min=0, max=las_cntmax))
    duty_cnt = Signal(intbv(0, min=0, max=pwmlength))

    @always_comb
    def duty():
        if duty_cnt<pwmwidth and resetlaser==0:
            laserpin.next=1
        else:
            laserpin.next=0

    @always(clock.posedge)
    def lascntgen():
        if las_cnt >= las_cntmax-1:
            las_cnt.next=0
            if duty_cnt>=pwmlength-1:
                duty_cnt.next=0
            else:
                duty_cnt.next=duty_cnt+1
        else:
            las_cnt.next=las_cnt+1

    return instances()


@block
def testbench():
    # Xula2 board pins
    clock = Signal(bool(0))
    # Input Pin
    resetlaser=ResetSignal(0,active=1,async=True) # enable/disable getpolyperiod
    resetpoly=ResetSignal(0,active=1,async=True)  # enable/disable polygen
    # Output Pin
    polypin=Signal(bool(0))
    laserpin=Signal(bool(0))
    # Modules
    plaser=polylaser(polypin, laserpin, clock, resetpoly,resetlaser)

    # CLOCK
    HALF_PERIOD=delay(round(1/(2*xula_freq)*1e9))
    @always(HALF_PERIOD)
    def clkgen():
        clock.next = not clock

    return instances()

if __name__ == '__main__':
    test_inst=testbench()
    test_inst.config_sim(trace=True)
    test_inst.run_sim(1/2100*10*1E9) # i.e. 1 second

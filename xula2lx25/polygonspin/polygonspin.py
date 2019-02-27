from myhdl import block, always_seq, intbv, Signal, ResetSignal, delay
from myhdl import always, instances

xula_freq = 12e6  # frequency is 12 MHz on Xula2
poly_freq = 400   # max frequency polygon is 2.1 kHz, reduced to 1 kHz


@block
def polydriver(polypin, clock, reset=None):
    cnt_max = round(xula_freq/(poly_freq*2))  # clock_frequency*led_rate
    clk_cnt = Signal(intbv(0, min=0, max=cnt_max))

    @always_seq(clock.posedge, reset)
    def polygen():
        if clk_cnt >= cnt_max-1:
            clk_cnt.next = 0
            polypin.next = not polypin
        else:
            clk_cnt.next = clk_cnt+1

    return polygen


@block
def testbench():
    # Xula2 board pins
    clock = Signal(bool(0))
    # Input Pin
    resetpoly = ResetSignal(0, active=1, async=True)  # enable/disable polygen
    # Output Pin
    polypin = Signal(bool(0))

    polygen = polydriver(polypin, clock, resetpoly)
    # CLOCK

    @block
    def clkdriver(clock):
        interval = delay(round(1/(2*xula_freq)*1e9))

        @always(interval)
        def clkgen():
            clock.next = not clock
            return clkgen
    clkgen=clkdriver(clock)

    return instances()


if __name__ == '__main__':
    test_inst = testbench()
    test_inst.config_sim(trace=True)
    test_inst.run_sim(1/2100*10*1E9)

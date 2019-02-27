from myhdl import always, delay, Signal, intbv


def clkdriver(clock):
    clk_frequency = 12e6  # clk frequency is 12 MHz on Xula2
    interval = delay(round(1/clk_frequency*1e9))

    @always(interval)
    def clkgen():
        clock.next = not clock
    return clkgen


def strobe(clock, led):
    led_rate = 333e-3  # strobe change rate of 333ms
    clk_frequency = 12e6  # clk frequency is 12 MHz on Xula2
    clk_frequency = 12e6  # clk frequency is 12 MHz on Xula2
    cnt_max = round(clk_frequency*led_rate)  # clock_frequency*led_rate
    clk_cnt = Signal(intbv(0, min=0, max=cnt_max))

    @always(clock.posedge)
    def blinkled():
        if clk_cnt >= cnt_max-1:
            clk_cnt.next = 0
            led.next = not led
        else:
            clk_cnt.next = clk_cnt+1
    return blinkled


def testbench():
    led = Signal(bool(0))
    clock = Signal(bool(0))
    klok = clkdriver(clock)
    led = strobe(clock, led)
    return klok, led


if __name__ == '__main__':
    # TODO het duurt nu 666ms voordat de led verandert!?
    tb_led = traceSignals(testbench)
    sim = Simulation(tb_led)
    sim.run(1E9)

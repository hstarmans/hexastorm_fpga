# Company: Hexastorm
# Author: Rik Starmans
# Date: 17-8-2017
# Description:  program is decribed in *.odt in this folder
from myhdl import block, Signal, intbv, delay, always_seq, always_comb
from myhdl import ResetSignal, instances, always, StopSimulation, instance


def constants(xula_freq=12e6):
    #  Physics
    steps_mm = 76.199     # steps per mm, FELIXframe at 1/16 microstep
    mm_s_home = 3          # homing speed
    home_bounce = 4        # bounce distance in mm
    home_dir = False       # homing direction
    # Physics --> Xula
    step_freq_home = round(mm_s_home*steps_mm)
    step_cnt_home = round(xula_freq/(step_freq_home*2))
    home_count = round(home_bounce*steps_mm)
    home_freq = round(xula_freq/home_count)
    return home_dir, step_cnt_home, home_freq


@block
def stepperdriver(dir_pino, step_pino, complete_pino, trigger_pini,
                  clock, reset, xula_freq=12e6):
    home_dir, step_cnt_home, home_freq = constants(xula_freq)
    clk_cnt = Signal(intbv(0, min=0, max=step_cnt_home))
    bounce_cnt = Signal(intbv(0, min=0, max=home_freq))

    @always_comb
    def switch():
        if bounce_cnt == 1:
            complete_pino.next = 1
        else:
            complete_pino.next = 0

    @always_seq(clock.posedge, reset)
    def polygen():

        # bounce action
        if trigger_pini:
            dir_pino.next = not home_dir
            bounce_cnt.next = home_freq-1
        elif (not trigger_pini) & (0 == bounce_cnt):
            dir_pino.next = home_dir
        else:
            dir_pino.next = not home_dir
            if bounce_cnt > 1:
                bounce_cnt.next = bounce_cnt-1

        # sends pulses to stepper driver
        if bounce_cnt != 1:
            if clk_cnt >= clk_cnt.max-1:
                clk_cnt.next = 0
                step_pino.next = not step_pino
            else:
                clk_cnt.next = clk_cnt + 1
        else:
            clk_cnt.next = 0
            step_pino.next = 0
    return instances()



@block
def testbench():
    # Xula2 board pins
    clock = Signal(bool(0))
    xula_freq = 100e3
    # Input Pin
    reset = ResetSignal(0, active=1, async=True)
    en_pini = Signal(bool(1))
    trigger_pini = Signal(bool(0))
    # Output Pin
    dir_pino = Signal(bool(0))
    step_pino = Signal(bool(0))
    complete_pino = Signal(bool(0))
    # Stepper Generator
    stepgen = stepperdriver(dir_pino, step_pino, complete_pino, trigger_pini,
                            clock, reset, xula_freq)

    # Clock Generator
    @block
    def clkdriver(clock):
        interval = delay(round(1/(2*xula_freq)*1e9))

        @always(interval)
        def clkgen():
            clock.next = not clock
        return clkgen

    clkgen = clkdriver(clock)

    @instance
    def stimulus():
        # NOTE: 1e9 equals 1 second
        sec = 1E9
        yield delay(round(0.1*sec))
        trigger_pini.next = 1
        yield delay(round(0.01*sec))
        trigger_pini.next = 0
        yield delay(round(0.3*sec))
        raise StopSimulation
    return instances()


def test_bench():
    """pytest test_bench

    Test can be executed with the pytest package
    advantages see; http://www.myhdl.org/docs/examples/stopwatch/
    """
    test_inst = testbench()
    test_inst.config_sim(trace=True)
    test_inst.run_sim()
    # test_inst.run_sim(1E9)  # i.e. second

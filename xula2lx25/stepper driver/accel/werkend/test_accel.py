# Company: Hexastorm:
# Author: Rik Starmans
# Date: 17-8-2017
# Description:  program is decribed in *.odt in this folder
from myhdl import block, Signal, intbv, delay, always_seq, always_comb
from myhdl import ResetSignal, instances, always, StopSimulation, instance

# TODO:
#    1. NO change of signal on step
#    2. Circuit needs to be tested

def constants(xula_freq=12e6):
    #  Physics
    steps_rev = 1       # steps per revolution
    microsteps = 1       # microsteps
    mm_rev = 1            # mm per revolution
    mm_s_start = 1        # mm per s
    mm_s_trgt = 12        # mm per s (speed)
    acc_time = 1          # time needed for acceleration
    # Physics --> Xula
    step_freq_strt = round(mm_s_start/mm_rev*steps_rev*microsteps)
    step_freq_trgt = round(mm_s_trgt/mm_rev*steps_rev*microsteps)
    step_cnt_strt = round(xula_freq/(step_freq_strt*2))
    step_cnt_trgt = round(xula_freq/(step_freq_trgt*2))
    # NOTE: step_cnt_trg << step_cnt_strt
    cnt_acc = round((step_cnt_strt-step_cnt_trgt)/(
        acc_time*xula_freq)*step_cnt_trgt)
    return step_cnt_strt, step_cnt_trgt, cnt_acc


@block
def stepperdriver(dir_pino, step_pino, en_pino, clock,
                  reset, xula_freq=12e6):

    counter_photodiode = Signal(intbv(0, min=0, max=round(12e6)))
    
    @always_comb
    def dirpin():
        if reset == 0:
            dir_pino.next = 1
            en_pino.next = 1
        else:
            dir_pino.next = 0
            en_pino.next = 0

    @always_seq(clock.posedge, reset)
    def count():
        if counter_photodiode >= counter_photodiode.max-1:
            counter_photodiode.next = 0
            step_pino.next = not step_pino
        else:
            counter_photodiode.next = counter_photodiode+1
    return instances() 


    return instances()


@block
def testbench():
    # Xula2 board pins
    clock = Signal(bool(0))
    xula_freq = 100e3
    # Input Pin
    reset = ResetSignal(0, active=1, async=True)
    en_pini = Signal(bool(1))
    dir_pini = Signal(bool(0))
    # Output Pin
    en_pino = Signal(bool(0))
    dir_pino = Signal(bool(0))
    step_pino = Signal(bool(0))

    # Stepper Generator
    stepgen = stepperdriver(dir_pino, step_pino, en_pino, dir_pini, en_pini,
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
        interval = delay(round(1E9))
        yield interval
        assert 1 == 1
        raise StopSimulation
    return instances()


def test_bench():
    """pytest test_bench

    Test are can be executed with the pytest package
    advantages see; http://www.myhdl.org/docs/examples/stopwatch/
    """
    test_inst = testbench()
    test_inst.config_sim(trace=True)
    test_inst.run_sim()
    # test_inst.run_sim(1E9)  # i.e. second

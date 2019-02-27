# Company: Hexastorm:
# Author: Rik Starmans
# Date: 17-8-2017
# Description:  program is decribed in *.odt in this folder
from myhdl import block, Signal, intbv, delay, always_seq, always_comb
from myhdl import ResetSignal, instances, always, StopSimulation, instance
import unittest

def constants(xula_freq=12e6):
    steps_rev = 60       # steps per revolution
    mm_rev = 1           # mm per revolution
    mm_s_start = 1       # mm per s
    mm_s_trgt = 12       # mm per s (speed)
    acc_time = 1         # time needed for acceleration
    step_freq_strt = round(mm_s_start/mm_rev*steps_rev)
    step_freq_trgt = round(mm_s_trgt/mm_rev*steps_rev)
    return step_freq_strt, step_freq_trgt, acc_time 


@block
def stepperdriver(dir_pino, step_pino, en_pino, dir_pini,
                  en_pini, clock, reset=None, xula_freq=12e6):
    step_freq_strt, step_freq_trgt, acc_time = constants(xula_freq)
    # clock_frequency*led_rate
    step_cnt_strt = round(xula_freq/(step_freq_strt*2))
    step_cnt_trgt = round(xula_freq/(step_freq_trgt*2))
    # NOTE: step_cnt_trg << step_cnt_strt
    cnt_acc = round((step_cnt_strt-step_cnt_trgt)/(acc_time*xula_freq)*step_cnt_trgt)
    ramp_cnt = Signal(intbv(step_cnt_strt-1, min=0, max=step_cnt_strt))
    acc_cnt = Signal(intbv(0, min=0, max=step_cnt_trgt))
    clk_cnt = Signal(intbv(0, min=0, max=step_cnt_strt))

    @always_comb
    def dirpin():
        dir_pino = dir_pini

    @always_seq(clock.posedge, reset)
    def polygen():

        # calculates current speed
        if acc_cnt >= acc_cnt.max - 1:
            acc_cnt.next = 0
            if en_pini:
                if ramp_cnt > step_cnt_trgt+cnt_acc:
                    ramp_cnt.next = ramp_cnt-cnt_acc
            else:
                if ramp_cnt < step_cnt_strt - cnt_acc:
                    ramp_cnt.next = ramp_cnt + cnt_acc
        else:
            acc_cnt.next = acc_cnt + 1

        # sends pulses to stepper driver given current speed
        if clk_cnt >= ramp_cnt-1:
            clk_cnt.next = 0
            if en_pini:
                en_pino = 1
                step_pino.next = not step_pino
            else:
                if clk_cnt < step_cnt_strt - 10:
                    en_pino = 1
                    step_pino.next = not step_pino
                else:
                    en_pino = 0
        else:
            clk_cnt.next = clk_cnt + 1
    
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
        print("Testing equality of 1 to 1")
        assert 1 == 1
        print(" passed")
        raise StopSimulation
    return instances()


if __name__ == '__main__':
    test_inst = testbench()
    test_inst.config_sim(trace=True)
    test_inst.run_sim()
    # test_inst.run_sim(1E9)  # i.e. second

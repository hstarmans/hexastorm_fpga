# Author: Rik Starmans
# Company: Hexastorm

from myhdl import block, intbv, always, instances, Signal, always_comb
from myhdl import instance, delay, StopSimulation, ResetSignal, always_seq
from myhdl import enum

# Xula board
xula_freq = 12e6  # clock frequency xula2


@block
def motor(clock, CS, SYNC, din, dout, SClk1, SClk2, reset):
    """
    clock: in std_logic; --spartan 6
    CS:    out st_logic
    din:   in std_logic  --ADC
    dout:  out std_logic --DAC
    SClk:  out std_logic --ADC
    SClk2: out std_logic --DAC

    function is documentated with Tutorial 15 - ADC's and DAC's
    on the Spartan 3E Starter Board
    """
    state_type = enum("IDLE", "READ", "FUNC", "WRITE")
    state = Signal(state_type.READ)
    data = Signal(intbv(0)[12:0])
    cnt = Signal(intbv(0, min=0, max=20))
    clkdiv = Signal(intbv(0, min=0, max=6))
    newclk = Signal(bool(0))

    @always_comb
    def sync_clocks():
        SClk1.next = newclk
        SClk2.next = newclk

    @always_seq(clock.posedge, reset)
    def FSM():
        if clkdiv == 5 and newclk == 1:
            if state == state_type.IDLE:
                CS.next = 1
                SYNC.next = 1
                if cnt == 15:
                    cnt.next = 0
                    state.next = state_type.READ
                else:
                    cnt.next = cnt + 1
                    state.next = state_type.IDLE
            elif state == state_type.READ:
                CS.next = 0
                SYNC.next = 1
                cnt.next = cnt + 1
                if cnt < 4:
                    cnt.next = cnt + 1
                    state.next = state_type.READ
                elif cnt > 3 and cnt < 16:
                    cnt.next = cnt + 1
                    data.next[15-cnt] = din
                    state.next = state_type.READ
                elif cnt == 16:
                    cnt.next = 0
                    state.next = state_type.FUNC
            elif state == state_type.FUNC:
                CS.next = 1
                SYNC.next = 1
                cnt.next = 0
                # NOTE: different operation than example
                data.next = (data.max-1)-data
                state.next = state_type.WRITE
            elif state == state_type.WRITE:
                CS.next = 1
                SYNC.next = 0
                if cnt < 4:
                    cnt.next = cnt + 1
                    dout.next = 0
                    state.next = state_type.WRITE
                elif cnt > 3 and cnt < 16:
                    cnt.next = cnt + 1
                    dout.next = data[15-cnt]
                    state.next = state_type.WRITE
                elif cnt == 16:
                    cnt.next = 0
                    state.next = state_type.IDLE

            else:
                raise ValueError("Undefined State")

    @always_seq(clock.posedge, reset)
    def clock_divider():
        if clkdiv == 5:
            # a.next = not a equals a.next = a^1
            newclk.next = not newclk
            clkdiv.next = 0
        else:
            clkdiv.next = clkdiv + 1
    return instances()


@block
def testbench():
    # Input pins
    din = Signal(bool(1))
    reset = ResetSignal(0, active=1, async=True)
    # Output pins
    CS = Signal(bool(0))
    SYNC = Signal(bool(0))
    dout = Signal(bool(1))
    SClk1 = Signal(bool(0))
    SClk2 = Signal(bool(0))
    # FPGA clock pin
    clock = Signal(bool(0))
    # Modules
    motorgen = motor(clock, CS, SYNC, din, dout, SClk1, SClk2, reset)
    # CLOCK
    HALF_PERIOD = delay(round(1/(2*xula_freq)*1e9))

    @always(HALF_PERIOD)
    def clkgen():
        clock.next = not clock

    @instance
    def stimulus():
        for i in range(1000):
            yield clock.negedge
        raise StopSimulation

    return instances()


if __name__ == '__main__':
    test_inst = testbench()
    test_inst.config_sim(trace=True)
    test_inst.run_sim()

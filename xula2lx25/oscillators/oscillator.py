from myhdl import Signal, delay, always, Simulation, intbv, traceSignals


def testbench():
    clk = Signal(0)
    cnt = Signal(intbv(0, min=0, max=4))
    toggle = Signal(bool(0))

    @always(delay(10))
    def driveclk():
        clk.next = not clk

    @always(clk.posedge)
    def spin():
        print("aap")
        if cnt == 4-1:
            toggle.next = not toggle
            cnt.next = 0
        else:
            cnt.next = cnt+1
    return driveclk, spin


tb_fsm = traceSignals(testbench)
sim = Simulation(tb_fsm)
sim.run(150)

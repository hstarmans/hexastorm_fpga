from myhdl import Signal, delay, always, now, Simulation, intbv 


def ClkDriver(clk):
    halfPeriod = delay(10) # one full clock cycle
    @always(halfPeriod)
    def driveClk():
        clk.next = not clk
    return driveClk

def SpinPolygon(clk):
    @always(clk.posedge)
    def spin():
        if cnt==4-1:
            toggle.next=not toggle
            cnt.next=0
            print("%s triple tick" % now()) #triggered at 3.5 clock cyles --> 70 ns
        else:
            cnt.next=cnt+1
            print("%s tick" % now())
    return spin

clk = Signal(0)
cnt = Signal(intbv(0, min=0, max=4))
toggle = Signal(bool(0))
clkdriver_inst = ClkDriver(clk)
spinpolygon_inst = SpinPolygon(clk)
sim = Simulation(clkdriver_inst,spinpolygon_inst)
sim.run(150)

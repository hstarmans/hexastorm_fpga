# Author: Rik Starmans
# Company: Hexastorm
# Date: : 15-9-2017

from myhdl import block, intbv, always, instances, Signal, always_comb
from myhdl import instance, delay, StopSimulation, ResetSignal, always_seq
# Xula board
xula_freq = 12e6  # clock frequency xula2

# Polygon
#  if the pins point toward you
#  the polygon rotates clockwise
#  Polygon rotates at 21000 RPM which equals 350 Hz
#  For 21000 RPM, the polygon should be pulsed at 350x6=2100 HZ
#  The polygon is not perfectly balanced; typical frequency is 1000 Hz.
poly_freq = 400
facets = 4  # number of facets

# LASER
#
#   0  --> laser is off
#   1  --> laser is on
PERIOD_POLYGON = round(xula_freq/poly_freq)


@block
def polydriver(clock, polypin, laserpin, enable, reset):
    counter_polygon = Signal(intbv(0, min=0, max=PERIOD_POLYGON//2))

    @always_seq(clock.posedge, reset)
    def polygen():
        if counter_polygon >= counter_polygon.max-1:
            counter_polygon.next = 0
            polypin.next = not polypin
        else:
            counter_polygon.next = counter_polygon+1

    @always_comb
    def switchlaser():
        if enable == 1:
            laserpin.next = 1
        else:
            laserpin.next = 0

    return instances()


@block
def testbench():
    # Input Pins
    reset = ResetSignal(0, active=1, async=True)
    enable = Signal(bool(0))
    # Output Pins
    polypin = Signal(bool(0))
    laserpin = Signal(bool(0))
    photodiodepin = ResetSignal(0, active=1, async=True)
    clock = Signal(bool(0))
    # Modules
    polygen = polydriver(clock, photodiodepin, polypin, laserpin, enable, reset)
    # CLOCK
    HALF_PERIOD = delay(round(1/(2*xula_freq)*1e9))

    @always(HALF_PERIOD)
    def clkgen():
        clock.next = not clock

    @instance
    def stimulus():
        yield clock.negedge
        for i in range(10):
            count = round(PERIOD_DIODE)
            current = 0
            while current < count:
                yield clock.negedge
                current = current+1
            photodiodepin.next = 1
            yield clock.negedge
            yield clock.negedge
            yield clock.negedge
            photodiodepin.next = 0
        raise StopSimulation

    return instances()


if __name__ == '__main__':
    test_inst = testbench()
    test_inst.config_sim(trace=True)
    test_inst.run_sim()

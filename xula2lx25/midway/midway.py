# Author: Rik Starmans
# Company: Hexastorm

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

# PHOTODIODE
#
# NOTE:  IF YOUR CONSTANTS ARE OFF the systems behaves very irregular
# jumpers need to be on 5V-PWR and a jumper on GPIO-5V
# 8 bit shift works, light ends up at the "opposite" side, pixel is visible
# 9 bit shift works, light ends up at the opposite side
# 10 bit shift works, works
# 11 bit shift does not work 21khz, works 100khz
# 12 bit works @ 100khz
# Constants [used to simplify code]
PERIOD_POLYGON = round(xula_freq/poly_freq)
# bitshift of 12 also works
BIT_SHIFT = 7    # 8 bit works  --> LOWER LEADS to smaller end spot
COUNTER_MIN = 0  # --> higher did not produce better results
# Photodiode pin check
PERIOD_DIODE = round(xula_freq/(poly_freq/6*facets))
# Photodiode counting threshholds at 1 percent (count should be much closer)
LOW_DIODE = round(0.95*PERIOD_DIODE)
HIGH_DIODE = round(1.00001*PERIOD_DIODE)

# MIDDLE ON (for testing)
#  a violation of the bounds leads to errors
#  2090 works still space left between 90 and 10 bit shift hit
#  2080 works but a lot of space left
#  1060 does not work

# 50 -- 60 good @ andika's box 10-10
# 50 -- 90 good @ andika's box 10-10
# 30 -- 90 good @ andika's box 10-10
# 20 -- 90 

LOW_BOUND = round(0.2*PERIOD_DIODE)
UP_BOUND = round(0.9*PERIOD_DIODE)


@block
def polydriver(clock, photodiodepin, polypin, laserpin, enable, reset):
#    fail = Signal(intbv(0, min=0, max=10))
    counter = Signal(intbv(0, min=0, max=COUNTER_MIN+1))
    counter_polygon = Signal(intbv(0, min=0, max=PERIOD_POLYGON//2))
    counter_photodiode = Signal(intbv(0, min=0, max=round(HIGH_DIODE)))

    @always_seq(clock.posedge, reset)
    def polygen():
        if counter_polygon >= counter_polygon.max-1:
            counter_polygon.next = 0
            polypin.next = not polypin
        else:
            counter_polygon.next = counter_polygon+1

    @always_comb
    def switchlaser():
        if reset == 1:
            laserpin.next = 0
        # laser on in the middle (changed comparison not supported by myhdl)
        elif LOW_BOUND < counter_photodiode and (counter_photodiode < UP_BOUND
                                                 and enable):
            laserpin.next = 1
        # NOTE: THE LASER IS DETECTED AT THE START; polygon rotates clockwise
        # laser on at the edges, i.e. 99.6 percent
        # division implemented with bit shift and subtraction
        elif counter_photodiode >= PERIOD_DIODE-(PERIOD_DIODE >> BIT_SHIFT):
            laserpin.next = 1
        # laser off everywhere else
        else:
            laserpin.next = 0

    @always_seq(clock.posedge, reset)
    def count():
        if counter_photodiode >= counter_photodiode.max-1:
            counter_photodiode.next = 0
#        elif photodiodepin == 1 and fail >= 1:
#            counter_photodiode.next = 0
#            fail.next = fail-1
        elif photodiodepin == 1 and counter_photodiode > LOW_DIODE:
#            fail.next = 0
            counter.next = counter + 1
            counter_photodiode.next = counter_photodiode+1
            if counter > COUNTER_MIN:
                counter_photodiode.next = 0
                counter.next = 0
        #NOTE: not clear if this is wise
        #elif counter_photodiode > HIGH_DIODE:
        #    counter_photodiode.next = counter_photodiode-PERIOD_DIODE 
        #    counter.next = 0
#            if fail <= fail.max-1:
#                fail.next = fail+1
        else:
            counter_photodiode.next = counter_photodiode+1
            counter.next = 0
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

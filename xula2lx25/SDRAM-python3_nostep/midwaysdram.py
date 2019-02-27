# Author: Rik Starmans
# Company: Hexastorm
# Date: 3-3-2017

from myhdl import block, ResetSignal, instances
from myhdl import Signal, intbv, always, always_comb, always_seq
from sdram_cntl import sdram_cntl
from sdram import *
from host_intf import HostIntf
from sd_intf import SdramIntf

# Xula 2 board
xula_freq = 12e6

# Polygon
poly_freq = 400  # TEST 400
facets = 4

# Photodiode laser loop:
BIT_SHIFT = 7
COUNTER_MIN = 1

# Constants [used to simplify code]
PERIOD_POLYGON = round(xula_freq/poly_freq)
PERIOD_DIODE = round(xula_freq/(poly_freq/6*facets))
LINESPEED = round(xula_freq)  # --> you get 1 new line per second
LOW_DIODE = round(0.999*PERIOD_DIODE)
HIGH_DIODE = round(1.001*PERIOD_DIODE)
LOW_LASER = round(0.4*PERIOD_DIODE)

# BITWIDTH of polygon addres
# NOTE:  len(intbv(1000,min=0,max=1001)) == len(bin(1000))-2
laser_rate = 1E5
PIXELS = laser_rate//poly_freq  # NOTE NOT IDEAL
RESOLUTION = 10/PIXELS  # NOTE: INVALID, rought estimate
PIXELBITS = len(bin(PIXELS))-2
PIXELBITS = 8
# THE DATA WIDTH is 16
# THE ADDRESS WIDTH IS NOT WELL UNDERSTOOD
# UDARA uses 24 bits and notes SDRAM Side row + col + bank
# his datawidth is also 16 (i.e you agree)
#  data_width = 16 # SDRAM data width


@block
def polydriver(clock, reset, photodiodepin, polypin, laserpin, start,
               sdram_clk_o, sdram_clk_i, sd_intf):

    # NOTE: naming originates from udara

    host_intf = HostIntf()
    sdramCntl_inst = sdram_cntl(sdram_clk_i, host_intf, sd_intf)

    counter_facet = Signal(intbv(0, min=0, max=facets))
    counter_speed = Signal(intbv(0, min=0, max=LINESPEED))
    counter_line = Signal(intbv(0, min=0, max=1000))
    counter_polygon = Signal(intbv(0, min=0, max=PERIOD_POLYGON//2))
    counter_photodiode = Signal(intbv(0, min=0, max=round(HIGH_DIODE)))
    # Photodiode Laser loop
    # trigger is used to define exposure time photodiode, its not used
    counter_trigger = Signal(intbv(0, min=0, max=round(HIGH_DIODE)))
    value = Signal(intbv(0, min=0, max=round(HIGH_DIODE)))
    # TODO: +3 originates from https://github.com/xesscorp/
    #                          CAT-Board/blob/master/tests/sdram_test.py
    #       not clear why this is needed
    address = Signal(intbv(0)[len(host_intf.addr_i)+3:])
    memreset = Signal(bool(0))  # NOT USED
    wr_enable = Signal(bool(0))  # NOT USED
    rd_enable = Signal(bool(0))
    val = Signal(bool(0))  # NOT USED
    #
    laserpin_mem = Signal(bool(0))

    @always_comb
    def host_connections():
        host_intf.rst_i.next = memreset
        host_intf.wr_i.next = wr_enable and not host_intf.done_o
        host_intf.rd_i.next = rd_enable and not host_intf.done_o
        host_intf.data_i.next = val
        host_intf.addr_i.next = address

    @always_comb
    def clock_routing():
        sdram_clk_o.next = clock

    @always(sdram_clk_i.posedge)
    def sdram_reader():
        if start == 1:
            laserpin_mem.next = 0
        else:
            if host_intf.done_o == 0:
                rd_enable.next = True
            else:
                rd_enable.next = False
                address.next[PIXELBITS:0] = counter_photodiode[
                    len(counter_photodiode):(len(counter_photodiode)
                                             - PIXELBITS)]  # NOTE was 15
                # len(counter_line)=10
                address.next[(PIXELBITS+5):PIXELBITS] = counter_line
                address.next[27:(PIXELBITS+5)] = 0
                laserpin_mem.next = host_intf.data_o[0]

    @always(clock.posedge)
    def linecount():
        if reset == 1:
            counter_line.next = 0
        elif counter_speed >= counter_speed.max-1:
            counter_speed.next = 0
            if counter_line >= counter_line.max-1:
                counter_line.next = counter_line
            else:
                counter_line.next = counter_line+1
        else:
            counter_speed.next = counter_speed+1

    @always_seq(clock.posedge, reset)
    def polygen():
        if counter_polygon >= counter_polygon.max-1:
            counter_polygon.next = 0
            polypin.next = not polypin
        else:
            counter_polygon.next = counter_polygon+1

    @always_comb
    def switchlaser():  # NOTE: why use next in combitorial statement
        if reset == 1:
            laserpin.next = 0
        # SINGLE FACET: counter_facet == 0
        elif counter_photodiode < LOW_LASER:
            laserpin.next = 0
        elif counter_photodiode >= value-(value >> BIT_SHIFT):
            laserpin.next = 1
      #  elif counter_facet == 0:
      #      laserpin.next = laserpin_mem
      #  else:
      #      laserpin.next = 0
        else:
            laserpin.next = laserpin_mem

    @always_seq(clock.posedge, reset)
    def count():
        if counter_photodiode >= counter_photodiode.max-1:
            counter_photodiode.next = 0
            counter_trigger.next = 0
        elif photodiodepin == 1 and (counter_photodiode > LOW_DIODE
                                     and counter_photodiode < HIGH_DIODE):
            if counter_trigger > COUNTER_MIN:
                value.next = counter_photodiode-COUNTER_MIN
                counter_photodiode.next = 0
                counter_trigger.next = 0
                if counter_facet >= counter_facet.max-1:
                    counter_facet.next = 0
                else:
                    counter_facet.next = counter_facet+1
            else:
                counter_trigger.next = counter_trigger+1
                counter_photodiode.next = counter_photodiode+1
        else:
            counter_photodiode.next = counter_photodiode+1
            counter_trigger.next = 0
    return instances()


if __name__ == '__main__':
    print("Executing verilog conversion test")
    # previous examples
    clock = Signal(bool(0))
    reset = ResetSignal(bool(0), async=True, active=1)
    polypin = Signal(bool(0))
    photodiodepin = Signal(bool(0))
    laserpin = Signal(bool(0))
    # TODO: implement
    start, sdram_clk_o, sdram_clk_i = [Signal(bool(0)) for _ in range(3)]
    # NOTE: the following is also a placeholder
    sd_intf = SdramIntf()
    polydriver_inst = polydriver(clock, reset, photodiodepin, polypin,
                                 laserpin, start, sdram_clk_o, sdram_clk_i, sd_intf)
    polydriver_inst.convert(hdl='VHDL')

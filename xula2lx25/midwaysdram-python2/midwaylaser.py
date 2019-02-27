# Author: Rik Starmans
# Company: Hexastorm

from myhdl import *
from sdram_cntl import * # vanderbout uses different name
from sdram import *
from host_intf import *
from sd_intf import *

# Xula 2 board
xula_freq=12e6

# Polygon
poly_freq=1000
facets=4

# Constants [used to simplify code]
PERIOD_POLYGON=int(round(xula_freq/poly_freq))
PERIOD_DIODE=int(round(xula_freq/(poly_freq/6*facets)))
LINESPEED=int(round(xula_freq)) # --> you get 1 new line per second
LOW_DIODE=int(round(0.9*PERIOD_DIODE))
LOW_LASER=int(round(0.5*PERIOD_DIODE))

# THE DATA WIDTH is 16
# THE ADDRESS WIDTH IS NOT WELL UNDERSTOOD
# UDARA uses 24 bits and notes SDRAM Side row + col + bank
# his datawidth is also 16 (i.e you agree)
#  data_width = 16 # SDRAM data width


def polydriver(clock, reset, photodiodepin, polypin, laserpin, start, sdram_clk_o, sdram_clk_i,sd_intf):

    #NOTE: naming originates from udara
    
    host_intf = HostIntf()
    sdramCntl_inst = sdram_cntl(sdram_clk_i, host_intf, sd_intf)

    counter_speed=Signal(intbv(0,min=0, max=LINESPEED))
    counter_line=Signal(intbv(0, min=0, max=1000))
    counter_polygon = Signal(intbv(0, min=0, max=PERIOD_POLYGON//2))
    counter_photodiode=Signal(intbv(0, min=0, max=int(round(PERIOD_POLYGON*10))))
    # counter_value is not used, memory values are based on a precalculated value
    counter_value = Signal(intbv(0,min=0,max=round(PERIOD_POLYGON*10)))
    # TODO: +3 originates from https://github.com/xesscorp/CAT-Board/blob/master/tests/sdram_test.py
    #       not clear why this is needed
    address = Signal(intbv(0)[len(host_intf.addr_i)+3:]) 
    memreset = Signal(bool(0)) # NOT USED
    wr_enable = Signal(bool(0)) # NOT USED
    rd_enable = Signal(bool(0))
    val = Signal(bool(0)) # NOT USED
    # 
    laserpin_mem = Signal(bool(0))

    @always_comb
    def host_connections():
        host_intf.rst_i.next = memreset
        host_intf.wr_i.next= wr_enable and not host_intf.done_o
        host_intf.rd_i.next= rd_enable and not host_intf.done_o
        host_intf.data_i.next = val
        host_intf.addr_i.next = address
 
    @always_comb
    def clock_routing():
        sdram_clk_o.next = clock

    
    @always(sdram_clk_i.posedge)
    def sdram_reader():
        if start == 0:
             laserpin_mem.next=0
        else: 
            if host_intf.done_o == 0:
                rd_enable.next = True
            else:
                rd_enable.next = False
                #LENGTH IS 5 
                #LENGTH  len(intbv(PERIOD_DIODE,min=0,max=PERIOD_DIODE+1))=15
                address.next[5:0]=counter_photodiode[15:10]
                # len(counter_line)=10 
                address.next[15:5]=counter_line                 
                address.next[27:15]=0
                laserpin_mem.next=host_intf.data_o[0] 

    @always(clock.posedge)
    def linecount():
        if reset==1:
            counter_line.next=0
        elif counter_speed>=counter_speed.max-1:
             counter_speed.next=0
             if counter_line>=counter_line.max-1:
                 counter_line.next=counter_line 
             else:
                 counter_line.next=counter_line+1
        else:
             counter_speed.next=counter_speed+1


    @always_seq(clock.posedge,reset=reset)
    def polygen():
        if counter_polygon >= counter_polygon.max-1:
            counter_polygon.next=0
            polypin.next=not polypin
        else:
            counter_polygon.next=counter_polygon+1

    @always_comb
    def switchlaser():  #NOTE: why use next in combitorial statement
        if reset==1:
            laserpin.next=0
        elif counter_photodiode<LOW_LASER:
             laserpin.next=0        
        elif counter_photodiode >= counter_value-(counter_value>>10):
            laserpin.next=1
        else:
            laserpin.next= laserpin_mem

    @always_seq(clock.posedge, reset)
    def count():
        if photodiodepin==1 and counter_photodiode > LOW_DIODE:
            counter_value.next=counter_photodiode
            counter_photodiode.next=0
        elif counter_photodiode>=counter_photodiode.max-1:
            counter_photodiode.next=0
        else:
            counter_photodiode.next=counter_photodiode+1

    return instances()

if __name__ == '__main__':
    print("Executing verilog conversion test")
    # previous examples
    clock = Signal(bool(0))
    reset = ResetSignal(bool(0),async=True,active=1)
    polypin= Signal(bool(0))
    photodiodepin = Signal(bool(0))
    laserpin = Signal(bool(0))
    #TODO: implement
    start, sdram_clk_o, sdram_clk_i= [Signal(bool(0)) for _ in range(3)]
    # NOTE: the following is also a placeholder
    sd_intf = SdramIntf()
    toVHDL(polydriver,clock, reset, photodiodepin, polypin, laserpin, start, sdram_clk_o, sdram_clk_i,sd_intf)

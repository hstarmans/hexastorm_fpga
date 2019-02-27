from rhea.build.boards import get_board
from polylaserspin import polylaser

# use gxscon to get the pin assignments
# odd side is PM1, the other two are PM2 and PM3
# TODO: simplify pin assignmint

def build():
    # get the development board the design is targetting
    brd = get_board('xula2')

    # Set the ports for the design (top-level) and the
    # signal type for the ports.  If the port name matches
    # one of the FPGA default port names they do not need
    # to be remapped. 
    brd.add_port(name='polypin', pins=('B1',)) # i.e. D6 GR3
    brd.add_port(name='laserpin', pins=('F2',)) # i.e D2 GR2
    brd.add_reset('resetpoly',active=1,async=True,pins=('E1',)) # i.e. BCM 22
    brd.add_reset('resetlaser',active=1,async=True,pins=('C16',)) # i.e. BCM 23
    # assign the top-level HDL module (python function)
    # as the top-level
    flow=brd.get_flow(polylaser)
    flow.run()
    info = flow.get_utilization()
    print(info)

def main():
    # make sure you are linked to xtclsh
    build()


if __name__ == '__main__':
    main()

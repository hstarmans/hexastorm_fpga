from rhea.build.boards import get_board

from midway import polydriver

def build():
    # get the development board the design is targetting
    brd = get_board('xula2')

    # Set the ports for the design (top-level) and the
    # signal type for the ports.  If the port name matches
    # one of the FPGA default port names they do not need
    # to be remapped.
    brd.add_port(name='polypin', pins=('T4',)) # i.e. D0
    brd.add_port(name='laserpin', pins=('R1',)) # i.e. D2 on PM2
    brd.add_port(name='photodiodepin',pins=('J4',)) # i.e. D6 
    brd.add_reset('resetpoly',active=1,async=True,pins=('E1',)) # i.e. BCM 22
    brd.add_reset('resetlaser',active=1,async=True,pins=('C16',)) # i.e. BCM 23

    # assign the top-level HDL module (python function)
    # as the top-level
    flow=brd.get_flow(polydriver)
    flow.run()
    info = flow.get_utilization()
    print(info)

def main():
    # make sure you are linked to xtclsh
    build()


if __name__ == '__main__':
    main()

from rhea.build.boards import get_board
from polygonspin import polydriver

# use gxsconn to get the pin assignments
# odd side is PM1, the other two are PM2 and PM3


def build():
    # get the development board the design is targetting
    brd = get_board('xula2')

    # Set the ports for the design (top-level) and the
    # signal type for the ports.  If the port name matches
    # one of the FPGA default port names they do not need
    # to be remapped.
    brd.add_port(name='polypin', pins=('t7',)) # i.e. PM1 GR1-D1
    brd.add_reset('resetpoly',active=1,async=True,pins=('E1',)) # i.e. BCM 22
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

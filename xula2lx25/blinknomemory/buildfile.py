from rhea.build.boards import get_board

from ledblinker import strobe

def build():
    # get the development board the design is targetting
    brd = get_board('xula2')

    # Set the ports for the design (top-level) and the
    # signal type for the ports.  If the port name matches
    # one of the FPGA default port names they do not need
    # to be remapped.
    brd.add_port(name='led', pins=('T7',))

    # assign the top-level HDL module (python function)
    # as the top-level
    flow=brd.get_flow(strobe)
    flow.run()
    info = flow.get_utilization()
    pprint(info)

def main():
    # make sure you are linked to xtclsh
    build()


if __name__ == '__main__':
    main()

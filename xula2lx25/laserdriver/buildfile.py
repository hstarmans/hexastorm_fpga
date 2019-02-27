from rhea.build.boards import get_board

from laserdriver import laserdriver

def build():
    # get the development board the design is targetting
    brd = get_board('xula2')
    # chinese driver; PM3 GR2-D2 = F2
    # IC HAUS; M2 is pin6 using DEFAULT PMOD Numbers
    brd.add_port(name='laserpin', pins=('r16',)) #i.e.
    brd.add_reset('reset', active=1, async=True, pins=('E1',)) #i.e. BCM22
    #NOTE: TO measure the voltage level,
    #      look at the top of the board, the connections toward you
    #      stickit socket are bottem, photodiode pin is upper richt most
    #      connect ground via PMOD
    # assign the top-level HDL module (python function)
    # as the top-level
    flow=brd.get_flow(laserdriver)
    flow.run()
    info = flow.get_utilization()
    print(info)

def main():
    # make sure you are linked to xtclsh
    build()


if __name__ == '__main__':
    main()

from rhea.build.boards import get_board
from test_endstop import stepperdriver

# use gxsconn to get the pin assignments



def build():
    # get the development board the design is targetting
    brd = get_board('xula2')

    # Set the ports for the design (top-level) and the
    # signal type for the ports.  If the port name matches
    # one of the FPGA default port names they do not need
    # to be remapped.

    # XULA --> STEPPER
    brd.add_port(name='step_pino', pins=('e2',))                # D4, PM3
    brd.add_port(name='dir_pino', pins=('c1',))                 # D5, PM3
    # ENDSTOP --> XULA    
    brd.add_port(name='trigger_pini', pins=('h2',))             # D0, PM3
    # RASPBERRY --> XULA
    brd.add_reset('reset', active=1, async=True, pins=('E1',))  # BCM 22
    # XULA --> RASPBERRY
    brd.add_port(name='complete_pino', pins=('m16',))           # BCM 13
    # assign the top-level HDL module (python function)
    # as the top-level
    flow=brd.get_flow(stepperdriver)
    flow.run()
    info = flow.get_utilization()
    print(info)

def main():
    # make sure you are linked to xtclsh
    build()


if __name__ == '__main__':
    main()

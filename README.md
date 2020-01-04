# hexastorm_fpga
FPGA code used to calibrate the Hexastorm. The code is very dated. It was used for the first Hexastorm.
The code is not being maintained. I have decided to switch from MyHDL to Migen. The internal sram is used as ringbuffer.
Data is uploaded via SPI. The code can be here [here](https://github.com/hstarmans/migen_tests)

## HIGH LIGHTS
The following folders in the project;
* midway_sdram-python2; rotating polygon, laser detects starts facet via photodiode and reads data from SDRAM.
Data can be uploaded to the SDRAM with XSTOOL; which is provided by XESS.
* SDRAM-python3_nostep; same as above but python2 ported to python3

## LOW LIGHTS
* blinknomemory ; blinks the onboard xula led
* DAC_ADC; probably doesnt work, a failed attempt to add a DAC_ADC converter
* diodecollection; also forgot what it does
* midway; pulses the laser in the middle of facet using the feedback of a photodiode
* stepper driver; rotates a stepper driver

## Conclusion
It turned out that the Xula-LX25 was a great learning project but a hard board to build a machine around.
In the end, I switched to the Beaglebone. The Beaglebone does, however, not have the potential to reach the speeds of an FPGA.
A new project to build a FPGA controller is underway, first tests can be found [here](https://github.com/hstarmans/migen_tests).




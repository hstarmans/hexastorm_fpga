# hexastorm_fpga
FPGA code used to calibrate the Hexastorm. The code is very dated. It was used for the first Hexastorm.
The code is not being maintained.

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
In the future, I might therefore return to MyHDL. If I am going to do this, I still need to solve the following problems;
* current code is ugly (solvable)
* it is not possible to upload data to the sdram, only via XSTOOLS (challenge, no idea how to solve it)
* could I use a ring buffer like is done with the beaglebone?

## Advice
You can add a beaglewire to the beaglebone. The beaglewire uses the lattice so you can compile bitstreams via Linux.
As alternative to MyHDL you can try Migen. I guess the whole project would be very hard, hope this helps!




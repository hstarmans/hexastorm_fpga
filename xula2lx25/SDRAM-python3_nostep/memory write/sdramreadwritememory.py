import RPi.GPIO as GPIO
  2 from time import sleep
  3 
  4 from xstools.xsboard import XsBoard
  5 
  6 # PINS
  7 GPIO.setmode(GPIO.BCM)
  8 RESET=22 # RESET PIN
  9 START=23 # START PIN
 10 GPIO.setup(RESET,GPIO.OUT)
 11 GPIO.setup(START,GPIO.OUT)
 12 
 13 board=XsBoard.get_xsboard()
 14 
 15 #WRITE SDRAM
 16 print("Writing file to SDRAM")
 17 keys = range(0,50000*2+1)
 18 values = len(keys)*[255] # i.e 11111111
 19 data = IntelHex()
 20 data.fromdict(dict(zip(keys, values)))
 21 board.write_sdram(data,0,len(keys))
 22 print("RESET HIGH, START HIGH")
 23 GPIO.output(RESET,1)
 24 GPIO.output(START,1)
 25 print("Uploading bit stream")
 26 board.configure("sdram.bit")
 27 print("RESET LOW")
 28 GPIO.output(RESET,0)
 29 print("WAIT 10 seconds for board to get into calibration")
 30 sleep(10)
 31 print("START ILLUMINATION")
 32 GPIO.output(START,0)
 33 print("WAIT 30 SECONDS to finish illumination")
 34 sleep(30)
 35 print("STOPPING BOARD")
 36 GPIO.output(RESET,1)
 37 GPIO.output(START,1)


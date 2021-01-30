import sys
from machine import ADC, Pin, UART
import ustruct
import time

# Constants
ControlChange = 0xb0

# Devices
exp = machine.ADC(Pin(26)) # Expression pedal device on pin 31
uart = machine.UART(1, 31250) # UART Midi device on pin 6
led = machine.Pin(25, Pin.OUT) # Pico onboard led

# Midi settings
midi_channel = 1 # Target midi channel to write to
cc = 68 # Target Control Change number - this is for Behringer X32 Matrix 5
cc_min = 0 # Minimum desired CC output
cc_max = 97 # Maximum desired CC output (only want fader to go to unity gain - hence not 127)

# Initialise variables
# Set these to reverse thresholds to enable self calibration
exp_min = 65535 
exp_max = 0

cc_previous = 0

# This function translates the expression pedal value to the equivalent CC value
def translate(exp_val):
  if exp_max - exp_min > 40000:
    ret = int((((exp_val - exp_min) * (cc_max - cc_min)) / (exp_max - exp_min)) + cc_min)
  else:
    return 0

  if ret > 0:
    return ret
  else:
    return 0

while True:
  exp_current = exp.read_u16()
  cc_current = translate(exp_current)
  if exp_current > exp_max:
    exp_max = exp_current
  elif exp_current < exp_min:
    exp_min = exp_current

  if cc_current != cc_previous:
    led.value(1) # Turn led on
    uart.write(ustruct.pack("bbb",ControlChange + midi_channel - 1,cc,cc_current))
    led.value(0) # Turn led off
    cc_previous = cc_current
    print("Writing Midi Channel: {}, ControlChange: {}, Value {}. Exp Pedal: cur: {}, min: {}, max: {}".format(midi_channel, cc, cc_current, exp_current, exp_min, exp_max))
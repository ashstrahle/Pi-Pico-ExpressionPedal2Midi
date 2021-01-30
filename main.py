import sys
from machine import ADC, Pin, UART
import ustruct
import time

# Constants
ControlChange = 0xb0

# Midi settings
midi_channel = 1 # Target midi channel to write to
cc = 68 # Target Control Change number - this is for Behringer X32 Matrix 5
cc_min = 0 # Minimum desired CC output
cc_max = 97 # Maximum desired CC output (only want fader to go to unity gain - hence not 127)

exp_calibration_threshold = 40000 # This is the minimum amount of change required successful for calibration

# Devices
exp = machine.ADC(Pin(26)) # Expression pedal device on pin 31
uart = machine.UART(1, 31250) # UART Midi device on pin 6
led = machine.Pin(25, Pin.OUT) # Pico onboard led

# Initialise variables
# Set these to reverse thresholds to enable self calibration
exp_min = 65535 
exp_max = 1

# This function translates the expression pedal value to the equivalent CC value
def translate(exp_val):
  ret = int((((exp_val - exp_min) * (cc_max - cc_min)) / (exp_max - exp_min)) + cc_min)
  if ret > 0:
    return ret
  else:
    return 0

exp_previous = exp.read_u16()
while True:
  exp_current = exp.read_u16()

  # Only process if the change ratio is greater than the possible number of CC values
  if abs(exp_current - exp_previous)/exp_max > 1/(cc_max - cc_min): 
    if exp_current > exp_max:
      exp_max = exp_current
    elif exp_current < exp_min:
      exp_min = exp_current
    exp_previous = exp_current

    # Only send midi when calibration threshold has been reached
    if exp_max - exp_min > exp_calibration_threshold: 
      cc_val = translate(exp_current)
      led.value(1) # Turn led on
      uart.write(ustruct.pack("bbb",ControlChange + midi_channel - 1,cc,cc_val))
      led.value(0) # Turn led off
      print("Writing Midi Channel: {}, ControlChange: {}, Value {}. Exp Pedal: cur: {}, min: {}, max: {}".format(midi_channel, cc, cc_val, exp_current, exp_min, exp_max))
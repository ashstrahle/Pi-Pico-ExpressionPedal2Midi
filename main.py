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

# Expression pedal maximum and minimum
# Set these to reverse thresholds
exp_min = 65535 
exp_max = 0

# Midi settings
midi_channel = 1 # Target midi channel to write to
cc = 68 # Target Control Change number - this is for Behringer X32 Matrix 5
cc_min = 0 # Minimum desired CC output
cc_max = 97 # Maximum desired CC output (only want fader to go to unity gain - hence not 127)

# This function translates the expression pedal value to the equivalent CC value
def translate(exp_val):
  ret = int((((exp_val - exp_min) * (cc_max - cc_min)) / (exp_max - exp_min)) + cc_min)
  if ret > 0:
    return ret
  else:
    return 0
  # return int((((exp_val - exp_min) * (cc_max - cc_min)) / (exp_max - exp_min)) + cc_min)

exp_previous = 0

while True:
  exp_current = exp.read_u16()
  if exp_current > exp_max:
    exp_max = exp_current
  elif exp_current < exp_min:
    exp_min = exp_current

  if exp_current != exp_previous and exp_max - exp_min > 40000:
    led.value(1) # Turn led on
    cc_val = translate(exp_current)
    uart.write(ustruct.pack("bbb",ControlChange + midi_channel - 1,cc,cc_val))
    led.value(0) # Turn led off
    exp_previous = exp_current
    print("Writing Midi Channel: {}, ControlChange: {}, Value {}. Exp Pedal: cur: {}, min: {}, max: {}".format(midi_channel, cc, cc_val, exp_current, exp_min, exp_max))
    time.sleep(0.05)
from machine import ADC, Pin
import midi

# Devices
exp = machine.ADC(31) # Expression pedal device on pin 31
serial = pyb.USB_VCP()
led = Pin(25, Pin.OUT)

# Expression pedal settings
exp_min = 0 # Expression pedal minimum value
exp_max = 65535 #Expression pedal maximum value

# Midi settings
midi_channel = 1 # Target midi channel to write to
cc = 68 # Target Control Change number - this is for Behringer X32 Matrix 5
cc_min = 0 # Minimum desired CC output
cc_max = 100 # Maximum desired CC output (only want fader to go to unity gain - hence not 127)

# This function translates the expression pedal value to the equivalent CC value
def translate(exp_val):
  return (((exp_val - exp_min) * (cc_max - cc_min)) / (exp_max - exp_min)) + cc_min

# Test the translate function:
# for i in range(65535):
#   print (translate(i))

usb_midi = midi.Controller(serial, channel=midi_channel)
exp_value_previous = 0

while True:
  exp_value_current = exp.read_u16()
  if exp_value_current != exp_value_previous:
    led.value(1) # Turn led on
    cc_val = translate(exp_value_current)
    usb_midi.control_change(cc, cc_val)
    led.value(0) # Turn led off
    exp_value_previous = exp_value_current
    print("Writing CC value " + cc_val)
import usb_midi
import adafruit_midi
from adafruit_midi.control_change import ControlChange
import digitalio
import analogio
# import busio
import board
import time

# Devices
exp = analogio.AnalogIn(board.A0) # Expression pedal
led = digitalio.DigitalInOut(board.LED)

# led = Pin(25, Pin.OUT)

# Expression pedal settings
exp_min = 0 # Expression pedal minimum value
exp_max = 65535 #Expression pedal maximum value

# Midi settings
midi_channel = 0 # Target midi channel to write to
cc = 68 # Target Control Change number - this is for Behringer X32 Matrix 5
cc_min = 0 # Minimum desired CC output
cc_max = 100 # Maximum desired CC output (only want fader to go to unity gain - hence not 127)

# This function translates the expression pedal value to the equivalent CC value
def translate(exp_val):
  return int((((exp_val - exp_min) * (cc_max - cc_min)) / (exp_max - exp_min)) + cc_min)

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=midi_channel)


# uart = busio.UART(board.GP4, board.GP5, baudrate=31250)
# midi = adafruit_midi.MIDI(midi_out=uart, out_channel=midi_channel)

cc_val_last = 0

led.switch_to_output(value=True)
while True:
  # cc_val = translate(exp.value)
  # if cc_val != cc_val_last:
  #   led.switch_to_output(value=False) # Flicker led
  #   midi.send(ControlChange(cc, cc_val)) # Write midi
  #   led.switch_to_output(value=True)
  #   cc_val_last = cc_val
  for i in range(100):
    led.switch_to_output(value=True)
    midi.send(ControlChange(cc, i))
    led.switch_to_output(value=False)
    time.sleep(0.05)
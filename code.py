################################################################################
#
# Pi-Pico-ExpressionPedal2Midi
#
# using USB midi. Midi messages are sent simultaneoulsy to UART1 and USB.
# Set desired midi channel, change control, and maximum and minimum values
#
# Upon run/power on, move expresson pedal from maximum to minimum to calibrate
# your pedal. CC commands will immediately start sending once calibrated.
#
# Ashley Strahle
# https://github.com/ashstrahle
#
################################################################################

import sys
import struct
import time
import board
import busio
import analogio
import digitalio
import math
import usb_midi
import adafruit_midi
from adafruit_midi.timing_clock import TimingClock
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.pitch_bend import PitchBend
from adafruit_midi.control_change import ControlChange

# Midi output settings
midi_channel = 1  # Target midi channel to write to
cc = 1  # Target Control Change number - Expression Pedal
cc_min = 0  # Minimum desired CC output - 0 - 127
cc_max = 127  # Maximum desired CC output - 0 - 127

# Expression pedal settings
logarithmic = True  # Expression pedal logarithmic or linear. Set to False for linear
log_base = 100  # This value changes the feel of the log curve

# Required percentage of expression pedal movement for calibration
exp_pedal_calibration_percent = 80 # 0 - 100

# Devices
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
exp = analogio.AnalogIn(board.GP26)  # Expression pedal device on pin 31
uart = busio.UART(tx=board.GP4, rx=board.GP5, baudrate=31250, timeout=0.001)  # UART Midi device on pin 6
uart_midi = adafruit_midi.MIDI(midi_out=uart, out_channel=midi_channel - 1)
usb_midi = adafruit_midi.MIDI(
	midi_out=usb_midi.ports[1], out_channel=midi_channel - 1)

# This function translates the expression pedal value to the equivalent CC value
def translate(exp_val):
    if logarithmic:
	    scaled_val = math.log(exp_val, log_base)  # Apply logarithmic scaling
	    return int((((scaled_val - math.log(exp_min, log_base)) * (cc_max - cc_min)) / (math.log(exp_max, log_base) - math.log(exp_min, log_base))) + cc_min)
    else:
	    return int((((exp_val - exp_min) * (cc_max - cc_min)) / (exp_max - exp_min)) + cc_min)

# Initialise variables
offset = 1e-6  # Small offset to avoid log(0) error

# Set these to reverse thresholds to enable calibration
exp_min = 65535
exp_max = offset

exp_calibration_threshold = int(abs(exp_max - exp_min) * exp_pedal_calibration_percent / 100)
cc_ratio = 1/(cc_max - cc_min)  # Calculate number of possible CC values
exp_previous = exp.value

if exp_previous == 0:
    exp_previous = offset

# main loop
while True:
    exp_current = exp.value
    if exp_current == 0:
        exp_current = offset

    # Only process if the change ratio is greater than the possible number of CC values
    if abs(exp_current - exp_previous) / exp_max > cc_ratio:
        if exp_current > exp_max:
            exp_max = exp_current
        elif exp_current < exp_min:
            exp_min = exp_current
        exp_previous = exp_current

        # Only send midi when calibration threshold has been reached
        if exp_max - exp_min > exp_calibration_threshold:
            led.value = True  # Turn led on
            cc_val = translate(exp_current)
            uart_midi.send(ControlChange(cc, cc_val))
            usb_midi.send(ControlChange(cc, cc_val))
            led.value = False  # Turn led off
            print("Writing Midi Channel: {}, ControlChange: {}, Value {}. Exp Pedal: cur: {}, min: {}, max: {}".format(
                midi_channel, cc, cc_val, exp_current, exp_min, exp_max))
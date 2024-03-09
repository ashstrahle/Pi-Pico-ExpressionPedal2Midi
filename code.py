################################################################################
#
# Pi-Pico-ExpressionPedal2Midi (Multiple Pedals)
#
# Using USB midi. Midi messages are sent simultaneoulsy to UART1 and USB.
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

# Expression pedal settings
logarithmic = True  # Expression pedal logarithmic or linear. Set to False for linear
log_base = 100  # This value changes the feel of the log curve

# Required percentage of expression pedal movement for calibration
exp_pedal_calibration_percent = 80  # 0 - 100

# Define expression pedals
expression_pedals = [
    # Set expression pedal midi control change number, and min/max values
    {"pin": board.GP26, "midi_channel": 1, "cc": 1, "cc_min": 0, "cc_max": 127}, # Pedal 1. Pin 31
    {"pin": board.GP27, "midi_channel": 1, "cc": 2, "cc_min": 0, "cc_max": 127}, # Pedal 2. Pin 32
    {"pin": board.GP28, "midi_channel": 1, "cc": 3, "cc_min": 0, "cc_max": 127}  # Peadl 3. Pin 34
]

# Devices
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
uart = busio.UART(tx=board.GP4, rx=board.GP5, baudrate=31250, timeout=0.001)  # UART Midi device on pin 6
uart_midi = [adafruit_midi.MIDI(midi_out=uart, out_channel=pedal["midi_channel"] - 1) for pedal in expression_pedals]
usb_midi = [adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=pedal["midi_channel"] - 1) for pedal in expression_pedals]
# Initialize expression pedals
exp_values = [analogio.AnalogIn(pedal["pin"]) for pedal in expression_pedals]
exp_previous = [exp.value for exp in exp_values]
exp_min = [65535 for _ in expression_pedals]
exp_max = [1e-6 for _ in expression_pedals]
exp_calibration_threshold = [int(abs(exp_max[i] - exp_min[i]) * exp_pedal_calibration_percent / 100) for i in range(len(expression_pedals))]

# This function translates the expression pedal value to the equivalent CC value
def translate(exp_val, exp_min, exp_max, cc_min, cc_max):
    if logarithmic:
        scaled_val = math.log(exp_val, log_base)  # Apply logarithmic scaling
        return int((((scaled_val - math.log(exp_min, log_base)) * (cc_max - cc_min)) / (math.log(exp_max, log_base) - math.log(exp_min, log_base))) + cc_min)
    else:
        return int((((exp_val - exp_min) * (cc_max - cc_min)) / (exp_max - exp_min)) + cc_min)

# Main loop
while True:
    for i, exp in enumerate(exp_values):
        exp_current = exp.value
        if exp_current == 0:
            exp_current = 1e-6  # Small offset to avoid log(0) error

        # Only process if the change ratio is greater than the possible number of CC values
        if abs(exp_current - exp_previous[i]) / exp_max[i] > 1/(expression_pedals[i]["cc_max"] - expression_pedals[i]["cc_min"]):
            if exp_current > exp_max[i]:
                exp_max[i] = exp_current
            elif exp_current < exp_min[i]:
                exp_min[i] = exp_current
            exp_previous[i] = exp_current

            # Only send midi when calibration threshold has been reached
            if exp_max[i] - exp_min[i] > exp_calibration_threshold[i]:
                led.value = True  # Turn led on
                cc_val = translate(exp_current, exp_min[i], exp_max[i], expression_pedals[i]["cc_min"], expression_pedals[i]["cc_max"])
                uart_midi[i].send(ControlChange(expression_pedals[i]["cc"], cc_val))
                usb_midi[i].send(ControlChange(expression_pedals[i]["cc"], cc_val))
                led.value = False  # Turn led off
                print("Pedal {}: Writing Midi Channel: {}, ControlChange: {}, Value {}. Exp Pedal: cur: {}, min: {}, max: {}".format(
                    i + 1, expression.pedals[i]["midi_channel"], expression_pedals[i]["cc"], cc_val, exp_current, exp_min[i], exp_max[i]))

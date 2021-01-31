# Pi-Pico-ExpressionPedal2Midi

![](/docs/Pi-Pico-ExpressionPedal2Midi.gif)

![](/docs/Pi-Pico-ExpressionPedal2Midi2.jpeg)

This is a Raspberry Pi Pico MicroPython project that takes an expression pedal input via a TRS 1/4" jack connected to ADC pins on the Pico, and outputs respective Midi CC messages via UART.

Midi channel, CC number, and maximum and minimum values are customisable.

The expression pedal is automatically calibrated. At startup, simply move your pedal from minimum to maximum. The values are determined accordingly, and CC messages will start being sent.

## Recipe

Ingredients:

- Raspberry Pi Pico (loaded with MicroPython)
- ¼” jack TRS socket
- 5 pin DIN midi socket
- 10Ω resistor
- 33Ω resistor

Optional: breadboard, 40 pin male headers, pin cables, scotch

Power source:
Either USB or 3xAA battery holder

## Method

1. Load your Pico board with main.py
2. Customise the midi settings in the main.py file accordingly. Season to taste
3. Upload to your board using Thonny, or your favorite IDE.

Now for the stuffing:

### Midi port

![](/docs/Pi-Pico-ExpressionPedal2Midi4.jpeg)

Midi messages are sent via UART1. Here’s where we need the resistors to protect the board and your midi device. 

4. Connect a 10Ω resistor to pin 6 on the Pico (UART1 TX). T’other end of the resistor to pin 4 of your midi socket
5. Connect a 33Ω resistor to pin 36 on the Pico (3V3 OUT). T’other end of the resistor to pin 5 of your midi socket
6. Connect a Pico ground pin (any of 3, 8, 13, 18, 23, 28, or 33) to pin 2 of your midi socket

You’re done here, next…

### Expression pedal jack

![](/docs/Pi-Pico-ExpressionPedal2Midi3.jpeg)

The expression pedal is connected to ADC0 on the Pico.

7. Connect the jack sleeve to Pico ground pin (any or 3, 8, 13, 18, 23, 28, or 33)
8. Connect the jack ring to Pico pin 36 (ADC0)
9. Connect the jack tip to Pico pin 31 (3V3 OUT)

Jubilations, you’re done.

![](/docs/Pi-Pico-ExpressionPedal2Midi1.jpeg)

Ashley Strahle

https://github.com/ashstrahle

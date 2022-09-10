# [Pi-Pico-ExpressionPedal2Midi](https://github.com/ashstrahle/Pi-Pico-ExpressionPedal2Midi) now with added USB

![](/docs/Pi-Pico-ExpressionPedal2Midi.gif)

![](/docs/Pi-Pico-ExpressionPedal2Midi2.jpeg)

This is a Raspberry Pi Pico CircuitPython project that takes an expression pedal input via a TRS 1/4" jack connected to ADC pins on the Pico, and outputs respective Midi CC messages simultaneously to UART and USB.

Midi channel, CC number, and maximum and minimum values are customisable.

The expression pedal is automatically calibrated. At startup, simply move your pedal from minimum to maximum. The values are determined accordingly, and CC messages will start being sent.

## Recipe

### Ingredients

- Raspberry Pi Pico (loaded with MicroPython)
- ¼” jack TRS socket
- 5 pin DIN midi socket<sup>1</sup>
- 10Ω resistor<sup>1</sup>
- 33Ω resistor<sup>1</sup>

<sup>1</sup> Required only if using midi port (non-usb)

Optional: breadboard, 40 pin male headers, pin cables, scotch whisky

Power source:
Either USB or 3xAA battery holder

### Method

1. Download [CircuitPython](https://circuitpython.org/board/raspberry_pi_pico/) and install on your Pico.
2. Download [CircuitPython Libraries](https://circuitpython.org/libraries) and copy ```adafruit_midi``` folder to ```lib``` folder on your Pico.
3. Customise the midi settings in ```code.py```. Season to taste
4. Copy ```code.py``` to your Pico.

<i>Now for the stuffing:</i>

#### Expression Pedal Jack

![](/docs/Pi-Pico-ExpressionPedal2Midi3.jpeg)

The expression pedal is connected to ADC0 on the Pico.

5. Connect the jack sleeve to Pico ground pin (any of 3, 8, 13, 18, 23, 28, or 33)
6. Connect the jack ring to Pico pin 31 (ADC0)
7. Connect the jack tip to Pico pin 36 (3V3 OUT)

If you're only using USB, you're done! 

<i>Otherwise...</i>
#### Midi Port

![](/docs/Pi-Pico-ExpressionPedal2Midi4.jpeg)

Midi messages are sent simultaneously to USB and UART1. If you wish to connect your Pico to a Midi port, proeceed with the following.

8. Connect a 10Ω resistor to pin 6 on the Pico (UART1 TX). T’other end of the resistor to pin 4 of your midi socket
9. Connect a 33Ω resistor to pin 36 on the Pico (3V3 OUT). T’other end of the resistor to pin 5 of your midi socket
10. Connect a Pico ground pin (any of 3, 8, 13, 18, 23, 28, or 33) to pin 2 of your midi socket

Jubilations, you’re done.

![](/docs/Pi-Pico-ExpressionPedal2Midi1.jpeg)

![](/docs/Pi-Pico-ExpressionPedal2Midi5.jpeg)

![](/docs/Pi-Pico-ExpressionPedal2Midi6.jpeg)


Ashley Strahle

https://github.com/ashstrahle

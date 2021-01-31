# Pi-Pico-ExpressionPedal2Midi

![](/docs/Pi-Pico-ExpressionPedal2Midi.gif)

This is a Raspberry Pi Pico MicroPython project that takes an expression pedal input via a TRS 1/4" jack connected to ADC pins on the Pico, and outputs respective Midi CC messages via UART.

Midi channel, CC number, and maximum and minimum values are customisable.

The expression pedal is automatically calibrated. At startup, simply move your pedal from minimum to maximum. The values are determined accordingly, and CC messages will start being sent.

Ashley Strahle

https://github.com/ashstrahle


![](/docs/Pi-Pico-ExpressionPedal2Midi1.jpeg)
![](/docs/Pi-Pico-ExpressionPedal2Midi2.jpeg)
![](/docs/Pi-Pico-ExpressionPedal2Midi3.jpeg)
![](/docs/Pi-Pico-ExpressionPedal2Midi4.jpeg)

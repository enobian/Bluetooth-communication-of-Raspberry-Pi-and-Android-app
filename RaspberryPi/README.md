# Bluetooth SPP (Server) - Raspberry Pi

- Reads 8 GPIO pins to get 8bit value from ADC0804LCN output pins.
- Hosts Bluetooth SPP server end
- Detects if device is connected/disconnected and sends voltage value in ADC0804LCN input pins upon request.

Based on PyBluez Bluetooth Python extension module and example code: RFCOMM-server.py
Available here: https://github.com/karulis/pybluez

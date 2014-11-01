#!/usr/bin/env python

import serial


class Arduino(object):

    __OUTPUT_PINS = -1

    def __init__(self, port="/dev/ttyUSB0", baudrate=115200):
        self.port = port
        self.serial = serial.Serial(self.port, baudrate)
        serial.Serial()
        self.serial.write('99')

    def __str__(self):
        return "Arduino is on port {0} at {1} baud rate".format(self.serial.port, self.serial.baudrate)

    def output(self, pin_array):
        self.__send_data(len(pin_array))

        if isinstance(pin_array, list) or isinstance(pin_array, tuple):
            self.__OUTPUT_PINS = pin_array
            for each_pin in pin_array:
                self.__send_data(each_pin)
        return True

    def set_low(self, pin):
        """Set digital low"""
        self.__send_data('0')
        self.__send_data(pin)
        return True

    def set_high(self, pin):
        """Set digital high"""
        self.__send_data('1')
        self.__send_data(pin)
        return True

    def get_state(self, pin):
        """Get digital value"""
        self.__send_data('2')
        self.__send_data(pin)
        return self.__format_pin_state(self.__get_data()[0])

    def analog_write(self, pin, value):
        """Set analog value"""
        self.__send_data('3')
        self.__send_data(pin)
        self.__send_data(value)
        return True

    def analog_read(self, pin):
        """Get analog value"""
        self.__send_data('4')
        self.__send_data(pin)
        return self.__get_data()

    def turn_off(self):
        for each_pin in self.__OUTPUT_PINS:
            self.set_low(each_pin)
        return True

    def __send_data(self, serial_data):
        while self.__get_data()[0] != "w":
            pass
        self.serial.write(str(serial_data))

    def __get_data(self):
        return self.serial.readline().rstrip('\n')

    def __format_pin_state(self, pin_value):
        if pin_value == '1':
            return True
        else:
            return False

    def close(self):
        self.serial.close()
        return True


if __name__ == "__main__":
    import time
    port = "/dev/ttyUSB0"
    baudrate = 115200
    arduino = Arduino(port, baudrate)
    while 1:
        status = arduino.set_high(13)
        print("High: " + str(status))
        time.sleep(5)
        status = arduino.set_low(13)
        print("Low: " + str(status))
        time.sleep(5)

from machine import Pin
from time import sleep_ms
from onewire import DS18B20, OneWire


class DS18B_20():
    def __init__(self, PIN_DS18B20):

        self.statusRead = False
        # the device is on GPIO12
        self.dat = Pin(PIN_DS18B20)
        # create the onewire object
        self.ds = DS18B20(OneWire(self.dat))

    def DS18B20_Scan(self):# scan for devices on the bus
        self.roms = self.ds.scan()
        print('found devices:', self.roms)

    # loop 10 times and print all temperatures
    def getDS18B20(self):
        for i in range(10):
            print('temperatures:', end=' ')
            self.ds.convert_temp()
            sleep_ms(750)
            for rom in self.roms:
                print(self.ds.read_temp(rom), end=' ')
            print()

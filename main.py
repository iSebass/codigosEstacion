from machine import Pin, ADC, I2C
from time import sleep
from kit_sensores import *
from SEN0500 import *

PIN_WIND_DIRECTION = 34
PIN_ANEMOMETER     = 35
PIN_PLUVIOMETER    = 25


SDA_PIN            = 21
SCL_PIN            = 22
ADDRESS            = 0x22  
I2C_1              = 0x01
HPA                = 0x01
KPA                = 0x02
TEMP_C             = 0x03
TEMP_F             = 0x04


SCL_PIN = Pin(SCL_PIN, pull = Pin.PULL_UP, mode=Pin.OPEN_DRAIN)
SDA_PIN = Pin(SDA_PIN, pull = Pin.PULL_UP, mode=Pin.OPEN_DRAIN)
i2c_bus = I2C(0, scl=SCL_PIN, sda=SDA_PIN, freq=100000)


def run():
    #windS = Sensor_Kit(35)
    kitSensor          = SensorKit(PIN_WIND_DIRECTION,PIN_ANEMOMETER, PIN_PLUVIOMETER)
    SEN0500Device      = SEN0500_Sensor( bus=i2c_bus )
    
    while (SEN0500Device.begin() == False):
        print("Sensor initialize failed!!")
        sleep(1)
    print("Sensor  initialize success!!")
    while True:
            temp_C_SEN0500            = SEN0500Device.get_temperature(TEMP_C)
            temp_F_SEN0500            = SEN0500Device.get_temperature(TEMP_F)
            humidity_SEN0500          = SEN0500Device.get_humidity()
            ultraviolet_SEN0500       = SEN0500Device.get_ultraviolet_intensity()
            luminousintensity_SEN0500 = SEN0500Device.get_luminousintensity()
            atmosphere_HPA_SEN0500    = SEN0500Device.get_atmosphere_pressure(HPA)
            atmosphere_KPA_SEN0500    = SEN0500Device.get_atmosphere_pressure(KPA)
            elevation_SEN0500         = SEN0500Device.get_elevation()
            
            kitSensor.getAnemometerValue()
            kitSensor.getPluviometerValue()

            print("Temp °C: "+str(temp_C_SEN0500) )
            print("Temp °F: "+str(temp_F_SEN0500) )
            print("Humidity: "+str(humidity_SEN0500) )
            print("Ultraviolet: "+str(ultraviolet_SEN0500) )
            print("Luminousity: "+str(luminousintensity_SEN0500) )
            print("Atmosphere HPA: "+str(atmosphere_HPA_SEN0500) )
            print("Atmosphere KPA: "+str(atmosphere_KPA_SEN0500) )
            print("Elevation: "+str(elevation_SEN0500) )
            
            print(" ")
            print(" ")
            print(" ")
            print(" ")
            
            sleep(1)
        

if __name__ == "__main__":
    run()
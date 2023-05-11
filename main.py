from machine import Pin, ADC, I2C
from time import sleep
from kit_sensores import *
from SEN0500 import *
from ESP_CONNECTION import *
from DS3231 import *
import machine
import network
from umqtt.simple import MQTTClient




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


mqtt_broker = "62.171.140.128"
mqtt_topic = "variablesMeteorologicas"
mqtt_client_id = "esp32_client_uceva"

def sendInfluxDB(varType, location, value ):
    global client
    # Configuración de InfluxDB
    influxdb_measurement = varType  
    influxdb_tags        = "location="+location  
    influxdb_field       = "value"  
    temperature          = value
    topic                = varType  
    payload = "{},{} {}={}".format(influxdb_measurement, influxdb_tags, influxdb_field, temperature)
    client.publish(topic, payload)

def callback(topic, msg):
    print("Mensaje recibido en el tema: {}, Mensaje: {}".format(topic, msg))



def run():
    global client
    kitSensor          = SensorKit(PIN_WIND_DIRECTION,PIN_ANEMOMETER, PIN_PLUVIOMETER)
    rtc                = DS3231(bus = i2c_bus)
    SEN0500Device      = SEN0500_Sensor( bus=i2c_bus )
    wifi               = ESP32_CONNECTION()
    if wifi.status():
        print("ya esta conectado siii")
    else:
        status_wifi        =  wifi.connect()
    
    client = MQTTClient(client_id=mqtt_client_id, server=mqtt_broker)
    
    #client.setSSID_PASSW("SSID","PASSWORD")
    client.connect()
    
    client.set_callback(callback)
    client.subscribe(mqtt_topic)
    
    
    while (SEN0500Device.begin() == False):
        print("Sensor initialize failed!!")
        sleep(1)
    print("Sensor  initialize success!!")

    while True:
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        temp_C_SEN0500            = SEN0500Device.get_temperature(TEMP_C)
        temp_F_SEN0500            = SEN0500Device.get_temperature(TEMP_F)
        humidity_SEN0500          = SEN0500Device.get_humidity()
        ultraviolet_SEN0500       = SEN0500Device.get_ultraviolet_intensity()
        luminousintensity_SEN0500 = SEN0500Device.get_luminousintensity()
        atmosphere_HPA_SEN0500    = SEN0500Device.get_atmosphere_pressure(HPA)
        atmosphere_KPA_SEN0500    = SEN0500Device.get_atmosphere_pressure(KPA)
        elevation_SEN0500         = SEN0500Device.get_elevation()

        anemometer                = kitSensor.getAnemometerValue()
        pluviometer               = kitSensor.getPluviometerValue()
        wind_dir                  = kitSensor.getWindDir()
        
        print("Temp °C: "+str(temp_C_SEN0500) )
        print("Temp °F: "+str(temp_F_SEN0500) )
        print("Humidity: "+str(humidity_SEN0500) )
        print("Ultraviolet: "+str(ultraviolet_SEN0500) )
        print("Luminousity: "+str(luminousintensity_SEN0500) )
        print("Atmosphere HPA: "+str(atmosphere_HPA_SEN0500) )
        print("Atmosphere KPA: "+str(atmosphere_KPA_SEN0500) )
        print("Elevation: "+str(elevation_SEN0500) )
        
        print( str( rtc.getHour() ) +":"+str( rtc.getMinutes() )+":"+str( rtc.getSeconds() ) )

        print( str(rtc.getYear() )+"/"+str(rtc.getMonth() )+"/"+str(rtc.getDay() )  )
        
        sendInfluxDB("Temp", "UCEVA", str(temp_C_SEN0500) )
        sendInfluxDB("Humidity", "UCEVA", str(humidity_SEN0500) )
        sendInfluxDB("Ultraviolet", "UCEVA", str(ultraviolet_SEN0500) )
        sendInfluxDB("Luminousity", "UCEVA", str(luminousintensity_SEN0500) )
        sendInfluxDB("Atmosphere", "UCEVA", str(atmosphere_HPA_SEN0500) )
        
        #client.check_msg()
        sleep(1)
        
        
                    

if __name__ == "__main__":
    run()

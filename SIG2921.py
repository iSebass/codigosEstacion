from machine import UART, Pin, ADC, Timer
import time


global PinSoilTemp



class Environmental_sensors():
    
    def __init__(self, PINSOILTEMP):
        global PinSoilTemp
        
        self.SoilTemp = ADC(Pin(PINSOILTEMP))
        self.SoilTemp.atten(ADC.ATTN_11DB)
    
    def getSoilTemperature(self):
        SoilTemperature = self.SoilTemp.read()
        
        SoilTemperature = 100.0 - (SoilTemperature * 100.0 /4096.0)
        
        txtStatusSoilTemp =''
        
        if SoilTemperature<30.0:
            txtStatusSoilTemp='Suelo Seco'
        elif SoilTemperature >=30.0 and SoilTemperature<=68.0:
            txtStatusSoilTemp='Suelo Humedo'
        elif SoilTemperature >68.0:
            txtStatusSoilTemp='Suelo muy Humedo'
            
        
        print("Temp Suelo: "+str(SoilTemperature)+ ' %Humedad --> ' + txtStatusSoilTemp )
        
        return SoilTemperature

from machine import UART, Pin, ADC, Timer
import time

'''
    Para trabajar el sensor de direccion del viento se utilizo un potenciometro
    establecido en 20.4K Ohms, se debe reajustar al momento de instalar un trimmer
    o una resistencia de precision.
'''

global windSensor, windCurrentPosition, listCardinalPos
global count_wind,count_pluviometer,tSample, windSpeed, statusCountPluv

#Count es una variable para medir las vueltas que ha dado el anemometro en unidad de tiempo
count_wind        = 0
count_pluviometer = 0

tSample           = 1000

windSpeed         = 0
pluviometerValue  = 0


listCardinalPos = {1:"NORTE",
                   2:"OESTE DEL NORTE",
                   3:"OESTE",
                   4:"OESTE DEL SUR",
                   5:"SUR",
                   6:"ESTE DEL SUR",
                   7:"ESTE",
                   8:"ESTE DEL NORTE"}



#Metodos relacionados con la interrupciones
def pluviometerTick(self):
    global count_pluviometer,statusCountPluv
    if statusCountPluv:
        count_pluviometer +=1
        print("entro Pluvi")
    statusCountPluv= False

#Metodo encargado de contar cada que el anemometro de una vuelta.
def statusCountPluv(self):
    global count_pluviometer,statusCountPluv
    statusCountPluv=True



#Metodo encargado de contar cada que el anemometro de una vuelta.
def windTick(self):
        global count_wind
        count_wind +=1
        
#Metodo encargado de realizar la conversion de #Ticks vs Km/h -> m/s.
def sensorCalculate():
    global windSpeed, count_wind, count_pluviometer, pluviometerValue
    windSpeed        = (count_wind*0.666667)/(tSample/1000.0)
    pluviometerValue = count_pluviometer * 0.2794 
    count_wind=0
    count_pluviometer = 0
    


class SensorKit():
    
    def __init__(self, PinWindS, PinAnemometer, PinPluviometer):
        
        global windSensor, windCurrentPosition, listCardinalPos
        global count,tSample, windSpeed
        
        
        count_wind        = 0
        count_pluviometer = 0

        tSample           = 1000

        windSpeed         = 0
        pluviometerValue  = 0
        
        self.windSensor = ADC(Pin(PinWindS))
        self.windSensor.atten(ADC.ATTN_11DB)
        
        
        
        self.anemometerSensor =  Pin(PinAnemometer,Pin.IN)
        self.anemometerSensor.irq(handler=windTick, trigger=Pin.IRQ_FALLING)
        
        self.pluviometerSensor = Pin(PinPluviometer,Pin.IN)
        self.pluviometerSensor.irq(handler=statusCountPluv, trigger=Pin.IRQ_FALLING)
        
        #metodos para establecer muestreo
        self.tSampleAnemometro = Timer(1)
        self.tSampleAnemometro.init(period=tSample, mode=Timer.PERIODIC, callback=lambda t:
                                    sensorCalculate()
        )
        
        
        
        windPreviusPosition=1
        windCurrentPosition=1
        count=0
    
    def getPluviometerValue(self):
        global pluviometerValue
        print("Lluvia: "+str(pluviometerValue)+"mm Agua/s")
    
    
    #Metodo Anemometro
    def getAnemometerValue(self):
        global windSpeed
        
        print("velocidad del viento: "+str(windSpeed)+"m/s")
        
        #print( anemometerSensor.value() )
    
    #Metodos del sensor direccion del viento
    def getWindDir(self):
        global windCurrentPosition, windPreviusPosition, listCardinalPos
        wSensorRead = self.windSensor.read()
        
        windPreviusPosition = windCurrentPosition
        
        if wSensorRead>=2300 and wSensorRead<= 2450:
            windCurrentPosition = 1
            
        elif wSensorRead>=2850 and wSensorRead<= 3000:
            windCurrentPosition = 2
            
        elif wSensorRead>=3300 and wSensorRead<= 3470:
            windCurrentPosition = 3
            
        elif wSensorRead>=1600 and wSensorRead<=1680:
            windCurrentPosition = 4
        
        elif wSensorRead>=470 and wSensorRead<= 550:
            windCurrentPosition = 5
        
        elif wSensorRead>=230 and wSensorRead<= 270:
            windCurrentPosition = 6
            
        elif wSensorRead>=40 and wSensorRead<= 70:
            windCurrentPosition = 7
            
        elif wSensorRead>=900 and wSensorRead<= 1100:
            windCurrentPosition = 8
        
        print(listCardinalPos[windCurrentPosition])

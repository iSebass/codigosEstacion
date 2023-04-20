from machine import I2C, Pin
import math


I2C_MODE                           = 0x01
UART_MODE                          = 0x02
DEV_ADDRESS                        = 0x22

#Recursos a utilizar en el I2C
SDA_PIN                            = 21
SCL_PIN                            = 22
ADDRESS                            = 0x22  
I2C_1                              = 0x01
HPA                                = 0x01
KPA                                = 0x02
TEMP_C                             = 0x03
TEMP_F                             = 0x04

TEMP_REG_ADDR                      = 0x14
HIMIDITY_REG_ADDR                  = 0x16
ULTRAVIOLET_INTENSITY_REG_ADDR     = 0x05
LUMINOUS_INTENSITY_REG_ADDR        = 0x12
ATMOSPHERE_PRESSURE_REG_ADDR       = 0x18
ELEVATION_REG_ADDR                 = 0x18

TEMP_REG_LENGTH                    = 0x02
HUMIDITY_REG_LENGTH                = 0x02
ULTRAVIOLET_INTENSITY_REG_LENGTH   = 0x02
LUMINOUS_INTENSITY_REG_LENGTH      = 0x02
ATMOSPHERE_PRESSURE_REG_LENGTH     = 0x02
ELEVATION_REG_LENGTH               = 0x02






class SEN0500_Sensor():

    def __init__(self, bus, MODE = I2C_MODE ):

        self._addr = DEV_ADDRESS
        if MODE == UART_MODE:
            print("CONFIG UART MODE")
            self._uart_i2c = UART_MODE
        else:
            print("CONFIG I2C MODE")
            self._uart_i2c = I2C_MODE
            
        self.i2cbus = bus    
        print( self.i2cbus.scan() )
        

    def _detect_device_address(self):
        
        try:
            rbuf = self._read_reg(0x04,2)
            data = rbuf[0] << 8 | rbuf[1]
        except:
            return -1
        return data
        
          
    def begin(self):
        if self._detect_device_address() != DEV_ADDRESS:
             return False
        return True
        
  
    def get_temperature(self,unist):
        rbuf = self._read_reg(TEMP_REG_ADDR, TEMP_REG_LENGTH)
        
        if self._uart_i2c == I2C_MODE:
          data = rbuf[0] << 8 | rbuf[1]
       
        temp = (-45) +((data * 175.00) / 1024.00 / 64.00)
        if(unist == TEMP_F):
          temp = temp * 1.8 + 32 
        return round(temp,2)
        
  
    def get_humidity(self):
        rbuf = self._read_reg(HIMIDITY_REG_ADDR, HUMIDITY_REG_LENGTH)
        humidity = rbuf[0] << 8 | rbuf[1]
        humidity = (humidity / 1024) * 100 / 64
        return humidity
 
    def get_ultraviolet_intensity(self):
        version = self._read_reg(ULTRAVIOLET_INTENSITY_REG_ADDR, ULTRAVIOLET_INTENSITY_REG_LENGTH)
        if (version[0] << 8 | version[1]) == 0x1001:
          rbuf = self._read_reg(0x10, 2)
          data = rbuf[0] << 8 | rbuf[1]
          ultraviolet = data / 1800
        else:
          rbuf = self._read_reg(0x10, 2)
          data = rbuf[0] << 8 | rbuf[1]
          outputVoltage = 3.0 * data/1024
          ultraviolet = (outputVoltage - 0.99) * (15.0 - 0.0) / (2.9 - 0.99) + 0.0 
        return round(ultraviolet,2)
  
    def get_luminousintensity(self):
        rbuf = self._read_reg(LUMINOUS_INTENSITY_REG_ADDR ,LUMINOUS_INTENSITY_REG_LENGTH)
        data = rbuf[0] << 8 | rbuf[1]
        luminous = data * (1.0023 + data * (8.1488e-5 + data * (-9.3924e-9 + data * 6.0135e-13)))
        return round(luminous,2)

  
    def get_atmosphere_pressure(self, units):
        rbuf = self._read_reg(ATMOSPHERE_PRESSURE_REG_ADDR, ATMOSPHERE_PRESSURE_REG_LENGTH)
        atmosphere = rbuf[0] << 8 | rbuf[1]
        if units == KPA:
          atmosphere /= 10
        return atmosphere

  
    def get_elevation(self): 
        rbuf = self._read_reg(ELEVATION_REG_ADDR, ELEVATION_REG_LENGTH)
        elevation = rbuf[0] << 8 | rbuf[1]
        elevation = 44330 * (1.0 - pow(elevation / 1015.0, 0.1903));
        return round(elevation,2)
    
    def _read_reg(self, reg_addr, length):
        try:
            rslt = self.i2cbus.readfrom_mem(self._addr ,reg_addr , length)
        except:
            rslt = -1
        return rslt

    


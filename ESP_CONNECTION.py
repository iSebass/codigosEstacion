import network
from time import sleep


SSID = "VIRUS PELIGROSO"
PASS = "isebasss"


class ESP32_CONNECTION():
    
    def __init__(self):
        print("Modulo Inicializado")
        self._ssid = SSID
        self._pass = PASS
    
    def setSSID_PASSW(self, newSSID=SSID, newPASS=PASS):
        self._ssid = newSSID
        self._pass = newPASS
    
    def StartConnection(self):
        # Crear una instancia de la clase WLAN
        self.wlan = network.WLAN(network.STA_IF)
        
        # Conectar a la red Wi-Fi
        self.wlan.active(True)
        self.wlan.connect(self._ssid, self._pass)
        
        # Esperar a que se establezca la conexión
        time_out = 20000
        while not self.wlan.isconnected():
            time_out -= 1
            sleep(1)
            if time_out == 0:
                print("Error Trying Connection")
                return False
        print("Conexion establecida")
        return True
    
    
        
        

        

# Complete project details at https://RandomNerdTutorials.com/micropython-hc-sr04-ultrasonic-esp32-esp8266/
from machine import Pin, time_pulse_us,SoftI2C 
from time import sleep_us, sleep_ms, sleep
from machine import Pin, I2C
from lcd_api import LcdApi 
from i2c_lcd import I2cLcd  
from machine import Pin,PWM,ADC
I2C_ADDR = 0x27  
totalRows = 2  
totalColumns = 16 

LED = Pin(2, Pin.OUT)
buzzer=Pin(4,Pin.OUT)
bouttonPoussoir1=Pin(35,Pin.IN,Pin.PULL_UP)
potar = ADC(Pin(34))               # Initialise l'objet potar correspondant à notre potentiomètre sur la broche 4 sur la broche 34
potar.atten(ADC.ATTN_11DB) 
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000) 
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)        # étalonnage (étendue totale sur ESP32 : 3.3V)


#HC-SR04
TRIG_PIN = Pin(5, Pin.OUT)  #Pin 12 sur Esp8266
ECHO_PIN = Pin(18, Pin.IN)   #Pin 13 sur Esp8266
SOUND_SPEED=340 # Vitesse du son dans l'air
TRIG_PULSE_DURATION_US=10


def readDistanceCM():
    # Prepare le signal
    TRIG_PIN.value(0)
    sleep_us(5)
    # Créer une impulsion de 10 µs
    TRIG_PIN.value(1)
    sleep_us(TRIG_PULSE_DURATION_US)
    TRIG_PIN.value(0)
    ultrason_duration = time_pulse_us(ECHO_PIN, 1, 30000) # Renvoie le temps de propagation de l'onde (en µs)
    return SOUND_SPEED * ultrason_duration / 20000
while True:
    valeurPotar = potar.read()        
     
    distance = readDistanceCM()
    if  bouttonPoussoir1.value()== 1:  # Bouton appuyé (actif bas avec PULL_UP)
        
        lcd.putstr("MODE MAINTENANCE")
        sleep_ms(500)
        lcd.clear()
    elif distance < valeurPotar:
        lcd.putstr("Distance:"+str(distance)+ "cm")
        sleep_ms(500) 
        lcd.clear() 
        print("Distance:", distance, "cm")
        print("Valeur potar =", valeurPotar)
        sleep_ms(500)
        buzzer.value(1)
        LED.value(1)
    else:
        lcd.putstr("Distance:"+str(distance)+ "cm")
        sleep_ms(500) 
        lcd.clear()
        print("Distance:", distance, "cm")
        print("Valeur potar =", valeurPotar)
        buzzer.value(0)
        sleep_ms(500)
        LED.value(0) 
      

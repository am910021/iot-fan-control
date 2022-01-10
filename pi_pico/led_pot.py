from machine import Pin, PWM, ADC
import time

adc = ADC(Pin(26))
#pwm = PWM(Pin(15))
#pwm.freq(1000)

#pwm2 = PWM(Pin(14))
#pwm2.freq(1000)
#pwm2.duty_u16(65535)

while True:
    duty = adc.read_u16()
    #pwm.duty_u16(duty)
    print("power: %.0f, %f" % ((duty / 65535)*100, duty))
    time.sleep(0.1)
    
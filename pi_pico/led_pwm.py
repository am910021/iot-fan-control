from machine import Pin, PWM
from time import sleep

pwm = PWM(Pin(15))
pwm.freq(1000)

rel = PWM(Pin(0))
rel.freq(1000)

while True:
    for duty in range(65025):
        pwm.duty_u16(duty)
        rel.duty_u16(duty)
        print(duty)
        sleep(0.0001)
    for duty in range(65025, 0, -1):
        pwm.duty_u16(duty)
        rel.duty_u16(duty)
        print(duty)
        sleep(0.0001)
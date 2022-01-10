from machine import Pin, I2C
import utime as time
from dht import DHT11, InvalidChecksum
import sys

rels = [
    Pin(0, Pin.OUT),
    Pin(4, Pin.OUT),
    Pin(11, Pin.OUT),
    Pin(15, Pin.OUT),
    Pin(18, Pin.OUT),
    Pin(22, Pin.OUT),
    
    Pin(25, Pin.OUT)
    ]

for rel in rels:
    rel.value(0)
    
name=['A', 'B', 'C', 'D', 'E', 'F']
matrix = [
[ 0,  0,  0,  0, 80, 0],
[ 0,  0,  0, 64,  0, 100],
[ 0,  0,  0, 64,  0, 0],
[ 0, 80, 51,  0, 81, 0],
[64,  0,  0, 64,  0, 100],
[ 0, 80,  0,  0, 80, 100]
]

global_max=max(map(max, matrix))
print([(x.index(global_max) if global_max in x else -1) for x in matrix])

count=0
r = 0
step=[r]
while True:
    numbers = matrix[r]
    maxvalue = max(numbers)
    c = numbers.index(maxvalue)
    step.append(c)
    
    if maxvalue == global_max:
        break    
    r+=1
    if r >= len(matrix):
        r=0
    count+=1
    if count > len(matrix):
        break
mapping = [name[x] for x in step]
print(mapping)
for i in step:
    rels[i].toggle()
    



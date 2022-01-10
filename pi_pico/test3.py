name=['A', 'B', 'C', 'D', 'E', 'F']
matrix = [
[ 0,  0,  0,  0, 80, 0],
[ 0,  0,  0, 64,  0, 100],
[ 0,  0,  0, 64,  0, 0],
[ 0, 80, 51,  0, 80, 0],
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
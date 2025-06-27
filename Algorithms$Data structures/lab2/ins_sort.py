# bla bla bla ble ble ble ble
# HOP
# lingan guli guli guli vatalin gan guliii gan gu lingan guli guli guli vatalin gan guliii gan gu

import random
import time

arr100 = [random.randint(1, 100) for n in range(100)]
arr1000 = [random.randint(1, 1000) for n in range(1000)]
arr10k = [random.randint(1,10000) for n in range(10000)]

start=time.perf_counter()

#INSERT SORT
def insert(list, counter):
    for i in range(1, len(list)):
        key = list[i]
        j = i-1
        while j >= 0:
            counter[0] += 1
            if list[j] > key:
                list[j+1] = list[j]
                j -= 1
                counter[1] += 1
            else:
                break
        list[j+1]=key  
        if j+1 != i:
            counter[1] += 1
    return list


for l in range(1):
    counter = [0, 0]
    copy = arr100[:]
    insert(copy, counter)


end = time.perf_counter()

print("Time: ", end - start)
print("Compares: ", counter[0])
print("Moves: ", counter[1])

#-------------------------------------------------------------------------------------------------------------------------




import random
import time

arr100 = [random.randint(1, 100) for n in range(100)]
arr1000 = [random.randint(1, 1000) for n in range(1000)]
arr10k = [random.randint(1,10000) for n in range(10000)]

start = time.perf_counter()

# QUICK SORT
def partition(list, low, high, counters):
    pivot = list[low]
    i = low
    for j in range(low + 1, high + 1):
        counters[0] += 1  
        if list[j] < pivot:
            i += 1
            list[i], list[j] = list[j], list[i]
            counters[1] += 1  
    list[i], list[low] = list[low], list[i]
    counters[1] += 1  
    return i

def quick_sort(list, low, high, counters):
    if low < high:
        pivot = partition(list, low, high, counters)
        quick_sort(list, low, pivot - 1, counters)
        quick_sort(list, pivot + 1, high, counters)
    return list

counters = [0,0]  
print(quick_sort(arr100, 0, len(arr100) - 1, counters))

end = time.perf_counter()

# print("Time: ", end - start)
# print("Compares: ",counters[0])
# print("Moves: ",counters[1])
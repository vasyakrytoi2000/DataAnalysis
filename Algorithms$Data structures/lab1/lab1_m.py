n = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
def sum_even (a, i = 0):
    if i == len(a):
        return 0
    if a[i] % 2 == 0:
        return a[i] + sum_even(a, i + 1)
    return sum_even(a, i + 1)

def sum_n_even (a, i = 0):
    if i == len(a):
        return 0
    if a[i] % 2 != 0:
        return a[i] + sum_n_even(a, i + 1)
    return sum_n_even(a, i + 1)

print('even: ', sum_even(n))
print('not even: ', sum_n_even(n))
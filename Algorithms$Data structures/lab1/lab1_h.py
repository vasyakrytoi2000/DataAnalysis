def ev_hanoy(i, a, b, c,):
    if i == 1:
        print( i, ',', a, '>', c)
        return 
    ev_hanoy(i - 1, a, c, b,)
    print( i, ',', a, '>', c)
    ev_hanoy(i - 1, b, a, c, )
    

try:
    n = int(input("some integer number: "))  
except ValueError:
    print("integer number!!!😡😡😡")
else:
    if n == 0:
        print ('not zero also 🙂🙂🙂')       
    elif n < 0:
        print('positive also 😊😊😊')
    else:
        ev_hanoy(n, 'A', 'B', 'C', )



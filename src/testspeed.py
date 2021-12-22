import datetime

A = 100000000

a = datetime.datetime.now()

'''
x = []
for i in range(0,A):
    x.append(i*i)
'''
x = [i*i for i in range(0,A)]
b = datetime.datetime.now()

print("Time spent: ",b-a)

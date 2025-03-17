import random

d = lambda x: x != 9
n = random.randint(0, 10)


while d(n):
    print(n)
    n = random.randint(0, 10)

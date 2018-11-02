



for num in range(1, 10):
    if num % 3 == 0:
        print(num)

for num in range(0, 30, 3):
    print(num)

mylist = []
mylist = [num for num in range(0, 30, 3)]

print(mylist)

oddlist = [3, 12, 15]
newlist = [num for num in range(30) if num % 3 == 0 if num != oddlist[2]]
print(newlist)


















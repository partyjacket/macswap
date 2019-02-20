# exercise 4.1

fav_pizza = ['cheese', 'peperoni', 'sausage']
added_pizzas = ['veggie', 'thick crust']
fav_pizza.extend(added_pizzas)

for pizza in fav_pizza:
    print(f'I really like {pizza} pizza!')
print("Did I mention how much I like pizza?\n")

# exercise 4.2
my_animals = ['dog', 'cat', 'fish']
for animal in my_animals:
    print(f"{animal} would make a great pet!")
print("All of the animals mentioned would make a great pet now that I think about it!")

squares = []
for value in range(1,11):
    squares.append(value ** 2)
print(squares)

# exercise 4.3
for num in range(1, 21):
    print(num)
num_list = [num for num in range(1, 21)]
print(num_list)

# exercise 4.5
print(sum(num_list))
print (max(num_list))

# exercise 4.6 - compression
for odd in range(1, 21, 2):
    print(odd)
odd_list = [odd for odd in range(20) if odd % 2 == 1]
print(odd_list)

# exercise 4.7 - compression
three_list = [three for three in range(30) if three % 3 == 0]
print(three_list)

cubelist = []
for cube in range(1, 11):
    cubevalue = cube ** 3
    cubelist.append(cubevalue)
print(cubelist)

# exercise 4.8
shortcubelist = []
for shortcube in range(1, 121):
    if len(shortcubelist) < 10:
        shortcubelist.append(shortcube ** 3)
    else:
        break



print("ex 8", shortcubelist)

# exercise 4.9
cubecomp = [shortcube ** 3 for shortcube in range(1, 11)]
print(cubecomp)


# exercise 4.10
print("The first three pizzas I like are: ", fav_pizza[0:3])
print("The pizzas from the middle of my list are: ", fav_pizza[1:4])
print("The last 3 pizzas from my list are: ", fav_pizza[-3:])

if 'cheese' in fav_pizza:
    print("yep, it's in there")

if 'baked' not in fav_pizza:
    print("nope, baked is not in there")





#Exercise 2.8

multiply = 4 * 2
division = 16 / 2
addition = 4 + 4
exponent = 2 ** 3
subtraction = 10 - 2


ex_2_8 = []
ex_2_8.append(multiply)
ex_2_8.append(division)
ex_2_8.append(addition)
ex_2_8.insert(3, exponent)
ex_2_8.append(subtraction)

for whattype in ex_2_8:
    if type(float):
        whattype = int(whattype)
    print(whattype)


#Exercise 2.9
favorite_number = 21
print("My favorite number is " + str(favorite_number))

#Exercise 2.10
comment_statement = "for this exercise I have to use comments"

''' This is a multiline comment
so apparently you can keep 
going, and going and going'''
#This is a regular comment


age = int(input("what is your age?"))

if age <= 4:
    print("The cost to enter is $5 because you're {0}.".format(age))
elif (age >= 5) and (age <= 17):
    print(f"The cost to enter is $10 because you're under 18, but older than 4. You stated you are {age}. Have fun!")
else:
    print(f"The cost to enter for all adults is $20. You stated you are {age} years old. Have fun!")

if age <= 4:
    price = 5
elif (age >= 5) and (age <= 17):
    price = 10
elif age > 17 and age < 30:
    price = 20
else:
    price = 30
print(f"The cost of admission is ${price} based on the fact that you are {age}. Have fun!")





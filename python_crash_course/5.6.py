# Exercise 5.6
age_input = int(input("what is your age?"))

if age_input < 2:
    print("you are a baby")
elif (age_input > 1) and (age_input < 4):
    print("you are a toddler")
elif (age_input >= 4) and (age_input < 13):
    print("you are a kid")
elif (age_input >= 13) and (age_input < 20):
    print("you are a teenager")
elif (age_input >= 20) and (age_input < 65):
    print("you are an adult")
else:
    print("you an old geezer!")


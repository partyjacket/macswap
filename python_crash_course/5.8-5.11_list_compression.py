
# Exercise 5.8
usernames = ['Jason', 'hobart', 'dewd', 'bart', 'admin']

lowerusername = [user.lower() for user in usernames]


reg_greeting = "Hello, thanks for logging in!"

admin_greeting = f"thanks for logging in {lowerusername[0]}"

print(admin_greeting)


# Exercise 5.9
for username in usernames:
    del(username)


if usernames:
    print("We need to find some users!")

# Exercise 5.10

current_users = ['Jason', 'hobart', 'dewd', 'bart', 'admin']
new_users = ['Bob', 'Harry', 'hobart', 'Dewd']

for new_user in new_users:
    if new_user.lower() in current_users:
        print(f'Sorry, the name {new_user.title()} is already taken, please choose another')
    if new_user.lower() not in current_users:
        print(f"Congrats!, the username {new_user.title()} is available!")

# Exercise 5.11

ordinals = [num for num in range(1,10)]

for ordinal in ordinals:
    if ordinal == 1:
        ordinal = str(ordinal) + 'st'
    elif ordinal == 2:
        ordinal = str(ordinal) + 'nd'
    elif ordinal == 3:
        ordinal = str(ordinal) + 'rd'
    else:
        ordinal = str(ordinal) + 'th'
    print(ordinal, '\n')





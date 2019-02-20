

# exercise 3.1
myfriends = ['Don', 'Ryan', 'John', 'Jamison']
for friend in myfriends:
    print(friend)

# exercise 3.2
greeting = "Hello"
for friend in myfriends:
    print(f'{greeting}, {friend}')

# exercise 3.3
mybooks = ["the two towers", 'charlie and the chocolate factory', "wool"]
print("My favorite book this year was", mybooks[2].title())

mybooks.append('magic tree house')
print(mybooks)
mybooks.insert(2, 'narnia')
print(mybooks)

brookesbook = mybooks.pop(2)
print(brookesbook)
print(mybooks)

# exercise 3.4
dinner_guests = ['Don', 'Ryan', 'John', 'Jamison']

dinner_invite = "Hi, can you please come to dinner:"

for guest in dinner_guests:
    print(f'{dinner_invite}, {guest}')

# exercise 3.5
removal = dinner_guests.pop(1)
dismiss = f'Hi {removal}, please dont come to dinner!'
print(dismiss)
dinner_guests.insert(0, "Holly")
print(dinner_guests)

print(f'Hi {dinner_guests[0]}, can you please come for dinner?')

for name in dinner_guests:
    print(f'Hello {name}, can you please come to dinner')

new_guests = ["carol", "elliott", "james"]
addguest = new_guests[0]
dinner_guests.append(new_guests[0])
dinner_guests.insert(0, new_guests[1])
dinner_guests.append(new_guests[2])
print(dinner_guests)

testing = [guests for guests in new_guests]
new_guests.sort()

another_guest_list = [guest.title() for guest in dinner_guests]
print(sorted(another_guest_list))




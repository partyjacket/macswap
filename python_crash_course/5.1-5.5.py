# Exercise 5.3 - 5.5
player_earned = "Hi player, you just earned: "
green = 5
yellow = 10
red = 15

colors = {'green': 5, 'yellow': 10, 'red': 15}

player1 = 'Player1'

player2 = 'Player2'

player1_points = 0

alien_color = input("What color was the alien?")
if alien_color:
    print(f'Hi {player1}, you just shot down a {alien_color} alien. You earn {colors[alien_color]}!')
    player1_points = player1_points + colors[alien_color]
print(f"This is your new score! {player1_points}")

# elif alien_color == 'red':
#     print(f'Hi {player1}, you just shot down a {alien_color} alien. You earn {colors}!')
#     player1_points = player1_points + colors
#
# else:
#     print(f"You don't get squat for shooting down a {alien_color} alien!")
# print(f"This is your new score! {player1_points}")


# alien_color = input("What color was the alien?")
# if alien_color == 'green':
#     print(f'Hi {player1}, you just shot down a {alien_color} alien. You earn {green}!')
#     player1_points = player1_points + green
#
# elif alien_color == 'red':
#     print(f'Hi {player1}, you just shot down a {alien_color} alien. You earn {red}!')
#     player1_points = player1_points + red
#
# else:
#     print(f"You don't get squat for shooting down a {alien_color} alien!")
#print(f"This is your new score! {player1_points}")



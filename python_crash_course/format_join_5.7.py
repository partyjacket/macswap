

fav_fruits = ['bananas', 'apple', 'berries', 'peach', 'pear']

store_fruits = ['bananas', 'nectarine', 'peach', 'pear', 'kiwi', 'pineappl', 'plum']

sletters = ['n', 'r', 'i', 'e', 'm']

fav_fruits.remove('apple')
instock = []
notinstock = []
for fruit in fav_fruits:
    if fruit in store_fruits:
        if fruit[-1] in sletters:
            fruit = fruit + 's'
        elif fruit[-1] == 's':
                fruit = fruit
        elif fruit[-2:] != 'es':
            fruit = fruit + 'es'

        print(f"Yep!, we have {fruit} in stock!")
    else:
        if fruit not in store_fruits:
            if fruit[-1] in sletters:
                fruit = fruit + 's'
                notinstock.append(fruit)
            elif fruit[-1] == 's':
                fruit = fruit
                notinstock.append(fruit)
            elif fruit[-2:] != 'es':
                fruit = fruit + 'es'
                notinstock.append(fruit)

if len(notinstock) >= 2:
    print(f"Sorry, we don't have {', '.join(notinstock[:-1])} and {notinstock[-1]} in stock.")
else:
    print(f"Sorry, we don't have {notinstock[0]} in stock.")




for store_fruit in store_fruits:
    if store_fruit not in fav_fruits:
        if store_fruit[-1] in sletters:
            store_fruit = store_fruit + 's'
            instock.append(store_fruit)
        elif store_fruit[-1] == 's':
            store_fruit = store_fruit
            instock.append(store_fruit)
        elif store_fruit[-2:] != 'es':
            store_fruit = store_fruit + 'es'
            instock.append(store_fruit)
print(f"But we do have {', '.join(instock[:-1])} and {instock[-1]} in stock you can try!")
print("\nSecond take with 2.7 string formats - But we do have %s and %s in stock you can try!" % (', '.join(instock[:-1]), instock[-1]))














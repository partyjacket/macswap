

new_dict = {
    'Jason': 'eggs',
    'Holly:': 'toast',
    'Brooke': 'bagels',
    'Skylar': 'cereal',
}

new_dict['Grams'] = 'hamburger'

for name, food in new_dict.items():
    print(f"Hi, my name is {name} and my favorite breakfast food is {food.title()}!")

print(new_dict.keys())

daughters = ['Brooke', 'Skylar']

# for daughter in daughters:
if daughters[0] and daughters[1] in new_dict:
    print("{}'s favorite breakfast is {}, {}'s favorite breakfast is {}".format(
        daughters[0], new_dict[daughters[0]], daughters[1], new_dict[daughters[1]]))


# Exercise 6.1
userdict = {
    'user1': {
        'First': 'Marv',
        'Last': 'Tester',
        'City': 'Cottonwod',
    },
    'user2': {
        'First': 'Jason',
        'Last': 'Patterson',
        'City': 'Draper',
    },
    'user3': {
        'First': 'Carol',
        'Last': 'Patterson',
        'City': 'Lansing',
    }
}


fullusername = []
for user, info in userdict.items():
    fullusername = info['First'] + " " + info['Last']
    print(f"\n{user}'s full name is {info['First']} {info['Last']}.\n The city they live in is {info['City']}.")

    print("\n%s's full name is %s.\n The city they live in is %s." % (user, fullusername, info['City']))

# Exercise 6.2

num_dicts = {
    'Jason': {
        'favnum1': 3,
        'favnum2': 4
    },
    'Holly': {
        'favnum1': 83,
        'favnum2': 33
    },
    'Marv': {
        'favnum1': 32,
        'favnum2': 22
    }
}

for name, favs in num_dicts.items():
    print("\n%s's first favorite number is %d, and second favorite number is %d"
          % (name, favs['favnum1'], favs['favnum2']))

# Exercise 6.3

glossary = {
    'function': 'explicitly passed arguments',
    'method': 'a function embedded in a class',
    'parameter': 'set an expected variable in a function',
    'argument': 'what you pass into a function - parameter is the placeholder'
}

for term, definition in glossary.items():
    print("\nGlossary term: %s"
          " \ndefinition: %s" % (term, definition))

glossary_list = []

for term, definition in glossary.items():
    print(len(definition))
    glossary_list.append(term)
    print(glossary_list)

teslist = ['one', 'two', 'three']

for testitem in teslist:
    print(str(teslist.index(testitem)) + "this s the index")

the_things_I_know = ['method', 'parameter']

for keys, vals in glossary.items():
    if keys in the_things_I_know:
        print("Hey!, I know about %ss, and that's in the list!" % (keys))
    elif keys not in the_things_I_know:
        print("crapola!, I've don't know squat about %s" % keys)

















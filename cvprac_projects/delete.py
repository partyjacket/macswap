#Pig latin by Nosa ...
vowel = ['a', 'e', 'i', 'o', 'u', 'y']
total = []
worde = raw_input("Give me a word!").lower().strip()
words = worde.split()
for word in words:
    if not word.isalpha():
        print(word + " is not a word")
    else:
        check = [1 if char in vowel else 0 for char in word]
        same = (set(check))

        print 'This is the check', check, 'This is the same', same
        if check[0] == 1:
            total.append(word+'yay')
        elif len(same) == 1 and same[0] == 0:
            total.append(word+'ay')
        else:
            argot = ''+word[0]
            for value in range(1, len(check)):
                if check[value] == check[value-1]:
                    argot += word[value]
                else:
                    answer = word[value:]+argot
                    total.append(answer+'ay' if check[0] == 0
                                 else answer+'yay')
                    break
print (" ".join(total))
vowel = ['a', 'e', 'i', 'o', 'u', 'y']
names = ['Jason', 'Brian']
worde = raw_input("Give me a word!").lower().strip()
words = worde.split()
for word in words:
    if not word.isalpha():
        print(word + " is not a word")
    else:
        check = [1 if char in vowel else 0 for char in word]

        same = (set(check))
        print check

obj = ["Even" if i % 2 == 0 'by3' if i % 3 == 0 else "Odd" for i in range(10)]
print obj
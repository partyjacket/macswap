dad = 'Jason'
daughter1 = 'Brooke'
daughter2 = 'sky'
mom = 'holly'

message = "    Hello"

#Exercise 2.3
formal = message + " " + dad + " " + daughter1 + " " + daughter2 + " " + mom
print(formal)

#Exercise 2.4
print("\n" + formal.upper())
print("\n" + formal.lower())
print("\n" + formal.title())

addnewline = "\n"

#Exercise 2.5
quote = '"Man who go to bed, wake up"'
print(addnewline + quote + addnewline)


#Exercise 2.6
tapspace = '\tthis is a sentence with a tab'
print(tapspace + addnewline)
strip_left_tab_space = tapspace.lstrip()
print(strip_left_tab_space + " " + "That's been removed!")
newlinespace = "\nThis is a sentence with a newline in front of it"
print(newlinespace)

print(newlinespace.strip() + " " + "The new newline has been removed here")



#Exercise 2.7
dad = '  Jason'
formal = message + " " + dad.lstrip() + " " + daughter1 + " " + daughter2 + " " + mom
print(formal.title())

print(formal.title().lstrip())



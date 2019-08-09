

def format_ordinal():
    number = (raw_input('Please pick a number between 1 and 10: '))
    while number.isdigit():
        if int(number) == 0:
            print("You cannot choose Zero, please pick a number betwixt 1 and 10!")
            return format_ordinal()
        elif int(number) < 1 or int(number) > 10:
            print("{0} is too high, please pick another number you jackass!!!".format(number))
            return format_ordinal()
        else:
            number = int(number) + 1
            ordinals = range(1, number)
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
        break
    else:
        print("You have to pick a number jackass!")
        return format_ordinal()

format_ordinal()


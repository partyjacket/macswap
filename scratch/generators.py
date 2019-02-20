def is_prime(num):
    if num <= 2:
        return False
    if num == 5:
        return True
    if num > 3 and num % 2 == 0 or num % 3 == 0 or num % 5 == 0:
        return False
    else:
        return True

mylist = list()

def get_primes_list(nums):
    for value in range(nums):
        if is_prime(value):
            mylist.append(value)
    mylist_len = len(mylist)
    print 'number of primes in list is:', mylist_len
    return mylist_len


def get_primes(nums):
    for value in range(nums):
        if is_prime(value):
            mylist.append(nums)
            yield value


thenum = int(raw_input("Please give me a number!"))

number_of_primes = get_primes_list(thenum)

prime = get_primes(thenum)

for i in range(number_of_primes):
    print next(prime)
















def is_prime(num):
    if num > 3 and num % 2 == 0 or num % 3 == 0:
        return False
    else:
        return True


def get_primes(*args):
    nullList = list()
    result_list = list()
    nullList = [int(value) for value in args]
    # for value in args:
    #     nullList.append(int(value))
    result_list = [element for element in nullList if is_prime(element)]
    # for element in nullList:
    #     if is_prime(element):
    #         result_list.append(element)
    return result_list

# listofnums = []
# for i in range(21):
#     if get_primes(i):
#         listofnums.append(i)
listofnums = [i for i in range(21) if get_primes(i)]

for integer in listofnums:
    print integer

def simple_get():
    yield 1
    yield 2
    yield 3

for yvalue in simple_get():
    print yvalue

mygen = simple_get()
print next(mygen)
print next(mygen)
print next(mygen)

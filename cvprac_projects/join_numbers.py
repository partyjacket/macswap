

def join_ports(ports_proposed):
    string_ports_proposed = []
    join_ports_proposed = []

    for item in ports_proposed:
        string_ports_proposed.append(str(item))
    string_ports_proposed.append(',')


    index = 0
    for item in string_ports_proposed:
        next_index = index + 1
        if next_index == len(string_ports_proposed):
            break

        elif string_ports_proposed[index].isdigit() and string_ports_proposed[next_index].isdigit():
            newdigit = string_ports_proposed[index] + string_ports_proposed[next_index]
            join_ports_proposed.append(newdigit)
            index = index + 2

        elif string_ports_proposed[index].isdigit() and string_ports_proposed[next_index] == ',':
            join_ports_proposed.append(string_ports_proposed[index])
            index += 1

        elif string_ports_proposed[index].isdigit():
            join_ports_proposed.append(string_ports_proposed[index])
            index += 1

        elif string_ports_proposed[index] == ',':
            index += 1

    join_ports_proposed = [int(x) for x in join_ports_proposed]
    join_ports_proposed.sort()
    return join_ports_proposed


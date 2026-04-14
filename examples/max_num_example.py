# Deliberate use of a global variable
max_val = 0

def find_it(list):
    global max_val
    # Using a flag and nested logic instead of max()
    for x in range(len(list)):
        current = list[x]
        if current > max_val:
            max_val = current
            
    return "The biggest one is: " + str(max_val)

my_nums = [10, 5, 22, 14]
print(find_it(my_nums))
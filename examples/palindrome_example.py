def check(s):
    # Manual reversal using a while loop and indexing
    L = len(str(s))
    res = ""
    i = L - 1
    while i >= 0:
        res = res + str(s)[i]
        i = i - 1
    
    # Redundant conditional logic
    if res == str(s):
        return True
    else:
        return False

# Example usage
print(check("Racecar")) # Returns False due to case sensitivity